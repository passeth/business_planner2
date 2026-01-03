---
name: business-plan
description: AI 기반 사업계획서 자동 생성 시스템 v2.1 - 자기 평가 기반 반복 개선
---
# /business-plan 커맨드

AI 기반 사업계획서 생성 시스템 v2.1을 시작합니다.

## 🚨 필수 실행 규칙

**이 커맨드를 실행할 때 반드시 아래 순서를 따라야 합니다:**

1. **세션 폴더 먼저 생성** → `outputs/YYYYMMDD_[project_slug]/`
2. **progress.json 즉시 생성** → 폴더 생성 후 바로 생성 (Skip 불가)
3. **각 Phase 후 Evaluator 호출** → 평가 없이 다음 Phase 진행 금지
4. **Human Loop 체크포인트 준수** → Phase 0, 4, 5 후 사용자 확인 필수

---

## 사용법

```
/business-plan [지원사업 주제 또는 사업 아이디어]
```

## 예시

```
/business-plan KOTRA 수출바우처 - AI 기반 K-뷰티 글로벌 마케팅 플랫폼
```

---

## 워크플로우 개요

```
STEP 0: 세션 초기화 (폴더 + progress.json 생성)
    ↓
Phase 0: 브레인스토밍 → Evaluator → [사용자 선택]
    ↓
Phase 1: 조사 기획 → Evaluator
    ↓
Phase 2 & 3: 시장조사 + 학술조사 (병렬) → Evaluator
    ↓
Phase 4: 분석 및 아이디어 도출 → Evaluator → [사용자 선택]
    ↓
Phase 5: 사업계획서 작성 → Evaluator → [사용자 검토]
    ↓
Phase 6: 최종 포맷 맞춤 → Evaluator
```

---

## 🔴 실행 지침 (반드시 순서대로)

### STEP 0: 세션 초기화 (필수!)

**0-1. 세션 폴더 생성:**
```bash
mkdir outputs/YYYYMMDD_[project_slug]/
```

**0-2. progress.json 즉시 생성 (Write 도구 사용):**
```json
{
  "session_id": "YYYYMMDD_[project_slug]",
  "topic": "[사용자 입력 주제]",
  "status": "in_progress",
  "current_phase": "phase0",
  "created_at": "[ISO 8601 timestamp]",
  "updated_at": "[ISO 8601 timestamp]",
  "phases": {
    "phase0": {"status": "pending", "iterations": 0, "score": null, "output_file": null},
    "phase1": {"status": "pending", "iterations": 0, "score": null, "output_file": null},
    "phase2": {"status": "pending", "iterations": 0, "score": null, "output_file": null},
    "phase3": {"status": "pending", "iterations": 0, "score": null, "output_file": null},
    "phase4": {"status": "pending", "iterations": 0, "score": null, "output_file": null},
    "phase5": {"status": "pending", "iterations": 0, "score": null, "output_file": null},
    "phase6": {"status": "pending", "iterations": 0, "score": null, "output_file": null}
  },
  "human_decisions": [],
  "evaluations": [],
  "error_log": []
}
```

⚠️ **progress.json이 생성되지 않으면 다음 단계로 진행하지 마세요!**

### STEP 1-7: Phase 실행

각 Phase에서 반드시 다음 4단계를 수행:

```
1. progress.json 업데이트 (status: "in_progress")
2. Phase 에이전트 실행 (Task 도구 사용)
3. Evaluator 에이전트 호출 (Task 도구 사용) ← 필수!
4. 평가 결과에 따라 재시도 또는 완료 처리
```

### Human Loop 체크포인트

| 시점 | 필수 질문 |
|-----|----------|
| Phase 0 완료 후 | "어떤 사업 컨셉으로 진행할까요?" |
| Phase 4 완료 후 | "어떤 아이디어를 중점적으로 발전시킬까요?" |
| Phase 5 완료 후 | "사업계획서 초안을 검토해주세요. 수정이 필요한가요?" |
| Phase 6 전 | "최종 제출 양식을 알려주세요" |

### 최종 출력물

```
outputs/YYYYMMDD_project/
├── progress.json              ← 필수! 상태 관리
├── phase0_brainstorm.md
├── phase1_research_plan.md
├── phase2_market_report.md
├── phase3_academic_report.md
├── phase4_ideation_report.md
├── phase5_detailed_plan.md
├── phase6_final_document.md
└── evaluations/               ← 평가 기록 보관
    ├── phase0_eval.json
    └── ...
```

---

## 에이전트 참조

각 Phase에서 참조해야 할 에이전트 파일:

| Phase | 에이전트 파일 | 역할 |
|-------|-------------|------|
| 전체 | `meta-orchestrator.md` | 오케스트레이션 규칙 |
| 평가 | `evaluator-agent.md` | 품질 평가 기준 |
| 0 | `ideation-brainstorm-agent.md` | 브레인스토밍 |
| 1 | `research-planner.md` | 조사 기획 |
| 2 | `market-research-agent.md` | 시장조사 |
| 3 | `academic-research-agent.md` | 학술/트렌드 조사 |
| 4 | `analysis-ideation-agent.md` | 분석 및 아이디어 |
| 5 | `business-plan-writer.md` | 사업계획서 작성 |
| 6 | `format-finalizer.md` | 최종 포맷 맞춤 |

---

## 품질 기준 요약 (Evaluator 평가 기준)

| Phase | 필수 조건 | 통과 점수 |
|-------|----------|----------|
| 0 | 아이디어 ≥ 3개, SCAMPER/6Hats 적용 | ≥ 70 |
| 1 | 연구 질문 ≥ 10개, 영한 키워드 | ≥ 70 |
| 2 | 경쟁사 ≥ 3개, 출처 ≥ 5개, SWOT | ≥ 70 |
| 3 | 논문 ≥ 3개 또는 트렌드 ≥ 5개 | ≥ 70 |
| 4 | 아이디어 ≥ 3개, 근거 명시 | ≥ 70 |
| 5 | 8개 섹션 완성, 출처 연결 | ≥ 70 |
| 6 | 포맷 제약 100% 준수 | ≥ 70 |

**점수 < 70**: 피드백과 함께 재시도 (최대 3회)
**3회 실패 시**: Human Loop 또는 부분 완료로 진행

---

## 주의사항

### 재무 예측 제외

본 시스템은 AI의 정확성 한계를 인식하여 다음 항목을 **의도적으로 제외**합니다:

- 매출 예측
- 손익분기점 분석
- 상세 재무 모델

재무 계획은 전문가와 협업하여 별도로 작성하시기 바랍니다.

### API 요구사항

- **Grok API**: X(Twitter) 트렌드 분석에 사용
  - 환경변수: `XAI_API_KEY`
  - 실패 시 WebSearch로 폴백
- **InfraNodus**: 지식 그래프 분석에 사용
  - MCP 서버 필요
  - 실패 시 기본 텍스트 분석으로 폴백

---

## 에러 복구

progress.json에서 상태를 읽어 중단된 지점부터 재개할 수 있습니다.

```bash
# 중단된 세션 재개
/business-plan --resume outputs/20260103_160000_project/
```

**재개 시 동작:**
1. progress.json 읽기
2. `current_phase` 확인
3. 해당 Phase의 `status` 확인
4. `in_progress` 또는 `failed` 상태면 해당 Phase부터 재시작
5. `completed` 상태면 다음 Phase로 진행

---

*Business Plan Generator v2.1 - Meta Orchestrator Architecture*
