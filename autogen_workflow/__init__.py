"""
AutoGen Programming Workflow Package

This package implements a multi-agent programming workflow using the AutoGen framework.
It includes 5 specialized agents for collaborative software development:

1. Architect - Architecture design and management
2. Project Manager - Project coordination and management
3. Programmer - Code writing and implementation
4. Code Reviewer - Code review and suggestions
5. Code Optimizer - Code optimization based on reviews

The workflow follows modern AutoGen patterns with proper agent communication,
handoffs, and termination conditions.
"""

__version__ = "1.0.0"
__author__ = "DataLab Team"

from .workflow import ProgrammingWorkflow
from .config import WorkflowConfig

__all__ = ["ProgrammingWorkflow", "WorkflowConfig"]
