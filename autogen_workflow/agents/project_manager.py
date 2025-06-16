"""
Project Manager Agent for AutoGen Programming Workflow

This module implements the Project Manager agent responsible for coordinating
development tasks, managing workflow between agents, and ensuring project quality.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient


class ProjectManagerAgent:
    """
    Project Manager Agent responsible for project coordination and workflow management.
    
    This agent coordinates between different agents, manages the development workflow,
    tracks progress, and ensures quality standards are met throughout the project.
    """
    
    def __init__(self, model_client: ChatCompletionClient, config: Dict[str, Any]):
        """
        Initialize the Project Manager Agent.
        
        Args:
            model_client: The AI model client for generating responses
            config: Configuration dictionary containing agent settings
        """
        self.config = config
        self.agent = AssistantAgent(
            name=config["name"],
            model_client=model_client,
            description=config["description"],
            system_message=config["system_message"],
            handoffs=config["handoffs"]
        )
        
        # Project tracking
        self.project_status = {
            "current_phase": "planning",
            "tasks_completed": [],
            "tasks_in_progress": [],
            "tasks_pending": [],
            "issues": [],
            "milestones": []
        }
    
    def get_agent(self) -> AssistantAgent:
        """Get the underlying AutoGen AssistantAgent instance."""
        return self.agent
    
    def create_project_plan(self, architecture: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create detailed project plan based on architecture design.
        
        Args:
            architecture: Architecture design from Architect agent
            
        Returns:
            Comprehensive project plan
        """
        plan = {
            "project_overview": {
                "name": "Data Analysis API Server",
                "description": "High-performance data analysis API with visualization capabilities",
                "start_date": datetime.now().isoformat(),
                "estimated_duration": "12-16 weeks",
                "team_size": 5
            },
            "phases": self._create_development_phases(),
            "tasks": self._create_task_breakdown(),
            "milestones": self._create_milestones(),
            "resources": self._define_resources(),
            "risk_management": self._create_risk_plan(),
            "quality_gates": self._define_quality_gates()
        }
        
        return plan
    
    def _create_development_phases(self) -> List[Dict[str, Any]]:
        """Create development phases with timelines and objectives."""
        return [
            {
                "phase": "Architecture & Planning",
                "duration": "1-2 weeks",
                "objectives": [
                    "Finalize system architecture",
                    "Create detailed technical specifications",
                    "Set up development environment",
                    "Define coding standards and guidelines"
                ],
                "deliverables": ["Architecture document", "Technical specs", "Dev environment"]
            },
            {
                "phase": "Core Infrastructure",
                "duration": "3-4 weeks",
                "objectives": [
                    "Implement basic API framework",
                    "Set up database and data models",
                    "Create authentication system",
                    "Implement basic CRUD operations"
                ],
                "deliverables": ["API framework", "Database schema", "Auth system"]
            },
            {
                "phase": "Data Processing Engine",
                "duration": "4-5 weeks",
                "objectives": [
                    "Implement data ingestion services",
                    "Create data processing pipeline",
                    "Add statistical analysis features",
                    "Implement async task processing"
                ],
                "deliverables": ["Data ingestion", "Processing pipeline", "Analysis engine"]
            },
            {
                "phase": "Visualization & Advanced Features",
                "duration": "3-4 weeks",
                "objectives": [
                    "Implement chart generation",
                    "Add advanced analytics",
                    "Create dashboard functionality",
                    "Optimize performance"
                ],
                "deliverables": ["Visualization service", "Advanced analytics", "Dashboard"]
            },
            {
                "phase": "Testing & Deployment",
                "duration": "1-2 weeks",
                "objectives": [
                    "Comprehensive testing",
                    "Performance optimization",
                    "Security hardening",
                    "Production deployment"
                ],
                "deliverables": ["Test suite", "Performance report", "Production deployment"]
            }
        ]
    
    def _create_task_breakdown(self) -> List[Dict[str, Any]]:
        """Create detailed task breakdown structure."""
        return [
            {
                "id": "TASK-001",
                "title": "API Framework Setup",
                "description": "Set up FastAPI framework with basic structure",
                "priority": "High",
                "estimated_hours": 16,
                "assigned_to": "programmer",
                "dependencies": [],
                "status": "pending"
            },
            {
                "id": "TASK-002", 
                "title": "Database Schema Design",
                "description": "Design and implement PostgreSQL database schema",
                "priority": "High",
                "estimated_hours": 12,
                "assigned_to": "programmer",
                "dependencies": ["TASK-001"],
                "status": "pending"
            },
            {
                "id": "TASK-003",
                "title": "Authentication System",
                "description": "Implement JWT-based authentication and authorization",
                "priority": "High",
                "estimated_hours": 20,
                "assigned_to": "programmer",
                "dependencies": ["TASK-001"],
                "status": "pending"
            },
            {
                "id": "TASK-004",
                "title": "Data Upload Service",
                "description": "Implement file upload and validation service",
                "priority": "Medium",
                "estimated_hours": 24,
                "assigned_to": "programmer",
                "dependencies": ["TASK-002"],
                "status": "pending"
            },
            {
                "id": "TASK-005",
                "title": "Data Processing Engine",
                "description": "Implement core data processing and analysis engine",
                "priority": "High",
                "estimated_hours": 32,
                "assigned_to": "programmer",
                "dependencies": ["TASK-004"],
                "status": "pending"
            }
        ]
    
    def _create_milestones(self) -> List[Dict[str, Any]]:
        """Create project milestones with success criteria."""
        return [
            {
                "name": "Architecture Complete",
                "date": (datetime.now() + timedelta(weeks=2)).isoformat(),
                "criteria": ["Architecture approved", "Technical specs finalized", "Dev environment ready"]
            },
            {
                "name": "MVP Ready",
                "date": (datetime.now() + timedelta(weeks=8)).isoformat(),
                "criteria": ["Basic API functional", "Data upload working", "Simple analysis available"]
            },
            {
                "name": "Beta Release",
                "date": (datetime.now() + timedelta(weeks=12)).isoformat(),
                "criteria": ["All core features complete", "Testing complete", "Performance acceptable"]
            },
            {
                "name": "Production Launch",
                "date": (datetime.now() + timedelta(weeks=16)).isoformat(),
                "criteria": ["Security audit passed", "Load testing complete", "Documentation ready"]
            }
        ]
    
    def _define_resources(self) -> Dict[str, Any]:
        """Define required resources for the project."""
        return {
            "team": {
                "architect": {"role": "System Architect", "allocation": "25%"},
                "project_manager": {"role": "Project Manager", "allocation": "50%"},
                "programmer": {"role": "Senior Developer", "allocation": "100%"},
                "code_reviewer": {"role": "Code Reviewer", "allocation": "30%"},
                "code_optimizer": {"role": "Performance Engineer", "allocation": "25%"}
            },
            "infrastructure": {
                "development": ["Local dev environment", "Docker containers", "Git repository"],
                "testing": ["Test database", "CI/CD pipeline", "Testing tools"],
                "production": ["Cloud infrastructure", "Database cluster", "Monitoring tools"]
            },
            "tools": {
                "development": ["VS Code", "Python 3.9+", "FastAPI", "PostgreSQL"],
                "testing": ["pytest", "coverage", "locust", "security scanners"],
                "deployment": ["Docker", "Kubernetes", "Helm", "CI/CD pipeline"]
            }
        }
    
    def _create_risk_plan(self) -> Dict[str, Any]:
        """Create risk management plan."""
        return {
            "technical_risks": [
                {
                    "risk": "Performance bottlenecks with large datasets",
                    "probability": "Medium",
                    "impact": "High",
                    "mitigation": "Implement caching, optimize queries, use async processing"
                },
                {
                    "risk": "Integration complexity with external services",
                    "probability": "Low",
                    "impact": "Medium", 
                    "mitigation": "Create abstraction layers, implement circuit breakers"
                }
            ],
            "project_risks": [
                {
                    "risk": "Scope creep affecting timeline",
                    "probability": "Medium",
                    "impact": "Medium",
                    "mitigation": "Clear requirements, change control process"
                },
                {
                    "risk": "Resource availability issues",
                    "probability": "Low",
                    "impact": "High",
                    "mitigation": "Cross-training, documentation, backup resources"
                }
            ]
        }
    
    def _define_quality_gates(self) -> List[Dict[str, Any]]:
        """Define quality gates for each phase."""
        return [
            {
                "phase": "Architecture",
                "criteria": [
                    "Architecture review passed",
                    "Technical specs approved",
                    "Security review completed"
                ]
            },
            {
                "phase": "Development",
                "criteria": [
                    "Code review passed",
                    "Unit tests > 80% coverage",
                    "Integration tests passing",
                    "Security scan clean"
                ]
            },
            {
                "phase": "Testing",
                "criteria": [
                    "All tests passing",
                    "Performance benchmarks met",
                    "Security audit passed",
                    "Documentation complete"
                ]
            }
        ]
    
    def track_progress(self, task_id: str, status: str, notes: str = "") -> Dict[str, Any]:
        """
        Track progress of a specific task.
        
        Args:
            task_id: Unique task identifier
            status: Current status (pending, in_progress, completed, blocked)
            notes: Additional notes about the task
            
        Returns:
            Updated task status
        """
        update = {
            "task_id": task_id,
            "status": status,
            "updated_at": datetime.now().isoformat(),
            "notes": notes
        }
        
        # Update project status tracking
        if status == "completed":
            self.project_status["tasks_completed"].append(task_id)
        elif status == "in_progress":
            if task_id not in self.project_status["tasks_in_progress"]:
                self.project_status["tasks_in_progress"].append(task_id)
        
        return update
    
    def generate_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive project status report."""
        return {
            "project_health": self._assess_project_health(),
            "progress_summary": self._create_progress_summary(),
            "upcoming_milestones": self._get_upcoming_milestones(),
            "risks_and_issues": self._get_current_risks(),
            "recommendations": self._generate_recommendations()
        }
    
    def _assess_project_health(self) -> str:
        """Assess overall project health."""
        completed = len(self.project_status["tasks_completed"])
        total = completed + len(self.project_status["tasks_in_progress"]) + len(self.project_status["tasks_pending"])
        
        if total == 0:
            return "Not Started"
        
        completion_rate = completed / total
        
        if completion_rate >= 0.8:
            return "On Track"
        elif completion_rate >= 0.6:
            return "At Risk"
        else:
            return "Behind Schedule"
    
    def _create_progress_summary(self) -> Dict[str, Any]:
        """Create progress summary."""
        return {
            "current_phase": self.project_status["current_phase"],
            "tasks_completed": len(self.project_status["tasks_completed"]),
            "tasks_in_progress": len(self.project_status["tasks_in_progress"]),
            "tasks_pending": len(self.project_status["tasks_pending"]),
            "issues_count": len(self.project_status["issues"])
        }
    
    def _get_upcoming_milestones(self) -> List[Dict[str, Any]]:
        """Get upcoming milestones."""
        # This would typically query the milestone data
        return []
    
    def _get_current_risks(self) -> List[Dict[str, Any]]:
        """Get current risks and issues."""
        return self.project_status["issues"]
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on current status."""
        recommendations = []
        
        if len(self.project_status["issues"]) > 0:
            recommendations.append("Address current issues to prevent delays")
        
        if len(self.project_status["tasks_in_progress"]) > 3:
            recommendations.append("Consider focusing on fewer tasks to improve completion rate")
        
        return recommendations
