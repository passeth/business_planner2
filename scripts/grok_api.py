"""
Grok API Helper for Business Plan Generator v2.0
X(Twitter) 트렌드 분석 및 웹 검색을 위한 Grok API 래퍼
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

# API 설정
XAI_API_KEY = os.getenv('XAI_API_KEY')
XAI_API_URL = os.getenv('XAI_API_URL', 'https://api.x.ai/v1/chat/completions')
XAI_MODEL = os.getenv('XAI_MODEL', 'grok-4-fast')


class GrokAPI:
    """Grok API 클라이언트"""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or XAI_API_KEY
        self.api_url = XAI_API_URL
        self.model = XAI_MODEL

        if not self.api_key:
            raise ValueError("XAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요.")

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

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        if tools:
            payload["tools"] = tools

        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

    def x_search(self, query: str, context: str = "trend analyst") -> Dict[str, Any]:
        """
        X(Twitter) 검색 수행

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

        tools = [{"type": "x_search"}]

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

        tools = [{"type": "web_search"}]

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

        tools = [{"type": "x_search"}, {"type": "web_search"}]

        return self._make_request(messages, tools)


def x_search_kbeauty(query: str) -> str:
    """K-뷰티 트렌드 검색 헬퍼 함수"""
    try:
        grok = GrokAPI()
        result = grok.x_search(query, "K-beauty trend analyst")
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


def analyze_market_trends(keywords: List[str]) -> str:
    """시장 트렌드 분석 헬퍼 함수"""
    try:
        grok = GrokAPI()
        result = grok.analyze_trends(keywords)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"Error: {str(e)}"


# CLI 실행
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python grok_api.py <query>")
        print("Example: python grok_api.py 'K-beauty trends 2025'")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    print(f"Searching X/Twitter for: {query}\n")

    result = x_search_kbeauty(query)
    print(result)
