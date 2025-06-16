#!/usr/bin/env python3
"""
Test specific Gemini models to check availability.
"""

import asyncio
import aiohttp
import json
import os

async def test_gemini_model(model_name, api_key):
    """Test a specific Gemini model."""
    
    print(f"\n🧪 Testing model: {model_name}")
    print("-" * 50)
    
    # Prepare request
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
    
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Hello! Please respond with 'Hello from {model_name}!' to test the connection."
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
        print(f"🌐 URL: {url}")
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
                
                response_text = await response.text()
                
                if response.status == 200:
                    try:
                        result = json.loads(response_text)
                        
                        # Extract response text
                        if "candidates" in result and len(result["candidates"]) > 0:
                            candidate = result["candidates"][0]
                            if "content" in candidate and "parts" in candidate["content"]:
                                parts = candidate["content"]["parts"]
                                if len(parts) > 0 and "text" in parts[0]:
                                    response_content = parts[0]["text"]
                                    print(f"✅ SUCCESS!")
                                    print(f"📝 Response: {response_content}")
                                    return True
                        
                        print("⚠️ Unexpected response format")
                        print(f"📄 Full response: {json.dumps(result, indent=2)}")
                        return False
                        
                    except json.JSONDecodeError as e:
                        print(f"❌ JSON decode error: {e}")
                        print(f"📄 Raw response: {response_text}")
                        return False
                
                else:
                    print(f"❌ API Error {response.status}")
                    print(f"📄 Error response: {response_text}")
                    
                    # Try to parse error details
                    try:
                        error_data = json.loads(response_text)
                        if "error" in error_data:
                            error_info = error_data["error"]
                            print(f"🔍 Error details:")
                            print(f"   Code: {error_info.get('code', 'N/A')}")
                            print(f"   Message: {error_info.get('message', 'N/A')}")
                            print(f"   Status: {error_info.get('status', 'N/A')}")
                    except:
                        pass
                    
                    return False
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False


async def test_model_list(api_key):
    """Test listing available models."""
    
    print(f"\n📋 Testing model list API")
    print("-" * 50)
    
    url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    params = {
        "key": api_key
    }
    
    try:
        print("🔄 Fetching available models...")
        
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(
                url,
                params=params
            ) as response:
                
                print(f"📊 Status: {response.status}")
                
                if response.status == 200:
                    result = await response.json()
                    
                    if "models" in result:
                        models = result["models"]
                        print(f"✅ Found {len(models)} models:")
                        
                        gemini_models = []
                        for model in models:
                            model_name = model.get("name", "")
                            display_name = model.get("displayName", "")
                            
                            if "gemini" in model_name.lower():
                                gemini_models.append({
                                    "name": model_name,
                                    "display_name": display_name,
                                    "supported_methods": model.get("supportedGenerationMethods", [])
                                })
                        
                        print(f"\n🔍 Gemini models found ({len(gemini_models)}):")
                        for model in gemini_models:
                            print(f"   📦 {model['name']}")
                            print(f"      Display: {model['display_name']}")
                            print(f"      Methods: {model['supported_methods']}")
                            print()
                        
                        return gemini_models
                    
                else:
                    error_text = await response.text()
                    print(f"❌ Error {response.status}: {error_text}")
                    return []
    
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return []


async def main():
    """Run all model tests."""
    
    print("🔬 Gemini Model Availability Tests")
    print("=" * 60)
    
    # Get API key
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
    
    # Test models to check
    models_to_test = [
        "gemini-2.5-pro-preview-05-06",
        "gemini-2.5-pro-preview-06-05",
        "gemini-2.0-flash",  # Known working model for comparison
        "gemini-1.5-pro"     # Another common model
    ]
    
    # First, get list of available models
    available_models = await test_model_list(api_key)
    
    # Test each model
    results = {}
    for model in models_to_test:
        results[model] = await test_gemini_model(model, api_key)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary:")
    print("=" * 60)
    
    for model, success in results.items():
        status = "✅ AVAILABLE" if success else "❌ NOT AVAILABLE"
        print(f"  {model:<35} {status}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    working_models = [model for model, success in results.items() if success]
    if working_models:
        print(f"✅ Use these models: {', '.join(working_models)}")
    else:
        print("❌ No models are currently working. Check API key and network connection.")
    
    return len(working_models) > 0


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
