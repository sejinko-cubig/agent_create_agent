"""
LangGraph Analysis Creator - Full Harness Generator

Claude Code에서 사용할 수 있는 풀 하네스 구조를 로컬에 생성합니다.

사용법: python generate_harness.py
"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.join(BASE, "harness")


def write_file(rel_path: str, content: str):
    path = os.path.join(HARNESS, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  📄 {rel_path}")


def main():
    print("=" * 60)
    print("  LangGraph Analysis Creator - Full Harness 생성")
    print("=" * 60 + "\n")

    # ================================================================
    # README.md
    # ================================================================
    write_file("README.md", """\
# LangGraph Analysis Creator Harness

주제를 입력하면 input 데이터를 정의하고, LangGraph 분석 파이프라인 코드를 생성하며,
최종적으로 LLM이 분석 리포트를 생성하는 **멀티 Agent 하네스**입니다.

## 구조

```
harness/
├── CLAUDE.md              ← Claude Code 프로젝트 지침서
├── agent/                 ← Agent 정의 (역할, 시스템 프롬프트)
│   ├── planner.md         ← 주제 분석 + 데이터 스키마 설계
│   ├── coder.md           ← LangGraph 코드 생성
│   └── qa.md              ← 코드 리뷰 + 품질 검증
├── skill/                 ← Skill 정의 (재사용 가능한 능력 단위)
│   ├── data_architect.md  ← input 데이터 스키마 설계
│   ├── graph_builder.md   ← StateGraph 노드/엣지 구성
│   ├── llm_analyzer.md    ← LLM 분석 노드 설계
│   ├── report_designer.md ← LLM 리포트 생성
│   └── qa_reviewer.md     ← 코드 품질 검증
├── command/               ← 실행 스크립트
│   ├── create_analysis.py ← 전체 파이프라인 (Planner→Coder→QA 루프)
│   ├── run_qa.py          ← QA만 단독 실행
│   └── generate_report.py ← 리포트만 재생성
├── template/              ← 코드/리포트 템플릿
│   ├── langgraph_template.py
│   └── report_template.md
├── config/                ← 설정
│   ├── models.yaml
│   └── environment.yaml
└── examples/              ← 예시
    └── churn_prediction/
        ├── skill_input.md
        └── output.py
```

## 사용법

```bash
# 1. 의존성 설치
pip install anthropic langgraph langchain-anthropic pyyaml

# 2. API 키 설정
export ANTHROPIC_API_KEY=sk-ant-...

# 3. 주제 입력하여 분석 파이프라인 생성
python command/create_analysis.py --topic "이탈 예측 분석"

# 4. QA만 실행
python command/run_qa.py --file outputs/churn_analysis.py

# 5. 리포트만 재생성
python command/generate_report.py --file outputs/churn_analysis.py
```

## 워크플로우

```
주제 입력 → Planner Agent → Coder Agent ←→ QA Agent (루프) → 최종 코드 + 리포트
```
""")

    # ================================================================
    # CLAUDE.md
    # ================================================================
    write_file("CLAUDE.md", """\
# LangGraph Analysis Creator - Claude Code 지침서

## 프로젝트 개요
이 하네스는 주제를 입력받아 LangGraph 기반 데이터 분석 파이프라인을 자동 생성합니다.

## Agent 역할

### 1. Planner Agent (`agent/planner.md`)
- 주제를 분석하여 필요한 input 데이터 스키마를 설계
- `skill/data_architect.md` skill을 사용
- 출력: 데이터 스키마 정의 (TypedDict + 샘플 데이터)

### 2. Coder Agent (`agent/coder.md`)
- Planner의 스키마를 받아 완성된 LangGraph 코드 생성
- `skill/graph_builder.md`, `skill/llm_analyzer.md`, `skill/report_designer.md` skill 사용
- `template/langgraph_template.py`를 기반으로 코드 작성
- 출력: 실행 가능한 LangGraph Python 파일

### 3. QA Agent (`agent/qa.md`)
- Coder가 생성한 코드를 검증
- `skill/qa_reviewer.md` skill을 사용
- 피드백이 있으면 Coder에게 반환 → 수정 → 재검증 (최대 3회 루프)
- 출력: QA 리포트 (pass/fail + 피드백)

## 워크플로우 실행 순서

```
1. 사용자가 주제 입력 (예: "이탈 예측 분석")
2. Planner Agent 실행
   - data_architect skill로 input 스키마 설계
   - skill_input.md 파일 생성
3. Coder Agent 실행
   - skill_input.md 읽기
   - graph_builder + llm_analyzer + report_designer skill로 코드 생성
   - output.py 파일 생성
4. QA Agent 실행
   - output.py 코드 리뷰
   - 문제 발견 시 → Coder Agent에게 피드백 전달 → 3번으로 돌아감
   - 문제 없으면 → 최종 승인
5. 최종 코드 + 리포트 출력
```

## 모델 설정 (`config/models.yaml`)
- Planner: claude-sonnet-4-6 (빠른 분석)
- Coder: claude-sonnet-4-6 (코드 생성 최적)
- QA: claude-sonnet-4-6 (정밀 리뷰)
- LLM 분석 노드: claude-sonnet-4-6 (temperature 0.3)
- LLM 리포트 노드: claude-sonnet-4-6 (temperature 0.2)

## 규칙
- 코드는 항상 완성된 실행 가능 상태로 생성 (placeholder 금지)
- 샘플 데이터를 반드시 포함하여 즉시 테스트 가능하도록
- LLM 노드는 ChatAnthropic 사용
- 리포트는 한국어 마크다운으로 출력
- QA 루프는 최대 3회까지 반복
""")

    # ================================================================
    # agent/planner.md
    # ================================================================
    write_file("agent/planner.md", """\
# Planner Agent

## 역할
사용자가 입력한 분석 주제를 해석하고, 해당 주제에 필요한 데이터 스키마와 분석 계획을 수립합니다.

## 시스템 프롬프트

```
You are a Data Analysis Planner. Given an analysis topic, you:

1. Identify what data is needed for this analysis
2. Design the input data schema (columns, types, descriptions)
3. Define TypedDict for LangGraph State
4. Generate 5+ realistic sample data rows
5. Outline the analysis approach (what statistical methods, what LLM should analyze)

Output a structured skill_input.md file that the Coder Agent will use.

Always respond in Korean for descriptions, English for code/technical terms.
```

## 사용 Skill
- `skill/data_architect.md`

## 입력
- 분석 주제 (문자열, 예: "이탈 예측 분석", "매출 분석", "감성 분석")

## 출력
- `skill_input.md`: 데이터 스키마 + 샘플 데이터 + 분석 계획
""")

    # ================================================================
    # agent/coder.md
    # ================================================================
    write_file("agent/coder.md", """\
# Coder Agent

## 역할
Planner가 설계한 데이터 스키마(skill_input.md)를 기반으로
완성된 LangGraph 분석 파이프라인 코드를 생성합니다.

## 시스템 프롬프트

```
You are a LangGraph Code Generator. Given a skill_input.md file containing:
- Data schema (TypedDict)
- Sample data
- Analysis plan

You generate a COMPLETE, RUNNABLE LangGraph pipeline with these nodes:

1. validate_and_preprocess — Data validation, missing values, normalization
2. statistical_analysis — Topic-specific statistical analysis
3. llm_deep_analysis — Pass stats to LLM for pattern interpretation
4. llm_generate_report — Synthesize everything into a Korean markdown report

Rules:
- NO placeholders, NO "...", NO "pass" — every function must have real logic
- Include sample data and __main__ block for immediate testing
- Use ChatAnthropic(model="claude-sonnet-4-6") for LLM nodes
- LLM analysis node: temperature=0.3
- LLM report node: temperature=0.2
- Follow template/langgraph_template.py structure

If you receive QA feedback, fix the specific issues and regenerate the code.
```

## 사용 Skill
- `skill/graph_builder.md`
- `skill/llm_analyzer.md`
- `skill/report_designer.md`

## 입력
- `skill_input.md` (Planner 출력)
- QA 피드백 (선택, QA Agent에서 전달)

## 출력
- `output.py`: 완성된 LangGraph 파이프라인 코드
""")

    # ================================================================
    # agent/qa.md
    # ================================================================
    write_file("agent/qa.md", """\
# QA Agent

## 역할
Coder Agent가 생성한 LangGraph 코드를 검증하고,
문제 발견 시 구체적인 피드백을 Coder에게 전달합니다.

## 시스템 프롬프트

```
You are a Code Quality Reviewer for LangGraph analysis pipelines.

Review the generated code against these criteria:

1. STRUCTURE — StateGraph has all required nodes (validate, analyze, llm_analyze, report)
2. COMPLETENESS — No placeholders, no "...", no "pass", all functions have real logic
3. DATA — Sample data exists and matches the TypedDict schema
4. IMPORTS — All imports are correct and necessary
5. LLM NODES — ChatAnthropic is used with correct model and temperature
6. EDGE FLOW — Edges are connected correctly: validate→analyze→llm_analyze→report→END
7. RUNNABLE — __main__ block exists and invokes the graph with sample data
8. REPORT — LLM report prompt includes all 5 sections (요약, 데이터 개요, 발견사항, 인사이트, 권장 액션)

Output format:
- PASS: Code meets all criteria. No changes needed.
- FAIL: List each issue with:
  - [ISSUE] Description
  - [LINE] Approximate location
  - [FIX] Specific fix suggestion

Be strict but fair. Only fail for real issues, not style preferences.
```

## 사용 Skill
- `skill/qa_reviewer.md`

## 입력
- `output.py` (Coder 출력)
- `skill_input.md` (원본 스키마, 대조용)

## 출력
- QA 리포트: PASS 또는 FAIL + 피드백 목록
""")

    # ================================================================
    # skill/data_architect.md
    # ================================================================
    write_file("skill/data_architect.md", """\
# Skill: data_architect

## 목적
분석 주제에 맞는 input 데이터 스키마를 설계합니다.

## 실행 규칙

### 1. 주제 분석
- 주제 키워드에서 도메인 파악 (고객, 매출, 리뷰, 로그 등)
- 분석 목표 정의 (예측, 분류, 트렌드, 감성 등)

### 2. 컬럼 설계
- 식별자 컬럼 (1개): ID 역할
- 수치형 피처 (4~6개): 분석에 핵심적인 수치 데이터
- 범주형 피처 (1~2개): 세그먼트 분류용
- 타겟 컬럼 (1개): 분석 목표 변수 (이탈 여부, 만족도 등)
- 날짜/시간 컬럼 (선택): 시계열 분석 필요 시

### 3. TypedDict 정의
```python
class AnalysisState(TypedDict):
    topic: str
    raw_data: list[dict]
    cleaned_data: list[dict]
    stat_result: dict
    llm_analysis: str
    report: str
```

### 4. 샘플 데이터 생성
- 최소 15~20행
- 현실적인 값 분포 (편향 포함)
- 의도적 결측값 2~3건 포함 (전처리 테스트용)
- 타겟 변수 비율: 대략 40:60 ~ 50:50

### 5. 출력 형식
`skill_input.md` 파일로 출력:
```markdown
# 데이터 스키마: {주제}

## 컬럼 정의
| 필드 | 타입 | 설명 | 예시값 |
|------|------|------|--------|
| ... | ... | ... | ... |

## TypedDict
(코드 블록)

## 샘플 데이터
(Python dict 리스트)

## 분석 계획
1. 전처리: ...
2. 통계 분석: ...
3. LLM 분석 초점: ...
4. 리포트 핵심 섹션: ...
```

## 주제별 적응 예시

| 주제 | 핵심 피처 | 타겟 |
|------|-----------|------|
| 이탈 예측 | tenure, support_calls, satisfaction | churned (0/1) |
| 매출 분석 | daily_revenue, category, season | revenue_trend |
| 감성 분석 | review_text, rating, date | sentiment |
| 재고 최적화 | stock_level, demand, lead_time | stockout_risk |
""")

    # ================================================================
    # skill/graph_builder.md
    # ================================================================
    write_file("skill/graph_builder.md", """\
# Skill: graph_builder

## 목적
LangGraph StateGraph를 구성하는 완성된 코드를 생성합니다.

## 노드 정의 (4개 필수)

### Node 1: validate_and_preprocess
```
입력: raw_data (list[dict])
처리:
  - 결측값 탐지 → 수치형은 중앙값 대체, 범주형은 최빈값 대체
  - 이상치 범위 보정 (score 0~10 등)
  - Min-max 정규화 → {field}_norm 키 추가
  - Composite Risk/Score 계산 (도메인별 가중치 적용)
출력: cleaned_data (list[dict])
```

### Node 2: statistical_analysis
```
입력: cleaned_data
처리:
  - 기본 비율/빈도 계산 (타겟 변수 기준)
  - 그룹별 피처 평균 비교 (타겟 Y vs N)
  - Pearson 상관계수 계산 (타겟과의 상관관계)
  - 세그먼트 분류 (High/Medium/Low)
  - 범주형 변수별 분석
  - 기술 통계량 (min, max, mean, median, std)
출력: stat_result (dict)
```

### Node 3: llm_deep_analysis
```
입력: stat_result
처리:
  - 통계 결과를 구조화된 프롬프트로 변환
  - LLM에게 패턴 해석, 인사이트 도출 요청
  - 5가지 관점 분석 (동인, 프로파일, 패턴, 전략, 개선점)
출력: llm_analysis (str)
```

### Node 4: llm_generate_report
```
입력: stat_result + llm_analysis
처리:
  - 전체 분석 결과 종합
  - 구조화된 리포트 프롬프트 생성
  - LLM이 5개 섹션 한국어 마크다운 리포트 작성
출력: report (str)
```

## Edge 구성
```python
graph.set_entry_point("validate")
graph.add_edge("validate", "analyze")
graph.add_edge("analyze", "llm_analyze")
graph.add_edge("llm_analyze", "report")
graph.add_edge("report", END)
```

## 코드 구조 규칙
- 모든 함수는 `(state: AnalysisState) -> dict` 시그니처
- 반환값은 State의 특정 키만 업데이트하는 dict
- 각 노드 시작 시 진행 상황 print
- 수학 함수는 math/statistics 모듈만 사용 (numpy/pandas 금지)
""")

    # ================================================================
    # skill/llm_analyzer.md
    # ================================================================
    write_file("skill/llm_analyzer.md", """\
# Skill: llm_analyzer

## 목적
통계 분석 결과를 LLM에 전달하여 심층 인사이트를 도출합니다.

## LLM 설정
- 모델: `ChatAnthropic(model="claude-sonnet-4-6")`
- Temperature: 0.3 (일관된 분석)

## 프롬프트 구성 규칙

### 입력 데이터 포맷
통계 결과(stat_result)에서 다음을 추출하여 프롬프트에 포함:
- 전체 요약 수치 (대상 수, 비율 등)
- 피처별 평균 비교 (타겟 Y vs N)
- 상관관계 TOP 5 피처
- 세그먼트별 현황
- 범주형 변수 분석
- 주요 기술 통계

### 분석 요청 5가지 관점
1. **핵심 동인 (Key Drivers)** — 가장 강력한 영향 요인 3가지, 수치 근거
2. **고위험 프로파일** — 위험이 높은 대상의 구체적 특성 조합
3. **숨겨진 패턴** — 단순 평균 비교로 보이지 않는 잠재적 패턴, 이상 징후
4. **세그먼트별 전략** — 세그먼트/범주별 차별화된 대응 방향
5. **모델 개선 시사점** — 규칙 기반 한계, ML 적용 시 고려할 피처

### 프롬프트 템플릿
```
당신은 {domain} 전문 데이터 사이언티스트입니다.
아래 통계 분석 결과를 바탕으로 심층적인 인사이트를 도출해주세요.

=== 분석 데이터 개요 ===
{summary_stats}

=== 피처 평균 비교 ===
{mean_comparison}

=== 상관관계 TOP 5 ===
{correlations}

=== 세그먼트별 현황 ===
{segment_stats}

다음 5가지 관점에서 분석해주세요:
1. 핵심 동인...
2. 고위험 프로파일...
3. 숨겨진 패턴...
4. 세그먼트별 전략...
5. 모델 개선 시사점...

각 항목은 구체적인 수치를 인용하며 논리적으로 설명해주세요.
```
""")

    # ================================================================
    # skill/report_designer.md
    # ================================================================
    write_file("skill/report_designer.md", """\
# Skill: report_designer

## 목적
전체 분석 결과를 종합하여 LLM이 구조화된 한국어 리포트를 생성합니다.

## LLM 설정
- 모델: `ChatAnthropic(model="claude-sonnet-4-6")`
- Temperature: 0.2 (정확하고 일관된 리포트)

## 리포트 구조 (5개 섹션)

### 1. 요약 (Executive Summary)
- 핵심 발견사항 3줄 요약
- 즉각적인 비즈니스 임팩트
- 가장 중요한 수치 1~2개 강조

### 2. 데이터 개요
- 분석 데이터 스키마 설명 (마크다운 표)
- 데이터 품질 현황 (결측값, 이상값 처리 내역)
- 분석 대상 볼륨 및 핵심 비율

### 3. 통계 분석 결과
- 상관관계 피처 순위 (표)
- 타겟별 프로파일 비교 (표)
- 세그먼트별 현황 분석 (표)
- 범주형 변수별 분석

### 4. LLM 인사이트
- 핵심 동인 분석
- 고위험 프로파일 서술
- 숨겨진 패턴 및 이상 징후
- 세그먼트별 전략 방향

### 5. 권장 액션 플랜
- 우선순위별 실행 방안 (즉시 / 단기 / 중기)
- 예측 모델 고도화 로드맵
- 성과 지표(KPI) 제안

## 프롬프트 설계 원칙
- 구체적인 수치를 반드시 인용
- 실무 적용 가능한 액션 중심
- 마크다운 표 적극 활용
- 한국어 작성, 전문 용어는 영문 병기
""")

    # ================================================================
    # skill/qa_reviewer.md
    # ================================================================
    write_file("skill/qa_reviewer.md", """\
# Skill: qa_reviewer

## 목적
생성된 LangGraph 코드의 품질을 검증하고 피드백을 제공합니다.

## 검증 체크리스트 (8항목)

### 1. STRUCTURE
- [ ] StateGraph에 4개 필수 노드 존재 (validate, analyze, llm_analyze, report)
- [ ] AnalysisState TypedDict에 6개 필수 키 존재

### 2. COMPLETENESS
- [ ] 모든 함수에 실제 로직 구현 (placeholder 없음)
- [ ] "...", "pass", "TODO" 없음

### 3. DATA
- [ ] 샘플 데이터 15행 이상
- [ ] TypedDict 스키마와 샘플 데이터 컬럼 일치
- [ ] 의도적 결측값 포함 (전처리 테스트용)

### 4. IMPORTS
- [ ] 모든 import가 실제 사용됨
- [ ] langgraph, langchain_anthropic import 존재

### 5. LLM NODES
- [ ] ChatAnthropic(model="claude-sonnet-4-6") 사용
- [ ] 분석 노드 temperature=0.3
- [ ] 리포트 노드 temperature=0.2

### 6. EDGE FLOW
- [ ] set_entry_point("validate")
- [ ] validate → analyze → llm_analyze → report → END 순서

### 7. RUNNABLE
- [ ] if __name__ == "__main__" 블록 존재
- [ ] initial_state 정의 및 app.invoke() 호출
- [ ] 최종 리포트 print

### 8. REPORT
- [ ] LLM 리포트 프롬프트에 5개 섹션 포함
- [ ] 한국어 출력 지시

## 출력 형식
```
## QA 결과: {PASS|FAIL}

### 통과 항목
- [x] STRUCTURE: ...
- [x] COMPLETENESS: ...

### 실패 항목
- [ISSUE] {설명}
  [LINE] {위치}
  [FIX] {수정 방안}

### 종합 의견
{전체 평가}
```

## 루프 규칙
- FAIL 시 → 피드백을 Coder Agent에게 전달
- Coder가 수정 후 → 재검증
- 최대 3회 반복 후 강제 종료 (최선의 버전 채택)
""")

    # ================================================================
    # command/create_analysis.py
    # ================================================================
    write_file("command/create_analysis.py", """\
\"\"\"
LangGraph Analysis Creator - 전체 파이프라인 실행

사용법:
  python command/create_analysis.py --topic "이탈 예측 분석"

워크플로우:
  1. Planner Agent: 주제 분석 → skill_input.md 생성
  2. Coder Agent: skill_input.md → LangGraph 코드 생성
  3. QA Agent: 코드 검증 → 피드백 → Coder 수정 (최대 3회 루프)
  4. 최종 코드 + 리포트 출력
\"\"\"

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
    print("\\n[Step 1] Planner Agent 실행...")
    planner_system = load_agent("planner")
    data_architect_skill = load_skill("data_architect")

    planner_prompt = f\"\"\"주제: {args.topic}

아래 skill 정의에 따라 이 주제의 데이터 스키마를 설계해줘:

{data_architect_skill}

skill_input.md 형식으로 출력해줘.\"\"\"

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
        print(f"\\n[Step 2-{loop}] Coder Agent 실행 (루프 {loop}/{args.max_qa_loops})...")

        feedback_section = ""
        if qa_feedback:
            feedback_section = f\"\"\"

## QA 피드백 (이전 라운드)
아래 피드백을 반영하여 코드를 수정해줘:
{qa_feedback}\"\"\"

        coder_prompt = f\"\"\"주제: {args.topic}

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
Python 코드만 출력해줘 (마크다운 코드블록 없이).\"\"\"

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
        print(f"\\n[Step 3-{loop}] QA Agent 실행 (루프 {loop}/{args.max_qa_loops})...")

        qa_prompt = f\"\"\"아래 LangGraph 코드를 검증해줘:

## 원본 스키마
{skill_input}

## 생성된 코드
```python
{final_code}
```

## QA 체크리스트
{qa_reviewer_skill}

위 체크리스트에 따라 PASS 또는 FAIL 판정해줘.\"\"\"

        qa_result = run_agent(
            client,
            model=config["agents"]["qa"]["model"],
            system=qa_system,
            user_msg=qa_prompt,
        )

        qa_path = os.path.join(OUTPUT_DIR, f"qa_report_loop{loop}.md")
        with open(qa_path, "w") as f:
            f.write(qa_result)

        if "PASS" in qa_result.upper().split("\\n")[0] or "## QA 결과: PASS" in qa_result:
            print(f"  ✅ QA PASS — 코드 승인 완료")
            break
        else:
            print(f"  ❌ QA FAIL — 피드백 전달 후 재생성")
            qa_feedback = qa_result
    else:
        print(f"\\n  ⚠️  QA 루프 {args.max_qa_loops}회 초과 — 최선의 버전 채택")

    # ── 최종 결과 ──
    print("\\n" + "=" * 60)
    print("  ✅ 파이프라인 완료")
    print("=" * 60)
    print(f"  📁 출력 폴더: {OUTPUT_DIR}")
    print(f"  📄 skill_input.md  — 데이터 스키마")
    print(f"  📄 output.py       — LangGraph 코드")
    print(f"  📄 qa_report_*.md  — QA 리포트")
    print(f"\\n  실행: python {os.path.join(OUTPUT_DIR, 'output.py')}")


if __name__ == "__main__":
    main()
""")

    # ================================================================
    # command/run_qa.py
    # ================================================================
    write_file("command/run_qa.py", """\
\"\"\"
QA Agent 단독 실행

사용법:
  python command/run_qa.py --file outputs/output.py
\"\"\"

import argparse
import os
import yaml
from anthropic import Anthropic

HARNESS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser(description="QA Agent 단독 실행")
    parser.add_argument("--file", required=True, help="검증할 Python 파일 경로")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        code = f.read()

    config_path = os.path.join(HARNESS_ROOT, "harness", "config", "models.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    qa_skill_path = os.path.join(HARNESS_ROOT, "harness", "skill", "qa_reviewer.md")
    with open(qa_skill_path, "r") as f:
        qa_skill = f.read()

    qa_agent_path = os.path.join(HARNESS_ROOT, "harness", "agent", "qa.md")
    with open(qa_agent_path, "r") as f:
        qa_system = f.read()

    client = Anthropic()
    response = client.messages.create(
        model=config["agents"]["qa"]["model"],
        max_tokens=8000,
        system=qa_system,
        messages=[{
            "role": "user",
            "content": f\"\"\"아래 코드를 검증해줘:

```python
{code}
```

{qa_skill}\"\"\"
        }],
    )

    result = response.content[0].text
    print(result)

    out_path = os.path.join(os.path.dirname(args.file), "qa_report.md")
    with open(out_path, "w") as f:
        f.write(result)
    print(f"\\n📄 QA 리포트 저장: {out_path}")


if __name__ == "__main__":
    main()
""")

    # ================================================================
    # command/generate_report.py
    # ================================================================
    write_file("command/generate_report.py", """\
\"\"\"
리포트만 재생성

사용법:
  python command/generate_report.py --file outputs/output.py
\"\"\"

import argparse
import os
import yaml
from anthropic import Anthropic

HARNESS_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser(description="리포트 재생성")
    parser.add_argument("--file", required=True, help="LangGraph 코드 파일 경로")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        code = f.read()

    config_path = os.path.join(HARNESS_ROOT, "harness", "config", "models.yaml")
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    report_skill_path = os.path.join(HARNESS_ROOT, "harness", "skill", "report_designer.md")
    with open(report_skill_path, "r") as f:
        report_skill = f.read()

    client = Anthropic()
    response = client.messages.create(
        model=config["agents"]["coder"]["model"],
        max_tokens=8000,
        temperature=0.2,
        system="You are a report generation specialist. Extract the analysis results from the given LangGraph code and generate a comprehensive Korean markdown report.",
        messages=[{
            "role": "user",
            "content": f\"\"\"아래 LangGraph 코드의 통계 분석 로직과 샘플 데이터를 분석하여
리포트를 직접 생성해줘.

```python
{code}
```

리포트 구조:
{report_skill}\"\"\"
        }],
    )

    result = response.content[0].text
    out_path = os.path.join(os.path.dirname(args.file), "report.md")
    with open(out_path, "w") as f:
        f.write(result)
    print(f"📄 리포트 저장: {out_path}")
    print(result[:500] + "...")


if __name__ == "__main__":
    main()
""")

    # ================================================================
    # template/langgraph_template.py
    # ================================================================
    write_file("template/langgraph_template.py", """\
\"\"\"
LangGraph Analysis Pipeline Template
=====================================
이 템플릿을 기반으로 주제별 분석 파이프라인을 생성합니다.
Coder Agent가 이 구조를 따라 코드를 작성합니다.
\"\"\"

from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
import math
import statistics


# ============================================================
# State Definition — 모든 노드가 공유하는 상태
# ============================================================
class AnalysisState(TypedDict):
    topic: str
    raw_data: list[dict]
    cleaned_data: list[dict]
    stat_result: dict
    llm_analysis: str
    report: str


# ============================================================
# Sample Data — 주제에 맞게 15~20행 생성
# ============================================================
SAMPLE_DATA: list[dict] = [
    # Coder Agent가 주제에 맞는 샘플 데이터로 채움
]


# ============================================================
# Node 1: validate_and_preprocess
# ============================================================
def validate_and_preprocess(state: AnalysisState) -> dict:
    print("[Node 1] 데이터 검증 및 전처리 시작...")
    raw = state["raw_data"]
    # 1-A. 결측값 처리 (중앙값 대체)
    # 1-B. 범위/타입 검증
    # 1-C. Min-max 정규화
    # 1-D. Composite Score 계산
    # Coder Agent가 실제 로직으로 채움
    return {"cleaned_data": raw}


# ============================================================
# Node 2: statistical_analysis
# ============================================================
def statistical_analysis(state: AnalysisState) -> dict:
    print("[Node 2] 통계 분석 시작...")
    data = state["cleaned_data"]
    # 2-A. 기본 비율/빈도
    # 2-B. 그룹별 평균 비교
    # 2-C. Pearson 상관계수
    # 2-D. 세그먼트 분류
    # 2-E. 범주형 분석
    # 2-F. 기술 통계
    # Coder Agent가 실제 로직으로 채움
    return {"stat_result": {}}


# ============================================================
# Node 3: llm_deep_analysis
# ============================================================
def llm_deep_analysis(state: AnalysisState) -> dict:
    print("[Node 3] LLM 심층 분석 시작...")
    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.3)
    # Coder Agent가 통계 결과를 프롬프트로 변환
    prompt = "..."
    response = llm.invoke(prompt)
    print("  ✅ LLM 심층 분석 완료")
    return {"llm_analysis": response.content}


# ============================================================
# Node 4: llm_generate_report
# ============================================================
def llm_generate_report(state: AnalysisState) -> dict:
    print("[Node 4] LLM 리포트 생성 시작...")
    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.2)
    # Coder Agent가 리포트 프롬프트 생성
    prompt = "..."
    response = llm.invoke(prompt)
    print("  ✅ 리포트 생성 완료")
    return {"report": response.content}


# ============================================================
# Graph Construction
# ============================================================
def build_graph() -> StateGraph:
    graph = StateGraph(AnalysisState)
    graph.add_node("validate", validate_and_preprocess)
    graph.add_node("analyze", statistical_analysis)
    graph.add_node("llm_analyze", llm_deep_analysis)
    graph.add_node("report", llm_generate_report)
    graph.set_entry_point("validate")
    graph.add_edge("validate", "analyze")
    graph.add_edge("analyze", "llm_analyze")
    graph.add_edge("llm_analyze", "report")
    graph.add_edge("report", END)
    return graph.compile()


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  분석 파이프라인 시작")
    print("=" * 60)

    app = build_graph()
    initial_state: AnalysisState = {
        "topic": "",
        "raw_data": SAMPLE_DATA,
        "cleaned_data": [],
        "stat_result": {},
        "llm_analysis": "",
        "report": "",
    }
    final_state = app.invoke(initial_state)

    print("\\n" + "=" * 60)
    print("  최종 리포트")
    print("=" * 60)
    print(final_state["report"])
""")

    # ================================================================
    # template/report_template.md
    # ================================================================
    write_file("template/report_template.md", """\
# 📊 {주제} 분석 보고서

## 1. 요약 (Executive Summary)
- 핵심 발견사항 1
- 핵심 발견사항 2
- 핵심 발견사항 3

## 2. 데이터 개요

### 데이터 스키마
| 필드 | 타입 | 설명 |
|------|------|------|
| ... | ... | ... |

### 데이터 품질
- 총 데이터: N건
- 결측값 처리: N건
- 이상값 보정: N건

## 3. 통계 분석 결과

### 상관관계 피처 순위
| 순위 | 피처 | 상관계수 |
|------|------|----------|
| 1 | ... | ... |

### 그룹별 프로파일 비교
| 피처 | 그룹A 평균 | 그룹B 평균 | 차이 |
|------|-----------|-----------|------|
| ... | ... | ... | ... |

### 세그먼트별 현황
| 세그먼트 | 건수 | 비율 |
|----------|------|------|
| High | ... | ... |
| Medium | ... | ... |
| Low | ... | ... |

## 4. LLM 인사이트
### 핵심 동인
### 고위험 프로파일
### 숨겨진 패턴
### 세그먼트별 전략

## 5. 권장 액션 플랜

### 즉시 실행
- [ ] ...

### 단기 (1~3개월)
- [ ] ...

### 중기 (3~6개월)
- [ ] ...

### KPI 제안
| 지표 | 현재 | 목표 |
|------|------|------|
| ... | ... | ... |
""")

    # ================================================================
    # config/models.yaml
    # ================================================================
    write_file("config/models.yaml", """\
# LangGraph Analysis Creator - 모델 설정

agents:
  planner:
    model: "claude-sonnet-4-6"
    temperature: 0.0
    max_tokens: 8000
    description: "주제 분석 + 데이터 스키마 설계"

  coder:
    model: "claude-sonnet-4-6"
    temperature: 0.0
    max_tokens: 16000
    description: "LangGraph 코드 생성"

  qa:
    model: "claude-sonnet-4-6"
    temperature: 0.0
    max_tokens: 8000
    description: "코드 품질 검증"

llm_nodes:
  deep_analysis:
    model: "claude-sonnet-4-6"
    temperature: 0.3
    description: "통계 결과 → LLM 심층 분석"

  report_generation:
    model: "claude-sonnet-4-6"
    temperature: 0.2
    description: "최종 리포트 생성"

qa_loop:
  max_iterations: 3
  pass_threshold: "all 8 checks pass"
""")

    # ================================================================
    # config/environment.yaml
    # ================================================================
    write_file("config/environment.yaml", """\
# LangGraph Analysis Creator - 환경 설정

runtime:
  python: "3.11+"

dependencies:
  pip:
    - anthropic>=0.90.0
    - langgraph>=0.2.0
    - langchain-anthropic>=0.3.0
    - langchain-core>=0.3.0
    - pyyaml>=6.0

environment_variables:
  required:
    - ANTHROPIC_API_KEY
  optional:
    - LANGCHAIN_TRACING_V2  # LangSmith tracing
    - LANGCHAIN_API_KEY

managed_agent:
  type: cloud
  networking: unrestricted
  init_script: "pip install anthropic langgraph langchain-anthropic pyyaml -q"
""")

    # ================================================================
    # examples/churn_prediction/skill_input.md
    # ================================================================
    write_file("examples/churn_prediction/skill_input.md", """\
# 데이터 스키마: 이탈 예측 분석

## 컬럼 정의
| 필드 | 타입 | 설명 | 예시값 |
|------|------|------|--------|
| customer_id | str | 고객 고유 식별자 | "C001" |
| age | int | 고객 연령 | 45 |
| tenure_months | int | 가입 후 경과 월수 | 3 |
| monthly_charges | float | 월 청구 금액 | 89.0 |
| num_products | int | 사용 중인 상품 수 | 1 |
| support_calls | int | 최근 6개월 CS 문의 횟수 | 7 |
| last_login_days | int | 마지막 로그인 후 경과일 | 42 |
| satisfaction_score | int | CSAT 점수 (1-10) | 2 |
| payment_method | str | 결제 방식 (auto/manual) | "manual" |
| churned | int | 이탈 여부 (1=이탈, 0=유지) | 1 |

## TypedDict
```python
class AnalysisState(TypedDict):
    topic: str
    raw_data: list[dict]
    cleaned_data: list[dict]
    stat_result: dict
    llm_analysis: str
    report: str
```

## 분석 계획
1. 전처리: 결측값 중앙값 대체, 범위 보정, Min-max 정규화, Churn Risk Score 계산
2. 통계 분석: 이탈률, 피처 평균 비교, Pearson 상관계수, 위험 티어 분류, 결제방식 분석
3. LLM 분석 초점: 이탈 동인, 고위험 프로파일, 숨겨진 패턴, 세그먼트별 전략
4. 리포트 핵심 섹션: 요약, 데이터 개요, 통계 결과, LLM 인사이트, 권장 액션
""")

    # ================================================================
    # examples/churn_prediction/output.py (심볼릭 참조)
    # ================================================================
    write_file("examples/churn_prediction/output.py", """\
# 이 파일은 실제 생성된 예시 코드의 참조입니다.
# 전체 코드는 command/ 상위 디렉토리의 churn_analysis_langgraph.py를 참조하세요.
#
# 실행: python command/create_analysis.py --topic "이탈 예측 분석"
# 결과: outputs/output.py 에 생성됨
""")

    # ================================================================
    # 완료
    # ================================================================
    file_count = sum(
        len(files) for _, _, files in os.walk(HARNESS)
    )
    print(f"\n{'=' * 60}")
    print(f"  ✅ 총 {file_count}개 파일 생성 완료")
    print(f"  📁 경로: {HARNESS}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()

