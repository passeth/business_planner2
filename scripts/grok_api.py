"""
LLM API Helper for Business Plan Generator v2.0
Grok API 및 OpenRouter를 지원하는 통합 API 래퍼
X(Twitter) 트렌드 분석 및 웹 검색 기능 포함
"""

import os
import json
import requests
from typing import Optional, List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# LLM Provider 설정
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'auto')  # "grok", "openrouter", "auto"

# Grok API 설정
XAI_API_KEY = os.getenv('XAI_API_KEY')
XAI_API_URL = os.getenv('XAI_API_URL', 'https://api.x.ai/v1/chat/completions')
XAI_MODEL = os.getenv('XAI_MODEL', 'grok-2-latest')

# OpenRouter API 설정
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_API_URL = os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'x-ai/grok-2-1212')


def get_active_provider() -> str:
    """현재 활성화된 LLM Provider 반환"""
    if LLM_PROVIDER == 'grok' and XAI_API_KEY:
        return 'grok'
    elif LLM_PROVIDER == 'openrouter' and OPENROUTER_API_KEY:
        return 'openrouter'
    elif LLM_PROVIDER == 'auto':
        if XAI_API_KEY:
            return 'grok'
        elif OPENROUTER_API_KEY:
            return 'openrouter'
    return 'none'


class LLMClient:
    """통합 LLM 클라이언트 (Grok + OpenRouter 지원)"""

    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None):
        """
        Args:
            api_key: API 키 (None이면 환경변수에서 자동 로드)
            provider: "grok", "openrouter", 또는 None (자동 감지)
        """
        self.provider = provider or get_active_provider()

        if self.provider == 'grok':
            self.api_key = api_key or XAI_API_KEY
            self.api_url = XAI_API_URL
            self.model = XAI_MODEL
            self.supports_tools = True  # Grok은 X search, web search 도구 지원
        elif self.provider == 'openrouter':
            self.api_key = api_key or OPENROUTER_API_KEY
            self.api_url = OPENROUTER_API_URL
            self.model = OPENROUTER_MODEL
            self.supports_tools = False  # OpenRouter는 도구 지원 제한
        else:
            raise ValueError(
                "API 키가 설정되지 않았습니다.\n"
                "setup.py를 실행하여 설정하세요: python setup.py"
            )

        if not self.api_key:
            raise ValueError(
                f"{self.provider.upper()} API 키가 설정되지 않았습니다.\n"
                "setup.py를 실행하여 설정하세요: python setup.py"
            )

    def _make_request(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """API 요청 실행"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # OpenRouter 추가 헤더
        if self.provider == 'openrouter':
            headers["HTTP-Referer"] = "https://github.com/business-planner"
            headers["X-Title"] = "Business Plan Generator"

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # 도구 지원 (Grok만)
        if tools and self.supports_tools:
            payload["tools"] = tools

        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7
    ) -> str:
        """간단한 채팅 요청"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        result = self._make_request(messages, temperature=temperature)
        return result['choices'][0]['message']['content']

    def x_search(self, query: str, context: str = "trend analyst") -> Dict[str, Any]:
        """
        X(Twitter) 검색 수행 (Grok만 지원)

        Args:
            query: 검색 쿼리
            context: 분석 컨텍스트 (기본: trend analyst)

        Returns:
            검색 결과 딕셔너리
        """
        messages = [
            {
                "role": "system",
                "content": f"You are a {context} specializing in beauty and K-beauty trends on X/Twitter. "
                          "Analyze posts, identify trending topics, hashtags, and sentiment."
            },
            {
                "role": "user",
                "content": f"Search X/Twitter for: {query}\n\n"
                          "Provide:\n"
                          "1. Top 10 relevant posts/trends\n"
                          "2. Popular hashtags\n"
                          "3. Key influencers mentioned\n"
                          "4. Overall sentiment (positive/neutral/negative)\n"
                          "5. Notable patterns or insights"
            }
        ]

        tools = [{"type": "x_search"}] if self.supports_tools else None

        return self._make_request(messages, tools)

    def web_search(self, query: str, context: str = "research assistant") -> Dict[str, Any]:
        """
        웹 검색 수행

        Args:
            query: 검색 쿼리
            context: 검색 컨텍스트

        Returns:
            검색 결과 딕셔너리
        """
        messages = [
            {
                "role": "system",
                "content": f"You are a {context}. Search the web for relevant, up-to-date information."
            },
            {
                "role": "user",
                "content": f"Search for: {query}\n\n"
                          "Provide comprehensive results with sources."
            }
        ]

        tools = [{"type": "web_search"}] if self.supports_tools else None

        return self._make_request(messages, tools)

    def analyze_trends(
        self,
        keywords: List[str],
        industry: str = "K-beauty",
        time_period: str = "past week"
    ) -> Dict[str, Any]:
        """
        키워드 기반 트렌드 종합 분석

        Args:
            keywords: 분석할 키워드 목록
            industry: 산업 분야
            time_period: 분석 기간

        Returns:
            종합 트렌드 분석 결과
        """
        keywords_str = ", ".join(keywords)

        messages = [
            {
                "role": "system",
                "content": f"You are an expert trend analyst in the {industry} industry. "
                          "You analyze X/Twitter trends and web data to identify market opportunities."
            },
            {
                "role": "user",
                "content": f"Analyze trends for the following keywords in {industry} over the {time_period}:\n"
                          f"Keywords: {keywords_str}\n\n"
                          "Provide:\n"
                          "1. Trending topics per keyword\n"
                          "2. Cross-keyword patterns\n"
                          "3. Emerging themes\n"
                          "4. Influencer landscape\n"
                          "5. Consumer sentiment analysis\n"
                          "6. Business opportunity insights"
            }
        ]

        tools = [{"type": "x_search"}, {"type": "web_search"}] if self.supports_tools else None

        return self._make_request(messages, tools)


# 하위 호환성을 위한 GrokAPI alias
class GrokAPI(LLMClient):
    """GrokAPI 하위 호환성 클래스 (LLMClient 사용 권장)"""
    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key=api_key)


def x_search_kbeauty(query: str) -> str:
    """K-뷰티 트렌드 검색 헬퍼 함수"""
    try:
        client = LLMClient()
        result = client.x_search(query, "K-beauty trend analyst")
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


def analyze_market_trends(keywords: List[str]) -> str:
    """시장 트렌드 분석 헬퍼 함수"""
    try:
        client = LLMClient()
        result = client.analyze_trends(keywords)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


def get_provider_info() -> str:
    """현재 설정된 Provider 정보 반환"""
    provider = get_active_provider()
    if provider == 'grok':
        return f"Grok API (Model: {XAI_MODEL})"
    elif provider == 'openrouter':
        return f"OpenRouter (Model: {OPENROUTER_MODEL})"
    else:
        return "Not configured - run: python setup.py"


# CLI 실행
if __name__ == "__main__":
    import sys

    print(f"🔧 Active Provider: {get_provider_info()}\n")

    if len(sys.argv) < 2:
        print("Usage: python grok_api.py <query>")
        print("Example: python grok_api.py 'K-beauty trends 2025'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"🔍 Searching for: {query}\n")

    result = x_search_kbeauty(query)
    print(result)
