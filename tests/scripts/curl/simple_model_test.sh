#!/bin/bash

API_KEY="AIzaSyBvfAGPPtwtX2eCH2_OG1tkLGirfwfvyWk"

echo "Testing gemini-2.5-pro-preview-05-06..."
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-05-06:generateContent?key=${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}],"generationConfig":{"maxOutputTokens":10}}' \
  --connect-timeout 10 --max-time 30

echo -e "\n\nTesting gemini-2.5-pro-preview-06-05..."
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro-preview-06-05:generateContent?key=${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}],"generationConfig":{"maxOutputTokens":10}}' \
  --connect-timeout 10 --max-time 30

echo -e "\n\nTesting gemini-2.0-flash (known working)..."
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}],"generationConfig":{"maxOutputTokens":10}}' \
  --connect-timeout 10 --max-time 30
