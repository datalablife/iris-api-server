#!/bin/bash

# Secure Gemini API Test Script
# This script demonstrates secure API testing using environment variables

echo "🧪 Secure Gemini API Test"
echo "========================="

# SECURITY CHECK: Verify API key is set via environment variable
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "❌ Error: GOOGLE_API_KEY environment variable is not set"
    echo ""
    echo "To set your API key:"
    echo "  export GOOGLE_API_KEY='your_api_key_here'"
    echo ""
    echo "To get an API key:"
    echo "  1. Go to https://ai.google.dev/"
    echo "  2. Create a new project or select existing"
    echo "  3. Generate an API key"
    echo "  4. Set the environment variable"
    exit 1
fi

# Use environment variable (SECURE)
API_KEY="$GOOGLE_API_KEY"

# Show masked key for verification (SECURE - only shows first 10 chars)
echo "🔑 Using API key: ${API_KEY:0:10}..."
echo ""

# Test different Gemini models
models=(
    "gemini-2.0-flash"
    "gemini-1.5-pro"
    "gemini-2.5-pro-preview-05-06"
)

test_payload='{
    "contents": [
        {
            "parts": [
                {
                    "text": "Hello! Please respond with a simple greeting to test the connection."
                }
            ]
        }
    ],
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 50
    }
}'

# Test each model
for model in "${models[@]}"; do
    echo "🔬 Testing model: $model"
    echo "----------------------------------------"
    
    URL="https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${API_KEY}"
    
    # Make API request with timeout
    response=$(curl -s -X POST "$URL" \
        -H "Content-Type: application/json" \
        -d "$test_payload" \
        --connect-timeout 10 \
        --max-time 30)
    
    # Check if request was successful
    if [ $? -eq 0 ]; then
        # Check if response contains error
        if echo "$response" | grep -q '"error"'; then
            echo "❌ Error response:"
            echo "$response" | jq '.error.message' 2>/dev/null || echo "$response"
        else
            echo "✅ Success! Response received:"
            echo "$response" | jq '.candidates[0].content.parts[0].text' 2>/dev/null || echo "Response received (jq not available)"
        fi
    else
        echo "❌ Request failed (network error)"
    fi
    
    echo ""
done

echo "🎉 Test completed!"
echo ""
echo "💡 Tips:"
echo "  - Keep your API key secure and never commit it to version control"
echo "  - Monitor your API usage at https://console.cloud.google.com/"
echo "  - Set up billing alerts to avoid unexpected charges"
