#!/bin/bash
# Grok API X Search Script
# Usage: ./grok_search.sh "search query"

# Load environment variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [ -f "$ENV_FILE" ]; then
    export $(cat "$ENV_FILE" | grep -v '#' | xargs)
fi

# Check API key
if [ -z "$XAI_API_KEY" ]; then
    echo "Error: XAI_API_KEY not set"
    exit 1
fi

# Default values
API_URL="${XAI_API_URL:-https://api.x.ai/v1/chat/completions}"
MODEL="${XAI_MODEL:-grok-4-fast}"
QUERY="$1"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 \"search query\""
    echo "Example: $0 \"K-beauty trends 2025\""
    exit 1
fi

echo "Searching X/Twitter for: $QUERY"
echo "Using model: $MODEL"
echo "---"

# Make API request
curl -s -X POST "$API_URL" \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "'"$MODEL"'",
    "messages": [
      {
        "role": "system",
        "content": "You are a trend analyst specializing in beauty and K-beauty trends on X/Twitter. Analyze posts, identify trending topics, hashtags, and sentiment."
      },
      {
        "role": "user",
        "content": "Search X/Twitter for: '"$QUERY"'\n\nProvide:\n1. Top 10 relevant posts/trends\n2. Popular hashtags\n3. Key influencers mentioned\n4. Overall sentiment\n5. Notable patterns"
      }
    ],
    "tools": [{"type": "x_search"}],
    "temperature": 0.7,
    "max_tokens": 4096
  }' | python3 -m json.tool 2>/dev/null || cat
