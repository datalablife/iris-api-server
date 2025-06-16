#!/usr/bin/env python3
"""
Test model_info property fix.
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_model_info():
    """Test model_info property."""
    
    print("🧪 Testing model_info Property")
    print("=" * 40)
    
    try:
        from autogen_workflow.gemini_client import GeminiChatCompletionClient
        
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
        
        # Create client
        client = GeminiChatCompletionClient(
            model="gemini-2.5-pro-preview-05-06",
            api_key=api_key,
            temperature=0.7,
            max_tokens=100
        )
        
        print("✅ Client created successfully")
        
        # Test model_info property
        print("🔄 Testing model_info property...")
        model_info = client.model_info
        
        print("✅ model_info accessed successfully!")
        print(f"📊 Model info: {model_info}")
        
        # Check required fields
        required_fields = ["function_calling", "vision", "json_output"]
        for field in required_fields:
            if field in model_info:
                print(f"  ✅ {field}: {model_info[field]}")
            else:
                print(f"  ❌ Missing field: {field}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_workflow_creation():
    """Test workflow creation with fixed client."""
    
    print("\n🚀 Testing Workflow Creation")
    print("=" * 40)
    
    try:
        from autogen_workflow.workflow import ProgrammingWorkflow
        from autogen_workflow.config import WorkflowConfig
        
        # Create config with preview model
        config = WorkflowConfig.create_default()
        config.model_config.gemini_model = "gemini-2.5-pro-preview-05-06"
        
        print("✅ Config created")
        
        # Create workflow
        print("🔄 Creating workflow...")
        workflow = ProgrammingWorkflow(config)
        
        print("✅ Workflow created successfully!")
        print(f"📊 Model client type: {type(workflow.model_client).__name__}")
        print(f"🔧 Model: {workflow.model_client.model}")
        print(f"📋 Model info: {workflow.model_client.model_info}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    
    print("🔬 Model Info Property Tests")
    print("=" * 50)
    
    # Test 1: Model info property
    test1_result = test_model_info()
    
    # Test 2: Workflow creation
    test2_result = test_workflow_creation()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"  {'✅' if test1_result else '❌'} Model Info Property Test")
    print(f"  {'✅' if test2_result else '❌'} Workflow Creation Test")
    
    if test1_result and test2_result:
        print("\n🎉 All tests passed! Model info property is fixed.")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
