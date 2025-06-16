#!/bin/bash

API_KEY="AIzaSyBvfAGPPtwtX2eCH2_OG1tkLGirfwfvyWk"

echo "Testing gemini-2.5-pro-preview-05-06 with system instruction..."
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-05-06:generateContent?key=${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "systemInstruction": {
      "parts": [
        {
          "text": "You are a helpful assistant. Always provide clear, direct responses."
        }
      ]
    },
    "contents": [
      {
        "parts": [
          {
            "text": "Hello! Please introduce yourself."
          }
        ]
      }
    ],
    "generationConfig": {
      "temperature": 0.7,
      "maxOutputTokens": 100,
      "responseMimeType": "text/plain"
    }
  }'

echo -e "\n\n" 
echo "============================================================"
echo "Testing gemini-2.5-pro-preview-06-05 with system instruction..."
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-06-05:generateContent?key=${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "systemInstruction": {
      "parts": [
        {
          "text": "You are a helpful assistant. Always provide clear, direct responses."
        }
      ]
    },
    "contents": [
      {
        "parts": [
          {
            "text": "Hello! Please introduce yourself."
          }
        ]
      }
    ],
    "generationConfig": {
      "temperature": 0.7,
      "maxOutputTokens": 100,
      "responseMimeType": "text/plain"
    }
  }'
