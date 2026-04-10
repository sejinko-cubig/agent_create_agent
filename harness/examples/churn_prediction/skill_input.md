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
