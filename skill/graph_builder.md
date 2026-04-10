# Skill: graph_builder

## 역할
LangGraph StateGraph 전체 코드를 구성합니다.

## 노드 구성 (4개)

### Node 1: validate_and_preprocess
- 데이터 검증 (결측치, 타입, 범위)
- 결측값 중앙값 대체
- Min-max 정규화
- Composite Risk Score 계산

### Node 2: statistical_analysis
- 전체 이탈률 계산
- 이탈/유지 그룹별 피처 평균 비교
- Pearson 상관관계 분석
- 위험 티어 세그먼테이션 (High/Medium/Low)
- 결제 방식별 이탈률 분석
- 기술 통계량 산출

### Node 3: llm_deep_analysis
- 통계 분석 결과를 LLM(Claude)에 전달
- 핵심 이탈 동인 해석
- 고위험 고객 프로파일 도출
- 숨겨진 패턴 및 이상 징후 탐지
- 세그먼트별 전략 방향 제시

### Node 4: llm_generate_report
- 전체 분석 결과를 종합하여 LLM이 한국어 마크다운 리포트 생성
- 리포트 구조: 요약 → 데이터 개요 → 통계 결과 → LLM 인사이트 → 권장 액션

## Edge 흐름
```
validate → analyze → llm_analyze → report → END
```

## LLM 설정
- 모델: `claude-sonnet-4-6`
- 분석 노드 temperature: 0.3
- 리포트 노드 temperature: 0.2
