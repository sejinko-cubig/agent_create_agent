"""
Claude Managed Agents - 전체 실행 예제

사용법:
  1. pip install anthropic python-dotenv
  2. .env 파일에 ANTHROPIC_API_KEY=sk-ant-... 설정
  3. python managed_agent.py
"""

from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic()

# --- 1. Agent 생성 (누구를 고용할지) ---
agent = client.beta.agents.create(
    name="Coding Assistant",
    model="claude-sonnet-4-6",
    system="You are a helpful coding assistant. Write clean, well-documented code.",
    tools=[{"type": "agent_toolset_20260401"}],
)
print(f"Agent created: {agent.id} (version {agent.version})")

# --- 2. Environment 생성 (작업실 세팅) ---
environment = client.beta.environments.create(
    name="quickstart-env",
    config={
        "type": "cloud",
        "networking": {"type": "unrestricted"},
    },
)
print(f"Environment created: {environment.id}")

# --- 3. Session 시작 (Agent + Environment 연결) ---
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=environment.id,
    title="Quickstart session",
)
print(f"Session created: {session.id}")

# --- 4. 메시지 전송 + 스트리밍 ---
print("\n--- Agent 작업 시작 ---\n")

with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[
            {
                "type": "user.message",
                "content": [
                    {
                        "type": "text",
                        "text": "Create a Python script that generates the first 20 Fibonacci numbers and saves them to fibonacci.txt",
                    },
                ],
            },
        ],
    )

    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    print(block.text, end="", flush=True)
            case "agent.tool_use":
                print(f"\n[도구 사용: {event.name}]")
            case "session.status_idle":
                print("\n\n--- Agent 작업 완료 ---")
                break
