# Business Plan Generator v2.0

AI 기반 사업계획서 자동 생성 시스템 - Meta Orchestrator 아키텍처

## 개요

Business Plan Generator v2.0은 자기 평가 기반 반복 개선(Self-Evaluation Loop)을 도입한 차세대 사업계획서 생성 시스템입니다.

### 주요 특징

- **Meta Orchestrator**: Ralph Wiggum 패턴의 자기 평가 루프
- **Phase 0 추가**: 초기 아이디에이션/브레인스토밍 단계
- **Grok API 통합**: X(Twitter) 실시간 트렌드 분석
- **OpenRouter 지원**: Grok API 대안으로 다양한 모델 선택 가능
- **강화된 에러 핸들링**: 재시도 로직 및 폴백 전략

---

## 빠른 시작 (Quick Start)

### 1단계: 저장소 클론

```bash
git clone https://github.com/your-repo/business_planner_v2.git
cd business_planner_v2
```

### 2단계: 자동 설정 (권장)

```bash
python setup.py
```

대화형 설정 마법사가 실행됩니다:

```
==================================================
🚀 Business Plan Generator v2.0 Setup
==================================================

[1/3] LLM API 설정

  사용 가능한 옵션:
  • Grok API: X(Twitter) 실시간 검색 가능, 트렌드 분석에 최적
  • OpenRouter: 다양한 모델 선택 가능, Grok API 없어도 사용 가능

  어떤 API를 사용하시겠습니까?
    1. Grok API (xAI) - X/Twitter 검색 기능 포함
    2. OpenRouter - 다양한 모델 지원 (Grok API 대안)
    3. 둘 다 설정 (Grok 우선, OpenRouter 백업)
  선택 (1-3): _
```

### 3단계: 의존성 설치

```bash
pip install -r requirements.txt
```

### 4단계: 테스트 (선택)

```bash
python scripts/grok_api.py "K-beauty trends 2025"
```

### 5단계: 사용 시작

```bash
claude /business-plan "지원사업 주제 또는 사업 아이디어"
```

---

## 상세 설치 가이드

### 시스템 요구사항

| 항목 | 필수 여부 | 설명 |
|------|----------|------|
| Python 3.8+ | 필수 | setup.py 실행용 |
| Claude Code CLI | 필수 | 메인 실행 환경 |
| Grok API 키 | 선택 | X/Twitter 검색 기능 |
| OpenRouter API 키 | 선택 | Grok 대안 |
| InfraNodus API 키 | 선택 | 지식 그래프 분석 |

> **Note**: Grok API 또는 OpenRouter 중 **하나는 반드시** 필요합니다.

---

### API 키 발급 방법

#### Option A: Grok API (추천)

X(Twitter) 실시간 검색 기능을 사용할 수 있습니다.

1. https://console.x.ai/ 접속
2. 계정 생성 또는 로그인
3. API Keys 메뉴에서 새 키 생성
4. `xai-` 로 시작하는 키 복사

#### Option B: OpenRouter (Grok 대안)

Grok API가 없거나 다른 모델을 사용하고 싶을 때 선택합니다.

1. https://openrouter.ai/ 접속
2. 계정 생성 또는 로그인
3. https://openrouter.ai/keys 에서 API 키 생성
4. `sk-or-` 로 시작하는 키 복사

**OpenRouter 추천 모델:**

| 모델 | 특징 | 가격 |
|------|------|------|
| `x-ai/grok-2-1212` | Grok 2 성능, 추천 | 유료 |
| `anthropic/claude-3.5-sonnet` | 고품질 분석 | 유료 |
| `openai/gpt-4o` | 범용성 | 유료 |
| `google/gemini-2.0-flash-exp:free` | **무료** | 무료 |

#### Option C: InfraNodus (선택)

지식 그래프 분석 기능을 활성화합니다.

1. https://infranodus.com/ 접속
2. 계정 생성
3. https://infranodus.com/account/api 에서 API 키 확인

---

### 설정 방법 비교

#### 방법 1: setup.py 사용 (권장)

```bash
python setup.py
```

- 대화형으로 안내
- 자동 검증
- 실수 방지

#### 방법 2: 수동 설정

```bash
# 1. 템플릿 복사
cp .env.example .env          # macOS/Linux
copy .env.example .env        # Windows

# 2. .env 파일 편집
# 텍스트 에디터로 열어서 API 키 입력
```

`.env` 파일 예시:

```env
LLM_PROVIDER=auto

# Grok API (둘 중 하나만 있어도 됨)
XAI_API_KEY=xai-xxxxxxxxxxxxxxxxxxxx

# OpenRouter (Grok 없을 때 대안)
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxxxx
OPENROUTER_MODEL=x-ai/grok-2-1212

# InfraNodus (선택)
INFRANODUS_API_KEY=your_key_here
```

---

### LLM Provider 설정 옵션

`.env` 파일의 `LLM_PROVIDER` 값에 따라 동작이 달라집니다:

| 값 | 동작 | 권장 상황 |
|----|------|----------|
| `auto` | Grok 우선, 없으면 OpenRouter | **기본값, 권장** |
| `grok` | Grok API만 사용 | X 검색이 핵심일 때 |
| `openrouter` | OpenRouter만 사용 | Grok 없을 때 |

---

### MCP 서버 설정

이 프로젝트는 Claude Code의 MCP(Model Context Protocol) 서버를 지원합니다.

`.mcp.json` 파일이 이미 포함되어 있어 별도 설정 없이 자동 인식됩니다:

```json
{
  "mcpServers": {
    "infranodus": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-infranodus"],
      "env": {
        "INFRANODUS_API_KEY": "${INFRANODUS_API_KEY}"
      }
    }
  }
}
```

> **Note**: InfraNodus API 키를 설정했다면 Claude Code에서 자동으로 MCP 서버가 활성화됩니다.

---

### 설정 확인

설정이 완료되었는지 확인:

```bash
python scripts/grok_api.py
```

출력 예시:

```
🔧 Active Provider: Grok API (Model: grok-2-latest)

Usage: python grok_api.py <query>
Example: python grok_api.py 'K-beauty trends 2025'
```

또는:

```
🔧 Active Provider: OpenRouter (Model: x-ai/grok-2-1212)
```

---

### 트러블슈팅

#### "API 키가 설정되지 않았습니다" 에러

```bash
# setup.py 재실행
python setup.py
```

#### Windows에서 색상이 깨짐

```bash
# PowerShell 사용 권장
# 또는 Windows Terminal 설치
```

#### OpenRouter 429 에러 (Rate Limit)

무료 모델 사용 시 요청 제한에 걸릴 수 있습니다. 유료 모델로 변경하거나 잠시 후 재시도하세요.

#### InfraNodus MCP 연결 안됨

1. API 키가 `.env`에 설정되어 있는지 확인
2. Claude Code 재시작
3. `npx` 명령어가 작동하는지 확인: `npx --version`

---

## 워크플로우

```
Phase 0 → Phase 1 → Phase 2 & 3 (병렬) → Phase 4 → Phase 5 → Phase 6
  ↓          ↓            ↓                ↓          ↓          ↓
브레인스토밍  조사기획    시장+학술조사      분석     사업계획서   최종포맷
  ↓          ↓            ↓                ↓          ↓          ↓
[평가]     [평가]       [평가]           [평가]     [평가]     [평가]
```

## Phase별 상세

| Phase | 이름                | 완료 약속           | 주요 기능                             |
| ----- | ------------------- | ------------------- | ------------------------------------- |
| 0     | Ideation            | `PHASE0_COMPLETE` | SCAMPER, 6 Thinking Hats 브레인스토밍 |
| 1     | Research Planning   | `PHASE1_COMPLETE` | 5W1H 분석, 연구 질문 생성             |
| 2     | Market Research     | `PHASE2_COMPLETE` | TAM/SAM/SOM, 경쟁사, SWOT             |
| 3     | Academic Research   | `PHASE3_COMPLETE` | 논문, 기술 트렌드, Grok X검색         |
| 4     | Analysis & Ideation | `PHASE4_COMPLETE` | InfraNodus 지식 그래프, 아이디어 도출 |
| 5     | Business Plan       | `PHASE5_COMPLETE` | 8개 섹션 사업계획서 (재무 제외)       |
| 6     | Format Finalization | `PHASE6_COMPLETE` | 제출 양식 맞춤                        |

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
  - Grok API 실패 → OpenRouter 또는 WebSearch 대체
  - InfraNodus 실패 → 기본 텍스트 분석

## 품질 기준

| Phase | 필수 조건                      |
| ----- | ------------------------------ |
| 0     | 아이디어 ≥ 3개                |
| 1     | 연구 질문 ≥ 10개              |
| 2     | 경쟁사 ≥ 3개, 출처 ≥ 5개     |
| 3     | 논문 ≥ 3개 또는 트렌드 ≥ 5개 |
| 4     | 아이디어 ≥ 3개, 근거 명시     |
| 5     | 8개 섹션 완성                  |
| 6     | 포맷 제약 100% 준수            |

## 모집요강 제공 시점

### 핵심 원칙: "아이디어 먼저, 포맷은 마지막"

```
❌ 잘못된 접근: Phase 0에서 모집요강 제공
   → 아이디어가 요강의 제약에 갇혀 창의성 저하
   → "이 항목에 맞춰야 하니까..." 식의 제한된 사고

✅ 올바른 접근: Phase 6에서 모집요강 제공
   → Phase 0~5에서 제약 없이 우수한 아이디어 개발
   → Phase 6에서 완성된 아이디어를 요강에 맞게 설득력 있게 포장
```

### 언제 제공하나요?

| 시점                | Phase             | 제공 여부    | 이유                       |
| ------------------- | ----------------- | ------------ | -------------------------- |
| 프로젝트 시작       | Phase 0           | ❌           | 창의적 브레인스토밍 방해   |
| 조사 기획           | Phase 1           | ❌           | 조사 범위 불필요한 제한    |
| 시장/학술 조사      | Phase 2-3         | ❌           | 객관적 데이터 수집 필요    |
| 분석/아이디어       | Phase 4           | ❌           | 혁신적 아이디어 도출 방해  |
| 사업계획서 작성     | Phase 5           | ❌           | 완전한 사업 논리 구축 필요 |
| **최종 포맷** | **Phase 6** | **✅** | **이 시점에 제공**   |

### 제공 방법

```bash
# Phase 6 시작 시 모집요강 PDF 또는 MD 파일 제공
claude "모집요강을 분석해서 사업계획서를 최적화해주세요"

# 파일 경로 지정
/analyze-guidelines "path/to/모집요강.pdf"
```

### /analyze-guidelines 스킬이 하는 일

1. **프로그램 숨은 의도 분석**: 평가자가 정말 원하는 것 파악
2. **평가 기준 및 배점 추출**: 점수 극대화 전략 수립
3. **가점 항목 체크**: 해당 가점, 증빙 서류 목록
4. **섹션 매핑**: Phase 5 결과물 ↔ 모집요강 섹션 1:1 매핑
5. **톤앤매너 조정**: 평가자 관점에 맞는 표현 가이드

### 왜 이 방식이 효과적인가?

```
일반적인 접근:
  "KOTRA 수출바우처 신청하려는데 사업계획서 써줘"
  → 요강 항목 채우기에 급급
  → 깊이 없는 피상적 내용

우리 시스템:
  Phase 0~5: 진짜 좋은 사업 아이디어 깊이 개발
  Phase 6:   완성된 아이디어를 요강에 맞게 설득력 있게 포장
  → 차별화된 고품질 사업계획서
```

---

## 스킬 시스템

### 사용 가능한 스킬

| 스킬                    | 사용 Phase | 용도                                               |
| ----------------------- | ---------- | -------------------------------------------------- |
| `/x-search`           | Phase 3    | Grok API로 X/Twitter 실시간 트렌드 분석            |
| `/knowledge-graph`    | Phase 4    | InfraNodus 지식 그래프, 콘텐츠 갭, 아이디어 도출   |
| `/analyze-guidelines` | Phase 6    | 모집요강 심층 분석, 평가 기준/가점 추출, 매핑 전략 |

### 스킬 사용 예시

```bash
# X 트렌드 검색 (Phase 3)
/x-search "K-beauty trends 2025"

# 지식 그래프 분석 (Phase 4)
/knowledge-graph "[통합된 시장+학술 데이터]"

# 모집요강 분석 (Phase 6)
/analyze-guidelines "KOTRA_수출바우처_모집요강.pdf"
```

---

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
