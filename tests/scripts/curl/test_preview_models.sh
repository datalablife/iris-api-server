#!/bin/bash

API_KEY="AIzaSyBvfAGPPtwtX2eCH2_OG1tkLGirfwfvyWk"

echo "Testing gemini-2.5-pro-preview-05-06 with more tokens..."
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-05-06:generateContent?key=${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Please respond with a simple greeting. Say hello and introduce yourself."
          }
        ]
      }
    ],
    "generationConfig": {
      "temperature": 0.7,
      "maxOutputTokens": 100
    }
  }' | jq '.'

echo -e "\n\nTesting gemini-2.5-pro-preview-06-05 with more tokens..."
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-06-05:generateContent?key=${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Please respond with a simple greeting. Say hello and introduce yourself."
          }
        ]
      }
    ],
    "generationConfig": {
      "temperature": 0.7,
      "maxOutputTokens": 100
    }
  }' | jq '.'
