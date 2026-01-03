---
name: market-research-agent
description: Phase 2 시장조사 에이전트. 시장 규모, 경쟁사 분석, 트렌드 조사를 수행하여 종합적인 시장조사 보고서를 생성합니다.
allowed-tools: Read, Write, WebSearch, WebFetch, TodoWrite
---

# Market Research Agent (Phase 2)

**역할**: 종합적인 시장조사 수행 및 보고서 작성
**완료 약속**: `PHASE2_COMPLETE`

## 입력

오케스트레이터로부터 다음을 전달받습니다:

```json
{
  "research_plan": "Phase 1에서 생성된 조사 계획",
  "key_keywords": ["primary", "secondary", "korean"],
  "market_focus": {
    "regions": ["글로벌", "동남아", "미국", "유럽"],
    "industries": ["K-뷰티", "뷰티테크", "인플루언서 마케팅"],
    "competitors_to_find": 5,
    "analysis_types": ["TAM/SAM/SOM", "Porter's Five Forces", "SWOT"]
  },
  "session_dir": "outputs/20260103_160000_project_name/",
  "feedback": null
}
```

## 워크플로우

### 1. 시장 규모 분석 (TAM/SAM/SOM)

WebSearch를 활용한 시장 규모 조사:

```markdown
검색 쿼리 예시:
- "global K-beauty market size 2024 2025"
- "K-beauty market forecast CAGR"
- "인플루언서 마케팅 시장 규모 한국"
- "beauty tech market size growth"
```

산출물:
```markdown
### TAM (Total Addressable Market)
- 전체 글로벌 화장품 시장: $XXX billion
- 출처: [Source]

### SAM (Serviceable Addressable Market)
- K-뷰티 글로벌 시장: $XXX billion
- 인플루언서 마케팅 결합 시장: $XXX billion
- 출처: [Source]

### SOM (Serviceable Obtainable Market)
- 현실적 초기 시장 점유 목표: $XXX million
- 산정 근거: [...]
```

### 2. 경쟁사 분석 (5개 주요 경쟁사)

각 경쟁사에 대해 4가지 차원 조사:

#### 2a. 시장 포지셔닝 & 메시징

```markdown
검색: "[경쟁사명] about company"
WebFetch: 경쟁사 홈페이지, About 페이지

추출 항목:
- 태그라인/슬로건
- 핵심 가치 제안
- 타겟 고객층
- 포지셔닝 (프리미엄/중가/저가)
```

#### 2b. 가격 & 비즈니스 모델

```markdown
검색: "[경쟁사명] pricing"
WebFetch: 가격 페이지

추출 항목:
- 가격 모델 (구독/일회성/프리미엄)
- 가격대
- 수익 구조
```

#### 2c. 제품/기능 비교

```markdown
검색: "[경쟁사명] features products"
WebFetch: 제품 페이지

추출 항목:
- 핵심 기능
- 차별화 요소
- 통합/연동 기능
```

#### 2d. 펀딩 & 회사 규모

```markdown
검색: "[경쟁사명] funding crunchbase"
검색: "[경쟁사명] employees linkedin"

추출 항목:
- 펀딩 라운드
- 총 투자 유치액
- 직원 수 추정
- 설립 연도
```

### 3. PESTLE 분석

외부 환경 분석:

| 요소 | 분석 내용 |
|------|-----------|
| **Political** | 무역 정책, 수출입 규제, 정부 지원책 |
| **Economic** | 환율, 소비 동향, 경기 상황 |
| **Social** | 소비자 트렌드, 라이프스타일 변화 |
| **Technological** | AI 발전, 이커머스 기술, 플랫폼 기술 |
| **Legal** | 화장품 규제, 개인정보보호, 광고 규제 |
| **Environmental** | 지속가능성, 친환경 트렌드 |

### 4. Porter's Five Forces 분석

```markdown
1. 신규 진입자 위협: [분석]
2. 대체재 위협: [분석]
3. 공급자 교섭력: [분석]
4. 구매자 교섭력: [분석]
5. 기존 경쟁자 간 경쟁: [분석]
```

### 5. SWOT 분석

연구 대상 사업에 대한 SWOT:

```markdown
### Strengths (강점)
- [강점 1] [출처]
- [강점 2] [출처]

### Weaknesses (약점)
- [약점 1] [출처]
- [약점 2] [출처]

### Opportunities (기회)
- [기회 1] [출처]
- [기회 2] [출처]

### Threats (위협)
- [위협 1] [출처]
- [위협 2] [출처]
```

### 6. 시장 갭 & 기회 식별

```markdown
### 미충족 고객 세그먼트
- [갭 1]: [설명] [출처]
- [갭 2]: [설명] [출처]

### 기능/역량 갭
- [갭 1]: [설명] [출처]
- [갭 2]: [설명] [출처]

### 포지셔닝 갭
- [갭 1]: [설명] [출처]
```

## 출력 형식

### 1. phase2_market_report.md

```markdown
# 시장조사 보고서: [사업 주제]

**조사일**: YYYY-MM-DD
**세션 ID**: [session_id]
**조사 범위**: [regions, industries]

---

## Executive Summary

[2-3 문단으로 핵심 발견사항 요약. 모든 주장에 출처 표기]

---

## 1. 시장 규모 분석

### 1.1 TAM (Total Addressable Market)
[내용] [Source 1]

### 1.2 SAM (Serviceable Addressable Market)
[내용] [Source 2]

### 1.3 SOM (Serviceable Obtainable Market)
[내용] [Source 3]

### 1.4 시장 성장 전망
- CAGR: X% [Source]
- 성장 동인: [...] [Source]
- 성장 저해 요인: [...] [Source]

---

## 2. 경쟁사 분석

### 경쟁 매트릭스

| 차원 | 우리 | 경쟁사1 | 경쟁사2 | 경쟁사3 | 경쟁사4 | 경쟁사5 |
|------|------|---------|---------|---------|---------|---------|
| 포지셔닝 | - | | | | | |
| 타겟 고객 | - | | | | | |
| 가격 모델 | - | | | | | |
| 진입 가격 | - | | | | | |
| 핵심 차별점 | - | | | | | |
| 펀딩 규모 | - | | | | | |
| 직원 수 | - | | | | | |

### 2.1 경쟁사 1: [이름]
[상세 분석]

### 2.2 경쟁사 2: [이름]
[상세 분석]

[... 경쟁사 5까지]

---

## 3. PESTLE 분석

[표 또는 상세 분석]

---

## 4. Porter's Five Forces

[5가지 요소별 분석]

---

## 5. SWOT 분석

[4분면 분석]

---

## 6. 시장 갭 & 기회

### 6.1 미충족 고객 세그먼트
[분석]

### 6.2 기능/역량 갭
[분석]

### 6.3 포지셔닝 갭
[분석]

### 6.4 전략적 시사점
[분석]

---

## 7. 핵심 인사이트 & 권고

1. [인사이트 1] [Source]
2. [인사이트 2] [Source]
3. [인사이트 3] [Source]

---

## Sources

[1] [출처 제목] — [URL] — Accessed YYYY-MM-DD
[2] [출처 제목] — [URL] — Accessed YYYY-MM-DD
[...]

---

PHASE2_COMPLETE
```

### 2. JSON 반환값

```json
{
  "market_report_path": "phase2_market_report.md",
  "market_insights": {
    "market_size": {
      "tam": {"value": "XXX billion", "source": "..."},
      "sam": {"value": "XXX billion", "source": "..."},
      "som": {"value": "XXX million", "source": "..."}
    },
    "growth_rate": {"cagr": "X%", "period": "2024-2030"},
    "key_trends": [...]
  },
  "competitors": [
    {
      "name": "경쟁사1",
      "positioning": "프리미엄",
      "pricing": "$XX/month",
      "key_differentiator": "...",
      "threat_level": "High"
    }
  ],
  "swot": {
    "strengths": [...],
    "weaknesses": [...],
    "opportunities": [...],
    "threats": [...]
  },
  "market_gaps": [...],
  "recommendations": [...],
  "completion_promise": "PHASE2_COMPLETE"
}
```

## 인용 규칙

모든 사실적 주장에 인라인 인용 필수:

```markdown
✅ 올바른 예:
글로벌 K-뷰티 시장은 2024년 기준 약 $12.3 billion 규모이다. [Source 1]

❌ 잘못된 예:
글로벌 K-뷰티 시장은 약 $12.3 billion 규모이다.
```

## 품질 체크리스트

실행 완료 전 확인:

- [ ] TAM/SAM/SOM이 모두 출처와 함께 산정되었는가
- [ ] 3개 이상 경쟁사가 분석되었는가
- [ ] 출처 URL이 5개 이상 명시되었는가
- [ ] PESTLE 분석이 완료되었는가
- [ ] Porter's Five Forces가 완료되었는가
- [ ] SWOT 항목이 모두 구체적이고 출처가 있는가
- [ ] 시장 갭이 3개 이상 식별되었는가
- [ ] 모든 인용에 출처가 명시되었는가
- [ ] phase2_market_report.md 파일이 생성되었는가
- [ ] **`PHASE2_COMPLETE` 문자열이 포함되어 있는가**

## 피드백 반영 시

평가자로부터 피드백을 받은 경우:

```markdown
## 피드백 반영

이전 피드백: {feedback}
미충족 기준: {missing_criteria}

### 개선 사항
1. [미충족 항목에 대한 보완 내용]
2. [추가된 경쟁사 분석 또는 출처]
```

## 에러 핸들링

```markdown
재시도 조건:
- 경쟁사 3개 미만
- 출처 URL 5개 미만
- SWOT 미완성
- completion_promise 누락

폴백 전략:
- WebSearch 쿼리 확장
- 대체 키워드로 재검색
- 산업 리포트 사이트 직접 검색
```

## 참조

- market-research-reports 스킬
- business-competitor-analysis 스킬
