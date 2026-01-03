# Business Plan Generator v2.0 - 시스템 아키텍처

## 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    META ORCHESTRATOR (자기 평가 오케스트레이터)           │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Self-Evaluation Loop (Ralph Wiggum 패턴)                        │   │
│  │  ────────────────────────────────────────                        │   │
│  │  while (phase_status != "COMPLETE" && iterations < max_iter):    │   │
│  │    1. Execute Phase Agent                                        │   │
│  │    2. Run Evaluator Agent on output                              │   │
│  │    3. If quality_score >= threshold: mark COMPLETE               │   │
│  │    4. Else: provide feedback, re-run agent                       │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  Error Handling: retry(3) → fallback → graceful_degradation            │
│  State: progress.json (atomic writes, recovery support)                 │
└─────────────────────────────────────────────────────────────────────────┘
```

## 에이전트 구조

### Meta Orchestrator

```
.claude/agents/meta-orchestrator.md
```

**역할**: 전체 워크플로우 조율 및 자기 평가 루프 관리

**핵심 기능**:
- Phase 순차/병렬 실행
- Evaluator Agent 호출
- 품질 미달 시 피드백 기반 재시도
- 에러 핸들링 및 복구
- 상태 관리 (progress.json)

### Evaluator Agent

```
.claude/agents/evaluator-agent.md
```

**역할**: 각 Phase 출력물의 품질 평가

**평가 기준**:
```json
{
  "common": {
    "completion_promise_present": true,
    "required_fields_present": true,
    "output_file_created": true
  },
  "phase_specific": {
    "phase0": {"idea_count": ">=3", "techniques_applied": true},
    "phase1": {"question_count": ">=10", "keywords_bilingual": true},
    "phase2": {"competitor_count": ">=3", "source_urls": ">=5"},
    "phase3": {"paper_count": ">=3", "or": {"trend_count": ">=5"}},
    "phase4": {"idea_count": ">=3", "evidence_provided": true},
    "phase5": {"sections_complete": 8, "sources_linked": true},
    "phase6": {"format_compliance": "100%"}
  }
}
```

### Phase Agents

| Agent | 파일 | 완료 약속 |
|-------|------|-----------|
| Ideation Brainstorm | ideation-brainstorm-agent.md | PHASE0_COMPLETE |
| Research Planner | research-planner.md | PHASE1_COMPLETE |
| Market Research | market-research-agent.md | PHASE2_COMPLETE |
| Academic Research | academic-research-agent.md | PHASE3_COMPLETE |
| Analysis Ideation | analysis-ideation-agent.md | PHASE4_COMPLETE |
| Business Plan Writer | business-plan-writer.md | PHASE5_COMPLETE |
| Format Finalizer | format-finalizer.md | PHASE6_COMPLETE |

## 자기 평가 루프 상세

### 의사 코드

```python
def run_phase_with_evaluation(phase_agent, input_data, max_iterations=3):
    for iteration in range(max_iterations):
        # 1. Phase 에이전트 실행
        output = execute_agent(phase_agent, input_data)

        # 2. Evaluator 에이전트로 품질 평가
        evaluation = evaluate_output(output, phase_agent.quality_criteria)

        # 3. 평가 결과 확인
        if evaluation.score >= THRESHOLD and evaluation.completion_promise:
            log_success(phase_agent, iteration)
            return output  # 완료

        # 4. 개선 피드백 제공하고 재시도
        input_data.feedback = evaluation.improvement_suggestions
        log_retry(phase_agent, iteration, evaluation)

    # max_iterations 도달: 휴먼 루프 또는 graceful degradation
    return handle_max_iterations(phase_agent, output)
```

### 품질 임계값

| Phase | Threshold | 근거 |
|-------|-----------|------|
| 0 | 70% | 창의적 과정, 유연성 필요 |
| 1 | 75% | 조사 범위 정의 중요 |
| 2 | 80% | 데이터 정확성 중요 |
| 3 | 75% | API 의존성, 폴백 허용 |
| 4 | 75% | 창의적 과정 |
| 5 | 85% | 최종 문서 품질 중요 |
| 6 | 90% | 포맷 준수 필수 |

## 에러 핸들링 파이프라인

```
┌─────────────────────────────────────────────────────────────────┐
│  Error Handling Pipeline                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Primary Attempt                                              │
│     └─ Success → Continue                                        │
│     └─ Fail → Retry (max 3)                                      │
│                                                                  │
│  2. Retry with exponential backoff (1s, 2s, 4s)                 │
│     └─ Success → Continue                                        │
│     └─ Fail → Fallback Strategy                                  │
│                                                                  │
│  3. Fallback Strategies:                                         │
│     ├─ Grok API 실패 → WebSearch로 대체                          │
│     ├─ InfraNodus 실패 → 기본 텍스트 분석으로 대체                │
│     ├─ 특정 Phase 실패 → 이전 Phase 결과로 진행                   │
│     └─ 치명적 오류 → 상태 저장 후 중단, 복구 가능                 │
│                                                                  │
│  4. Error Logging:                                               │
│     └─ progress.json에 error_log 배열 추가                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## 상태 관리

### progress.json 구조

```json
{
  "session_id": "20260103_160000_project_name",
  "topic": "사업 주제",
  "current_phase": "phase2",
  "phases": {
    "phase0": {
      "status": "complete",
      "iterations": 1,
      "score": 85,
      "output_path": "phase0_brainstorm.md",
      "completion_promise": "PHASE0_COMPLETE"
    },
    "phase1": {
      "status": "complete",
      "iterations": 2,
      "score": 78,
      "output_path": "phase1_research_plan.md",
      "completion_promise": "PHASE1_COMPLETE"
    },
    "phase2": {
      "status": "in_progress",
      "iterations": 1,
      "score": null
    }
  },
  "human_loops": {
    "phase0_concept_selection": {
      "timestamp": "2026-01-03T16:05:00Z",
      "selected": "concept_1"
    }
  },
  "error_log": [
    {
      "phase": "phase3",
      "error_type": "API_ERROR",
      "message": "Grok API rate limit exceeded",
      "timestamp": "2026-01-03T16:30:00Z",
      "retry_count": 3,
      "fallback_used": "WebSearch",
      "resolved": true
    }
  ],
  "created_at": "2026-01-03T16:00:00Z",
  "updated_at": "2026-01-03T16:35:00Z"
}
```

## Grok API 통합

### Phase 3에서 활용

```bash
# X(Twitter) 트렌드 검색
curl -X POST "https://api.x.ai/v1/chat/completions" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-4-fast",
    "messages": [
      {"role": "system", "content": "You are a trend analyst."},
      {"role": "user", "content": "Search X/Twitter for K-beauty trends"}
    ],
    "tools": [{"type": "x_search"}]
  }'
```

### 폴백 전략

Grok API 실패 시:
1. 재시도 (3회, exponential backoff)
2. WebSearch로 대체: `"site:twitter.com [keyword]"`
3. 기존 트렌드 데이터로 진행

## InfraNodus 통합

### Phase 4에서 활용

```markdown
MCP 도구:
- generate_knowledge_graph: 지식 그래프 생성
- create_knowledge_graph: 저장 및 분석
- generate_topical_clusters: 토픽 클러스터 추출
- generate_content_gaps: 콘텐츠 갭 식별
- generate_research_ideas: 혁신 아이디어 생성
```

### 폴백 전략

InfraNodus 실패 시:
1. 기본 키워드 빈도 분석
2. 수동 토픽 클러스터링
3. AI 기반 텍스트 분석

## 폴더 구조

```
business_planner_v2/
├── .claude/
│   ├── agents/
│   │   ├── meta-orchestrator.md
│   │   ├── evaluator-agent.md
│   │   ├── ideation-brainstorm-agent.md  # Phase 0
│   │   ├── research-planner.md           # Phase 1
│   │   ├── market-research-agent.md      # Phase 2
│   │   ├── academic-research-agent.md    # Phase 3 + Grok
│   │   ├── analysis-ideation-agent.md    # Phase 4
│   │   ├── business-plan-writer.md       # Phase 5
│   │   └── format-finalizer.md           # Phase 6
│   ├── commands/
│   │   └── business-plan.md
│   └── settings.local.json
├── templates/
│   ├── phase0_brainstorm.template.md
│   ├── research-plan.template.md
│   └── business-plan.template.md
├── outputs/
│   └── [session_folders]/
└── docs/
    ├── README.md
    └── ARCHITECTURE.md
```

## 성능 고려사항

### 토큰 사용량

| 시나리오 | 예상 토큰 |
|----------|----------|
| 1회 통과 | ~50,000 |
| 평균 (1.5회 재시도) | ~75,000 |
| 최대 (모든 Phase 3회) | ~150,000 |

### 최적화 전략

1. 조기 종료 조건 적극 활용
2. 병렬 실행 (Phase 2 & 3)
3. 캐싱 (동일 쿼리 재사용)
4. 점진적 상세화 (필요시만 상세 분석)

## 확장 가능성

### 향후 개선 방향

1. **Multi-LLM 지원**: 특정 Phase에 다른 모델 사용
2. **웹 UI**: 진행 상황 시각화
3. **템플릿 커스터마이징**: 사용자 정의 양식
4. **협업 기능**: 다중 사용자 검토
