"""
Code Reviewer Agent for AutoGen Programming Workflow

This module implements the Code Reviewer agent responsible for analyzing code quality,
identifying security vulnerabilities, and ensuring adherence to coding standards.
"""

from typing import List, Dict, Any, Optional, Tuple
from autogen_agentchat.agents import AssistantAgent
from autogen_core.models import ChatCompletionClient
import re
import ast


class CodeReviewerAgent:
    """
    Code Reviewer Agent responsible for code quality assurance and review.
    
    This agent analyzes code for quality, security, performance, and adherence
    to coding standards, providing detailed feedback and recommendations.
    """
    
    def __init__(self, model_client: ChatCompletionClient, config: Dict[str, Any]):
        """
        Initialize the Code Reviewer Agent.
        
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
        
        # Review criteria and standards
        self.review_criteria = {
            "code_quality": {
                "readability": 0.8,
                "maintainability": 0.8,
                "complexity": 0.7,
                "documentation": 0.8
            },
            "security": {
                "vulnerability_scan": True,
                "input_validation": True,
                "authentication": True,
                "authorization": True
            },
            "performance": {
                "algorithm_efficiency": 0.8,
                "memory_usage": 0.8,
                "database_optimization": 0.8
            },
            "standards": {
                "pep8_compliance": True,
                "naming_conventions": True,
                "type_hints": True,
                "docstrings": True
            }
        }
    
    def get_agent(self) -> AssistantAgent:
        """Get the underlying AutoGen AssistantAgent instance."""
        return self.agent
    
    def review_code(self, code: str, file_type: str = "python") -> Dict[str, Any]:
        """
        Perform comprehensive code review.
        
        Args:
            code: Source code to review
            file_type: Type of code file (python, javascript, etc.)
            
        Returns:
            Comprehensive review results
        """
        review_result = {
            "overall_score": 0.0,
            "status": "NEEDS_REVISION",  # APPROVED, NEEDS_OPTIMIZATION, NEEDS_REVISION
            "quality_metrics": {},
            "issues": [],
            "warnings": [],
            "suggestions": [],
            "security_findings": [],
            "performance_issues": [],
            "standards_violations": []
        }
        
        if file_type == "python":
            review_result = self._review_python_code(code, review_result)
        
        # Calculate overall score
        review_result["overall_score"] = self._calculate_overall_score(review_result)
        
        # Determine status based on score and issues
        review_result["status"] = self._determine_review_status(review_result)
        
        return review_result
    
    def _review_python_code(self, code: str, review_result: Dict[str, Any]) -> Dict[str, Any]:
        """Review Python-specific code patterns and standards."""
        
        # Parse AST for analysis
        try:
            tree = ast.parse(code)
            review_result["quality_metrics"]["syntax_valid"] = True
        except SyntaxError as e:
            review_result["issues"].append({
                "type": "syntax_error",
                "severity": "high",
                "message": f"Syntax error: {str(e)}",
                "line": getattr(e, 'lineno', 0)
            })
            review_result["quality_metrics"]["syntax_valid"] = False
            return review_result
        
        # Code quality checks
        review_result = self._check_code_quality(code, tree, review_result)
        
        # Security checks
        review_result = self._check_security_issues(code, tree, review_result)
        
        # Performance checks
        review_result = self._check_performance_issues(code, tree, review_result)
        
        # Standards compliance
        review_result = self._check_coding_standards(code, tree, review_result)
        
        return review_result
    
    def _check_code_quality(self, code: str, tree: ast.AST, review_result: Dict[str, Any]) -> Dict[str, Any]:
        """Check code quality metrics."""
        
        lines = code.split('\n')
        
        # Check function complexity
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self._calculate_cyclomatic_complexity(node)
                if complexity > 10:
                    review_result["warnings"].append({
                        "type": "high_complexity",
                        "severity": "medium",
                        "message": f"Function '{node.name}' has high complexity ({complexity})",
                        "line": node.lineno,
                        "suggestion": "Consider breaking down into smaller functions"
                    })
        
        # Check line length
        for i, line in enumerate(lines, 1):
            if len(line) > 88:  # PEP 8 recommends 79, but 88 is acceptable
                review_result["standards_violations"].append({
                    "type": "line_length",
                    "severity": "low",
                    "message": f"Line {i} exceeds 88 characters ({len(line)})",
                    "line": i
                })
        
        # Check for TODO/FIXME comments
        todo_pattern = re.compile(r'#\s*(TODO|FIXME|HACK|XXX)', re.IGNORECASE)
        for i, line in enumerate(lines, 1):
            if todo_pattern.search(line):
                review_result["warnings"].append({
                    "type": "todo_comment",
                    "severity": "low",
                    "message": f"TODO/FIXME comment found on line {i}",
                    "line": i,
                    "suggestion": "Consider creating a proper issue or implementing the fix"
                })
        
        # Check for proper error handling
        has_try_except = any(isinstance(node, ast.Try) for node in ast.walk(tree))
        if not has_try_except and len(code) > 100:  # Only for non-trivial code
            review_result["suggestions"].append({
                "type": "error_handling",
                "severity": "medium",
                "message": "Consider adding error handling with try-except blocks",
                "suggestion": "Add appropriate exception handling for robustness"
            })
        
        return review_result
    
    def _check_security_issues(self, code: str, tree: ast.AST, review_result: Dict[str, Any]) -> Dict[str, Any]:
        """Check for security vulnerabilities."""
        
        # Check for SQL injection vulnerabilities
        sql_patterns = [
            r'execute\s*\(\s*["\'].*%.*["\']',  # String formatting in SQL
            r'cursor\.execute\s*\(\s*f["\']',    # f-strings in SQL
            r'\.format\s*\(\s*\).*execute'       # .format() with execute
        ]
        
        for pattern in sql_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                review_result["security_findings"].append({
                    "type": "sql_injection",
                    "severity": "high",
                    "message": "Potential SQL injection vulnerability detected",
                    "suggestion": "Use parameterized queries or ORM methods"
                })
        
        # Check for hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']'
        ]
        
        for pattern in secret_patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                review_result["security_findings"].append({
                    "type": "hardcoded_secret",
                    "severity": "high",
                    "message": f"Potential hardcoded secret on line {line_num}",
                    "line": line_num,
                    "suggestion": "Use environment variables or secure configuration"
                })
        
        # Check for unsafe eval/exec usage
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ['eval', 'exec']:
                    review_result["security_findings"].append({
                        "type": "unsafe_eval",
                        "severity": "high",
                        "message": f"Unsafe use of {node.func.id}() on line {node.lineno}",
                        "line": node.lineno,
                        "suggestion": "Avoid eval/exec or use safer alternatives"
                    })
        
        return review_result
    
    def _check_performance_issues(self, code: str, tree: ast.AST, review_result: Dict[str, Any]) -> Dict[str, Any]:
        """Check for performance issues."""
        
        # Check for inefficient loops
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                # Check for list concatenation in loops
                for child in ast.walk(node):
                    if (isinstance(child, ast.AugAssign) and 
                        isinstance(child.op, ast.Add) and
                        isinstance(child.target, ast.Name)):
                        review_result["performance_issues"].append({
                            "type": "inefficient_concatenation",
                            "severity": "medium",
                            "message": f"Inefficient list/string concatenation in loop on line {node.lineno}",
                            "line": node.lineno,
                            "suggestion": "Use list comprehension or join() for better performance"
                        })
        
        # Check for global variable usage
        for node in ast.walk(tree):
            if isinstance(node, ast.Global):
                review_result["performance_issues"].append({
                    "type": "global_variable",
                    "severity": "low",
                    "message": f"Global variable usage on line {node.lineno}",
                    "line": node.lineno,
                    "suggestion": "Consider using function parameters or class attributes"
                })
        
        return review_result
    
    def _check_coding_standards(self, code: str, tree: ast.AST, review_result: Dict[str, Any]) -> Dict[str, Any]:
        """Check adherence to coding standards."""
        
        # Check for type hints
        functions_without_hints = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.returns and node.name != '__init__':
                    functions_without_hints.append(node.name)
        
        if functions_without_hints:
            review_result["standards_violations"].append({
                "type": "missing_type_hints",
                "severity": "low",
                "message": f"Functions without return type hints: {', '.join(functions_without_hints)}",
                "suggestion": "Add type hints for better code documentation"
            })
        
        # Check for docstrings
        functions_without_docstrings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    functions_without_docstrings.append(node.name)
        
        if functions_without_docstrings:
            review_result["standards_violations"].append({
                "type": "missing_docstrings",
                "severity": "medium",
                "message": f"Functions without docstrings: {', '.join(functions_without_docstrings)}",
                "suggestion": "Add docstrings to document function purpose and parameters"
            })
        
        return review_result
    
    def _calculate_cyclomatic_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function."""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
        
        return complexity
    
    def _calculate_overall_score(self, review_result: Dict[str, Any]) -> float:
        """Calculate overall code quality score."""
        
        # Base score
        score = 100.0
        
        # Deduct points for issues
        for issue in review_result["issues"]:
            if issue["severity"] == "high":
                score -= 20
            elif issue["severity"] == "medium":
                score -= 10
            else:
                score -= 5
        
        # Deduct points for security findings
        for finding in review_result["security_findings"]:
            if finding["severity"] == "high":
                score -= 25
            elif finding["severity"] == "medium":
                score -= 15
            else:
                score -= 8
        
        # Deduct points for performance issues
        for issue in review_result["performance_issues"]:
            if issue["severity"] == "high":
                score -= 15
            elif issue["severity"] == "medium":
                score -= 8
            else:
                score -= 3
        
        # Deduct points for standards violations
        for violation in review_result["standards_violations"]:
            if violation["severity"] == "high":
                score -= 10
            elif violation["severity"] == "medium":
                score -= 5
            else:
                score -= 2
        
        return max(0.0, min(100.0, score))
    
    def _determine_review_status(self, review_result: Dict[str, Any]) -> str:
        """Determine review status based on findings."""
        
        # Check for critical issues
        high_severity_issues = [
            item for item in (
                review_result["issues"] + 
                review_result["security_findings"] + 
                review_result["performance_issues"]
            ) if item.get("severity") == "high"
        ]
        
        if high_severity_issues:
            return "NEEDS_REVISION"
        
        # Check overall score
        score = review_result["overall_score"]
        
        if score >= 85:
            return "APPROVED"
        elif score >= 70:
            return "NEEDS_OPTIMIZATION"
        else:
            return "NEEDS_REVISION"
    
    def generate_review_report(self, review_result: Dict[str, Any]) -> str:
        """Generate a comprehensive review report."""
        
        report = f"""
# Code Review Report

## Overall Assessment
- **Status**: {review_result['status']}
- **Quality Score**: {review_result['overall_score']:.1f}/100

## Summary
- Issues Found: {len(review_result['issues'])}
- Security Findings: {len(review_result['security_findings'])}
- Performance Issues: {len(review_result['performance_issues'])}
- Standards Violations: {len(review_result['standards_violations'])}

## Detailed Findings

### Critical Issues
"""
        
        # Add critical issues
        critical_items = [
            item for item in (
                review_result["issues"] + 
                review_result["security_findings"]
            ) if item.get("severity") == "high"
        ]
        
        if critical_items:
            for item in critical_items:
                report += f"- **{item['type']}** (Line {item.get('line', 'N/A')}): {item['message']}\n"
                if 'suggestion' in item:
                    report += f"  *Suggestion: {item['suggestion']}*\n"
        else:
            report += "No critical issues found.\n"
        
        report += "\n### Recommendations\n"
        
        # Add recommendations based on status
        if review_result['status'] == "APPROVED":
            report += "Code meets quality standards and is approved for deployment.\n"
        elif review_result['status'] == "NEEDS_OPTIMIZATION":
            report += "Code is functional but could benefit from optimization:\n"
            for item in review_result['suggestions']:
                report += f"- {item['message']}\n"
        else:
            report += "Code requires revision before approval:\n"
            for item in critical_items[:3]:  # Show top 3 issues
                report += f"- {item['message']}\n"
        
        return report
