#!/usr/bin/env python3
"""
Test updated Gemini client with preview model support.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_preview_model():
    """Test the updated Gemini client with preview model."""
    
    print("🧪 Testing Updated Gemini Client with Preview Model")
    print("=" * 60)
    
    try:
        from autogen_workflow.gemini_client import GeminiChatCompletionClient
        from autogen_core.models._types import UserMessage, SystemMessage
        
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
        
        # Test with preview model
        print("\n🔄 Testing gemini-2.5-pro-preview-05-06...")
        
        client = GeminiChatCompletionClient(
            model="gemini-2.5-pro-preview-05-06",
            api_key=api_key,
            temperature=0.7,
            max_tokens=100
        )
        
        print("✅ Client created successfully")
        
        # Test with system message and user message
        messages = [
            SystemMessage(content="You are a helpful AI assistant. Provide clear, direct responses.", source="system"),
            UserMessage(content="Hello! Please introduce yourself briefly.", source="user")
        ]
        
        print("🔄 Testing API call with system instruction...")
        result = await client.create(messages)
        
        print("✅ API call successful!")
        print(f"📝 Response: {result.content}")
        
        # Test with regular model for comparison
        print("\n🔄 Testing gemini-2.0-flash for comparison...")
        
        client2 = GeminiChatCompletionClient(
            model="gemini-2.0-flash",
            api_key=api_key,
            temperature=0.7,
            max_tokens=100
        )
        
        messages2 = [
            UserMessage(content="Hello! Please introduce yourself briefly.", source="user")
        ]
        
        result2 = await client2.create(messages2)
        
        print("✅ API call successful!")
        print(f"📝 Response: {result2.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_workflow_with_preview_model():
    """Test workflow with preview model."""
    
    print("\n🚀 Testing Workflow with Preview Model")
    print("=" * 60)
    
    try:
        from autogen_workflow.workflow import ProgrammingWorkflow
        from autogen_workflow.config import WorkflowConfig
        
        # Create config with preview model
        config = WorkflowConfig.create_default()
        config.model_config.gemini_model = "gemini-2.5-pro-preview-05-06"
        
        # Create workflow
        workflow = ProgrammingWorkflow(config)
        
        print("✅ Workflow created successfully")
        print(f"📊 Model client type: {type(workflow.model_client).__name__}")
        print(f"🔧 Model: {workflow.model_client.model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    
    print("🔬 Preview Model Integration Tests")
    print("=" * 70)
    
    # Test 1: Direct client test
    test1_result = await test_preview_model()
    
    # Test 2: Workflow integration
    test2_result = await test_workflow_with_preview_model()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Test Results:")
    print(f"  {'✅' if test1_result else '❌'} Preview Model Client Test")
    print(f"  {'✅' if test2_result else '❌'} Workflow Integration Test")
    
    if test1_result and test2_result:
        print("\n🎉 All tests passed! Preview model integration is working.")
        print("\n💡 Recommendations:")
        print("  ✅ Use gemini-2.5-pro-preview-05-06 for advanced capabilities")
        print("  ⚠️ Avoid gemini-2.5-pro-preview-06-05 (has response issues)")
        print("  🔄 Fallback to gemini-2.0-flash for stability")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
