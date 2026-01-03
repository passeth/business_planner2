# Business Plan Generator v2.0

AI 기반 사업계획서 자동 생성 시스템 - Meta Orchestrator 아키텍처

## 개요

Business Plan Generator v2.0은 자기 평가 기반 반복 개선(Self-Evaluation Loop)을 도입한 차세대 사업계획서 생성 시스템입니다.

### 주요 특징

- **Meta Orchestrator**: Ralph Wiggum 패턴의 자기 평가 루프
- **Phase 0 추가**: 초기 아이디에이션/브레인스토밍 단계
- **Grok API 통합**: X(Twitter) 실시간 트렌드 분석
- **강화된 에러 핸들링**: 재시도 로직 및 폴백 전략
- **재무 예측 제거**: AI 정확성 한계 인식

## 시스템 요구사항

### 필수
- Claude Code CLI

### API 키 (`.env` 파일에 설정)
- **XAI_API_KEY** (필수): Grok API - X(Twitter) 트렌드 분석용
  - 발급: https://console.x.ai/

### MCP 서버 (선택)
- **InfraNodus**: 지식 그래프 분석 (Phase 4 향상)
  - 없으면 기본 텍스트 분석으로 폴백

> **참고**: Supabase는 필요하지 않습니다. 상태 관리는 로컬 `progress.json` 파일로 처리됩니다.

## 설치 및 설정

### 1. 저장소 클론
```bash
git clone https://github.com/your-repo/business_planner_v2.git
cd business_planner_v2
```

### 2. 환경변수 설정
```bash
# .env.example을 복사하여 .env 생성
cp .env.example .env

# .env 파일을 열어 API 키 입력
# XAI_API_KEY=your_actual_api_key_here
```

### 3. Python 의존성 설치 (선택)
```bash
pip install -r requirements.txt
```

## 빠른 시작

```bash
# 1. 프로젝트 폴더로 이동
cd business_planner_v2

# 2. 사업계획서 생성 시작
claude /business-plan "지원사업 주제 또는 사업 아이디어"
```

## 워크플로우

```
Phase 0 → Phase 1 → Phase 2 & 3 (병렬) → Phase 4 → Phase 5 → Phase 6
  ↓          ↓            ↓                ↓          ↓          ↓
브레인스토밍  조사기획    시장+학술조사      분석     사업계획서   최종포맷
  ↓          ↓            ↓                ↓          ↓          ↓
[평가]     [평가]       [평가]           [평가]     [평가]     [평가]
```

## Phase별 상세

| Phase | 이름 | 완료 약속 | 주요 기능 |
|-------|------|-----------|----------|
| 0 | Ideation | `PHASE0_COMPLETE` | SCAMPER, 6 Thinking Hats 브레인스토밍 |
| 1 | Research Planning | `PHASE1_COMPLETE` | 5W1H 분석, 연구 질문 생성 |
| 2 | Market Research | `PHASE2_COMPLETE` | TAM/SAM/SOM, 경쟁사, SWOT |
| 3 | Academic Research | `PHASE3_COMPLETE` | 논문, 기술 트렌드, Grok X검색 |
| 4 | Analysis & Ideation | `PHASE4_COMPLETE` | InfraNodus 지식 그래프, 아이디어 도출 |
| 5 | Business Plan | `PHASE5_COMPLETE` | 8개 섹션 사업계획서 (재무 제외) |
| 6 | Format Finalization | `PHASE6_COMPLETE` | 제출 양식 맞춤 |

## 출력물

```
outputs/YYYYMMDD_HHMMSS_project_name/
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

## Human Loop (사용자 개입 지점)

1. **Phase 0 완료 후**: 브레인스토밍 컨셉 선택
2. **Phase 4 완료 후**: 아이디어 선택
3. **Phase 5 완료 후**: 사업계획서 초안 검토

## 에러 핸들링

- 최대 3회 재시도
- 지수 백오프 (1s, 2s, 4s)
- 폴백 전략:
  - Grok API 실패 → WebSearch 대체
  - InfraNodus 실패 → 기본 텍스트 분석

## 품질 기준

| Phase | 필수 조건 |
|-------|----------|
| 0 | 아이디어 ≥ 3개 |
| 1 | 연구 질문 ≥ 10개 |
| 2 | 경쟁사 ≥ 3개, 출처 ≥ 5개 |
| 3 | 논문 ≥ 3개 또는 트렌드 ≥ 5개 |
| 4 | 아이디어 ≥ 3개, 근거 명시 |
| 5 | 8개 섹션 완성 |
| 6 | 포맷 제약 100% 준수 |

## 주의사항

### 재무 예측 제외

본 시스템은 AI의 정확성 한계를 인식하여 재무 예측 섹션을 **의도적으로 제외**합니다.

포함되지 않는 항목:
- 매출 예측
- 손익분기점 분석
- 상세 재무 모델
- 투자 수익률 계산

재무 계획은 전문 회계사 또는 재무 컨설턴트와 협업하여 작성하시기 바랍니다.

## 라이선스

Internal Use Only

## 문서

- [ARCHITECTURE.md](./ARCHITECTURE.md) - 시스템 아키텍처 상세
