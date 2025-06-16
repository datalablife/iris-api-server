"""
Main entry point for AutoGen Programming Workflow

This module provides the main interface for running the multi-agent
programming workflow with command-line interface and example usage.
"""

import asyncio
import argparse
import json
import logging
import os
import sys
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

# Add the parent directory to the path for imports
sys.path.append(str(Path(__file__).parent.parent))

from autogen_workflow.workflow import ProgrammingWorkflow
from autogen_workflow.config import WorkflowConfig, ModelConfig


def setup_logging(log_level: str = "INFO") -> None:
    """Setup logging configuration."""
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('workflow.log')
        ]
    )


def load_config_from_file(config_path: str) -> Optional[WorkflowConfig]:
    """Load configuration from JSON file."""
    
    try:
        with open(config_path, 'r') as f:
            config_data = json.load(f)
        
        # Create model config
        model_config = ModelConfig(
            gemini_api_key=config_data.get("gemini_api_key"),
            gemini_model=config_data.get("gemini_model", "gemini-2.0-flash"),
            openai_api_key=config_data.get("openai_api_key"),
            openai_model=config_data.get("openai_model", "gpt-4o-mini"),
            temperature=config_data.get("temperature", 0.7),
            max_tokens=config_data.get("max_tokens", 4000)
        )
        
        # Create workflow config
        workflow_config = WorkflowConfig(model_config=model_config)
        workflow_config.max_rounds = config_data.get("max_rounds", 20)
        workflow_config.max_messages = config_data.get("max_messages", 50)
        workflow_config.timeout_seconds = config_data.get("timeout_seconds", 300)
        
        return workflow_config
        
    except Exception as e:
        logging.error(f"Failed to load config from {config_path}: {str(e)}")
        return None


def create_sample_config() -> Dict[str, Any]:
    """Create a sample configuration file."""
    
    return {
        "gemini_api_key": "your_gemini_api_key_here",
        "gemini_model": "gemini-2.0-flash",
        "openai_api_key": "your_openai_api_key_here", 
        "openai_model": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 4000,
        "max_rounds": 20,
        "max_messages": 50,
        "timeout_seconds": 300
    }


async def run_example_workflow() -> None:
    """Run an example programming workflow."""
    
    print("🚀 Starting AutoGen Programming Workflow Example")
    print("=" * 60)
    
    # Create workflow configuration
    config = WorkflowConfig.create_default()
    
    # Create workflow instance
    workflow = ProgrammingWorkflow(config)
    
    # Define example task
    task = """
Create a FastAPI-based data analysis API server with the following requirements:

1. **Core Features**:
   - File upload endpoint for CSV/Excel files
   - Data validation and preprocessing
   - Basic statistical analysis (mean, median, std, correlations)
   - Simple data visualization (charts)
   - Async processing for large files

2. **Technical Requirements**:
   - Use FastAPI framework with async/await
   - PostgreSQL database for metadata storage
   - Redis for caching and task queue
   - Proper error handling and logging
   - JWT authentication
   - API documentation with OpenAPI

3. **Quality Requirements**:
   - Clean, maintainable code with type hints
   - Comprehensive error handling
   - Unit tests with >80% coverage
   - Security best practices
   - Performance optimization for large datasets

4. **Deployment**:
   - Docker containerization
   - docker-compose for development
   - Environment-based configuration
   - Health check endpoints

Please design the architecture, create implementation plan, write the code,
review it for quality and security, and optimize for performance.
"""
    
    # Additional context
    context = {
        "project_type": "data_api",
        "target_environment": "production",
        "expected_load": "1000+ requests/hour",
        "team_size": "5 developers",
        "timeline": "12-16 weeks"
    }
    
    try:
        # Run the workflow
        print("🏗️  Initializing agents and workflow...")
        result = await workflow.run_workflow(task, context)
        
        if result["status"] == "success":
            print("\n✅ Workflow completed successfully!")
            print("=" * 60)
            
            # Display summary
            summary = result["result"]["summary"]
            print(f"📊 Workflow Summary:")
            print(f"   Duration: {summary.get('duration_seconds', 0):.1f} seconds")
            print(f"   Messages: {summary.get('total_messages', 0)}")
            print(f"   Artifacts: {summary.get('artifacts_generated', {})}")
            
            # Save artifacts
            await save_workflow_artifacts(result)
            
        else:
            print(f"\n❌ Workflow failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        logging.error(f"Workflow execution failed: {str(e)}", exc_info=True)


async def save_workflow_artifacts(result: Dict[str, Any]) -> None:
    """Save workflow artifacts to files."""
    
    artifacts = result.get("artifacts", {})
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"workflow_output_{timestamp}")
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n💾 Saving artifacts to: {output_dir}")
    
    # Save architecture design
    if artifacts.get("architecture_design"):
        with open(output_dir / "architecture_design.md", "w") as f:
            f.write(artifacts["architecture_design"])
        print("   ✓ Architecture design saved")
    
    # Save implementation plan
    if artifacts.get("implementation_plan"):
        with open(output_dir / "implementation_plan.md", "w") as f:
            f.write(artifacts["implementation_plan"])
        print("   ✓ Implementation plan saved")
    
    # Save source code files
    source_code = artifacts.get("source_code", [])
    if source_code:
        code_dir = output_dir / "source_code"
        code_dir.mkdir(exist_ok=True)
        
        for i, code_artifact in enumerate(source_code):
            with open(code_dir / f"code_file_{i+1}.py", "w") as f:
                f.write(code_artifact["content"])
        print(f"   ✓ {len(source_code)} source code files saved")
    
    # Save review reports
    reviews = artifacts.get("review_reports", [])
    if reviews:
        review_dir = output_dir / "reviews"
        review_dir.mkdir(exist_ok=True)
        
        for i, review in enumerate(reviews):
            with open(review_dir / f"review_report_{i+1}.md", "w") as f:
                f.write(review["content"])
        print(f"   ✓ {len(reviews)} review reports saved")
    
    # Save optimizations
    optimizations = artifacts.get("optimizations", [])
    if optimizations:
        opt_dir = output_dir / "optimizations"
        opt_dir.mkdir(exist_ok=True)
        
        for i, opt in enumerate(optimizations):
            with open(opt_dir / f"optimization_{i+1}.md", "w") as f:
                f.write(opt["content"])
        print(f"   ✓ {len(optimizations)} optimization reports saved")
    
    # Save complete workflow result
    with open(output_dir / "workflow_result.json", "w") as f:
        json.dump(result, f, indent=2, default=str)
    print("   ✓ Complete workflow result saved")


async def run_interactive_workflow() -> None:
    """Run interactive workflow with user input."""
    
    print("🤖 AutoGen Programming Workflow - Interactive Mode")
    print("=" * 60)
    
    # Get task from user
    print("\nPlease describe your programming task:")
    task = input("> ")
    
    if not task.strip():
        print("❌ No task provided. Exiting.")
        return
    
    # Optional context
    print("\nOptional: Provide additional context (press Enter to skip):")
    context_input = input("> ")
    context = {"user_context": context_input} if context_input.strip() else None
    
    # Create and run workflow
    config = WorkflowConfig.create_default()
    workflow = ProgrammingWorkflow(config)
    
    print(f"\n🚀 Starting workflow for task: {task[:100]}...")
    
    try:
        result = await workflow.run_workflow(task, context)
        
        if result["status"] == "success":
            print("\n✅ Workflow completed successfully!")
            await save_workflow_artifacts(result)
        else:
            print(f"\n❌ Workflow failed: {result.get('error')}")
            
    except KeyboardInterrupt:
        print("\n⏹️  Workflow interrupted by user")
    except Exception as e:
        print(f"\n💥 Error: {str(e)}")


def main():
    """Main entry point with command-line interface."""
    
    parser = argparse.ArgumentParser(
        description="AutoGen Programming Workflow - Multi-Agent Development System"
    )
    
    parser.add_argument(
        "--mode",
        choices=["example", "interactive", "config"],
        default="example",
        help="Workflow mode (default: example)"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    parser.add_argument(
        "--create-config",
        action="store_true",
        help="Create sample configuration file"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    
    # Create sample config if requested
    if args.create_config:
        config_data = create_sample_config()
        with open("workflow_config.json", "w") as f:
            json.dump(config_data, f, indent=2)
        print("✅ Sample configuration file created: workflow_config.json")
        print("Please edit the file with your API keys and preferences.")
        return
    
    # Check for API keys
    if not (os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")):
        print("⚠️  Warning: No API keys found in environment variables.")
        print("Please set GOOGLE_API_KEY or OPENAI_API_KEY, or use --create-config to create a config file.")
    
    # Run workflow based on mode
    try:
        if args.mode == "example":
            asyncio.run(run_example_workflow())
        elif args.mode == "interactive":
            asyncio.run(run_interactive_workflow())
        elif args.mode == "config":
            if args.config and os.path.exists(args.config):
                print(f"Loading configuration from: {args.config}")
                # Load and validate config
                config = load_config_from_file(args.config)
                if config:
                    print("✅ Configuration loaded successfully")
                else:
                    print("❌ Failed to load configuration")
            else:
                print("❌ Configuration file not found or not specified")
                
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        logging.error(f"Application error: {str(e)}", exc_info=True)
        print(f"💥 Application error: {str(e)}")


if __name__ == "__main__":
    main()
