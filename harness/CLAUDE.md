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
