"""
Code Analyzer Module for AI Coding Mentor
Handles Python code analysis including linting, formatting, and complexity analysis
"""

import subprocess
import tempfile
import os
import json
from typing import Dict, List, Any
import ast

def analyze_python_code(code: str) -> Dict[str, Any]:
    """
    Analyze Python code using flake8, black, and radon.
    
    Args:
        code: Python code string to analyze
    
    Returns:
        Dictionary containing analysis results
    """
    results = {
        "lint_issues": [],
        "formatting_needed": False,
        "formatted_code": "",
        "complexity": {}
    }
    
    # Create temporary file for analysis with explicit UTF-8 encoding
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
    
    try:
        # Run linting analysis
        results["lint_issues"] = run_flake8_analysis(temp_file_path)
        
        # Run formatting analysis
        formatted_code, formatting_needed = run_black_analysis(code)
        results["formatted_code"] = formatted_code
        results["formatting_needed"] = formatting_needed
        
        # Run complexity analysis
        results["complexity"] = run_radon_analysis(temp_file_path)
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
    
    return results

def run_flake8_analysis(file_path: str) -> List[Dict[str, Any]]:
    """
    Run flake8 linting on the code file.
    
    Args:
        file_path: Path to the temporary Python file
    
    Returns:
        List of linting issues
    """
    issues = []
    
    try:
        # Set environment for proper encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # Run flake8 with JSON output format and proper encoding
        try:
            result = subprocess.run(
                ['flake8', '--format=json', file_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30,
                env=env
            )
        except UnicodeDecodeError:
            result = subprocess.run(
                ['flake8', '--format=json', file_path],
                capture_output=True,
                text=False,
                timeout=30,
                env=env
            )
            result.stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ""
            result.stderr = result.stderr.decode('utf-8', errors='replace') if result.stderr else ""
        
        if result.stdout:
            # Parse flake8 JSON output
            try:
                flake8_data = json.loads(result.stdout)
                for item in flake8_data:
                    issues.append({
                        "line": item.get("line_number", 0),
                        "column": item.get("column_number", 0),
                        "message": item.get("text", ""),
                        "code": item.get("code", "")
                    })
            except json.JSONDecodeError:
                # Fallback to parsing standard flake8 output
                issues = parse_flake8_standard_output(result.stdout)
        
        # If no JSON output, try standard format
        if not issues and result.returncode != 0:
            try:
                result = subprocess.run(
                    ['flake8', file_path],
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=30,
                    env=env
                )
            except UnicodeDecodeError:
                result = subprocess.run(
                    ['flake8', file_path],
                    capture_output=True,
                    text=False,
                    timeout=30,
                    env=env
                )
                result.stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ""
            issues = parse_flake8_standard_output(result.stdout)
            
    except subprocess.TimeoutExpired:
        issues.append({
            "line": 0,
            "column": 0,
            "message": "Flake8 analysis timed out",
            "code": "TIMEOUT"
        })
    except FileNotFoundError:
        issues.append({
            "line": 0,
            "column": 0,
            "message": "Flake8 not installed. Install with: pip install flake8",
            "code": "MISSING"
        })
    except Exception as e:
        issues.append({
            "line": 0,
            "column": 0,
            "message": f"Flake8 analysis failed: {str(e)}",
            "code": "ERROR"
        })
    
    return issues

def parse_flake8_standard_output(output: str) -> List[Dict[str, Any]]:
    """Parse standard flake8 output format"""
    issues = []
    for line in output.strip().split('\n'):
        if line.strip():
            parts = line.split(':', 3)
            if len(parts) >= 4:
                try:
                    line_num = int(parts[1])
                    col_num = int(parts[2])
                    message_parts = parts[3].strip().split(' ', 1)
                    code = message_parts[0] if message_parts else ""
                    message = message_parts[1] if len(message_parts) > 1 else parts[3].strip()
                    
                    issues.append({
                        "line": line_num,
                        "column": col_num,
                        "message": message,
                        "code": code
                    })
                except (ValueError, IndexError):
                    continue
    return issues

def run_black_analysis(code: str) -> tuple[str, bool]:
    """
    Run black formatting analysis on the code.
    
    Args:
        code: Python code string
    
    Returns:
        Tuple of (formatted_code, formatting_needed)
    """
    try:
        # Set environment for proper encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # Run black with --diff to see what would change
        try:
            result = subprocess.run(
                ['black', '--diff', '-'],
                input=code,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30,
                env=env
            )
        except UnicodeDecodeError:
            result = subprocess.run(
                ['black', '--diff', '-'],
                input=code.encode('utf-8'),
                capture_output=True,
                text=False,
                timeout=30,
                env=env
            )
            result.stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ""
        
        # If there's diff output, formatting is needed
        formatting_needed = bool(result.stdout.strip())
        
        if formatting_needed:
            # Get the formatted code
            try:
                format_result = subprocess.run(
                    ['black', '-'],
                    input=code,
                    capture_output=True,
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=30,
                    env=env
                )
            except UnicodeDecodeError:
                format_result = subprocess.run(
                    ['black', '-'],
                    input=code.encode('utf-8'),
                    capture_output=True,
                    text=False,
                    timeout=30,
                    env=env
                )
                format_result.stdout = format_result.stdout.decode('utf-8', errors='replace') if format_result.stdout else ""
            formatted_code = format_result.stdout if format_result.returncode == 0 else code
        else:
            formatted_code = code
            
        return formatted_code, formatting_needed
        
    except subprocess.TimeoutExpired:
        return code, False
    except FileNotFoundError:
        return code, False  # Black not installed
    except Exception:
        return code, False

def run_radon_analysis(file_path: str) -> Dict[str, Any]:
    """
    Run radon complexity analysis on the code file.
    
    Args:
        file_path: Path to the temporary Python file
    
    Returns:
        Dictionary containing complexity metrics
    """
    complexity_data = {}
    
    try:
        # Set environment for proper encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # Run radon cyclomatic complexity
        try:
            cc_result = subprocess.run(
                ['radon', 'cc', '-j', file_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30,
                env=env
            )
        except UnicodeDecodeError:
            cc_result = subprocess.run(
                ['radon', 'cc', '-j', file_path],
                capture_output=True,
                text=False,
                timeout=30,
                env=env
            )
            cc_result.stdout = cc_result.stdout.decode('utf-8', errors='replace') if cc_result.stdout else ""
        
        if cc_result.returncode == 0 and cc_result.stdout:
            try:
                cc_data = json.loads(cc_result.stdout)
                if file_path in cc_data:
                    functions = cc_data[file_path]
                    if functions:
                        # Get average complexity
                        complexities = [func.get('complexity', 0) for func in functions]
                        complexity_data['complexity'] = sum(complexities) / len(complexities) if complexities else 0
                        complexity_data['max_complexity'] = max(complexities) if complexities else 0
                        complexity_data['function_count'] = len(functions)
            except json.JSONDecodeError:
                pass
        
        # Run radon maintainability index
        try:
            mi_result = subprocess.run(
                ['radon', 'mi', '-j', file_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=30,
                env=env
            )
        except UnicodeDecodeError:
            mi_result = subprocess.run(
                ['radon', 'mi', '-j', file_path],
                capture_output=True,
                text=False,
                timeout=30,
                env=env
            )
            mi_result.stdout = mi_result.stdout.decode('utf-8', errors='replace') if mi_result.stdout else ""
        
        if mi_result.returncode == 0 and mi_result.stdout:
            try:
                mi_data = json.loads(mi_result.stdout)
                if file_path in mi_data:
                    complexity_data['maintainability'] = mi_data[file_path].get('mi', 0)
            except json.JSONDecodeError:
                pass
                
    except subprocess.TimeoutExpired:
        complexity_data['error'] = "Radon analysis timed out"
    except FileNotFoundError:
        complexity_data['error'] = "Radon not installed. Install with: pip install radon"
    except Exception as e:
        complexity_data['error'] = f"Radon analysis failed: {str(e)}"
    
    # Fallback: basic AST analysis if radon fails
    if not complexity_data or 'error' in complexity_data:
        try:
            complexity_data.update(basic_ast_analysis(file_path))
        except Exception:
            pass
    
    return complexity_data

def basic_ast_analysis(file_path: str) -> Dict[str, Any]:
    """
    Basic complexity analysis using AST when radon is not available.
    
    Args:
        file_path: Path to the Python file
    
    Returns:
        Basic complexity metrics
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        tree = ast.parse(code)
        
        # Count functions and classes
        functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        
        # Count control flow statements (rough complexity indicator)
        control_flow = [
            node for node in ast.walk(tree) 
            if isinstance(node, (ast.If, ast.For, ast.While, ast.Try))
        ]
        
        return {
            'function_count': len(functions),
            'class_count': len(classes),
            'control_flow_count': len(control_flow),
            'estimated_complexity': len(control_flow) + len(functions),
            'analysis_type': 'basic_ast'
        }
        
    except Exception as e:
        return {'error': f"Basic AST analysis failed: {str(e)}"}

def check_dependencies() -> Dict[str, bool]:
    """
    Check if required analysis tools are installed.
    
    Returns:
        Dictionary indicating which tools are available
    """
    tools = {}
    
    # Set environment for proper encoding
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    for tool in ['flake8', 'black', 'radon']:
        try:
            try:
                result = subprocess.run(
                    [tool, '--version'], 
                    capture_output=True, 
                    text=True,
                    encoding='utf-8',
                    errors='replace',
                    timeout=5,
                    env=env
                )
            except UnicodeDecodeError:
                result = subprocess.run(
                    [tool, '--version'], 
                    capture_output=True, 
                    text=False,
                    timeout=5,
                    env=env
                )
            tools[tool] = result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            tools[tool] = False
    
    return tools