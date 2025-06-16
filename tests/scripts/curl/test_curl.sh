#!/bin/bash

# Test Gemini API with curl
echo "Testing Gemini API with curl..."

API_KEY="AIzaSyBvfAGPPtwtX2eCH2_OG1tkLGirfwfvyWk"
URL="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}"

curl -X POST "${URL}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Hello! Please respond with Hello from Gemini to test the connection."
          }
        ]
      }
    ],
    "generationConfig": {
      "temperature": 0.7,
      "maxOutputTokens": 100
    }
  }'
