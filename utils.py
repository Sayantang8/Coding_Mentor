"""
Utilities Module for AI Coding Mentor
Contains helper functions for file operations, exports, and UI utilities
"""

import json
from datetime import datetime
from typing import Dict, Any

def get_language_mode(language: str) -> str:
    """
    Map language names to ace editor modes.
    
    Args:
        language: Programming language name
    
    Returns:
        Ace editor mode string
    """
    language_modes = {
        "python": "python",
        "java": "java", 
        "javascript": "javascript",
        "js": "javascript",
        "py": "python"
    }
    
    return language_modes.get(language.lower(), "text")

def export_report(report_data: Dict[str, Any]) -> str:
    """
    Export analysis results and AI responses to a formatted report.
    
    Args:
        report_data: Dictionary containing all report data
    
    Returns:
        Formatted report as JSON string
    """
    
    # Create a structured report
    structured_report = {
        "report_metadata": {
            "generated_at": datetime.now().isoformat(),
            "tool": "AI Coding Mentor",
            "version": "2.0"
        },
        "session_data": {
            "problem_statement": report_data.get("problem_statement", ""),
            "programming_language": report_data.get("language", ""),
            "code_length": len(report_data.get("code", "")),
            "timestamp": report_data.get("timestamp", "")
        },
        "code_analysis": format_analysis_results(report_data.get("analysis_results")),
        "ai_assistance": format_ai_responses(report_data.get("gpt_responses", [])),
        "code_snapshot": report_data.get("code", "")
    }
    
    return json.dumps(structured_report, indent=2, ensure_ascii=False)

def format_analysis_results(analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format code analysis results for the report.
    
    Args:
        analysis_results: Raw analysis results
    
    Returns:
        Formatted analysis results
    """
    if not analysis_results:
        return {"status": "No analysis performed"}
    
    formatted = {
        "linting": {
            "issues_found": len(analysis_results.get("lint_issues", [])),
            "issues": analysis_results.get("lint_issues", [])
        },
        "formatting": {
            "needs_formatting": analysis_results.get("formatting_needed", False),
            "formatted_code_available": bool(analysis_results.get("formatted_code"))
        },
        "complexity": analysis_results.get("complexity", {})
    }
    
    return formatted

def format_ai_responses(gpt_responses: list) -> Dict[str, Any]:
    """
    Format AI responses for the report.
    
    Args:
        gpt_responses: List of AI responses
    
    Returns:
        Formatted AI responses
    """
    if not gpt_responses:
        return {"status": "No AI assistance requested"}
    
    formatted = {
        "total_interactions": len(gpt_responses),
        "interactions": []
    }
    
    for response in gpt_responses:
        formatted["interactions"].append({
            "type": response.get("type", "unknown"),
            "timestamp": response.get("timestamp", ""),
            "content_preview": response.get("content", "")[:200] + "..." if len(response.get("content", "")) > 200 else response.get("content", ""),
            "full_content": response.get("content", "")
        })
    
    return formatted

def validate_code_syntax(code: str, language: str) -> Dict[str, Any]:
    """
    Basic syntax validation for different languages.
    
    Args:
        code: Code string to validate
        language: Programming language
    
    Returns:
        Validation results
    """
    result = {
        "is_valid": True,
        "errors": [],
        "warnings": []
    }
    
    if not code.strip():
        result["warnings"].append("Code is empty")
        return result
    
    if language == "python":
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            result["is_valid"] = False
            result["errors"].append(f"Syntax Error: {str(e)}")
        except Exception as e:
            result["warnings"].append(f"Compilation warning: {str(e)}")
    
    # For Java and JavaScript, we'd need more sophisticated parsing
    # For now, just basic checks
    elif language == "java":
        if "class" not in code and "public" not in code:
            result["warnings"].append("Java code typically requires a class declaration")
    
    elif language == "javascript":
        # Basic bracket matching
        if code.count('{') != code.count('}'):
            result["warnings"].append("Mismatched curly braces")
        if code.count('(') != code.count(')'):
            result["warnings"].append("Mismatched parentheses")
    
    return result

def get_code_statistics(code: str) -> Dict[str, int]:
    """
    Get basic statistics about the code.
    
    Args:
        code: Code string to analyze
    
    Returns:
        Dictionary with code statistics
    """
    if not code:
        return {
            "total_lines": 0,
            "non_empty_lines": 0,
            "comment_lines": 0,
            "character_count": 0
        }
    
    lines = code.split('\n')
    
    stats = {
        "total_lines": len(lines),
        "non_empty_lines": len([line for line in lines if line.strip()]),
        "comment_lines": len([line for line in lines if line.strip().startswith('#')]),
        "character_count": len(code)
    }
    
    return stats

def format_timestamp(timestamp_str: str) -> str:
    """
    Format timestamp string for display.
    
    Args:
        timestamp_str: ISO format timestamp string
    
    Returns:
        Formatted timestamp string
    """
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return timestamp_str

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to specified length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_language_info(language: str) -> Dict[str, str]:
    """
    Get information about the programming language.
    
    Args:
        language: Programming language name
    
    Returns:
        Dictionary with language information
    """
    language_info = {
        "python": {
            "name": "Python",
            "extension": ".py",
            "description": "High-level, interpreted programming language",
            "features": "Dynamic typing, extensive libraries, readable syntax"
        },
        "java": {
            "name": "Java",
            "extension": ".java",
            "description": "Object-oriented, platform-independent language",
            "features": "Strong typing, JVM, enterprise applications"
        },
        "javascript": {
            "name": "JavaScript",
            "extension": ".js",
            "description": "Dynamic language for web development",
            "features": "Event-driven, functional programming, web APIs"
        }
    }
    
    return language_info.get(language.lower(), {
        "name": language.title(),
        "extension": f".{language.lower()}",
        "description": "Programming language",
        "features": "Various programming features"
    })