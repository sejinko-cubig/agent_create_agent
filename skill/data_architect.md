# Skill: data_architect

## 역할
주제(topic)가 주어지면 분석에 필요한 input 데이터 스키마를 설계합니다.

## 수행 내용
- 분석 주제에 적합한 컬럼/필드 식별
- LangGraph State용 TypedDict 타입 정의
- 현실적인 샘플 데이터 3~5행 생성

## 출력 예시 (이탈 예측 분석)
```python
class AnalysisState(TypedDict):
    topic: str
    raw_data: list[dict]        # customer_id, age, tenure_months, monthly_charges, ...
    cleaned_data: list[dict]
    stat_result: dict
    llm_analysis: str
    report: str
```

### 데이터 필드 정의
| 필드 | 타입 | 설명 |
|------|------|------|
| customer_id | str | 고객 고유 식별자 |
| age | int | 고객 연령 |
| tenure_months | int | 가입 후 경과 월수 |
| monthly_charges | float | 월 청구 금액 |
| num_products | int | 사용 중인 상품 수 |
| support_calls | int | 최근 6개월 CS 문의 횟수 |
| last_login_days | int | 마지막 로그인 후 경과일 |
| satisfaction_score | int | CSAT 점수 (1-10) |
| payment_method | str | 결제 방식 (auto/manual) |
| churned | int | 이탈 여부 (1=이탈, 0=유지) |
