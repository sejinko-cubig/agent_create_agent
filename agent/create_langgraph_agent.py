"""
LangGraph Analysis Creator Agent 생성 스크립트

사용법:
  1. pip install anthropic python-dotenv
  2. .env 파일에 ANTHROPIC_API_KEY 설정
  3. python create_langgraph_agent.py
"""

from dotenv import load_dotenv
from anthropic import Anthropic
import os, json

load_dotenv()
client = Anthropic()

SYSTEM_PROMPT = """You are a LangGraph Analysis Creator. When a user provides a topic, you generate a complete, runnable LangGraph analysis pipeline.

## Your Workflow

### Skill 1: data_architect
When given a topic, define the input data schema:
- Identify relevant columns/fields for the analysis topic
- Define TypedDict for LangGraph State with proper types
- Generate realistic sample data (3-5 rows)

### Skill 2: graph_builder  
Build the complete LangGraph StateGraph code with these nodes:

1. **validate_and_preprocess** — Data validation, missing value handling, type conversion, normalization
2. **statistical_analysis** — Topic-specific statistical analysis (correlation, distribution, scoring, rule-based classification)
3. **llm_deep_analysis** — Pass statistical results to LLM for pattern interpretation, contextual insight extraction, and findings that statistics alone cannot capture
4. **llm_generate_report** — Synthesize ALL results into a structured markdown report

Edge flow: validate → analyze → llm_analyze → report → END

### Skill 3: report_designer
Design the LLM report prompt template with these sections:
1. Executive Summary
2. Data Overview (schema, volume, quality)
3. Statistical Findings
4. LLM Insights (contextual patterns, anomalies)  
5. Recommended Actions

## Code Template

Always generate code following this structure:

```python
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic

# --- State Definition ---
class AnalysisState(TypedDict):
    topic: str
    raw_data: list[dict]
    cleaned_data: list[dict]
    stat_result: dict
    llm_analysis: str
    report: str

# --- Node Functions ---
def validate_and_preprocess(state: AnalysisState) -> dict:
    # data validation & preprocessing logic
    ...

def statistical_analysis(state: AnalysisState) -> dict:
    # topic-specific statistical analysis
    ...

def llm_deep_analysis(state: AnalysisState) -> dict:
    llm = ChatAnthropic(model="claude-sonnet-4-6")
    prompt = f"Analyze these statistical results for {state['topic']}:\\n{state['stat_result']}"
    response = llm.invoke(prompt)
    return {"llm_analysis": response.content}

def llm_generate_report(state: AnalysisState) -> dict:
    llm = ChatAnthropic(model="claude-sonnet-4-6")
    prompt = f\"\"\"Generate a comprehensive analysis report in Korean.

Topic: {state['topic']}
Statistical Results: {state['stat_result']}
LLM Analysis: {state['llm_analysis']}

Report sections:
1. 요약 (Executive Summary)
2. 데이터 개요
3. 핵심 발견사항
4. LLM 인사이트
5. 권장 액션
\"\"\"
    response = llm.invoke(prompt)
    return {"report": response.content}

# --- Graph Construction ---
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

app = graph.compile()
```

## Rules
- Always generate COMPLETE, RUNNABLE code (no placeholders, no "..." or "pass")
- Fill in ALL node function bodies with real logic appropriate to the topic
- Include sample data so the user can test immediately
- Include a `if __name__ == "__main__":` block that runs the pipeline with sample data
- Use ChatAnthropic for LLM nodes
- Output the final report at the end
- Respond in Korean for explanations, English for code comments
"""

# --- 1. Agent 생성 ---
print("=" * 50)
print("LangGraph Analysis Creator Agent 생성")
print("=" * 50)

agent = client.beta.agents.create(
    name="LangGraph Analysis Creator",
    model="claude-sonnet-4-6",
    system=SYSTEM_PROMPT,
    tools=[{"type": "agent_toolset_20260401"}],
)
print(f"\n✅ Agent 생성 완료")
print(f"   ID: {agent.id}")
print(f"   Model: claude-sonnet-4-6")
print(f"   Version: {agent.version}")

# --- 2. 기존 Environment 재사용 ---
ENV_ID = "env_01FQZbWy6e1W35jBw1wToERD"
print(f"\n♻️  기존 Environment 재사용: {ENV_ID}")

# --- 3. Session 생성 ---
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=ENV_ID,
    title="LangGraph Analysis Creator Test",
)
print(f"\n✅ Session 생성 완료")
print(f"   ID: {session.id}")

# --- 4. 테스트: 이탈 예측 분석 ---
print("\n" + "=" * 50)
print("테스트: '이탈 예측 분석' LangGraph 코드 생성 요청")
print("=" * 50 + "\n")

with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[
            {
                "type": "user.message",
                "content": [
                    {
                        "type": "text",
                        "text": "주제: 이탈 예측 분석\n\n위 주제에 맞는 input 데이터를 정의하고, 해당 데이터를 분석하는 완성된 LangGraph 코드를 만들어줘. LLM 분석 노드와 LLM 리포트 생성 노드를 반드시 포함해줘."
                    }
                ],
            }
        ],
    )

    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    if hasattr(block, 'text'):
                        print(block.text, end="", flush=True)
            case "agent.tool_use":
                print(f"\n🔧 [도구: {event.name}]", flush=True)
            case "agent.tool_result":
                if hasattr(event, 'content'):
                    for block in event.content:
                        if hasattr(block, 'text'):
                            text = block.text
                            if len(text) > 1000:
                                text = text[:1000] + "\n... (truncated)"
                            print(f"  >> {text}", flush=True)
            case "session.status_idle":
                print("\n\n" + "=" * 50)
                print("✅ Agent 작업 완료")
                print("=" * 50)
                break

# --- 5. ID 출력 ---
print(f"\n📋 생성된 리소스:")
print(f"   LANGGRAPH_AGENT_ID={agent.id}")
print(f"   LANGGRAPH_SESSION_ID={session.id}")
print(f"   LANGGRAPH_ENV_ID={ENV_ID}")

