#!/usr/bin/env python3
"""Test AutoGen imports to find correct module structure."""

def test_imports():
    print("Testing AutoGen imports...")
    
    try:
        from autogen_agentchat.agents import AssistantAgent
        print("✅ autogen_agentchat.agents.AssistantAgent - OK")
    except ImportError as e:
        print(f"❌ autogen_agentchat.agents.AssistantAgent - {e}")
    
    try:
        from autogen_core.models import ChatCompletionClient
        print("✅ autogen_core.models.ChatCompletionClient - OK")
    except ImportError as e:
        print(f"❌ autogen_core.models.ChatCompletionClient - {e}")
    
    try:
        from autogen_agentchat.teams import Swarm
        print("✅ autogen_agentchat.teams.Swarm - OK")
    except ImportError as e:
        print(f"❌ autogen_agentchat.teams.Swarm - {e}")
    
    try:
        from autogen_agentchat.conditions import HandoffTermination
        print("✅ autogen_agentchat.conditions.HandoffTermination - OK")
    except ImportError as e:
        print(f"❌ autogen_agentchat.conditions.HandoffTermination - {e}")
    
    try:
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        print("✅ autogen_ext.models.openai.OpenAIChatCompletionClient - OK")
    except ImportError as e:
        print(f"❌ autogen_ext.models.openai.OpenAIChatCompletionClient - {e}")
    
    try:
        from autogen_ext.models.gemini import GeminiChatCompletionClient
        print("✅ autogen_ext.models.gemini.GeminiChatCompletionClient - OK")
    except ImportError as e:
        print(f"❌ autogen_ext.models.gemini.GeminiChatCompletionClient - {e}")
    
    # Try alternative imports
    print("\nTrying alternative imports...")
    
    try:
        import autogen_core
        print(f"✅ autogen_core available: {dir(autogen_core)}")
    except ImportError as e:
        print(f"❌ autogen_core - {e}")
    
    try:
        import autogen_agentchat
        print(f"✅ autogen_agentchat available")
    except ImportError as e:
        print(f"❌ autogen_agentchat - {e}")

if __name__ == "__main__":
    test_imports()
