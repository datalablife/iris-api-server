#!/usr/bin/env python3
"""
Installation Test Script for AutoGen Programming Workflow

This script tests if all dependencies are properly installed
and the workflow can be initialized.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported."""
    
    print("🔍 Testing imports...")
    
    try:
        # Test core Python modules
        import asyncio
        import logging
        import json
        print("  ✓ Core Python modules")
        
        # Test AutoGen modules
        from autogen_agentchat.agents import AssistantAgent
        from autogen_agentchat.teams import Swarm
        from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        print("  ✓ AutoGen modules")
        
        # Test Google Gemini (optional)
        try:
            import google.generativeai as genai
            print("  ✓ Google Gemini support available")
        except ImportError:
            print("  ⚠️ Google Gemini support not available (optional)")
        
        # Test our workflow modules
        from autogen_workflow.config import WorkflowConfig, ModelConfig
        from autogen_workflow.workflow import ProgrammingWorkflow
        print("  ✓ Workflow modules")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False


def test_configuration():
    """Test configuration creation."""
    
    print("\n🔧 Testing configuration...")
    
    try:
        from autogen_workflow.config import WorkflowConfig, ModelConfig
        
        # Test model config creation
        model_config = ModelConfig()
        print("  ✓ Model configuration created")
        
        # Test workflow config creation
        workflow_config = WorkflowConfig.create_default()
        print("  ✓ Workflow configuration created")
        
        # Test config validation (should fail without API keys)
        try:
            workflow_config.validate()
            print("  ⚠️ Configuration validation passed (API keys found)")
        except ValueError as e:
            print("  ✓ Configuration validation working (no API keys)")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False


def test_workflow_initialization():
    """Test workflow initialization without API keys."""
    
    print("\n🚀 Testing workflow initialization...")
    
    try:
        from autogen_workflow.config import WorkflowConfig, ModelConfig
        from autogen_workflow.workflow import ProgrammingWorkflow
        
        # Create config with dummy API key for testing
        model_config = ModelConfig(
            openai_api_key="dummy_key_for_testing",
            openai_model="gpt-4o-mini"
        )
        
        workflow_config = WorkflowConfig(model_config=model_config)
        
        # This should work without actually calling the API
        print("  ✓ Workflow configuration created")
        
        # Test agent config retrieval
        architect_config = workflow_config.get_agent_config("architect")
        if architect_config:
            print("  ✓ Agent configurations accessible")
        else:
            print("  ❌ Agent configurations not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ Workflow initialization error: {e}")
        return False


def check_api_keys():
    """Check for API keys in environment."""
    
    print("\n🔑 Checking API keys...")
    
    gemini_key = os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if gemini_key:
        print("  ✓ Google Gemini API key found")
    else:
        print("  ⚠️ Google Gemini API key not found")
    
    if openai_key:
        print("  ✓ OpenAI API key found")
    else:
        print("  ⚠️ OpenAI API key not found")
    
    if not gemini_key and not openai_key:
        print("  ❌ No API keys found!")
        print("     Set GOOGLE_API_KEY or OPENAI_API_KEY environment variable")
        print("     Or copy .env.example to .env and add your keys")
        return False
    
    return True


def check_file_structure():
    """Check if all required files are present."""
    
    print("\n📁 Checking file structure...")
    
    required_files = [
        "autogen_workflow/__init__.py",
        "autogen_workflow/config.py",
        "autogen_workflow/workflow.py",
        "autogen_workflow/main.py",
        "autogen_workflow/agents/__init__.py",
        "autogen_workflow/agents/architect.py",
        "autogen_workflow/agents/project_manager.py",
        "autogen_workflow/agents/programmer.py",
        "autogen_workflow/agents/code_reviewer.py",
        "autogen_workflow/agents/code_optimizer.py",
        "requirements.txt",
        "README.md"
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        return False
    
    return True


def main():
    """Run all installation tests."""
    
    print("🧪 AutoGen Programming Workflow - Installation Test")
    print("=" * 60)
    
    tests = [
        ("File Structure", check_file_structure),
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("Workflow Initialization", test_workflow_initialization),
        ("API Keys", check_api_keys)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  💥 {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Installation is ready.")
        print("\nNext steps:")
        print("1. Set your API keys (GOOGLE_API_KEY or OPENAI_API_KEY)")
        print("2. Run the demo: python demo.py")
        print("3. Or run the main workflow: python autogen_workflow/main.py")
    else:
        print("\n⚠️ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Check Python version (requires 3.9+)")
        print("3. Verify all files are present")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
