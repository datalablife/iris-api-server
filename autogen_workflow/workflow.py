"""
Programming Workflow using AutoGen Framework

This module implements a comprehensive multi-agent programming workflow
with 5 specialized agents for collaborative software development.
"""

import asyncio
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime

# AutoGen imports
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import Swarm
from autogen_agentchat.conditions import HandoffTermination, TextMentionTermination, MaxMessageTermination
from autogen_agentchat.messages import HandoffMessage
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Google Gemini support (preferred by user)
try:
    # Try real Gemini client first (now with preview model support)
    from .gemini_client import GeminiChatCompletionClient
    GEMINI_CLIENT_AVAILABLE = True
    GEMINI_MOCK_MODE = False
except ImportError:
    try:
        # Fallback to mock client for testing
        from .mock_gemini_client import MockGeminiChatCompletionClient as GeminiChatCompletionClient
        GEMINI_CLIENT_AVAILABLE = True
        GEMINI_MOCK_MODE = True
    except ImportError:
        GEMINI_CLIENT_AVAILABLE = False
        GEMINI_MOCK_MODE = False

from .config import WorkflowConfig, ModelConfig
from .agents import (
    ArchitectAgent,
    ProjectManagerAgent,
    ProgrammerAgent,
    CodeReviewerAgent,
    CodeOptimizerAgent
)


class ProgrammingWorkflow:
    """
    Main programming workflow orchestrator using AutoGen framework.
    
    This class manages the entire multi-agent programming workflow,
    coordinating between 5 specialized agents for collaborative development.
    """
    
    def __init__(self, config: Optional[WorkflowConfig] = None):
        """
        Initialize the programming workflow.
        
        Args:
            config: Workflow configuration, uses default if None
        """
        self.config = config or WorkflowConfig.create_default()
        self.config.validate()
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize model client
        self.model_client = self._create_model_client()
        
        # Initialize agents
        self.agents = self._create_agents()
        
        # Create workflow team
        self.team = self._create_team()
        
        # Workflow state
        self.workflow_state = {
            "current_phase": "initialization",
            "start_time": None,
            "end_time": None,
            "messages": [],
            "artifacts": {},
            "status": "ready"
        }
    
    def _create_model_client(self):
        """Create appropriate model client based on configuration."""

        # Prefer Gemini if available and configured (user preference)
        if (GEMINI_CLIENT_AVAILABLE and
            self.config.model_config.gemini_api_key and
            self.config.model_config.gemini_model):

            mode_info = " (Mock Mode)" if GEMINI_MOCK_MODE else " (Real API)"
            self.logger.info(f"Using Google Gemini model: {self.config.model_config.gemini_model}{mode_info}")

            return GeminiChatCompletionClient(
                model=self.config.model_config.gemini_model,
                api_key=self.config.model_config.gemini_api_key,
                temperature=self.config.model_config.temperature,
                max_tokens=self.config.model_config.max_tokens
            )

        # Fallback to OpenAI only if API key is provided and valid
        elif (self.config.model_config.openai_api_key and
              self.config.model_config.openai_api_key != "your_openai_api_key_here"):

            self.logger.info(f"Using OpenAI model: {self.config.model_config.openai_model}")

            return OpenAIChatCompletionClient(
                model=self.config.model_config.openai_model,
                api_key=self.config.model_config.openai_api_key,
                temperature=self.config.model_config.temperature,
                max_tokens=self.config.model_config.max_tokens
            )

        else:
            available_keys = []
            if self.config.model_config.gemini_api_key:
                available_keys.append("Gemini")
            if (self.config.model_config.openai_api_key and
                self.config.model_config.openai_api_key != "your_openai_api_key_here"):
                available_keys.append("OpenAI")

            if not available_keys:
                raise ValueError("No valid API key found. Please configure GOOGLE_API_KEY or OPENAI_API_KEY")
            else:
                raise ValueError(f"Available API keys: {available_keys}, but client creation failed. Check GEMINI_CLIENT_AVAILABLE={GEMINI_CLIENT_AVAILABLE}")
    
    def _create_agents(self) -> Dict[str, Any]:
        """Create all agents for the workflow."""
        
        agents = {}
        
        # Create Architect Agent
        architect_config = self.config.get_agent_config("architect")
        agents["architect"] = ArchitectAgent(
            model_client=self.model_client,
            config=architect_config.__dict__
        )
        
        # Create Project Manager Agent
        pm_config = self.config.get_agent_config("project_manager")
        agents["project_manager"] = ProjectManagerAgent(
            model_client=self.model_client,
            config=pm_config.__dict__
        )
        
        # Create Programmer Agent
        programmer_config = self.config.get_agent_config("programmer")
        agents["programmer"] = ProgrammerAgent(
            model_client=self.model_client,
            config=programmer_config.__dict__
        )
        
        # Create Code Reviewer Agent
        reviewer_config = self.config.get_agent_config("code_reviewer")
        agents["code_reviewer"] = CodeReviewerAgent(
            model_client=self.model_client,
            config=reviewer_config.__dict__
        )
        
        # Create Code Optimizer Agent
        optimizer_config = self.config.get_agent_config("code_optimizer")
        agents["code_optimizer"] = CodeOptimizerAgent(
            model_client=self.model_client,
            config=optimizer_config.__dict__
        )
        
        self.logger.info("All agents created successfully")
        return agents
    
    def _create_team(self) -> Swarm:
        """Create the agent team using Swarm pattern."""
        
        # Extract AutoGen agents
        autogen_agents = [agent.get_agent() for agent in self.agents.values()]
        
        # Define termination conditions
        handoff_termination = HandoffTermination(target="user")
        text_termination = TextMentionTermination("TERMINATE")
        max_messages_termination = MaxMessageTermination(max_messages=self.config.max_messages)
        
        # Combine termination conditions
        termination_condition = handoff_termination | text_termination | max_messages_termination
        
        # Create Swarm team
        team = Swarm(
            participants=autogen_agents,
            termination_condition=termination_condition
        )
        
        self.logger.info("Agent team created successfully")
        return team
    
    async def run_workflow(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the complete programming workflow.
        
        Args:
            task: The programming task description
            context: Additional context for the task
            
        Returns:
            Workflow results with all artifacts and messages
        """
        
        self.logger.info(f"Starting programming workflow for task: {task}")
        
        # Update workflow state
        self.workflow_state.update({
            "status": "running",
            "start_time": datetime.now(),
            "current_phase": "architecture_design"
        })
        
        try:
            # Prepare initial task with context
            initial_task = self._prepare_initial_task(task, context)
            
            # Run the workflow
            result = await self._execute_workflow(initial_task)
            
            # Update final state
            self.workflow_state.update({
                "status": "completed",
                "end_time": datetime.now(),
                "current_phase": "completed"
            })
            
            self.logger.info("Programming workflow completed successfully")
            
            return {
                "status": "success",
                "result": result,
                "workflow_state": self.workflow_state,
                "artifacts": self.workflow_state["artifacts"]
            }
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {str(e)}", exc_info=True)
            
            self.workflow_state.update({
                "status": "failed",
                "end_time": datetime.now(),
                "error": str(e)
            })
            
            return {
                "status": "error",
                "error": str(e),
                "workflow_state": self.workflow_state
            }
        
        finally:
            # Cleanup
            await self.cleanup()
    
    def _prepare_initial_task(self, task: str, context: Optional[Dict[str, Any]]) -> str:
        """Prepare the initial task with context and instructions."""
        
        task_template = f"""
# Programming Task

## Task Description
{task}

## Context
{context or "No additional context provided"}

## Workflow Instructions
This task will be processed through our multi-agent programming workflow:

1. **Architect**: Will design the system architecture and technical approach
2. **Project Manager**: Will create implementation plan and coordinate development
3. **Programmer**: Will implement the code based on architecture and plan
4. **Code Reviewer**: Will review code quality, security, and best practices
5. **Code Optimizer**: Will optimize code for performance and maintainability

## Expected Deliverables
- System architecture design
- Implementation plan with milestones
- Complete, working code implementation
- Code review report with quality assessment
- Optimized code with performance improvements
- Comprehensive documentation

Please start with the architecture design phase.
"""
        
        return task_template
    
    async def _execute_workflow(self, task: str) -> Dict[str, Any]:
        """Execute the main workflow logic."""
        
        # Run the team workflow
        task_result = await Console(self.team.run_stream(task=task))
        
        # Store messages and extract artifacts
        self.workflow_state["messages"] = task_result.messages
        self._extract_artifacts(task_result.messages)
        
        return {
            "messages": task_result.messages,
            "artifacts": self.workflow_state["artifacts"],
            "summary": self._generate_workflow_summary()
        }
    
    def _extract_artifacts(self, messages: List[Any]) -> None:
        """Extract code artifacts and deliverables from messages."""
        
        artifacts = {
            "architecture_design": None,
            "implementation_plan": None,
            "source_code": [],
            "review_reports": [],
            "optimizations": [],
            "documentation": []
        }
        
        for message in messages:
            content = getattr(message, 'content', '')
            source = getattr(message, 'source', '')
            
            # Extract artifacts based on source agent
            if source == "architect":
                if "architecture" in content.lower() or "design" in content.lower():
                    artifacts["architecture_design"] = content
            
            elif source == "project_manager":
                if "plan" in content.lower() or "milestone" in content.lower():
                    artifacts["implementation_plan"] = content
            
            elif source == "programmer":
                if "```" in content:  # Code blocks
                    artifacts["source_code"].append({
                        "timestamp": datetime.now(),
                        "content": content
                    })
            
            elif source == "code_reviewer":
                if "review" in content.lower() or "quality" in content.lower():
                    artifacts["review_reports"].append({
                        "timestamp": datetime.now(),
                        "content": content
                    })
            
            elif source == "code_optimizer":
                if "optimization" in content.lower() or "performance" in content.lower():
                    artifacts["optimizations"].append({
                        "timestamp": datetime.now(),
                        "content": content
                    })
        
        self.workflow_state["artifacts"] = artifacts
    
    def _generate_workflow_summary(self) -> Dict[str, Any]:
        """Generate a summary of the workflow execution."""
        
        start_time = self.workflow_state.get("start_time")
        end_time = self.workflow_state.get("end_time")
        duration = None
        
        if start_time and end_time:
            duration = (end_time - start_time).total_seconds()
        
        return {
            "duration_seconds": duration,
            "total_messages": len(self.workflow_state["messages"]),
            "artifacts_generated": {
                "architecture_design": bool(self.workflow_state["artifacts"].get("architecture_design")),
                "implementation_plan": bool(self.workflow_state["artifacts"].get("implementation_plan")),
                "source_code_files": len(self.workflow_state["artifacts"].get("source_code", [])),
                "review_reports": len(self.workflow_state["artifacts"].get("review_reports", [])),
                "optimizations": len(self.workflow_state["artifacts"].get("optimizations", []))
            },
            "workflow_phases": [
                "architecture_design",
                "project_planning", 
                "code_implementation",
                "code_review",
                "code_optimization"
            ]
        }
    
    async def cleanup(self) -> None:
        """Cleanup resources after workflow completion."""
        try:
            if hasattr(self.model_client, 'close'):
                await self.model_client.close()
            self.logger.info("Workflow cleanup completed")
        except Exception as e:
            self.logger.warning(f"Cleanup warning: {str(e)}")
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status."""
        return {
            "status": self.workflow_state["status"],
            "current_phase": self.workflow_state["current_phase"],
            "start_time": self.workflow_state.get("start_time"),
            "messages_count": len(self.workflow_state["messages"]),
            "artifacts_count": len(self.workflow_state.get("artifacts", {}))
        }
