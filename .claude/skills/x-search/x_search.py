#!/usr/bin/env python3
"""
X (Twitter) Search Skill using Grok API.

Usage:
    python x_search.py "search query"
    python x_search.py "K-beauty trends" --context "cosmetics business"
"""
import os
import sys
import argparse
from pathlib import Path

# Load environment variables from .env
def load_env():
    env_path = Path(__file__).parent.parent.parent.parent / '.env'
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env()

def search_x(query: str, context: str = None, language: str = None) -> str:
    """
    Execute X search with Grok API.

    Args:
        query: Search query string
        context: Business context for better analysis
        language: Language filter (ko, en, ja, etc.)

    Returns:
        Formatted markdown string with search results
    """
    try:
        from xai_sdk import Client
        from xai_sdk.chat import user, system
        from xai_sdk.tools import x_search
    except ImportError:
        return """## Error: xai-sdk not installed

Please install the xAI SDK:
```bash
pip install xai-sdk
```
"""

    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        return """## Error: XAI_API_KEY not set

Please configure your API key in the .env file:
```
XAI_API_KEY=your_api_key_here
```

Get your API key from: https://console.x.ai/
"""

    try:
        client = Client(api_key=api_key)
        model = os.getenv("XAI_MODEL", "grok-4-fast")

        chat = client.chat.create(
            model=model,
            tools=[x_search()]
        )

        system_prompt = """You are a trend analyst specializing in social media trends on X (Twitter).

Your task is to search X and provide a comprehensive analysis including:

1. **Trending Topics**: List the most relevant trending topics related to the query
2. **Popular Hashtags**: Identify hashtags being used (with sentiment)
3. **Key Influencer Mentions**: Notable accounts discussing this topic
4. **Sentiment Analysis**: Overall sentiment breakdown (positive/neutral/negative %)
5. **Key Insights**: Actionable business insights from the trends

IMPORTANT:
- Provide ACTUAL data from search results, not examples
- Include real usernames and post summaries when available
- Focus on recent activity (last 7 days preferred)
- Format response in clean, structured markdown
"""

        if context:
            system_prompt += f"\n\nBusiness Context: {context}\nTailor your insights to this specific business context."

        if language:
            system_prompt += f"\n\nFocus on posts in: {language}"

        chat.append(system(system_prompt))
        chat.append(user(f"Search X (Twitter) for: {query}"))

        print(f"Searching X for: {query}...", file=sys.stderr)
        response = chat.sample()

        return response.content

    except Exception as e:
        return f"""## Error: X Search Failed

**Error**: {str(e)}

### Fallback Suggestion
Try using WebSearch with:
- `site:twitter.com {query}`
- `site:x.com {query}`
"""


def main():
    parser = argparse.ArgumentParser(
        description='Search X (Twitter) using Grok API'
    )
    parser.add_argument('query', help='Search query')
    parser.add_argument('--context', '-c', help='Business context for analysis')
    parser.add_argument('--language', '-l', help='Language filter (ko, en, ja)')
    parser.add_argument('--output', '-o', help='Output file path')

    args = parser.parse_args()

    result = search_x(args.query, args.context, args.language)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Results saved to: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()
