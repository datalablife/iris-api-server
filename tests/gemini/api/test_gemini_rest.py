#!/usr/bin/env python3
"""
Test Gemini REST API implementation.
"""

import asyncio
import os
import aiohttp
import json

async def test_gemini_rest_api():
    """Test direct Gemini REST API call."""
    
    print("🧪 Testing Gemini REST API")
    print("=" * 40)
    
    # Get API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ No GOOGLE_API_KEY found")
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
    
    try:
        print("🔄 Making API call...")
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                json=payload,
                headers=headers,
                params=params
            ) as response:
                
                print(f"📊 Status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    print("✅ API call successful!")
                    
                    # Extract response text
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            parts = candidate["content"]["parts"]
                            if len(parts) > 0 and "text" in parts[0]:
                                response_text = parts[0]["text"]
                                print(f"📝 Response: {response_text}")
                                return True
                    
                    print("⚠️ Unexpected response format")
                    print(f"📄 Full response: {json.dumps(result, indent=2)}")
                    return False
                
                else:
                    error_text = await response.text()
                    print(f"❌ API Error {response.status}: {error_text}")
                    return False
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_custom_gemini_client():
    """Test our custom Gemini client."""
    
    print("\n🚀 Testing Custom Gemini Client")
    print("=" * 40)
    
    try:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from autogen_workflow.gemini_client import GeminiChatCompletionClient
        from autogen_core.models._types import UserMessage
        
        # Get API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ No GOOGLE_API_KEY found")
            return False
        
        print(f"✅ API key found: {api_key[:10]}...")
        
        # Create client
        client = GeminiChatCompletionClient(
            model="gemini-2.0-flash",
            api_key=api_key,
            temperature=0.7,
            max_tokens=100
        )
        
        print("✅ Gemini client created successfully")
        
        # Test simple message
        messages = [
            UserMessage(content="Hello! Please respond with 'Hello from Gemini!' to test the connection.", source="user")
        ]
        
        print("🔄 Testing client API call...")
        result = await client.create(messages)
        
        print("✅ Client API call successful!")
        print(f"📝 Response: {result.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    
    print("🔬 Gemini REST API Tests")
    print("=" * 50)
    
    # Test 1: Direct REST API
    test1_result = await test_gemini_rest_api()
    
    # Test 2: Custom client
    test2_result = await test_custom_gemini_client()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"  {'✅' if test1_result else '❌'} Direct REST API Test")
    print(f"  {'✅' if test2_result else '❌'} Custom Client Test")
    
    if test1_result and test2_result:
        print("\n🎉 All tests passed! Gemini REST API integration is working.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
