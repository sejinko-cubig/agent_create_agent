# Skill: qa_reviewer

## 목적
생성된 LangGraph 코드의 품질을 검증하고 피드백을 제공합니다.

## 검증 체크리스트 (8항목)

### 1. STRUCTURE
- [ ] StateGraph에 4개 필수 노드 존재 (validate, analyze, llm_analyze, report)
- [ ] AnalysisState TypedDict에 6개 필수 키 존재

### 2. COMPLETENESS
- [ ] 모든 함수에 실제 로직 구현 (placeholder 없음)
- [ ] "...", "pass", "TODO" 없음

### 3. DATA
- [ ] 샘플 데이터 15행 이상
- [ ] TypedDict 스키마와 샘플 데이터 컬럼 일치
- [ ] 의도적 결측값 포함 (전처리 테스트용)

### 4. IMPORTS
- [ ] 모든 import가 실제 사용됨
- [ ] langgraph, langchain_anthropic import 존재

### 5. LLM NODES
- [ ] ChatAnthropic(model="claude-sonnet-4-6") 사용
- [ ] 분석 노드 temperature=0.3
- [ ] 리포트 노드 temperature=0.2

### 6. EDGE FLOW
- [ ] set_entry_point("validate")
- [ ] validate → analyze → llm_analyze → report → END 순서

### 7. RUNNABLE
- [ ] if __name__ == "__main__" 블록 존재
- [ ] initial_state 정의 및 app.invoke() 호출
- [ ] 최종 리포트 print

### 8. REPORT
- [ ] LLM 리포트 프롬프트에 5개 섹션 포함
- [ ] 한국어 출력 지시

## 출력 형식
```
## QA 결과: {PASS|FAIL}

### 통과 항목
- [x] STRUCTURE: ...
- [x] COMPLETENESS: ...

### 실패 항목
- [ISSUE] {설명}
  [LINE] {위치}
  [FIX] {수정 방안}

### 종합 의견
{전체 평가}
```

## 루프 규칙
- FAIL 시 → 피드백을 Coder Agent에게 전달
- Coder가 수정 후 → 재검증
- 최대 3회 반복 후 강제 종료 (최선의 버전 채택)
