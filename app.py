import streamlit as st
import json
import sys
import io
import subprocess
import tempfile
import os
from datetime import datetime
from streamlit_ace import st_ace

# Import our custom modules
from gpt_helper import generate_hint, help_me_write, generate_full_solution
from code_analyzer import analyze_python_code
from utils import export_report, get_language_mode
from config import get_config

# Configure the page
st.set_page_config(
    page_title="AI Coding Mentor",
    page_icon="🧠",
    layout="wide"
)

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'gpt_responses' not in st.session_state:
    st.session_state.gpt_responses = []
if 'code_history' not in st.session_state:
    st.session_state.code_history = []
if 'execution_output' not in st.session_state:
    st.session_state.execution_output = None
if 'execution_error' not in st.session_state:
    st.session_state.execution_error = None
if 'code_editor_content' not in st.session_state:
    st.session_state.code_editor_content = ""
if 'editor_key' not in st.session_state:
    st.session_state.editor_key = 0

def get_basic_template(language):
    """Get a basic code template for the specified language"""
    templates = {
        "python": """def main():
    # Write your code here
    pass

if __name__ == "__main__":
    main()""",
        "java": """public class Solution {
    public static void main(String[] args) {
        // Write your code here
        
    }
}""",
        "javascript": """function main() {
    // Write your code here
    
}

main();"""
    }
    return templates.get(language, "")

def get_two_sum_template(language):
    """Get a Two Sum problem template for the specified language"""
    templates = {
        "python": """def two_sum(nums, target):
    # Given an array of integers nums and an integer target,
    # return indices of the two numbers such that they add up to target.
    pass

# Test the function
nums = [2, 7, 11, 15]
target = 9
result = two_sum(nums, target)
print(f"Indices: {result}")""",
        "java": """import java.util.*;

public class Solution {
    public int[] twoSum(int[] nums, int target) {
        // Given an array of integers nums and an integer target,
        // return indices of the two numbers such that they add up to target.
        return new int[]{};
    }
    
    public static void main(String[] args) {
        Solution solution = new Solution();
        int[] nums = {2, 7, 11, 15};
        int target = 9;
        int[] result = solution.twoSum(nums, target);
        System.out.println("Indices: " + Arrays.toString(result));
    }
}""",
        "javascript": """function twoSum(nums, target) {
    // Given an array of integers nums and an integer target,
    // return indices of the two numbers such that they add up to target.
    
}

// Test the function
const nums = [2, 7, 11, 15];
const target = 9;
const result = twoSum(nums, target);
console.log("Indices:", result);"""
    }
    return templates.get(language, "")

def main():
    # Sidebar with minimal configuration info
    with st.sidebar:
        st.header("⚙️ Configuration")
        config = get_config()
        openai_config = config["openai"]
        
        # API Status - minimal information
        api_key_status = "✅ Configured" if openai_config["api_key"] else "❌ Missing"
        st.write(f"**API Status:** {api_key_status}")
        
        # Add other sidebar content here if needed
        st.markdown("---")

    # Main header
    st.title("🧠 AI Coding Mentor")
    st.markdown("*Your intelligent coding companion for problem-solving and code improvement*")
    
    # Add some spacing
    st.markdown("---")
    
    # Create layout columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Problem Statement")
        problem_statement = st.text_area(
            "Describe your coding problem:",
            placeholder="e.g., Two Sum problem - Given an array of integers and a target sum, find two numbers that add up to the target.",
            height=150,
            help="Enter a clear description of the coding problem you want to solve",
            key="problem_statement"
        )
    
    with col2:
        st.subheader("💻 Programming Language")
        language = st.selectbox(
            "Choose your preferred language:",
            options=["python", "java", "javascript"],
            index=0,
            help="Select the programming language for your solution",
            key="language_select"
        )
    
    # Code editor section
    st.markdown("---")
    st.subheader("✏️ Code Editor")
    
    # Add template buttons
    template_col1, template_col2, template_col3, template_col4 = st.columns(4)
    
    # Track button clicks
    basic_clicked = False
    two_sum_clicked = False
    clear_clicked = False
    clear_output_clicked = False
    
    with template_col1:
        if st.button("📝 Basic Template", help="Load a basic code template"):
            basic_clicked = True
    
    with template_col2:
        if st.button("🔄 Two Sum", help="Load Two Sum problem template"):
            two_sum_clicked = True
    
    with template_col3:
        if st.button("🧹 Clear Editor", help="Clear the code editor"):
            clear_clicked = True
    
    with template_col4:
        if st.button("🗑️ Clear Output", help="Clear execution results"):
            clear_output_clicked = True
    
    # Handle button clicks
    if basic_clicked:
        st.session_state.code_editor_content = get_basic_template(language)
        st.session_state.editor_key += 1
        st.rerun()
    
    if two_sum_clicked:
        st.session_state.code_editor_content = get_two_sum_template(language)
        st.session_state.editor_key += 1
        st.rerun()
    
    if clear_clicked:
        st.session_state.code_editor_content = ""
        st.session_state.editor_key += 1
        st.rerun()
    
    if clear_output_clicked:
        st.session_state.execution_output = None
        st.session_state.execution_error = None
        st.rerun()
    
    # Get initial value for code editor
    initial_code = st.session_state.get('code_editor_content', '')
    
    # Create a container for the integrated editor and output
    editor_container = st.container()
    
    with editor_container:
        # Code editor
        code = st_ace(
            value=initial_code,
            placeholder=f"Write your {language} code here...",
            language=get_language_mode(language),
            theme="monokai",
            key=f"code_editor_{st.session_state.editor_key}",
            height=400,
            auto_update=True,
            font_size=14,
            tab_size=4,
            wrap=False,
            annotations=None,
            markers=None
        )
        
        # Update session state with current editor content
        st.session_state.code_editor_content = code
        
        # Integrated control panel (compact, right below editor)
        control_col1, control_col2, control_col3 = st.columns([2, 2, 1])
        
        with control_col1:
            run_btn = st.button(
                "▶️ Run Code",
                help="Execute your code and see the output",
                use_container_width=True,
                type="primary"
            )
        
        with control_col2:
            analyze_btn = st.button(
                "🔍 Analyze Code",
                help="Run linting, formatting, and complexity analysis (Python only)",
                use_container_width=True
            )
        
        with control_col3:
            if st.button("🗑️", help="Clear output", use_container_width=True):
                st.session_state.execution_output = None
                st.session_state.execution_error = None
                st.rerun()
        
        # Embedded output section (seamlessly integrated with editor)
        if st.session_state.execution_output is not None or st.session_state.execution_error is not None:
            # Create a styled output container that looks like part of the editor
            st.markdown("""
            <style>
            .output-container {
                background-color: #1e1e1e;
                border: 1px solid #404040;
                border-top: none;
                border-radius: 0 0 8px 8px;
                margin-top: -8px;
                padding: 16px;
                font-family: 'Courier New', monospace;
                color: #d4d4d4;
            }
            .output-header {
                color: #569cd6;
                font-weight: bold;
                margin-bottom: 12px;
                font-size: 14px;
            }
            .success-output {
                background-color: #1b2d1b;
                border-left: 4px solid #4caf50;
                padding: 12px;
                margin: 8px 0;
                border-radius: 4px;
                color: #81c784;
            }
            .error-output {
                background-color: #2d1b1b;
                border-left: 4px solid #f44336;
                padding: 12px;
                margin: 8px 0;
                border-radius: 4px;
                color: #ef5350;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="output-container">', unsafe_allow_html=True)
            st.markdown('<div class="output-header">🖥️ Output</div>', unsafe_allow_html=True)
            
            # Display output content
            if st.session_state.execution_output:
                st.code(st.session_state.execution_output, language="text")
            
            if st.session_state.execution_error:
                st.markdown(f'''
                <div class="error-output">
                <strong>❌ Error:</strong><br>
                <pre style="margin: 8px 0 0 0; white-space: pre-wrap; font-family: inherit;">{st.session_state.execution_error}</pre>
                </div>
                ''', unsafe_allow_html=True)
            
            if not st.session_state.execution_output and not st.session_state.execution_error:
                st.markdown('''
                <div class="success-output">
                ✅ Code executed successfully with no output.
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Assistance section
    st.markdown("---")
    st.subheader("🤖 AI Assistance")
    
    # Create button columns for AI actions
    ai_col1, ai_col2, ai_col3, ai_col4 = st.columns(4)
    
    with ai_col1:
        hint_btn = st.button(
            "💡 Get Hint",
            help="Get a conceptual hint for your problem",
            use_container_width=True
        )
    
    with ai_col2:
        help_write_btn = st.button(
            "✍️ Next Steps",
            help="Get guidance for the next 1-2 lines of code",
            use_container_width=True
        )
    
    with ai_col3:
        generate_solution_btn = st.button(
            "🤖 Full Solution",
            help="Generate a complete solution (for reference/learning)",
            use_container_width=True
        )
    
    with ai_col4:
        export_btn = st.button(
            "📄 Export Report",
            help="Download analysis results and AI suggestions",
            use_container_width=True
        )
    
    # Handle button actions
    if run_btn:
        handle_run_code(code, language)
    
    if analyze_btn:
        handle_analyze_code(code, language)
    
    if hint_btn:
        handle_get_hint(problem_statement, code, language)
    
    if help_write_btn:
        handle_help_write(problem_statement, code, language)
    
    if generate_solution_btn:
        handle_generate_solution(problem_statement, code, language)
    
    if export_btn:
        handle_export_report(problem_statement, code, language)
    
    # Display AI responses first (newest first)
    display_ai_responses()
    
    # Display analysis results
    display_analysis_results()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 14px;'>
            AI Coding Mentor v2.0 - Interactive Coding Problem Solver with AI Assistance
        </div>
        """, 
        unsafe_allow_html=True
    )

def handle_run_code(code, language):
    """Handle run code button click"""
    if not code.strip():
        st.error("Please enter some code to run.")
        return
    
    with st.spinner(f"Running your {language} code..."):
        try:
            if language == "python":
                output, error = execute_python_code(code)
            elif language == "javascript":
                output, error = execute_javascript_code(code)
            elif language == "java":
                output, error = execute_java_code(code)
            else:
                st.error(f"Code execution not supported for {language}")
                return
            
            st.session_state.execution_output = output
            st.session_state.execution_error = error
            
            if error:
                st.error("Code execution completed with errors.")
            else:
                st.success("Code executed successfully!")
                
        except Exception as e:
            st.error(f"Execution failed: {str(e)}")
            st.session_state.execution_error = str(e)

def execute_python_code(code):
    """Execute Python code and capture output"""
    try:
        # Create a temporary file with UTF-8 encoding
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        
        # Set environment variables for proper encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONLEGACYWINDOWSSTDIO'] = '1'
        
        # Execute the code with comprehensive encoding handling
        try:
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=10,
                env=env
            )
        except UnicodeDecodeError:
            # Fallback: try with different encoding
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=False,  # Get bytes instead
                timeout=10,
                env=env
            )
            # Manually decode with error handling
            stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ""
            stderr = result.stderr.decode('utf-8', errors='replace') if result.stderr else ""
            # Create a mock result object
            class MockResult:
                def __init__(self, stdout, stderr, returncode):
                    self.stdout = stdout
                    self.stderr = stderr
                    self.returncode = returncode
            result = MockResult(stdout, stderr, result.returncode)
        
        # Clean up
        os.unlink(temp_file)
        
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out (10 seconds limit)"
    except Exception as e:
        return "", f"Error: {str(e)}"

def execute_javascript_code(code):
    """Execute JavaScript code using Node.js"""
    try:
        # Set environment for encoding
        env = os.environ.copy()
        env['NODE_OPTIONS'] = '--input-type=module'
        
        # Check if Node.js is available
        try:
            node_check = subprocess.run(
                ['node', '--version'], 
                capture_output=True, 
                text=True,
                encoding='utf-8',
                errors='replace',
                env=env
            )
        except UnicodeDecodeError:
            node_check = subprocess.run(
                ['node', '--version'], 
                capture_output=True, 
                text=False,
                env=env
            )
            node_check.stdout = node_check.stdout.decode('utf-8', errors='replace') if node_check.stdout else ""
            node_check.stderr = node_check.stderr.decode('utf-8', errors='replace') if node_check.stderr else ""
        
        if node_check.returncode != 0:
            return "", "Error: Node.js is not installed or not in PATH"
        
        # Create a temporary file with UTF-8 encoding
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
            f.write(code)
            temp_file = f.name
        
        # Execute the code with comprehensive encoding handling
        try:
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=10,
                env=env
            )
        except UnicodeDecodeError:
            result = subprocess.run(
                ['node', temp_file],
                capture_output=True,
                text=False,
                timeout=10,
                env=env
            )
            stdout = result.stdout.decode('utf-8', errors='replace') if result.stdout else ""
            stderr = result.stderr.decode('utf-8', errors='replace') if result.stderr else ""
            class MockResult:
                def __init__(self, stdout, stderr, returncode):
                    self.stdout = stdout
                    self.stderr = stderr
                    self.returncode = returncode
            result = MockResult(stdout, stderr, result.returncode)
        
        # Clean up
        os.unlink(temp_file)
        
        return result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out (10 seconds limit)"
    except Exception as e:
        return "", f"Error: {str(e)}"

def execute_java_code(code):
    """Execute Java code"""
    try:
        # Set environment for encoding
        env = os.environ.copy()
        env['JAVA_TOOL_OPTIONS'] = '-Dfile.encoding=UTF-8'
        
        # Check if Java is available
        try:
            java_check = subprocess.run(
                ['java', '--version'], 
                capture_output=True, 
                text=True,
                encoding='utf-8',
                errors='replace',
                env=env
            )
        except UnicodeDecodeError:
            java_check = subprocess.run(
                ['java', '--version'], 
                capture_output=True, 
                text=False,
                env=env
            )
            java_check.stdout = java_check.stdout.decode('utf-8', errors='replace') if java_check.stdout else ""
            java_check.stderr = java_check.stderr.decode('utf-8', errors='replace') if java_check.stderr else ""
        
        if java_check.returncode != 0:
            return "", "Error: Java is not installed or not in PATH"
        
        # Extract class name from code (simple approach)
        import re
        class_match = re.search(r'public\s+class\s+(\w+)', code)
        if not class_match:
            return "", "Error: No public class found in Java code"
        
        class_name = class_match.group(1)
        
        # Create temporary directory and file
        temp_dir = tempfile.mkdtemp()
        java_file = os.path.join(temp_dir, f"{class_name}.java")
        
        with open(java_file, 'w', encoding='utf-8') as f:
            f.write(code)
        
        # Compile the code with comprehensive encoding handling
        try:
            compile_result = subprocess.run(
                ['javac', '-encoding', 'UTF-8', java_file],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=10,
                env=env
            )
        except UnicodeDecodeError:
            compile_result = subprocess.run(
                ['javac', '-encoding', 'UTF-8', java_file],
                capture_output=True,
                text=False,
                timeout=10,
                env=env
            )
            compile_result.stdout = compile_result.stdout.decode('utf-8', errors='replace') if compile_result.stdout else ""
            compile_result.stderr = compile_result.stderr.decode('utf-8', errors='replace') if compile_result.stderr else ""
        
        if compile_result.returncode != 0:
            return "", f"Compilation Error: {compile_result.stderr}"
        
        # Run the code with comprehensive encoding handling
        try:
            run_result = subprocess.run(
                ['java', '-cp', temp_dir, class_name],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                timeout=10,
                env=env
            )
        except UnicodeDecodeError:
            run_result = subprocess.run(
                ['java', '-cp', temp_dir, class_name],
                capture_output=True,
                text=False,
                timeout=10,
                env=env
            )
            stdout = run_result.stdout.decode('utf-8', errors='replace') if run_result.stdout else ""
            stderr = run_result.stderr.decode('utf-8', errors='replace') if run_result.stderr else ""
            class MockResult:
                def __init__(self, stdout, stderr, returncode):
                    self.stdout = stdout
                    self.stderr = stderr
                    self.returncode = returncode
            run_result = MockResult(stdout, stderr, run_result.returncode)
        
        # Clean up
        import shutil
        shutil.rmtree(temp_dir)
        
        return run_result.stdout, run_result.stderr
        
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out (10 seconds limit)"
    except Exception as e:
        return "", f"Error: {str(e)}"

def handle_analyze_code(code, language):
    """Handle code analysis button click"""
    if not code.strip():
        st.error("Please enter some code to analyze.")
        return
    
    if language != "python":
        st.warning("Code analysis is currently only available for Python.")
        return
    
    with st.spinner("Analyzing your Python code..."):
        try:
            results = analyze_python_code(code)
            st.session_state.analysis_results = results
            st.success("Code analysis completed!")
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

def handle_get_hint(problem_statement, code, language):
    """Handle get hint button click"""
    if not problem_statement.strip():
        st.error("Please enter a problem statement to get a hint.")
        return
    
    with st.spinner("Generating hint..."):
        try:
            # Include execution output in hint generation
            execution_output = st.session_state.get('execution_output', '')
            execution_error = st.session_state.get('execution_error', '')
            
            hint = generate_hint(problem_statement, code, language, execution_output, execution_error)
            st.session_state.gpt_responses.append({
                "type": "hint",
                "content": hint,
                "timestamp": datetime.now().isoformat()
            })
            st.success("Hint generated!")
        except Exception as e:
            st.error(f"Failed to generate hint: {str(e)}")

def handle_help_write(problem_statement, code, language):
    """Handle next steps button click - provides small, educational code guidance"""
    if not problem_statement.strip():
        st.error("Please enter a problem statement to get coding help.")
        return
    
    with st.spinner("Generating next steps guidance..."):
        try:
            # Include execution output in code help generation
            execution_output = st.session_state.get('execution_output', '')
            execution_error = st.session_state.get('execution_error', '')
            
            suggestion = help_me_write(problem_statement, code, language, execution_output, execution_error)
            st.session_state.gpt_responses.append({
                "type": "next_steps",
                "content": suggestion,
                "timestamp": datetime.now().isoformat()
            })
            st.success("Next steps guidance generated!")
        except Exception as e:
            st.error(f"Failed to generate next steps guidance: {str(e)}")

def handle_generate_solution(problem_statement, code, language):
    """Handle generate full solution button click"""
    if not problem_statement.strip():
        st.error("Please enter a problem statement to generate a solution.")
        return
    
    with st.spinner("Generating complete solution..."):
        try:
            # Include execution output in solution generation
            execution_output = st.session_state.get('execution_output', '')
            execution_error = st.session_state.get('execution_error', '')
            
            solution = generate_full_solution(problem_statement, code, language, execution_output, execution_error)
            st.session_state.gpt_responses.append({
                "type": "full_solution",
                "content": solution,
                "timestamp": datetime.now().isoformat()
            })
            st.success("Complete solution generated!")
        except Exception as e:
            st.error(f"Failed to generate solution: {str(e)}")

def handle_export_report(problem_statement, code, language):
    """Handle export report button click"""
    try:
        report_data = {
            "problem_statement": problem_statement,
            "code": code,
            "language": language,
            "analysis_results": st.session_state.analysis_results,
            "gpt_responses": st.session_state.gpt_responses,
            "timestamp": datetime.now().isoformat()
        }
        
        report_content = export_report(report_data)
        
        st.download_button(
            label="📥 Download Report",
            data=report_content,
            file_name=f"coding_mentor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        st.success("Report ready for download!")
    except Exception as e:
        st.error(f"Failed to generate report: {str(e)}")

def display_ai_responses():
    """Display AI responses in reverse chronological order (newest first)"""
    if st.session_state.gpt_responses:
        # Add a clear button for AI responses
        clear_col1, clear_col2 = st.columns([3, 1])
        with clear_col2:
            if st.button("🗑️ Clear AI History", help="Clear all AI responses"):
                st.session_state.gpt_responses = []
                st.rerun()
        
        # Show all responses in reverse chronological order (newest first)
        for i, response in enumerate(reversed(st.session_state.gpt_responses)):
            response_number = len(st.session_state.gpt_responses) - i
            
            # Map response types to display names and icons
            type_mapping = {
                'hint': "💡 Hint",
                'next_steps': "✍️ Next Steps", 
                'code_help': "✍️ Code Help",  # Legacy support
                'full_solution': "🤖 Full Solution"
            }
            
            response_type = type_mapping.get(response['type'], f"🔧 {response['type'].title()}")
            timestamp = response['timestamp'][:19].replace('T', ' ')
            
            # Show newest responses expanded by default
            is_expanded = i == 0  # Only expand the very newest response
            
            with st.expander(f"{response_type} #{response_number} - {timestamp}", expanded=is_expanded):
                st.markdown(response["content"])

def display_analysis_results():
    """Display code analysis results"""
    if st.session_state.analysis_results:
        st.markdown("---")
        st.subheader("📊 Code Analysis Results")
        
        results = st.session_state.analysis_results
        
        # Create tabs for different analysis types
        tab1, tab2, tab3 = st.tabs(["🔍 Linting", "🎨 Formatting", "📈 Complexity"])
        
        with tab1:
            st.markdown("**Flake8 Linting Results:**")
            if results.get("lint_issues"):
                for issue in results["lint_issues"]:
                    st.warning(f"Line {issue['line']}: {issue['message']} ({issue['code']})")
            else:
                st.success("No linting issues found!")
        
        with tab2:
            st.markdown("**Black Formatting:**")
            if results.get("formatting_needed"):
                st.info("Code formatting suggestions available:")
                st.code(results.get("formatted_code", ""), language="python")
            else:
                st.success("Code is already well-formatted!")
        
        with tab3:
            st.markdown("**Radon Complexity Analysis:**")
            complexity = results.get("complexity", {})
            if complexity:
                st.metric("Cyclomatic Complexity", complexity.get("complexity", "N/A"))
                st.metric("Maintainability Index", complexity.get("maintainability", "N/A"))
            else:
                st.info("Complexity analysis not available")

if __name__ == "__main__":
    main()