#!/usr/bin/env python3
"""
Debug Gemini API calls.
"""

import asyncio
import os
import aiohttp
import json

async def debug_gemini_api():
    """Debug Gemini API call with detailed logging."""
    
    print("🔍 Debugging Gemini API Call")
    print("=" * 40)
    
    # Get API key from .env file directly
    api_key = None
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('GOOGLE_API_KEY='):
                    api_key = line.split('=', 1)[1].strip()
                    break

        if not api_key:
            print("❌ No GOOGLE_API_KEY found in .env file")
            return False

    except FileNotFoundError:
        print("❌ .env file not found")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Prepare request
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Hello! Please respond with 'Hello from Gemini!' to test the connection."
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 100
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    params = {
        "key": api_key
    }
    
    print(f"🌐 URL: {url}")
    print(f"📦 Payload: {json.dumps(payload, indent=2)}")
    print(f"🔑 Params: {params}")
    
    try:
        print("🔄 Making API call...")
        
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                url,
                json=payload,
                headers=headers,
                params=params
            ) as response:
                
                print(f"📊 Status: {response.status}")
                print(f"📋 Headers: {dict(response.headers)}")
                
                response_text = await response.text()
                print(f"📄 Raw response: {response_text}")
                
                if response.status == 200:
                    try:
                        result = json.loads(response_text)
                        print(f"✅ Parsed JSON: {json.dumps(result, indent=2)}")
                        
                        # Extract response text
                        if "candidates" in result and len(result["candidates"]) > 0:
                            candidate = result["candidates"][0]
                            if "content" in candidate and "parts" in candidate["content"]:
                                parts = candidate["content"]["parts"]
                                if len(parts) > 0 and "text" in parts[0]:
                                    response_text = parts[0]["text"]
                                    print(f"📝 Extracted text: {response_text}")
                                    return True
                        
                        print("⚠️ Unexpected response format")
                        return False
                        
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON decode error: {e}")
                        return False
                
                else:
                    print(f"❌ API Error {response.status}: {response_text}")
                    return False
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(debug_gemini_api())
    print(f"\n{'🎉 Success!' if success else '❌ Failed!'}")
