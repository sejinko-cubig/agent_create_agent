# Claude Managed Agents 온보딩 대화 문맥

## 목표
Claude Managed Agents API를 학습하고 실행하기

## 진행 상황

### 1. 개념 학습 완료
- **Managed Agents**: Anthropic이 호스팅하는 클라우드 인프라에서 에이전트를 실행하는 완전 관리형 서비스 (2026-04-08 공개 베타)
- 자체 에이전트 루프, 도구 실행, 런타임을 구축할 필요 없음

### 2. 핵심 개념 이해 완료

| 개념 | 설명 | 비유 |
|------|------|------|
| **Agent** | 모델, 시스템 프롬프트, 도구 정의 | "누구를 고용할지" |
| **Environment** | 에이전트가 실행되는 샌드박스 컨테이너 | "작업실 세팅" |
| **Session** | Agent + Environment를 연결한 실행 단위 | "자, 일 시작해" |

```
Agent(누구) + Environment(어디서) = Session(실행)
```

### 3. API 구조 이해 완료

#### 주요 엔드포인트
- `POST /v1/agents` — 에이전트 생성
- `POST /v1/environments` — 환경 생성
- `POST /v1/sessions` — 세션 시작
- `POST /v1/sessions/{id}/events` — 메시지 전송
- `GET /v1/sessions/{id}/stream` — SSE 스트리밍

#### 베타 헤더 필수
`anthropic-beta: managed-agents-2026-04-01` (SDK는 자동 설정)

### 4. 내장 도구
bash, read, write, edit, glob, grep, web_fetch, web_search
- `agent_toolset_20260401` 타입으로 전체 활성화
- 개별 도구 활성화/비활성화 가능
- 커스텀 도구 및 MCP 서버도 지원

### 5. `ant` CLI 학습 완료
- Anthropic 공식 CLI 도구
- `ant beta:agents create` = API 호출을 간소화한 CLI 명령어
- 설치: `brew install anthropics/tap/ant` (macOS)

### 6. 가격
- 인프라: $0.08/세션시간
- 토큰: Claude 모델별 일반 토큰 가격 적용

### 7. 실행 파일 생성 완료
- 파일: `managed_agent.py` (이 폴더에 있음)
- Python SDK 방식, 스트리밍 포함 전체 플로우
- 피보나치 수열 생성 예제

## 다음 단계 (아직 안 한 것)
- [ ] 실제 실행 (`python managed_agent.py`)
- [ ] 커스텀 도구 설정 실습
- [ ] MCP 서버 연동
- [ ] 멀티 에이전트 조율 (연구 미리보기 상태, 별도 액세스 요청 필요)
- [ ] Agent/Environment ID 재사용 패턴
- [ ] 에이전트 버전 관리

## 참고 문서
- 퀵스타트: https://platform.claude.com/docs/en/managed-agents/quickstart
- 개요: https://platform.claude.com/docs/en/managed-agents/overview
- 도구: https://platform.claude.com/docs/en/managed-agents/tools
- 이벤트/스트리밍: https://platform.claude.com/docs/en/managed-agents/events-and-streaming
