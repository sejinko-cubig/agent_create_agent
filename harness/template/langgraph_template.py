"""
LangGraph 분석 파이프라인 템플릿
=====================================
이 템플릿을 기반으로 주제별 분석 파이프라인을 생성합니다.
코딩 Agent가 이 구조를 따라 코드를 작성합니다.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
import math
import statistics


# ============================================================
# 상태 정의 — 모든 노드가 공유하는 상태
# ============================================================
class AnalysisState(TypedDict):
    topic: str
    raw_data: list[dict]
    cleaned_data: list[dict]
    stat_result: dict
    llm_analysis: str
    report: str


# ============================================================
# 샘플 데이터 — 주제에 맞게 15~20행 생성
# ============================================================
SAMPLE_DATA: list[dict] = [
    # 코딩 Agent가 주제에 맞는 샘플 데이터로 채움
]


# ============================================================
# 노드 1: 데이터 검증 및 전처리
# ============================================================
def validate_and_preprocess(state: AnalysisState) -> dict:
    print("[Node 1] 데이터 검증 및 전처리 시작...")
    raw = state["raw_data"]
    # 1-A. 결측값 처리 (중앙값 대체)
    # 1-B. 범위/타입 검증
    # 1-C. Min-max 정규화
    # 1-D. 종합 점수 계산
    # 코딩 Agent가 실제 로직으로 채움
    return {"cleaned_data": raw}


# ============================================================
# 노드 2: 통계 분석
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
    # 코딩 Agent가 실제 로직으로 채움
    return {"stat_result": {}}


# ============================================================
# 노드 3: LLM 심층 분석
# ============================================================
def llm_deep_analysis(state: AnalysisState) -> dict:
    print("[Node 3] LLM 심층 분석 시작...")
    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.3)
    # 코딩 Agent가 통계 결과를 프롬프트로 변환
    prompt = "..."
    response = llm.invoke(prompt)
    print("  ✅ LLM 심층 분석 완료")
    return {"llm_analysis": response.content}


# ============================================================
# 노드 4: LLM 리포트 생성
# ============================================================
def llm_generate_report(state: AnalysisState) -> dict:
    print("[Node 4] LLM 리포트 생성 시작...")
    llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0.2)
    # 코딩 Agent가 리포트 프롬프트 생성
    prompt = "..."
    response = llm.invoke(prompt)
    print("  ✅ 리포트 생성 완료")
    return {"report": response.content}


# ============================================================
# 그래프 구성
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
# 메인 실행
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

    print("\n" + "=" * 60)
    print("  최종 리포트")
    print("=" * 60)
    print(final_state["report"])
