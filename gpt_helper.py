"""
GPT Helper Module for AI Coding Mentor
Handles all AI/GenAI interactions for hints and code suggestions
"""

import os
import openai
from typing import Optional
from config import get_config

# Initialize OpenAI client
def get_openai_client():
    """Initialize OpenAI client with API key from environment"""
    config = get_config()
    openai_config = config["openai"]
    
    api_key = openai_config["api_key"]
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            organization=openai_config.get("org_id")
        )
        return client
    except ImportError:
        # Fallback for older OpenAI library versions
        openai.api_key = api_key
        if openai_config.get("org_id"):
            openai.organization = openai_config["org_id"]
        return openai

def get_model_name():
    """Get the configured model name"""
    config = get_config()
    return config["openai"]["model"]

def generate_hint(problem_statement: str, current_code: str, language: str, execution_output: str = "", execution_error: str = "") -> str:
    """
    Generate a conceptual hint for the coding problem.
    
    Args:
        problem_statement: Description of the coding problem
        current_code: User's current code attempt
        language: Programming language being used
        execution_output: Output from code execution (if any)
        execution_error: Error from code execution (if any)
    
    Returns:
        A conceptual hint without actual code
    """
    
    # Fallback response if OpenAI is not available
    if not os.getenv("OPENAI_API_KEY"):
        return generate_fallback_hint(problem_statement, current_code, language)
    
    try:
        client = get_openai_client()
        model_name = get_model_name()
        
        # Build execution context
        execution_context = ""
        if execution_output or execution_error:
            execution_context = f"""
        
        Recent execution results:
        Output: {execution_output if execution_output else "No output"}
        Errors: {execution_error if execution_error else "No errors"}
        """
        
        # Analyze the code to provide better context
        code_analysis = ""
        if current_code.strip():
            # Identify potential issues in the code
            try:
                if language == "python":
                    from code_analyzer import analyze_python_code
                    analysis_results = analyze_python_code(current_code)
                    if analysis_results.get("lint_issues"):
                        code_analysis = "\n\nPotential issues in the code:\n"
                        for issue in analysis_results.get("lint_issues")[:3]:  # Limit to top 3 issues
                            code_analysis += f"- Line {issue['line']}: {issue['message']}\n"
            except Exception:
                # If analysis fails, continue without it
                pass
        
        prompt = f"""
        You are an expert coding mentor. A student is working on this problem:
        
        Problem: {problem_statement}
        Language: {language}
        Current code attempt:
        ```{language}
        {current_code if current_code.strip() else "No code written yet"}
        ```{execution_context}{code_analysis}
        
        Provide a helpful conceptual hint that guides them toward the solution WITHOUT giving away the actual code.
        Focus on:
        - Key insights or approaches they should consider
        - Common patterns or algorithms that might apply
        - Edge cases they should think about
        - General problem-solving strategies
        - If there are execution errors, help them understand what might be wrong conceptually
        
        Your hint should be structured as follows:
        1. Start with a clear, concise statement about the core concept needed to solve the problem
        2. Explain why this approach is suitable for this specific problem
        3. Mention 1-2 edge cases they should consider
        4. If there are errors, explain the conceptual issue behind them
        5. End with an encouraging note
        
        Keep it encouraging and educational. Do NOT provide actual code.
        """
        
        messages = [
            {"role": "system", "content": "You are a helpful coding mentor who provides conceptual guidance without giving away solutions. You focus on teaching problem-solving strategies rather than providing direct answers."},
            {"role": "user", "content": prompt}
        ]
        
        # Try new OpenAI client first with retry logic
        max_retries = 2
        retry_count = 0
        last_error = None
        
        while retry_count <= max_retries:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    max_tokens=400,  # Increased token limit for more detailed hints
                    temperature=0.5  # Lower temperature for more focused responses
                )
                return response.choices[0].message.content.strip()
            except AttributeError:
                # Fallback to old OpenAI API
                try:
                    response = openai.ChatCompletion.create(
                        model=model_name,
                        messages=messages,
                        max_tokens=400,
                        temperature=0.5
                    )
                    return response.choices[0].message.content.strip()
                except Exception as e:
                    last_error = e
                    retry_count += 1
                    if retry_count > max_retries:
                        break
            except Exception as e:
                last_error = e
                retry_count += 1
                if retry_count > max_retries:
                    break
        
        # If we've exhausted retries, use the fallback
        return generate_fallback_hint(problem_statement, current_code, language)
        
    except Exception as e:
        print(f"Error generating hint: {str(e)}")
        return generate_fallback_hint(problem_statement, current_code, language)

def help_me_write(problem_statement: str, current_code: str, language: str, execution_output: str = "", execution_error: str = "") -> str:
    """
    Generate code suggestions for the next 2-3 lines with explanation.
    
    Args:
        problem_statement: Description of the coding problem
        current_code: User's current code attempt
        language: Programming language being used
        execution_output: Output from code execution (if any)
        execution_error: Error from code execution (if any)
    
    Returns:
        Code suggestions with explanations
    """
    
    # Fallback response if OpenAI is not available
    if not os.getenv("OPENAI_API_KEY"):
        return generate_fallback_code_help(problem_statement, current_code, language)
    
    try:
        client = get_openai_client()
        model_name = get_model_name()
        
        # Build execution context
        execution_context = ""
        if execution_output or execution_error:
            execution_context = f"""
        
        Recent execution results:
        Output: {execution_output if execution_output else "No output"}
        Errors: {execution_error if execution_error else "No errors"}
        """
        
        # Analyze the code to provide better context
        code_analysis = ""
        if current_code.strip():
            # Identify potential issues in the code
            try:
                if language == "python":
                    from code_analyzer import analyze_python_code
                    analysis_results = analyze_python_code(current_code)
                    if analysis_results.get("lint_issues"):
                        code_analysis = "\n\nPotential issues in the code:\n"
                        for issue in analysis_results.get("lint_issues")[:5]:  # Limit to top 5 issues
                            code_analysis += f"- Line {issue['line']}: {issue['message']}\n"
                    
                    # Add complexity analysis if available
                    if analysis_results.get("complexity_issues"):
                        code_analysis += "\nComplexity analysis:\n"
                        for func, score in analysis_results.get("complexity_issues").items():
                            code_analysis += f"- Function '{func}' has complexity score of {score}\n"
            except Exception:
                # If analysis fails, continue without it
                pass
        
        # Extract test cases from problem statement if possible
        test_cases = extract_test_cases(problem_statement, language)
        test_case_context = ""
        if test_cases:
            test_case_context = "\n\nPossible test cases extracted from the problem:\n" + test_cases
        
        prompt = f"""
        You are an expert coding mentor helping a student learn to code step by step.
        
        Problem: {problem_statement}
        Language: {language}
        Current code:
        ```{language}
        {current_code if current_code.strip() else "# Starting fresh"}
        ```{execution_context}{code_analysis}{test_case_context}
        
        Provide guidance for the NEXT 1-3 lines of code only. CRITICAL REQUIREMENTS:
        - The code you suggest must be syntactically correct and executable
        - If there are syntax errors in current code, fix them first
        - Suggest only the immediate next step (1-3 lines maximum)
        - Ensure proper indentation and syntax for {language}
        - If starting fresh, provide a proper function signature with correct parameters
        - Test your suggested code mentally to ensure it works
        
        Format your response as:
        **Next Step:**
        ```{language}
        [1-3 lines of syntactically correct, executable code]
        ```
        
        **Why this step:**
        [Brief explanation of why this is the logical next step]
        
        **Learning tip:**
        [Educational insight about this step or concept]
        
        IMPORTANT: The code must be functional and ready to run. Focus on correctness first, then education.
        """
        
        messages = [
            {"role": "system", "content": "You are a helpful coding mentor who provides step-by-step coding guidance with syntactically correct, executable code."},
            {"role": "user", "content": prompt}
        ]
        
        # Try new OpenAI client first with retry logic
        max_retries = 2
        retry_count = 0
        last_error = None
        
        while retry_count <= max_retries:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    max_tokens=500,
                    temperature=0.3
                )
                return response.choices[0].message.content.strip()
            except AttributeError:
                # Fallback to old OpenAI API
                try:
                    response = openai.ChatCompletion.create(
                        model=model_name,
                        messages=messages,
                        max_tokens=500,
                        temperature=0.3
                    )
                    return response.choices[0].message.content.strip()
                except Exception as e:
                    last_error = e
                    retry_count += 1
                    if retry_count > max_retries:
                        break
            except Exception as e:
                last_error = e
                retry_count += 1
                if retry_count > max_retries:
                    break
        
        # If we've exhausted retries, use the fallback
        return generate_fallback_code_help(problem_statement, current_code, language)
        
    except Exception as e:
        print(f"Error generating code suggestions: {str(e)}")
        return generate_fallback_code_help(problem_statement, current_code, language)


def extract_test_cases(problem_statement: str, language: str) -> str:
    """
    Extract potential test cases from a problem statement.
    
    Args:
        problem_statement: Description of the coding problem
        language: Programming language being used
    
    Returns:
        A string containing potential test cases in the appropriate language format
    """
    # Simple heuristic to extract examples from problem statement
    test_cases = ""
    
    # Look for common patterns that indicate examples
    example_patterns = [
        r"Example\s*\d*\s*:([\s\S]*?)(?=Example\s*\d|$)",
        r"Input\s*:([\s\S]*?)Output\s*:([\s\S]*?)(?=Input|$)",
        r"Test Case\s*\d*\s*:([\s\S]*?)(?=Test Case\s*\d|$)"
    ]
    
    for pattern in example_patterns:
        matches = re.findall(pattern, problem_statement, re.IGNORECASE)
        if matches:
            for i, match in enumerate(matches):
                if isinstance(match, tuple):  # Input/Output pattern
                    input_val = match[0].strip()
                    output_val = match[1].strip()
                    test_cases += f"Example {i+1}:\nInput: {input_val}\nExpected Output: {output_val}\n\n"
                else:  # Other patterns
                    test_cases += f"Example {i+1}:\n{match.strip()}\n\n"
    
    # If we found examples, convert them to code-like test cases based on language
    if test_cases:
        if language == "python":
            test_cases += "\nPossible test code:\n```python\n"
            test_cases += "def test_solution():\n    assert solution(...) == expected_output\n"
            test_cases += "```\n"
        elif language == "javascript":
            test_cases += "\nPossible test code:\n```javascript\n"
            test_cases += "function testSolution() {\n    console.assert(solution(...) === expectedOutput);\n}\n"
            test_cases += "```\n"
        elif language == "java":
            test_cases += "\nPossible test code:\n```java\n"
            test_cases += "void testSolution() {\n    assertEquals(expectedOutput, solution(...));\n}\n"
            test_cases += "```\n"
    
    return test_cases

def generate_full_solution(problem_statement: str, current_code: str, language: str, execution_output: str = "", execution_error: str = "") -> str:
    """
    Generate a complete solution for the coding problem.
    
    Args:
        problem_statement: Description of the coding problem
        current_code: User's current code attempt
        language: Programming language being used
        execution_output: Output from code execution (if any)
        execution_error: Error from code execution (if any)
    
    Returns:
        A complete solution with explanation
    """
    
    # Fallback response if OpenAI is not available
    if not os.getenv("OPENAI_API_KEY"):
        return generate_fallback_full_solution(problem_statement, current_code, language)
    
    try:
        client = get_openai_client()
        model_name = get_model_name()
        
        # Build execution context
        execution_context = ""
        if execution_output or execution_error:
            execution_context = f"""
        
        Current execution results:
        Output: {execution_output if execution_output else "No output"}
        Errors: {execution_error if execution_error else "No errors"}
        """
        
        # Analyze the code to provide better context
        code_analysis = ""
        if current_code.strip():
            # Identify potential issues in the code
            try:
                if language == "python":
                    from code_analyzer import analyze_python_code
                    analysis_results = analyze_python_code(current_code)
                    if analysis_results.get("lint_issues"):
                        code_analysis = "\n\nPotential issues in the current code:\n"
                        for issue in analysis_results.get("lint_issues")[:3]:  # Limit to top 3 issues
                            code_analysis += f"- Line {issue['line']}: {issue['message']}\n"
            except Exception:
                # If analysis fails, continue without it
                pass
        
        # Extract test cases from problem statement if possible
        test_cases = extract_test_cases(problem_statement, language)
        test_case_context = ""
        if test_cases:
            test_case_context = "\n\nPossible test cases extracted from the problem:\n" + test_cases
        
        # Determine problem type for better solution generation
        problem_type = classify_problem_type(problem_statement)
        problem_type_context = f"\n\nProblem classification: {problem_type}" if problem_type else ""
        
        prompt = f"""
        You are an expert coding mentor. A student has been working on this problem and now wants to see a complete solution for learning purposes.
        
        Problem: {problem_statement}{problem_type_context}
        Language: {language}
        Student's current attempt:
        ```{language}
        {current_code if current_code.strip() else "No code written yet"}
        ```{execution_context}{code_analysis}{test_case_context}
        
        CRITICAL REQUIREMENTS for the solution:
        - The code MUST be syntactically correct and executable
        - Include proper function signatures with correct parameter types
        - Handle ALL edge cases appropriately (empty inputs, negative values, overflow, etc.)
        - Include COMPREHENSIVE test cases that demonstrate the solution works for all scenarios
        - Use proper variable names and follow language conventions
        - The solution should run without errors when executed
        - Include proper error handling where appropriate
        
        Provide a complete, working solution with detailed explanation. Include:
        - A complete, correct, and EXECUTABLE solution
        - Comprehensive test cases that prove it works for all scenarios
        - Step-by-step explanation of the approach
        - Key concepts and algorithms used
        - Time and space complexity analysis
        - Common pitfalls to avoid
        
        Format your response as:
        **Complete Solution:**
        ```{language}
        [complete working code with comments]
        ```
        
        **Test Cases:**
        ```{language}
        [comprehensive test cases that verify all scenarios]
        ```
        
        **Explanation:**
        [Detailed step-by-step explanation]
        
        **Key Concepts:**
        [Important programming concepts demonstrated]
        
        **Complexity:**
        - Time: [time complexity with explanation]
        - Space: [space complexity with explanation]
        
        **Edge Cases Handled:**
        [List of edge cases the solution handles]
        
        **Learning Notes:**
        [Additional insights for learning]
        
        IMPORTANT: The code must be production-ready and executable. Test it mentally before providing.
        """
        
        messages = [
            {"role": "system", "content": "You are a helpful coding mentor who provides complete, executable solutions with educational explanations. Always ensure code is syntactically correct and includes comprehensive test cases that verify all scenarios. Your solutions must handle all edge cases and follow best practices for the given programming language."},
            {"role": "user", "content": prompt}
        ]
        
        # Try new OpenAI client first with retry logic
        max_retries = 2
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    max_tokens=2000,  # Increased token limit for more comprehensive solutions
                    temperature=0.2   # Low temperature for more reliable and focused solutions
                )
                return response.choices[0].message.content.strip()
            except AttributeError:
                # Fallback to old OpenAI API
                try:
                    response = openai.ChatCompletion.create(
                        model=model_name,
                        messages=messages,
                        max_tokens=2000,
                        temperature=0.2
                    )
                    return response.choices[0].message.content.strip()
                except Exception as e:
                    print(f"Error with old API: {str(e)}")
                    retry_count += 1
                    if retry_count > max_retries:
                        break
            except Exception as e:
                print(f"Error with new API: {str(e)}")
                retry_count += 1
                if retry_count > max_retries:
                    break
        
        # If we've exhausted retries, use the fallback
        return generate_fallback_full_solution(problem_statement, current_code, language)
        
    except Exception as e:
        print(f"Error generating full solution: {str(e)}")
        return generate_fallback_full_solution(problem_statement, current_code, language)

def generate_fallback_hint(problem_statement: str, current_code: str, language: str) -> str:
    """Generate a fallback hint when OpenAI is not available"""
    
    hints = {
        "two sum": "Consider using a hash map to store values you've seen and their indices. This can help you find complements efficiently.",
        "array": "Think about whether you need to iterate through the array once or multiple times. Consider edge cases like empty arrays.",
        "string": "Consider string manipulation methods and whether you need to track character positions or frequencies.",
        "tree": "Think about tree traversal methods (DFS, BFS) and what information you need to track at each node.",
        "graph": "Consider how to represent the graph and what traversal algorithm would be most appropriate.",
        "sort": "Think about the time complexity requirements and whether you need a stable sort.",
        "search": "Consider whether binary search could apply if the data is sorted, or if you need linear search."
    }
    
    # Simple keyword matching for fallback hints
    problem_lower = problem_statement.lower()
    for keyword, hint in hints.items():
        if keyword in problem_lower:
            return f"💡 **Hint:** {hint}\n\n**General approach:** Break the problem into smaller steps and think about the most efficient data structures for your needs."
    
    return "💡 **General Hint:** Start by understanding the problem requirements clearly. Think about edge cases, choose appropriate data structures, and consider the time/space complexity of your approach."

def generate_fallback_code_help(problem_statement: str, current_code: str, language: str) -> str:
    """Generate fallback code help when OpenAI is not available"""
    
    problem_lower = problem_statement.lower()
    
    # Detect common problem types and provide specific help
    if "palindrome" in problem_lower:
        if language == "python":
            return """**Next Step:**
```python
def is_palindrome(x):
    # Handle negative numbers - they can't be palindromes
    if x < 0:
        return False
```

**Why this step:**
Negative numbers cannot be palindromes because of the negative sign, so we handle this edge case first.

**Learning tip:**
Always consider edge cases early in your solution. For palindromes, think about negative numbers, single digits, and numbers ending in zero."""
        
    elif "two sum" in problem_lower or "target" in problem_lower:
        if language == "python":
            return """**Next Step:**
```python
def two_sum(nums, target):
    # Use a hash map to store values and their indices
    num_map = {}
```

**Why this step:**
A hash map allows us to look up complements in O(1) time, making the solution more efficient than nested loops.

**Learning tip:**
Hash maps are excellent for problems where you need to find pairs or check if values exist quickly."""
    
    if not current_code.strip():
        if language == "python":
            return """**Next Step:**
```python
def solve_problem(input_param):
    # Define your function with appropriate parameters
    # Consider what the function should return
    pass
```

**Why this step:**
Start with a proper function signature. Think about what inputs you need and what type of output is expected.

**Learning tip:**
Good function design starts with understanding the inputs and expected outputs."""
        elif language == "java":
            return """**Next Step:**
```java
public class Solution {
    public int solveProblem(int[] input) {
        // Define your method with proper parameters and return type
        return 0;
    }
}
```

**Why this step:**
Java requires explicit type declarations. Consider what data types your inputs and outputs should be.

**Learning tip:**
Strong typing in Java helps catch errors early and makes your code more robust."""
        else:  # javascript
            return """**Next Step:**
```javascript
function solveProblem(input) {
    // Start by defining your function
    // Consider what the function should return
    return null;
}
```

**Why this step:**
JavaScript functions should have clear purposes. Think about the expected input and output.

**Learning tip:**
Even though JavaScript is dynamically typed, it's good practice to be consistent with your data types."""
    
    return """**Next Step:**
Based on your current code, consider adding:
- Input validation (check for null/empty inputs)
- Main algorithm implementation
- Proper return statement

**Why this step:**
Building incrementally helps you catch errors early and understand each part of your solution.

**Learning tip:**
Test each small piece as you build it. This makes debugging much easier."""

def extract_test_cases(problem_statement: str, language: str) -> str:
    """Extract potential test cases from the problem statement
    
    Args:
        problem_statement: Description of the coding problem
        language: Programming language being used
        
    Returns:
        String containing extracted test cases formatted for the language
    """
    # Look for common test case indicators in the problem statement
    test_cases = []
    lines = problem_statement.split('\n')
    
    # Look for lines with 'Example', 'Input', 'Output', 'Test Case' keywords
    example_mode = False
    current_example = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for example section headers
        if any(keyword in line.lower() for keyword in ['example', 'test case', 'sample input', 'example input']):
            # If we have a complete example, add it before starting a new one
            if example_mode and 'input' in current_example and 'output' in current_example:
                test_cases.append(current_example)
            
            example_mode = True
            current_example = {}
            continue
            
        # Look for input/output pairs
        if example_mode:
            if any(keyword in line.lower() for keyword in ['input', 'input:']) and ':' in line:
                current_example['input'] = line.split(':', 1)[1].strip()
            elif any(keyword in line.lower() for keyword in ['output', 'output:', 'result', 'result:']) and ':' in line:
                current_example['output'] = line.split(':', 1)[1].strip()
                # Don't reset current_example here to handle multi-line examples
    
    # Add the last example if it's complete
    if example_mode and 'input' in current_example and 'output' in current_example:
        test_cases.append(current_example)
    
    # Look for patterns like "Given X, return Y" or "For input X, output should be Y"
    if not test_cases:
        for i, line in enumerate(lines):
            if i < len(lines) - 1:  # Ensure we have at least one more line
                current_line = line.lower()
                next_line = lines[i+1].lower() if i+1 < len(lines) else ""
                
                # Check for patterns like "Given [input], return [output]"
                if ('given' in current_line and 'return' in current_line) or \
                   ('input' in current_line and 'output' in next_line) or \
                   ('for example' in current_line):
                    
                    # Extract this line and the next few lines as a potential test case
                    example_text = ' '.join(lines[i:i+3])  # Take this line and next 2 lines
                    
                    # Try to extract input/output from the text
                    input_match = None
                    output_match = None
                    
                    if 'given' in example_text.lower() and 'return' in example_text.lower():
                        parts = example_text.split('return', 1)
                        if len(parts) > 1:
                            input_part = parts[0]
                            if 'given' in input_part.lower():
                                try:
                                    input_match = input_part.split('given', 1)[1].strip()
                                except IndexError:
                                    # Handle case where 'given' might be capitalized or part of another word
                                    input_match = input_part.split('Given', 1)[1].strip() if 'Given' in input_part else input_part.strip()
                            else:
                                input_match = input_part.strip()
                            output_match = parts[1].strip()
                    
                    if input_match and output_match:
                        test_cases.append({'input': input_match, 'output': output_match})
                    else:
                        test_cases.append({'description': example_text})
    
    # Look for code blocks that might contain examples
    code_block_mode = False
    code_block = ""
    for line in lines:
        line_stripped = line.strip()
        if line_stripped.startswith('```'):
            if code_block_mode:  # End of code block
                # Check if the code block contains test cases
                if ('assert' in code_block or 
                    'test(' in code_block.lower() or 
                    'expect(' in code_block.lower() or
                    'example' in code_block.lower()):
                    test_cases.append({'code_example': code_block})
                code_block = ""
                code_block_mode = False
            else:  # Start of code block
                code_block_mode = True
                # Skip language identifier if present (e.g., ```python)
                if len(line_stripped) > 3:
                    continue
        elif code_block_mode:
            code_block += line + "\n"
            
    # Special handling for JavaScript code examples with comments
    if language == "javascript" and not test_cases:
        for i, line in enumerate(lines):
            if '//' in line and ('return' in line.lower() or 'expect' in line.lower()):
                # This might be a JavaScript example with comments
                code_example = ""
                # Collect a few lines around this one
                start = max(0, i-2)
                end = min(len(lines), i+3)
                for j in range(start, end):
                    code_example += lines[j] + "\n"
                test_cases.append({'code_example': code_example})
    
    # Format the test cases according to the language
    formatted_tests = format_test_cases(test_cases, language)
    return formatted_tests

def format_test_cases(test_cases, language):
    """Format extracted test cases for the specific language"""
    if not test_cases:
        return ""
    
    # Define comment syntax based on language
    if language == "python":
        comment_prefix = "# "
        header = "# Test cases extracted from problem statement:\n"
    elif language in ["javascript", "java"]:
        comment_prefix = "// "
        header = "// Test cases extracted from problem statement:\n"
    else:
        comment_prefix = "# "
        header = "# Test cases extracted from problem statement:\n"
    
    result = header
    
    # Process each test case
    for i, test in enumerate(test_cases):
        if 'input' in test and 'output' in test:
            result += f"{comment_prefix}Test {i+1}: Input: {test['input']} | Expected Output: {test['output']}\n"
        elif 'description' in test:
            result += f"{comment_prefix}Test {i+1}: {test['description']}\n"
        elif 'code_example' in test:
            # Format code examples as executable test cases when possible
            code = test['code_example'].strip()
            result += f"{comment_prefix}Test example {i+1} (from code block):\n"
            
            # Try to convert code examples to actual test cases
            if language == "python":
                # Check if it's already a test function or assert statement
                if code.startswith("def test_") or "assert" in code:
                    result += code + "\n"
                else:
                    # Try to wrap it in a test function
                    result += f"""
# Example code that can be converted to test:
{code}
"""
            elif language == "javascript":
                if "test(" in code or "assert" in code or "expect(" in code:
                    result += code + "\n"
                else:
                    result += f"""
// Example code that can be converted to test:
{code}
"""
            elif language == "java":
                if "@Test" in code or "assert" in code:
                    result += code + "\n"
                else:
                    result += f"""
// Example code that can be converted to test:
{code}
"""
            else:
                result += f"{comment_prefix}Code example:\n{code}\n"
    
    # Try to generate actual test code based on extracted test cases
    if test_cases and language == "python":
        # Add a section with actual test code for Python
        input_output_pairs = [test for test in test_cases if 'input' in test and 'output' in test]
        if input_output_pairs:
            result += "\n# Generated test function:\n"
            result += "def test_solution():\n"
            for i, test in enumerate(input_output_pairs):
                result += f"    # Test case {i+1}\n"
                result += f"    assert solution({test['input']}) == {test['output']}\n"
    
    # Generate JavaScript test functions if needed
    elif test_cases and language == "javascript":
        # Look for code examples that might be function calls
        code_examples = []
        for test in test_cases:
            if 'code_example' in test:
                code = test['code_example']
                # Extract function calls from JavaScript code examples
                lines = code.split('\n')
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                        
                    # Handle both comment styles: // returns and /* returns */
                    if '//' in line:
                        parts = line.split('//', 1)
                        func_call = parts[0].strip()
                        comment = parts[1].strip()
                        
                        # Check if this is a function call with expected result
                        if func_call and ('return' in comment.lower() or 'expect' in comment.lower()):
                            expected = comment
                            if expected.startswith('returns '):  # Handle 'returns X' format
                                expected = expected[8:].strip()
                            code_examples.append((func_call, expected))
        
        # Generate Jest-style test function if we found examples
        if code_examples:
            result += "\n// Generated test function:\n"
            # Extract function name from the first example
            if code_examples:
                func_name = code_examples[0][0].split('(')[0]
                result += f"test('{func_name} function', () => {{\n"
                
                for func_call, expected in code_examples:
                    result += f"    expect({func_call}).toBe({expected});\n"
                
                result += "});\n"
        
        # If we didn't find any code examples but have code_example test cases,
        # try to generate a test function directly from the code
        if not code_examples:
            for test in test_cases:
                if 'code_example' in test:
                    code = test['code_example']
                    # Check if this looks like JavaScript function calls
                    if "(" in code and ")" in code and "'" in code:
                        # Try to extract function name and examples
                        func_name = None
                        examples = []
                        
                        lines = code.split('\n')
                        for line in lines:
                            line = line.strip()
                            if not line or line.startswith('```'):
                                continue
                                
                            # Look for function calls
                            if "(" in line and ")" in line:
                                # Extract function name
                                if not func_name and "(" in line:
                                    func_name = line.split("(")[0].strip()
                                
                                # Extract function call and expected result
                                if "//" in line:
                                    parts = line.split("//", 1)
                                    call = parts[0].strip()
                                    expected = parts[1].strip()
                                    if expected.startswith("returns"):
                                        expected = expected[7:].strip()
                                    examples.append((call, expected))
                        
                        if func_name and examples:
                            result += "\n// Generated test function:\n"
                            result += f"test('{func_name} function', () => {{\n"
                            
                            for call, expected in examples:
                                result += f"    expect({call}).toBe({expected});\n"
                            
                            result += "});\n"
    
    return result

def classify_problem_type(problem_statement: str) -> str:
    """Classify the type of coding problem based on keywords and patterns
    
    Args:
        problem_statement: Description of the coding problem
        
    Returns:
        String indicating the problem type
    """
    problem_lower = problem_statement.lower()
    
    # Check for common problem types
    if any(term in problem_lower for term in ['palindrome', 'mirror', 'reads the same']):
        return "palindrome"
    elif any(term in problem_lower for term in ['two sum', 'pair sum', 'find two numbers', 'sum to target']):
        return "two sum"
    elif any(term in problem_lower for term in ['fibonacci', 'sequence of numbers']):
        return "fibonacci"
    elif any(term in problem_lower for term in ['sort', 'arrange', 'order']):
        return "sorting"
    elif 'binary search' in problem_lower:
        return "binary search"
    elif any(term in problem_lower for term in ['search', 'find element', 'locate']):
        return "searching"
    elif any(term in problem_lower for term in ['tree', 'binary tree', 'node']):
        return "tree"
    elif any(term in problem_lower for term in ['graph', 'vertex', 'edge', 'connection']):
        return "graph"
    elif any(term in problem_lower for term in ['dynamic programming', 'dp', 'optimal substructure']):
        return "dynamic_programming"
    elif any(term in problem_lower for term in ['recursion', 'recursive']):
        return "recursion"
    elif any(term in problem_lower for term in ['string', 'substring', 'text']):
        return "string"
    elif any(term in problem_lower for term in ['array', 'list', 'elements']):
        return "array_manipulation"
    
    # Default
    return "general"

def generate_fallback_full_solution(problem_statement: str, current_code: str, language: str) -> str:
    """Generate fallback full solution when OpenAI is not available"""
    
    problem_lower = problem_statement.lower()
    problem_type = classify_problem_type(problem_statement)
    
    # Provide specific solutions for common problems
    if "palindrome" in problem_lower and language == "python":
        return """**Complete Solution:**
```python
def is_palindrome(x):
    # Handle negative numbers - they cannot be palindromes
    if x < 0:
        return False
    
    # Handle single digit numbers - they are palindromes
    if x < 10:
        return True
    
    # Convert to string and check if it reads the same forwards and backwards
    str_x = str(x)
    return str_x == str_x[::-1]

# Alternative solution without string conversion
def is_palindrome_no_string(x):
    if x < 0:
        return False
    
    # Reverse the number
    original = x
    reversed_num = 0
    
    while x > 0:
        reversed_num = reversed_num * 10 + x % 10
        x //= 10
    
    return original == reversed_num

# Test cases
test_cases = [121, -121, 10, 0, 1, 12321]
for test in test_cases:
    result1 = is_palindrome(test)
    result2 = is_palindrome_no_string(test)
    print(f"is_palindrome({test}) = {result1}, no_string = {result2}")
```

**Explanation:**
Two approaches are provided:
1. String method: Convert number to string and compare with its reverse
2. Mathematical method: Reverse the number mathematically and compare

**Key Concepts:**
- Edge case handling (negative numbers, single digits)
- String manipulation vs mathematical operations
- Algorithm efficiency trade-offs

**Complexity:**
- Time: O(log n) where n is the input number
- Space: O(1) for mathematical method, O(log n) for string method

**Test Cases Explained:**
- 121: Palindrome (reads same forwards/backwards)
- -121: Not palindrome (negative sign)
- 10: Not palindrome (01 ≠ 10)
- 0, 1: Single digits are palindromes

**Learning Notes:**
Consider both string and mathematical approaches. The mathematical method avoids string conversion as requested in many problem statements."""
    
    elif ("two sum" in problem_lower or "target" in problem_lower) and language == "python":
        return """**Complete Solution:**
```python
def two_sum(nums, target):
    # Use hash map for O(n) solution
    num_map = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    
    return []  # No solution found

# Test cases
test_cases = [
    ([2, 7, 11, 15], 9),
    ([3, 2, 4], 6),
    ([3, 3], 6),
    ([1, 2, 3], 7)
]

for nums, target in test_cases:
    result = two_sum(nums, target)
    print(f"two_sum({nums}, {target}) = {result}")
    if result:
        print(f"  Verification: {nums[result[0]]} + {nums[result[1]]} = {nums[result[0]] + nums[result[1]]}")
```

**Explanation:**
Uses a hash map to store numbers and their indices. For each number, we check if its complement (target - number) exists in the map.

**Key Concepts:**
- Hash map for O(1) lookups
- Single pass algorithm
- Complement calculation

**Complexity:**
- Time: O(n) - single pass through array
- Space: O(n) - hash map storage

**Test Cases Explained:**
- [2,7,11,15], target=9: indices [0,1] because 2+7=9
- [3,2,4], target=6: indices [1,2] because 2+4=6
- [3,3], target=6: indices [0,1] because 3+3=6

**Learning Notes:**
Hash maps are powerful for problems requiring fast lookups. This approach is much better than the O(n²) nested loop solution."""
    
    # Generic fallback for other problems
    if language == "python":
        return """**Complete Solution:**
```python
def solve_problem(input_data):
    # Generic template - customize based on your specific problem
    
    # Step 1: Validate input
    if not input_data:
        return None
    
    # Step 2: Initialize variables
    result = None
    
    # Step 3: Main algorithm (customize this part)
    # Add your specific logic here
    
    # Step 4: Return result
    return result

# Test the function with sample data
test_input = "sample_input"
result = solve_problem(test_input)
print(f"Result: {result}")

# Add more specific test cases based on your problem
```

**Explanation:**
This is a generic template. Customize the main algorithm section based on your specific problem requirements.

**Key Concepts:**
- Input validation
- Clear function structure
- Testing with sample data

**Complexity:**
- Time: Depends on your implementation
- Space: Depends on data structures used

**Learning Notes:**
Always start with input validation and clear function structure. Build your solution incrementally."""
    
    elif language == "java":
        return """**Complete Solution:**
```java
public class Solution {
    public int solveProblem(int[] input) {
        // Generic template - customize based on your problem
        
        // Step 1: Validate input
        if (input == null || input.length == 0) {
            return -1; // or appropriate default
        }
        
        // Step 2: Initialize variables
        int result = 0;
        
        // Step 3: Main algorithm (customize this part)
        // Add your specific logic here
        
        // Step 4: Return result
        return result;
    }
    
    public static void main(String[] args) {
        Solution solution = new Solution();
        int[] testInput = {1, 2, 3, 4, 5};
        int result = solution.solveProblem(testInput);
        System.out.println("Result: " + result);
    }
}
```

**Explanation:**
Generic Java template with proper structure and error handling.

**Key Concepts:**
- Object-oriented design
- Input validation
- Static main method for testing

**Learning Notes:**
Java's strong typing helps catch errors early. Always validate inputs and use appropriate return types."""
    
    else:  # javascript
        return """**Complete Solution:**
```javascript
function solveProblem(input) {
    // Generic template - customize based on your problem
    
    // Step 1: Validate input
    if (!input || input.length === 0) {
        return null;
    }
    
    // Step 2: Initialize variables
    let result = null;
    
    // Step 3: Main algorithm (customize this part)
    // Add your specific logic here
    
    // Step 4: Return result
    return result;
}

// Test the function
const testInput = [1, 2, 3, 4, 5];
const result = solveProblem(testInput);
console.log("Result:", result);

// Add more test cases as needed
```

**Explanation:**
Generic JavaScript template with modern syntax and proper structure.

**Key Concepts:**
- Function design
- Input validation
- Modern JavaScript syntax (const, let)

**Learning Notes:**
JavaScript's flexibility allows for various programming styles. Choose consistent patterns and validate inputs."""