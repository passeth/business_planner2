---
name: x-search
description: Grok API를 활용한 X(Twitter) 실시간 트렌드 검색. 키워드로 최신 트렌드, 인플루언서 반응, 소비자 센티멘트를 분석합니다. Phase 3 학술조사에서 소셜 트렌드 파악에 사용됩니다.
---

# X Search Skill

X(Twitter) 실시간 트렌드 검색 및 분석

## Purpose

Grok API의 `x_search` 도구를 활용하여 X(Twitter)에서 실시간 트렌드, 해시태그, 인플루언서 반응을 검색하고 분석합니다.

## When to Use

- 특정 키워드의 X 트렌드 분석
- 인플루언서/KOL 반응 수집
- 소비자 센티멘트 파악
- 해시태그 트렌드 모니터링
- 실시간 뉴스/이벤트 반응 조사

## Usage

### 기본 사용법

```bash
# 환경변수 설정 필요
export XAI_API_KEY="your-api-key"

# 스킬 호출
/x-search "K-beauty trends 2025"
```

### 입력 파라미터

| 파라미터 | 설명 | 예시 |
|---------|------|------|
| query | 검색 쿼리 | "K-beauty influencer marketing" |
| language | 언어 필터 (선택) | "ko", "en", "ja" |
| date_range | 날짜 범위 (선택) | "7d", "30d" |

### 출력 형식

```markdown
## X 트렌드 분석 결과

**검색 쿼리**: [query]
**분석 일시**: YYYY-MM-DD HH:MM

### 트렌딩 토픽
1. [토픽1] - 언급량: 높음
2. [토픽2] - 언급량: 중간

### 인기 해시태그
- #Kbeauty (긍정적)
- #skincare (중립)

### 주요 인플루언서 언급
- @influencer1: "포스트 내용 요약"
- @influencer2: "포스트 내용 요약"

### 센티멘트 분석
- 긍정: 65%
- 중립: 25%
- 부정: 10%

### 핵심 인사이트
1. [인사이트1]
2. [인사이트2]
```

## Implementation

### Python Script

```python
#!/usr/bin/env python3
"""X Search using Grok API with x_search tool."""
import os
import sys
from xai_sdk import Client
from xai_sdk.chat import user, system
from xai_sdk.tools import x_search

def search_x(query: str, context: str = None) -> str:
    """Execute X search with Grok API."""
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        return "Error: XAI_API_KEY not set. Please configure .env file."

    client = Client(api_key=api_key)
    chat = client.chat.create(
        model="grok-4-fast",
        tools=[x_search()]
    )

    system_prompt = """You are a trend analyst specializing in social media trends.
Search X (Twitter) and provide:
1. Trending topics related to the query
2. Popular hashtags
3. Key influencer mentions
4. Overall sentiment (positive/neutral/negative percentages)
5. Actionable insights for business planning

Format your response in structured markdown.
Always provide ACTUAL data from search results, not examples."""

    if context:
        system_prompt += f"\n\nBusiness context: {context}"

    chat.append(system(system_prompt))
    chat.append(user(f"Search X for trends about: {query}"))

    response = chat.sample()
    return response.content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python x_search.py \"query\"")
        sys.exit(1)

    result = search_x(sys.argv[1])
    print(result)
```

## Integration with Agents

### Phase 3 (Academic Research Agent)

```markdown
# academic-research-agent.md 에서 호출

## 3. X(Twitter) 트렌드 분석

/x-search 스킬을 사용하여 소셜 트렌드를 분석합니다:

1. 핵심 키워드로 X 검색
2. 트렌딩 토픽 및 해시태그 수집
3. 인플루언서 반응 분석
4. 센티멘트 분석 결과 정리
```

## Error Handling

| 에러 | 원인 | 해결책 |
|-----|------|--------|
| API_KEY_NOT_SET | 환경변수 미설정 | .env 파일에 XAI_API_KEY 설정 |
| RATE_LIMIT | API 호출 한도 초과 | 1분 대기 후 재시도 |
| NO_RESULTS | 검색 결과 없음 | 쿼리 확장 또는 WebSearch 폴백 |

## Fallback Strategy

Grok API 실패 시:
1. 재시도 (최대 3회, 지수 백오프)
2. WebSearch로 대체: `site:twitter.com {query}`
3. 대체 결과임을 명시하고 진행

## Related

- xai-grok-agent 글로벌 스킬 (상세 레퍼런스)
- academic-research-agent (Phase 3)
- Grok API 문서: https://docs.x.ai/
