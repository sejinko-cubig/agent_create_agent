"""
================================================
  Customer Churn Prediction Analysis Pipeline
  LangGraph + Claude (claude-sonnet-4-6)
================================================
Topic  : 이탈 예측 분석
Author : LangGraph Analysis Creator
"""

import os
import math
import statistics
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic


# ============================================================
# 0. State Definition
#    AnalysisState stores every artifact produced by each node.
# ============================================================
class AnalysisState(TypedDict):
    topic: str
    raw_data: list[dict]
    cleaned_data: list[dict]
    stat_result: dict
    llm_analysis: str
    report: str


# ============================================================
# 1. Sample Data
#    Realistic customer records for churn analysis.
#    Fields:
#      customer_id       - unique customer identifier
#      age               - customer age
#      tenure_months     - months since subscription start
#      monthly_charges   - monthly billing amount (KRW 1,000 units)
#      num_products      - number of active products/services
#      support_calls     - customer-service call count (last 6 months)
#      last_login_days   - days since last platform login
#      satisfaction_score- CSAT score 1-10
#      payment_method    - 'auto' | 'manual'
#      churned           - 1 = churned, 0 = retained (ground truth label)
# ============================================================
SAMPLE_DATA: list[dict] = [
    # --- High-risk churners (churned = 1) ---
    {
        "customer_id": "C001", "age": 45, "tenure_months": 3,
        "monthly_charges": 89, "num_products": 1, "support_calls": 7,
        "last_login_days": 42, "satisfaction_score": 2,
        "payment_method": "manual", "churned": 1,
    },
    {
        "customer_id": "C002", "age": 32, "tenure_months": 6,
        "monthly_charges": 120, "num_products": 1, "support_calls": 5,
        "last_login_days": 30, "satisfaction_score": 3,
        "payment_method": "manual", "churned": 1,
    },
    {
        "customer_id": "C003", "age": 55, "tenure_months": 2,
        "monthly_charges": 75, "num_products": 1, "support_calls": 9,
        "last_login_days": 60, "satisfaction_score": 1,
        "payment_method": "manual", "churned": 1,
    },
    {
        "customer_id": "C004", "age": 28, "tenure_months": 4,
        "monthly_charges": 95, "num_products": 2, "support_calls": 6,
        "last_login_days": 25, "satisfaction_score": 4,
        "payment_method": "auto", "churned": 1,
    },
    {
        "customer_id": "C005", "age": 61, "tenure_months": 1,
        "monthly_charges": 55, "num_products": 1, "support_calls": 8,
        "last_login_days": 75, "satisfaction_score": 2,
        "payment_method": "manual", "churned": 1,
    },
    # --- Medium-risk customers ---
    {
        "customer_id": "C006", "age": 38, "tenure_months": 14,
        "monthly_charges": 110, "num_products": 2, "support_calls": 3,
        "last_login_days": 15, "satisfaction_score": 5,
        "payment_method": "auto", "churned": 0,
    },
    {
        "customer_id": "C007", "age": 42, "tenure_months": 11,
        "monthly_charges": 130, "num_products": 2, "support_calls": 4,
        "last_login_days": 18, "satisfaction_score": 6,
        "payment_method": "manual", "churned": 0,
    },
    {
        "customer_id": "C008", "age": 50, "tenure_months": 9,
        "monthly_charges": 85, "num_products": 2, "support_calls": 2,
        "last_login_days": 20, "satisfaction_score": 5,
        "payment_method": "auto", "churned": 1,
    },
    {
        "customer_id": "C009", "age": 35, "tenure_months": 16,
        "monthly_charges": 140, "num_products": 3, "support_calls": 3,
        "last_login_days": 10, "satisfaction_score": 6,
        "payment_method": "auto", "churned": 0,
    },
    {
        "customer_id": "C010", "age": 29, "tenure_months": 8,
        "monthly_charges": 100, "num_products": 1, "support_calls": 5,
        "last_login_days": 22, "satisfaction_score": 4,
        "payment_method": "manual", "churned": 1,
    },
    # --- Low-risk loyal customers ---
    {
        "customer_id": "C011", "age": 33, "tenure_months": 36,
        "monthly_charges": 200, "num_products": 4, "support_calls": 1,
        "last_login_days": 2, "satisfaction_score": 9,
        "payment_method": "auto", "churned": 0,
    },
    {
        "customer_id": "C012", "age": 47, "tenure_months": 48,
        "monthly_charges": 180, "num_products": 3, "support_calls": 0,
        "last_login_days": 1, "satisfaction_score": 10,
        "payment_method": "auto", "churned": 0,
    },
    {
        "customer_id": "C013", "age": 26, "tenure_months": 24,
        "monthly_charges": 150, "num_products": 3, "support_calls": 1,
        "last_login_days": 3, "satisfaction_score": 8,
        "payment_method": "auto", "churned": 0,
    },
    {
        "customer_id": "C014", "age": 39, "tenure_months": 30,
        "monthly_charges": 220, "num_products": 5, "support_calls": 2,
        "last_login_days": 5, "satisfaction_score": 9,
        "payment_method": "auto", "churned": 0,
    },
    {
        "customer_id": "C015", "age": 52, "tenure_months": 42,
        "monthly_charges": 195, "num_products": 4, "support_calls": 1,
        "last_login_days": 4, "satisfaction_score": 8,
        "payment_method": "auto", "churned": 0,
    },
    # --- Edge / anomaly cases ---
    {
        "customer_id": "C016", "age": None, "tenure_months": 5,  # missing age
        "monthly_charges": 60, "num_products": 1, "support_calls": 6,
        "last_login_days": 35, "satisfaction_score": 3,
        "payment_method": "manual", "churned": 1,
    },
    {
        "customer_id": "C017", "age": 44, "tenure_months": 20,
        "monthly_charges": None, "num_products": 2, "support_calls": 2,  # missing charge
        "last_login_days": 12, "satisfaction_score": 7,
        "payment_method": "auto", "churned": 0,
    },
    {
        "customer_id": "C018", "age": 31, "tenure_months": 7,
        "monthly_charges": 105, "num_products": 2, "support_calls": 4,
        "last_login_days": 28, "satisfaction_score": 5,
        "payment_method": "auto", "churned": 0,
    },
    {
        "customer_id": "C019", "age": 67, "tenure_months": 60,  # long-tenure but unhappy
        "monthly_charges": 250, "num_products": 5, "support_calls": 8,
        "last_login_days": 50, "satisfaction_score": 3,
        "payment_method": "manual", "churned": 1,
    },
    {
        "customer_id": "C020", "age": 23, "tenure_months": 2,
        "monthly_charges": 40, "num_products": 1, "support_calls": 0,
        "last_login_days": 8, "satisfaction_score": 7,
        "payment_method": "auto", "churned": 0,
    },
]


# ============================================================
# Node 1 ─ validate_and_preprocess
#   • Missing value detection & imputation
#   • Type coercion & range validation
#   • Min-max normalization for numeric features
#   • Risk-score computation per customer
# ============================================================
def validate_and_preprocess(state: AnalysisState) -> dict:
    print("\n[Node 1] 데이터 검증 및 전처리 시작...")

    raw: list[dict] = state["raw_data"]
    issues: list[str] = []

    # ── 1-A. Impute missing values with column medians ──────────
    numeric_fields = [
        "age", "tenure_months", "monthly_charges",
        "num_products", "support_calls", "last_login_days",
        "satisfaction_score",
    ]
    medians: dict[str, float] = {}
    for field in numeric_fields:
        vals = [r[field] for r in raw if r.get(field) is not None]
        if vals:
            sorted_vals = sorted(vals)
            n = len(sorted_vals)
            medians[field] = (
                sorted_vals[n // 2] if n % 2 == 1
                else (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
            )

    cleaned: list[dict] = []
    for row in raw:
        record = dict(row)
        for field in numeric_fields:
            if record.get(field) is None:
                record[field] = medians.get(field, 0)
                issues.append(
                    f"[{record['customer_id']}] '{field}' 결측값 → 중앙값({medians.get(field, 0)}) 대체"
                )
        cleaned.append(record)

    # ── 1-B. Range / type validation ────────────────────────────
    for record in cleaned:
        if not (0 <= record["satisfaction_score"] <= 10):
            record["satisfaction_score"] = max(0, min(10, record["satisfaction_score"]))
            issues.append(f"[{record['customer_id']}] satisfaction_score 범위 보정")
        if record["last_login_days"] < 0:
            record["last_login_days"] = 0
            issues.append(f"[{record['customer_id']}] last_login_days 음수 → 0 보정")

    # ── 1-C. Min-max normalization (store as new keys: *_norm) ──
    def minmax(values: list[float]) -> list[float]:
        lo, hi = min(values), max(values)
        if hi == lo:
            return [0.5] * len(values)
        return [(v - lo) / (hi - lo) for v in values]

    norm_fields = [
        "tenure_months", "monthly_charges", "num_products",
        "support_calls", "last_login_days", "satisfaction_score",
    ]
    for field in norm_fields:
        vals = [r[field] for r in cleaned]
        normed = minmax(vals)
        for record, nv in zip(cleaned, normed):
            record[f"{field}_norm"] = round(nv, 4)

    # ── 1-D. Composite Churn Risk Score (0-100) ─────────────────
    #   Higher score → higher churn risk
    #   Formula weights are domain-driven:
    #     + high support_calls  (weight 25 %)
    #     + high last_login_days (weight 25 %)
    #     + low  satisfaction    (weight 30 %)
    #     + low  tenure          (weight 10 %)
    #     + low  num_products    (weight 10 %)
    for record in cleaned:
        risk = (
            record["support_calls_norm"]    * 25 +
            record["last_login_days_norm"]  * 25 +
            (1 - record["satisfaction_score_norm"]) * 30 +
            (1 - record["tenure_months_norm"])       * 10 +
            (1 - record["num_products_norm"])        * 10
        )
        record["churn_risk_score"] = round(risk, 2)

    print(f"  ✅ 총 {len(cleaned)}건 처리 완료 | 이슈 {len(issues)}건")
    for issue in issues:
        print(f"     ⚠️  {issue}")

    return {"cleaned_data": cleaned}


# ============================================================
# Node 2 ─ statistical_analysis
#   • Overall churn rate
#   • Feature mean comparison (churned vs retained)
#   • Pearson correlation with churn label
#   • Risk-tier segmentation (High / Medium / Low)
#   • Payment method breakdown
#   • Confusion-proxy: risk score alignment with ground truth
# ============================================================
def statistical_analysis(state: AnalysisState) -> dict:
    print("\n[Node 2] 통계 분석 시작...")

    data = state["cleaned_data"]
    n = len(data)

    churned  = [r for r in data if r["churned"] == 1]
    retained = [r for r in data if r["churned"] == 0]

    # ── 2-A. Basic churn metrics ─────────────────────────────────
    churn_rate = round(len(churned) / n * 100, 2)

    # ── 2-B. Mean comparison per feature ────────────────────────
    numeric_feats = [
        "age", "tenure_months", "monthly_charges",
        "num_products", "support_calls", "last_login_days",
        "satisfaction_score", "churn_risk_score",
    ]

    def avg(lst: list[dict], field: str) -> float:
        vals = [r[field] for r in lst if r.get(field) is not None]
        return round(sum(vals) / len(vals), 2) if vals else 0.0

    mean_comparison: dict[str, dict] = {}
    for feat in numeric_feats:
        mean_comparison[feat] = {
            "overall":  avg(data, feat),
            "churned":  avg(churned, feat),
            "retained": avg(retained, feat),
            "diff":     round(avg(churned, feat) - avg(retained, feat), 2),
        }

    # ── 2-C. Pearson correlation with churn label ────────────────
    def pearson(xs: list[float], ys: list[float]) -> float:
        n_ = len(xs)
        if n_ < 2:
            return 0.0
        mx, my = sum(xs) / n_, sum(ys) / n_
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        dx  = math.sqrt(sum((x - mx) ** 2 for x in xs))
        dy  = math.sqrt(sum((y - my) ** 2 for y in ys))
        return round(num / (dx * dy), 4) if dx * dy != 0 else 0.0

    churn_labels = [r["churned"] for r in data]
    correlations: dict[str, float] = {}
    for feat in numeric_feats:
        feat_vals = [r[feat] for r in data]
        correlations[feat] = pearson(feat_vals, churn_labels)

    top_correlations = sorted(
        correlations.items(), key=lambda x: abs(x[1]), reverse=True
    )[:5]

    # ── 2-D. Risk tier segmentation ─────────────────────────────
    def tier(score: float) -> str:
        if score >= 60:
            return "High"
        elif score >= 35:
            return "Medium"
        return "Low"

    tier_counts: dict[str, int] = {"High": 0, "Medium": 0, "Low": 0}
    tier_churn:  dict[str, int] = {"High": 0, "Medium": 0, "Low": 0}
    for r in data:
        t = tier(r["churn_risk_score"])
        tier_counts[t] += 1
        if r["churned"] == 1:
            tier_churn[t] += 1

    tier_stats: dict[str, dict] = {}
    for t in ["High", "Medium", "Low"]:
        cnt = tier_counts[t]
        tier_stats[t] = {
            "count":      cnt,
            "churned":    tier_churn[t],
            "churn_rate": round(tier_churn[t] / cnt * 100, 1) if cnt > 0 else 0.0,
        }

    # ── 2-E. Payment method analysis ────────────────────────────
    auto_customers   = [r for r in data if r["payment_method"] == "auto"]
    manual_customers = [r for r in data if r["payment_method"] == "manual"]

    def churn_rate_of(group: list[dict]) -> float:
        if not group:
            return 0.0
        return round(sum(r["churned"] for r in group) / len(group) * 100, 1)

    payment_analysis = {
        "auto":   {"count": len(auto_customers),   "churn_rate": churn_rate_of(auto_customers)},
        "manual": {"count": len(manual_customers), "churn_rate": churn_rate_of(manual_customers)},
    }

    # ── 2-F. Risk score alignment accuracy ──────────────────────
    correct = sum(
        1 for r in data
        if (tier(r["churn_risk_score"]) in ["High", "Medium"]) == (r["churned"] == 1)
    )
    alignment_accuracy = round(correct / n * 100, 1)

    # ── 2-G. Descriptive stats for key features ──────────────────
    def desc_stats(values: list[float]) -> dict:
        sorted_v = sorted(values)
        n_ = len(sorted_v)
        mean_ = sum(sorted_v) / n_
        variance = sum((v - mean_) ** 2 for v in sorted_v) / n_
        return {
            "min":    round(min(sorted_v), 2),
            "max":    round(max(sorted_v), 2),
            "mean":   round(mean_, 2),
            "median": round(sorted_v[n_ // 2], 2),
            "std":    round(math.sqrt(variance), 2),
        }

    descriptive = {
        feat: desc_stats([r[feat] for r in data])
        for feat in ["tenure_months", "monthly_charges", "satisfaction_score",
                     "support_calls", "last_login_days", "churn_risk_score"]
    }

    stat_result = {
        "total_customers":    n,
        "churned_count":      len(churned),
        "retained_count":     len(retained),
        "overall_churn_rate": churn_rate,
        "mean_comparison":    mean_comparison,
        "correlations":       correlations,
        "top_corr_features":  top_correlations,
        "risk_tier_stats":    tier_stats,
        "payment_analysis":   payment_analysis,
        "alignment_accuracy": alignment_accuracy,
        "descriptive_stats":  descriptive,
    }

    print(f"  ✅ 전체 이탈률: {churn_rate}%")
    print(f"  ✅ 위험 티어 분포: High={tier_counts['High']}, Medium={tier_counts['Medium']}, Low={tier_counts['Low']}")
    print(f"  ✅ 상위 이탈 상관 피처: {[f[0] for f in top_correlations[:3]]}")

    return {"stat_result": stat_result}


# ============================================================
# Node 3 ─ llm_deep_analysis
#   • Pass statistical results to Claude for deeper interpretation
#   • Extract non-obvious patterns, anomalies, segment narratives
# ============================================================
def llm_deep_analysis(state: AnalysisState) -> dict:
    print("\n[Node 3] LLM 심층 분석 시작...")

    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.3)

    stat = state["stat_result"]

    # Format key stats concisely for the prompt
    top_corr_str = "\n".join(
        f"  - {feat}: {corr:+.4f}" for feat, corr in stat["top_corr_features"]
    )
    tier_str = "\n".join(
        f"  - {tier}: {v['count']}명, 이탈률 {v['churn_rate']}%"
        for tier, v in stat["risk_tier_stats"].items()
    )
    payment_str = "\n".join(
        f"  - {method}: {v['count']}명, 이탈률 {v['churn_rate']}%"
        for method, v in stat["payment_analysis"].items()
    )
    mean_diff_str = "\n".join(
        f"  - {feat}: 이탈={v['churned']}, 유지={v['retained']}, 차이={v['diff']:+.2f}"
        for feat, v in stat["mean_comparison"].items()
        if feat != "churn_risk_score"
    )

    prompt = f"""당신은 고객 이탈 예측 전문 데이터 사이언티스트입니다.
아래 통계 분석 결과를 바탕으로 심층적인 인사이트와 패턴을 도출해주세요.

=== 분석 데이터 개요 ===
- 전체 고객 수: {stat['total_customers']}명
- 이탈 고객: {stat['churned_count']}명 ({stat['overall_churn_rate']}%)
- 유지 고객: {stat['retained_count']}명
- 위험 점수 정렬 정확도: {stat['alignment_accuracy']}%

=== 이탈 여부별 피처 평균 비교 ===
{mean_diff_str}

=== 이탈 상관관계 TOP 5 피처 ===
{top_corr_str}

=== 위험 티어별 이탈 현황 ===
{tier_str}

=== 결제 방식별 이탈률 ===
{payment_str}

=== 주요 피처 기술 통계 ===
- tenure_months: 평균 {stat['descriptive_stats']['tenure_months']['mean']}개월, 중앙값 {stat['descriptive_stats']['tenure_months']['median']}
- satisfaction_score: 평균 {stat['descriptive_stats']['satisfaction_score']['mean']}, 표준편차 {stat['descriptive_stats']['satisfaction_score']['std']}
- support_calls: 평균 {stat['descriptive_stats']['support_calls']['mean']}회, 최대 {stat['descriptive_stats']['support_calls']['max']}회
- last_login_days: 평균 {stat['descriptive_stats']['last_login_days']['mean']}일

다음 관점에서 분석해주세요:
1. **핵심 이탈 동인(Key Churn Drivers)**: 통계에서 드러나는 가장 강력한 이탈 유발 요인 3가지를 근거와 함께 설명
2. **고위험 고객 프로파일**: 이탈 위험이 높은 고객의 구체적인 특성 조합(페르소나)을 서술
3. **숨겨진 패턴 및 이상 징후**: 단순 평균 비교로는 보이지 않는 잠재적 패턴이나 주목할 anomaly
4. **세그먼트별 차별화 전략 필요성**: 위험 티어 및 결제방식 데이터가 시사하는 세그먼트별 대응 전략 방향
5. **예측 모델 개선 시사점**: 현재 규칙 기반 위험 점수의 한계와 ML 모델 적용 시 고려할 핵심 피처

각 항목은 구체적인 수치를 인용하며 논리적으로 설명해주세요. 인사이트가 풍부하고 실무 적용 가능한 분석을 제공해주세요.
"""

    response = llm.invoke(prompt)
    print("  ✅ LLM 심층 분석 완료")
    return {"llm_analysis": response.content}


# ============================================================
# Node 4 ─ llm_generate_report
#   • Synthesize ALL outputs into a structured Korean Markdown report
# ============================================================
def llm_generate_report(state: AnalysisState) -> dict:
    print("\n[Node 4] LLM 리포트 생성 시작...")

    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.2)

    stat = state["stat_result"]

    tier_table = "\n".join(
        f"| {tier} | {v['count']} | {v['churned']} | {v['churn_rate']}% |"
        for tier, v in stat["risk_tier_stats"].items()
    )
    payment_table = "\n".join(
        f"| {m} | {v['count']} | {v['churn_rate']}% |"
        for m, v in stat["payment_analysis"].items()
    )
    top_feats = "\n".join(
        f"{i+1}. **{feat}** (상관계수: {corr:+.4f})"
        for i, (feat, corr) in enumerate(stat["top_corr_features"])
    )

    prompt = f"""당신은 기업의 Customer Success 전략을 담당하는 수석 데이터 애널리스트입니다.
아래 정보를 종합하여 경영진과 실무팀 모두가 이해할 수 있는 전문적인 이탈 예측 분석 보고서를 한국어 마크다운으로 작성해주세요.

============================
[통계 분석 결과 요약]
- 분석 대상: {stat['total_customers']}명
- 전체 이탈률: {stat['overall_churn_rate']}%
- 이탈 고객 수: {stat['churned_count']}명 / 유지 고객: {stat['retained_count']}명
- 위험 점수 정렬 정확도: {stat['alignment_accuracy']}%

[이탈 상관 TOP 5 피처]
{top_feats}

[위험 티어별 현황]
{tier_table}

[결제 방식별 이탈률]
{payment_table}

[피처 평균 비교 주요 항목]
- satisfaction_score: 이탈={stat['mean_comparison']['satisfaction_score']['churned']}, 유지={stat['mean_comparison']['satisfaction_score']['retained']}
- support_calls: 이탈={stat['mean_comparison']['support_calls']['churned']}, 유지={stat['mean_comparison']['support_calls']['retained']}
- tenure_months: 이탈={stat['mean_comparison']['tenure_months']['churned']}, 유지={stat['mean_comparison']['tenure_months']['retained']}
- last_login_days: 이탈={stat['mean_comparison']['last_login_days']['churned']}, 유지={stat['mean_comparison']['last_login_days']['retained']}

============================
[LLM 심층 분석 결과]
{state['llm_analysis']}
============================

다음 구조로 완성도 높은 보고서를 작성해주세요:

# 📊 고객 이탈 예측 분석 보고서

## 1. 요약 (Executive Summary)
- 핵심 발견사항 3줄 요약
- 즉각적인 비즈니스 임팩트

## 2. 데이터 개요
- 분석 데이터 스키마 설명 (표 형식)
- 데이터 품질 현황 (결측값, 이상값 처리 내역)
- 분석 대상 볼륨 및 이탈률

## 3. 통계 분석 결과
- 이탈 상관관계 피처 순위 (표 포함)
- 이탈/유지 고객 프로파일 비교 (표 포함)
- 위험 티어별 현황 분석 (표 포함)
- 결제 방식별 이탈률 분석

## 4. LLM 인사이트
- 핵심 이탈 동인 분석
- 고위험 고객 페르소나
- 숨겨진 패턴 및 이상 징후
- 세그먼트별 전략 방향

## 5. 권장 액션 플랜
- 우선순위 별 구체적 실행 방안 (즉시/단기/중기)
- 예측 모델 고도화 로드맵
- 성과 지표(KPI) 제안

보고서는 구체적인 수치를 반드시 포함하고, 실무에서 바로 활용 가능한 액션 중심으로 작성해주세요.
표(Markdown table)를 적극 활용하고 이모지로 가독성을 높여주세요.
"""

    response = llm.invoke(prompt)
    print("  ✅ 리포트 생성 완료")
    return {"report": response.content}


# ============================================================
# Graph Construction
# ============================================================
def build_graph() -> StateGraph:
    graph = StateGraph(AnalysisState)

    graph.add_node("validate",    validate_and_preprocess)
    graph.add_node("analyze",     statistical_analysis)
    graph.add_node("llm_analyze", llm_deep_analysis)
    graph.add_node("report",      llm_generate_report)

    graph.set_entry_point("validate")
    graph.add_edge("validate",    "analyze")
    graph.add_edge("analyze",     "llm_analyze")
    graph.add_edge("llm_analyze", "report")
    graph.add_edge("report",      END)

    return graph.compile()


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  🚀 고객 이탈 예측 분석 LangGraph 파이프라인 시작")
    print("=" * 60)

    app = build_graph()

    initial_state: AnalysisState = {
        "topic":        "고객 이탈 예측 분석 (Customer Churn Prediction)",
        "raw_data":     SAMPLE_DATA,
        "cleaned_data": [],
        "stat_result":  {},
        "llm_analysis": "",
        "report":       "",
    }

    final_state = app.invoke(initial_state)

    # ── Print final report ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("  📄 최종 분석 리포트")
    print("=" * 60)
    print(final_state["report"])

    # ── Optionally save report to file ──────────────────────────
    report_path = "churn_analysis_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(final_state["report"])
    print(f"\n✅ 리포트가 '{report_path}' 파일로 저장되었습니다.")

