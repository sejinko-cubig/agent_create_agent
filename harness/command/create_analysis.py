"""
LangGraph Analysis Creator - 전체 파이프라인 실행

사용법:
  python command/create_analysis.py --topic "이탈 예측 분석"

워크플로우:
  1. Planner Agent: 주제 분석 → skill_input.md 생성
  2. Coder Agent: skill_input.md → LangGraph 코드 생성
  3. QA Agent: 코드 검증 → 피드백 → Coder 수정 (최대 3회 루프)
  4. 최종 코드 + 리포트 출력
"""

import argparse
import os
import sys
import yaml
from anthropic import Anthropic

# 하네스 루트 경로
HARNESS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(HARNESS_ROOT, "outputs")


def load_config():
    config_path = os.path.join(HARNESS_ROOT, "harness", "config", "models.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def load_skill(name: str) -> str:
    skill_path = os.path.join(HARNESS_ROOT, "harness", "skill", f"{name}.md")
    with open(skill_path, "r") as f:
        return f.read()


def load_agent(name: str) -> str:
    agent_path = os.path.join(HARNESS_ROOT, "harness", "agent", f"{name}.md")
    with open(agent_path, "r") as f:
        return f.read()


def load_template(name: str) -> str:
    tmpl_path = os.path.join(HARNESS_ROOT, "harness", "template", f"{name}")
    with open(tmpl_path, "r") as f:
        return f.read()


def run_agent(client: Anthropic, model: str, system: str, user_msg: str, temp: float = 0.0) -> str:
    response = client.messages.create(
        model=model,
        max_tokens=16000,
        temperature=temp,
        system=system,
        messages=[{"role": "user", "content": user_msg}],
    )
    return response.content[0].text


def main():
    parser = argparse.ArgumentParser(description="LangGraph Analysis Creator")
    parser.add_argument("--topic", required=True, help="분석 주제 (예: 이탈 예측 분석)")
    parser.add_argument("--max-qa-loops", type=int, default=3, help="QA 루프 최대 횟수")
    args = parser.parse_args()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    client = Anthropic()
    config = load_config()

    print("=" * 60)
    print(f"  LangGraph Analysis Creator")
    print(f"  주제: {args.topic}")
    print("=" * 60)

    # ── Step 1: Planner Agent ──
    print("\n[Step 1] Planner Agent 실행...")
    planner_system = load_agent("planner")
    data_architect_skill = load_skill("data_architect")

    planner_prompt = f"""주제: {args.topic}

아래 skill 정의에 따라 이 주제의 데이터 스키마를 설계해줘:

{data_architect_skill}

skill_input.md 형식으로 출력해줘."""

    skill_input = run_agent(
        client,
        model=config["agents"]["planner"]["model"],
        system=planner_system,
        user_msg=planner_prompt,
    )

    skill_input_path = os.path.join(OUTPUT_DIR, "skill_input.md")
    with open(skill_input_path, "w") as f:
        f.write(skill_input)
    print(f"  ✅ skill_input.md 생성 완료")

    # ── Step 2 & 3: Coder ↔ QA Loop ──
    coder_system = load_agent("coder")
    qa_system = load_agent("qa")
    graph_builder_skill = load_skill("graph_builder")
    llm_analyzer_skill = load_skill("llm_analyzer")
    report_designer_skill = load_skill("report_designer")
    qa_reviewer_skill = load_skill("qa_reviewer")
    langgraph_template = load_template("langgraph_template.py")

    qa_feedback = ""
    final_code = ""

    for loop in range(1, args.max_qa_loops + 1):
        # ── Coder Agent ──
        print(f"\n[Step 2-{loop}] Coder Agent 실행 (루프 {loop}/{args.max_qa_loops})...")

        feedback_section = ""
        if qa_feedback:
            feedback_section = f"""

## QA 피드백 (이전 라운드)
아래 피드백을 반영하여 코드를 수정해줘:
{qa_feedback}"""

        coder_prompt = f"""주제: {args.topic}

## 데이터 스키마
{skill_input}

## Skill 참조
{graph_builder_skill}

{llm_analyzer_skill}

{report_designer_skill}

## 코드 템플릿
{langgraph_template}
{feedback_section}

위 스키마와 skill 정의에 따라 완성된 LangGraph 파이프라인 코드를 생성해줘.
Python 코드만 출력해줘 (마크다운 코드블록 없이)."""

        final_code = run_agent(
            client,
            model=config["agents"]["coder"]["model"],
            system=coder_system,
            user_msg=coder_prompt,
        )

        code_path = os.path.join(OUTPUT_DIR, "output.py")
        with open(code_path, "w") as f:
            f.write(final_code)
        print(f"  ✅ output.py 생성 완료")

        # ── QA Agent ──
        print(f"\n[Step 3-{loop}] QA Agent 실행 (루프 {loop}/{args.max_qa_loops})...")

        qa_prompt = f"""아래 LangGraph 코드를 검증해줘:

## 원본 스키마
{skill_input}

## 생성된 코드
```python
{final_code}
```

## QA 체크리스트
{qa_reviewer_skill}

위 체크리스트에 따라 PASS 또는 FAIL 판정해줘."""

        qa_result = run_agent(
            client,
            model=config["agents"]["qa"]["model"],
            system=qa_system,
            user_msg=qa_prompt,
        )

        qa_path = os.path.join(OUTPUT_DIR, f"qa_report_loop{loop}.md")
        with open(qa_path, "w") as f:
            f.write(qa_result)

        if "PASS" in qa_result.upper().split("\n")[0] or "## QA 결과: PASS" in qa_result:
            print(f"  ✅ QA PASS — 코드 승인 완료")
            break
        else:
            print(f"  ❌ QA FAIL — 피드백 전달 후 재생성")
            qa_feedback = qa_result
    else:
        print(f"\n  ⚠️  QA 루프 {args.max_qa_loops}회 초과 — 최선의 버전 채택")

    # ── 최종 결과 ──
    print("\n" + "=" * 60)
    print("  ✅ 파이프라인 완료")
    print("=" * 60)
    print(f"  📁 출력 폴더: {OUTPUT_DIR}")
    print(f"  📄 skill_input.md  — 데이터 스키마")
    print(f"  📄 output.py       — LangGraph 코드")
    print(f"  📄 qa_report_*.md  — QA 리포트")
    print(f"\n  실행: python {os.path.join(OUTPUT_DIR, 'output.py')}")


if __name__ == "__main__":
    main()
