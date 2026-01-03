---
name: knowledge-graph
description: InfraNodus MCP를 활용한 지식 그래프 분석. 텍스트에서 토픽 클러스터, 콘텐츠 갭, 연구 질문을 도출합니다. Phase 4 분석/아이디에이션에서 혁신적 아이디어 발굴에 사용됩니다.
---

# Knowledge Graph Skill

InfraNodus 기반 지식 그래프 분석 및 아이디어 도출

## Purpose

텍스트 데이터를 지식 그래프로 변환하여 토픽 클러스터, 콘텐츠 갭, 잠재적 연결고리를 발견합니다. 이를 통해 혁신적인 연구 질문과 사업 아이디어를 도출합니다.

## When to Use

- 대량의 조사 데이터에서 패턴 발견
- 토픽 클러스터 및 핵심 개념 추출
- 콘텐츠 갭 (연결되지 않은 주제) 식별
- 혁신적 아이디어 및 연구 질문 생성
- 경쟁사/시장 분석 결과 시각화

## Available MCP Tools

InfraNodus MCP 서버가 제공하는 도구들:

| 도구 | 용도 |
|-----|------|
| `generate_knowledge_graph` | 텍스트에서 지식 그래프 생성 |
| `generate_topical_clusters` | 토픽 클러스터 추출 |
| `generate_content_gaps` | 콘텐츠 갭 식별 |
| `generate_research_questions` | 연구 질문 생성 |
| `generate_research_ideas` | 혁신 아이디어 생성 |
| `develop_latent_topics` | 숨겨진 토픽 발견 |
| `develop_conceptual_bridges` | 개념적 연결고리 제안 |

## Usage

### 기본 사용법

```bash
# 스킬 호출
/knowledge-graph "분석할 텍스트 또는 파일 경로"
```

### 워크플로우

```
입력 텍스트 (Phase 2+3 결과물)
         ↓
    지식 그래프 생성
         ↓
    토픽 클러스터 추출
         ↓
    콘텐츠 갭 식별
         ↓
    연구 질문/아이디어 생성
         ↓
    출력: 구조화된 인사이트
```

### 입력 형식

```json
{
  "text": "분석할 텍스트 (Phase 2+3 결과물 결합)",
  "analysis_type": "full | clusters | gaps | questions | ideas",
  "model": "gpt-4o | claude-sonnet-4 | grok-4-fast"
}
```

### 출력 형식

```markdown
## 지식 그래프 분석 결과

**분석 일시**: YYYY-MM-DD HH:MM
**텍스트 길이**: N 문자
**추출된 개념**: N개

---

### 1. 토픽 클러스터

| 클러스터 | 핵심 키워드 | 중요도 |
|---------|------------|--------|
| 클러스터 A | keyword1, keyword2, keyword3 | 높음 |
| 클러스터 B | keyword4, keyword5 | 중간 |

---

### 2. 콘텐츠 갭 (숨겨진 기회)

연결되지 않은 클러스터 쌍에서 발견된 기회:

| 갭 | 클러스터 A | 클러스터 B | 잠재적 연결 |
|----|-----------|-----------|------------|
| 갭 1 | AI 기술 | 고객 경험 | AI 기반 개인화 |
| 갭 2 | 인플루언서 | 제품 개발 | 공동 창작 |

---

### 3. 연구 질문

콘텐츠 갭에서 도출된 질문:

1. 어떻게 [클러스터 A]와 [클러스터 B]를 연결할 수 있을까?
2. [갭 영역]에서 어떤 혁신이 가능할까?

---

### 4. 혁신 아이디어

| 아이디어 | 근거 (콘텐츠 갭) | 실현 가능성 |
|---------|-----------------|------------|
| 아이디어 1 | 갭 1에서 도출 | 높음 |
| 아이디어 2 | 갭 2에서 도출 | 중간 |

---

### 5. 핵심 인사이트

1. [인사이트 1]
2. [인사이트 2]
3. [인사이트 3]
```

## Integration with Agents

### Phase 4 (Analysis & Ideation Agent)

```markdown
# analysis-ideation-agent.md 에서 호출

## 지식 그래프 분석

/knowledge-graph 스킬을 사용하여:

1. Phase 2+3 결과물을 결합
2. 지식 그래프 생성 및 분석
3. 콘텐츠 갭에서 아이디어 도출
4. 사용자에게 아이디어 선택 요청
```

## MCP Tool Examples

### 1. 지식 그래프 생성

```javascript
// MCP 호출
mcp__infranodus__generate_knowledge_graph({
  text: "Phase 2+3 조사 결과물...",
  modifyAnalyzedText: "none",
  includeGraph: false,
  addNodesAndEdges: false
})
```

### 2. 토픽 클러스터 추출

```javascript
mcp__infranodus__generate_topical_clusters({
  text: "분석할 텍스트..."
})
```

### 3. 콘텐츠 갭 식별

```javascript
mcp__infranodus__generate_content_gaps({
  text: "분석할 텍스트..."
})
```

### 4. 연구 질문 생성

```javascript
mcp__infranodus__generate_research_questions({
  text: "분석할 텍스트...",
  modelToUse: "gpt-4o",
  gapDepth: 0,
  useSeveralGaps: true
})
```

### 5. 혁신 아이디어 생성

```javascript
mcp__infranodus__generate_research_ideas({
  text: "분석할 텍스트...",
  modelToUse: "claude-sonnet-4",
  gapDepth: 0,
  useSeveralGaps: true
})
```

## Error Handling

| 에러 | 원인 | 해결책 |
|-----|------|--------|
| MCP_NOT_CONNECTED | InfraNodus MCP 미연결 | .mcp.json 확인 |
| TEXT_TOO_SHORT | 분석할 텍스트 부족 | 더 많은 데이터 제공 |
| API_ERROR | InfraNodus API 오류 | 재시도 또는 폴백 |

## Fallback Strategy

InfraNodus 실패 시:

1. **기본 텍스트 분석**:
   - 키워드 빈도 분석
   - TF-IDF 기반 중요 개념 추출
   - 공출현 분석으로 연관 개념 파악

2. **수동 분석 가이드 제공**:
   ```markdown
   ## 폴백: 수동 분석 가이드

   InfraNodus 연결 실패. 수동 분석을 수행합니다:

   1. 핵심 키워드 추출 (빈도 기반)
   2. 관련 키워드 그룹화
   3. 그룹 간 연결 가능성 탐색
   ```

## Related

- analysis-ideation-agent (Phase 4)
- InfraNodus: https://infranodus.com/
- .mcp.json 설정 파일
