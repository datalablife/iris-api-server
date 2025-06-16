#!/bin/bash

# Test Gemini models using curl
echo "🔬 Testing Gemini Models with curl"
echo "============================================================"

API_KEY="AIzaSyBvfAGPPtwtX2eCH2_OG1tkLGirfwfvyWk"

# Models to test
models=(
    "gemini-2.5-pro-preview-05-06"
    "gemini-2.5-pro-preview-06-05"
    "gemini-2.0-flash"
    "gemini-1.5-pro"
)

# Test payload
payload='{
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

echo "✅ API key: ${API_KEY:0:10}..."
echo ""

# Test each model
for model in "${models[@]}"; do
    echo "🧪 Testing model: $model"
    echo "--------------------------------------------------"
    
    url="https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${API_KEY}"
    
    echo "🌐 URL: $url"
    echo "🔄 Making API call..."
    
    # Make the request and capture both status and response
    response=$(curl -s -w "\n%{http_code}" -X POST "$url" \
        -H "Content-Type: application/json" \
        -d "$payload" 2>&1)
    
    # Extract status code (last line) and response body (everything else)
    status_code=$(echo "$response" | tail -n1)
    response_body=$(echo "$response" | head -n -1)
    
    echo "📊 Status: $status_code"
    
    if [ "$status_code" = "200" ]; then
        echo "✅ SUCCESS!"
        # Try to extract the text response
        text_response=$(echo "$response_body" | jq -r '.candidates[0].content.parts[0].text' 2>/dev/null)
        if [ "$text_response" != "null" ] && [ "$text_response" != "" ]; then
            echo "📝 Response: $text_response"
        else
            echo "📄 Full response: $response_body"
        fi
    else
        echo "❌ FAILED!"
        echo "📄 Error response: $response_body"
        
        # Try to extract error details
        error_message=$(echo "$response_body" | jq -r '.error.message' 2>/dev/null)
        if [ "$error_message" != "null" ] && [ "$error_message" != "" ]; then
            echo "🔍 Error: $error_message"
        fi
    fi
    
    echo ""
done

echo "============================================================"
echo "📊 Testing model list API"
echo "============================================================"

list_url="https://generativelanguage.googleapis.com/v1beta/models?key=${API_KEY}"
echo "🔄 Fetching available models..."

list_response=$(curl -s -w "\n%{http_code}" "$list_url" 2>&1)
list_status=$(echo "$list_response" | tail -n1)
list_body=$(echo "$list_response" | head -n -1)

echo "📊 Status: $list_status"

if [ "$list_status" = "200" ]; then
    echo "✅ SUCCESS!"
    echo "🔍 Extracting Gemini models..."
    
    # Extract Gemini models
    gemini_models=$(echo "$list_body" | jq -r '.models[] | select(.name | contains("gemini")) | .name' 2>/dev/null)
    
    if [ -n "$gemini_models" ]; then
        echo "📦 Available Gemini models:"
        echo "$gemini_models" | while read -r model; do
            echo "   - $model"
        done
    else
        echo "⚠️ No Gemini models found or unable to parse response"
        echo "📄 Raw response: $list_body"
    fi
else
    echo "❌ FAILED!"
    echo "📄 Error: $list_body"
fi

echo ""
echo "============================================================"
echo "✅ Test completed!"
