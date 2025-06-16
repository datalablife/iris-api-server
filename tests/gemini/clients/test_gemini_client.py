#!/usr/bin/env python3
"""
Test script for custom Gemini client integration.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_gemini_client():
    """Test our custom Gemini client."""
    
    print("🧪 Testing Custom Gemini Client")
    print("=" * 40)
    
    try:
        from autogen_workflow.gemini_client import GeminiChatCompletionClient
        from autogen_core.models import UserMessage
        
        # Check API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ No GOOGLE_API_KEY found in environment")
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
        
        print("🔄 Testing API call...")
        result = await client.create(messages)
        
        print("✅ API call successful!")
        print(f"📝 Response: {result.choices[0].message.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_workflow_with_gemini():
    """Test workflow initialization with Gemini client."""
    
    print("\n🚀 Testing Workflow with Gemini")
    print("=" * 40)
    
    try:
        from autogen_workflow.workflow import ProgrammingWorkflow
        from autogen_workflow.config import WorkflowConfig
        
        # Create workflow
        config = WorkflowConfig.create_default()
        workflow = ProgrammingWorkflow(config)
        
        print("✅ Workflow created successfully")
        print(f"📊 Model client type: {type(workflow.model_client).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    
    print("🔬 Gemini Client Integration Tests")
    print("=" * 50)
    
    # Test 1: Direct Gemini client
    test1_result = await test_gemini_client()
    
    # Test 2: Workflow integration
    test2_result = await test_workflow_with_gemini()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"  {'✅' if test1_result else '❌'} Gemini Client Test")
    print(f"  {'✅' if test2_result else '❌'} Workflow Integration Test")
    
    if test1_result and test2_result:
        print("\n🎉 All tests passed! Gemini integration is working.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
