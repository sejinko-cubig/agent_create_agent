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
