#!/usr/bin/env python3
"""
Simple test for Gemini API connection.
"""

import os
import asyncio

async def test_gemini_api():
    """Test direct Gemini API connection."""
    
    print("🧪 Testing Direct Gemini API Connection")
    print("=" * 40)
    
    try:
        import google.generativeai as genai
        
        # Get API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ No GOOGLE_API_KEY found")
            return False
        
        print(f"✅ API key found: {api_key[:10]}...")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Create model
        model = genai.GenerativeModel('gemini-2.0-flash')
        print("✅ Model created")
        
        # Test simple generation
        print("🔄 Testing API call...")
        response = model.generate_content("Hello! Please respond with 'Hello from Gemini!' to test the connection.")
        
        print("✅ API call successful!")
        print(f"📝 Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_gemini_api())
    print(f"\n{'🎉 Success!' if success else '❌ Failed!'}")
