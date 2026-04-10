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
