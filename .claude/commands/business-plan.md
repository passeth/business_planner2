---
name: business-plan
description: AI 기반 사업계획서 자동 생성 시스템 v2.0 - 자기 평가 기반 반복 개선
---
# /business-plan 커맨드

AI 기반 사업계획서 생성 시스템 v2.0을 시작합니다.

## 사용법

```
/business-plan [지원사업 주제 또는 사업 아이디어]
```

## 예시

```
/business-plan KOTRA 수출바우처 - AI 기반 K-뷰티 글로벌 마케팅 플랫폼
```

## 워크플로우 개요

```
Phase 0: 브레인스토밍 → [사용자 선택]
    ↓
Phase 1: 조사 기획
    ↓
Phase 2 & 3: 시장조사 + 학술조사 (병렬)
    ↓
Phase 4: 분석 및 아이디어 도출 → [사용자 선택]
    ↓
Phase 5: 사업계획서 작성 → [사용자 검토]
    ↓
Phase 6: 최종 포맷 맞춤
```

## 실행 지침

### 1. 세션 초기화

```markdown
세션 폴더 생성:
outputs/YYYYMMDD_HHMMSS_[project_name]/
```

### 2. Meta Orchestrator 호출

`meta-orchestrator` 에이전트를 사용하여 전체 워크플로우를 조율합니다.

**입력 형식:**

```json
{
  "topic": "[사용자 입력 주제]",
  "target_format": {
    "type": "KOTRA 수출바우처",
    "constraints": {
      "max_pages": 20,
      "max_chars": 50000
    }
  },
  "session_dir": "outputs/YYYYMMDD_HHMMSS_project/"
}
```

### 3. Phase별 자기 평가 루프

각 Phase에서:

1. Phase 에이전트 실행
2. Evaluator 에이전트로 품질 평가
3. 기준 미달 시 피드백과 함께 재시도 (최대 3회)
4. 기준 충족 시 다음 Phase 진행

### 4. Human Loop (사용자 개입)

- **Phase 0 완료 후**: 브레인스토밍 컨셉 선택
- **Phase 4 완료 후**: 아이디어 선택
- **Phase 5 완료 후**: 사업계획서 초안 검토

### 5. 최종 출력물

```
outputs/YYYYMMDD_HHMMSS_project/
├── phase0_brainstorm.md
├── phase1_research_plan.md
├── phase2_market_report.md
├── phase3_academic_report.md
├── phase4_ideation_report.md
├── phase5_detailed_plan.md
├── final/
│   └── business_plan_final.md
└── progress.json
```

## 에이전트 호출 순서

```
1. meta-orchestrator (전체 조율)
   ├── ideation-brainstorm-agent (Phase 0)
   ├── evaluator-agent (평가)
   ├── research-planner (Phase 1)
   ├── evaluator-agent (평가)
   ├── market-research-agent (Phase 2) ──┐
   ├── academic-research-agent (Phase 3) ├─ 병렬
   ├── evaluator-agent (평가) ───────────┘
   ├── analysis-ideation-agent (Phase 4)
   ├── evaluator-agent (평가)
   ├── business-plan-writer (Phase 5)
   ├── evaluator-agent (평가)
   ├── format-finalizer (Phase 6)
   └── evaluator-agent (최종 평가)
```

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

## 품질 기준 요약

| Phase | 필수 조건                           |
| ----- | ----------------------------------- |
| 0     | 아이디어 ≥ 3개, SCAMPER/6Hats 적용 |
| 1     | 연구 질문 ≥ 10개, 영한 키워드      |
| 2     | 경쟁사 ≥ 3개, 출처 ≥ 5개, SWOT    |
| 3     | 논문 ≥ 3개 또는 트렌드 ≥ 5개      |
| 4     | 아이디어 ≥ 3개, 근거 명시          |
| 5     | 8개 섹션 완성, 출처 연결            |
| 6     | 포맷 제약 100% 준수                 |

## 에러 복구

progress.json에서 상태를 읽어 중단된 지점부터 재개할 수 있습니다.

```bash
# 중단된 세션 재개
/business-plan --resume outputs/20260103_160000_project/
```

---

*Business Plan Generator v2.0 - Meta Orchestrator Architecture*
