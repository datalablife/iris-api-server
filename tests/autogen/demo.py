#!/usr/bin/env python3
"""
AutoGen Programming Workflow Demo

This script demonstrates the multi-agent programming workflow
with a simple example task.
"""

import asyncio
import os
import sys
import logging
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from autogen_workflow.workflow import ProgrammingWorkflow
from autogen_workflow.config import WorkflowConfig, ModelConfig


async def demo_simple_task():
    """Demonstrate the workflow with a simple programming task."""
    
    print("🚀 AutoGen Programming Workflow Demo")
    print("=" * 50)
    
    # Check for API keys
    gemini_key = os.getenv("GOOGLE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not gemini_key and not openai_key:
        print("❌ Error: No API keys found!")
        print("Please set one of the following environment variables:")
        print("  - GOOGLE_API_KEY (for Gemini)")
        print("  - OPENAI_API_KEY (for OpenAI)")
        print("\nExample:")
        print("  export GOOGLE_API_KEY='your_api_key_here'")
        return
    
    # Create configuration
    model_config = ModelConfig(
        gemini_api_key=gemini_key,
        gemini_model="gemini-2.0-flash",
        openai_api_key=openai_key,
        openai_model="gpt-4o-mini",
        temperature=0.7,
        max_tokens=2000  # Reduced for demo
    )
    
    config = WorkflowConfig(model_config=model_config)
    config.max_messages = 20  # Reduced for demo
    config.max_rounds = 10    # Reduced for demo
    
    # Create workflow
    workflow = ProgrammingWorkflow(config)
    
    # Define a simple task
    task = """
Create a simple Python FastAPI application with the following features:

1. A health check endpoint that returns {"status": "healthy"}
2. A POST endpoint /calculate that accepts two numbers and returns their sum
3. Basic error handling for invalid inputs
4. Proper HTTP status codes
5. Simple logging

Requirements:
- Use FastAPI framework
- Include type hints
- Add basic input validation
- Include a simple test

This is a demo task, so keep the implementation simple and focused.
"""
    
    context = {
        "demo_mode": True,
        "complexity": "simple",
        "focus": "basic_functionality"
    }
    
    print(f"📋 Task: {task[:100]}...")
    print(f"🔧 Using model: {model_config.gemini_model if gemini_key else model_config.openai_model}")
    print("\n🏃 Starting workflow...\n")
    
    try:
        # Run the workflow
        result = await workflow.run_workflow(task, context)
        
        if result["status"] == "success":
            print("\n✅ Demo completed successfully!")
            print("=" * 50)
            
            # Show summary
            summary = result["result"]["summary"]
            print(f"📊 Summary:")
            print(f"   Duration: {summary.get('duration_seconds', 0):.1f} seconds")
            print(f"   Messages: {summary.get('total_messages', 0)}")
            
            # Show artifacts
            artifacts = result.get("artifacts", {})
            print(f"\n📁 Generated artifacts:")
            
            if artifacts.get("architecture_design"):
                print("   ✓ Architecture design")
            
            if artifacts.get("implementation_plan"):
                print("   ✓ Implementation plan")
            
            source_code = artifacts.get("source_code", [])
            if source_code:
                print(f"   ✓ {len(source_code)} source code files")
            
            reviews = artifacts.get("review_reports", [])
            if reviews:
                print(f"   ✓ {len(reviews)} code review reports")
            
            optimizations = artifacts.get("optimizations", [])
            if optimizations:
                print(f"   ✓ {len(optimizations)} optimization reports")
            
            # Save demo results
            await save_demo_results(result)
            
        else:
            print(f"\n❌ Demo failed: {result.get('error', 'Unknown error')}")
            
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n💥 Demo error: {str(e)}")
        logging.error(f"Demo failed: {str(e)}", exc_info=True)


async def save_demo_results(result):
    """Save demo results to a simple output file."""
    
    output_file = Path("demo_output.txt")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("AutoGen Programming Workflow Demo Results\n")
        f.write("=" * 50 + "\n\n")
        
        # Write summary
        summary = result["result"]["summary"]
        f.write(f"Duration: {summary.get('duration_seconds', 0):.1f} seconds\n")
        f.write(f"Messages: {summary.get('total_messages', 0)}\n\n")
        
        # Write artifacts
        artifacts = result.get("artifacts", {})
        
        if artifacts.get("architecture_design"):
            f.write("ARCHITECTURE DESIGN:\n")
            f.write("-" * 20 + "\n")
            f.write(artifacts["architecture_design"][:500] + "...\n\n")
        
        if artifacts.get("implementation_plan"):
            f.write("IMPLEMENTATION PLAN:\n")
            f.write("-" * 20 + "\n")
            f.write(artifacts["implementation_plan"][:500] + "...\n\n")
        
        source_code = artifacts.get("source_code", [])
        if source_code:
            f.write("SOURCE CODE:\n")
            f.write("-" * 20 + "\n")
            for i, code in enumerate(source_code[:2]):  # Show first 2 files
                f.write(f"File {i+1}:\n")
                f.write(code["content"][:500] + "...\n\n")
    
    print(f"📄 Demo results saved to: {output_file}")


def setup_demo_logging():
    """Setup logging for demo."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('demo.log')
        ]
    )


def main():
    """Main demo function."""
    
    # Setup logging
    setup_demo_logging()
    
    print("🎯 AutoGen Programming Workflow Demo")
    print("This demo will run a simple programming task through the multi-agent workflow.")
    print("\nPress Ctrl+C at any time to stop the demo.\n")
    
    try:
        # Run the demo
        asyncio.run(demo_simple_task())
        
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user. Goodbye!")
    except Exception as e:
        print(f"\n💥 Demo failed: {str(e)}")
        logging.error(f"Demo failed: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()
