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
