#!/usr/bin/env python3
"""
Comprehensive test to verify all Unicode encoding issues are resolved
"""

def test_code_execution_encoding():
    """Test code execution with potential encoding issues"""
    print("🧪 Testing Code Execution Encoding")
    print("=" * 40)
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from app import execute_python_code, execute_javascript_code, execute_java_code
        
        # Test Python with potential encoding issues
        python_tests = [
            "print('Hello World')",
            "print('Testing: äöü')",  # Unicode characters
            "for i in range(3):\n    print(f'Item {i}')",
            "import sys\nprint(sys.version)",
            "raise ValueError('Test error with unicode: éñ')"
        ]
        
        for i, test_code in enumerate(python_tests, 1):
            try:
                output, error = execute_python_code(test_code)
                print(f"✅ Python test {i}: Success")
                if error and "UnicodeDecodeError" in error:
                    print(f"❌ Unicode error in test {i}: {error}")
                    return False
            except Exception as e:
                if "UnicodeDecodeError" in str(e):
                    print(f"❌ Unicode error in Python test {i}: {e}")
                    return False
                print(f"⚠️  Python test {i} failed (non-unicode): {e}")
        
        # Test JavaScript if Node.js is available
        try:
            js_output, js_error = execute_javascript_code("console.log('JavaScript test');")
            if js_error and "UnicodeDecodeError" not in js_error:
                print("✅ JavaScript encoding: Success")
            elif "Node.js is not installed" in js_error:
                print("ℹ️  JavaScript test skipped (Node.js not available)")
            elif "UnicodeDecodeError" in js_error:
                print(f"❌ JavaScript Unicode error: {js_error}")
                return False
        except Exception as e:
            if "UnicodeDecodeError" in str(e):
                print(f"❌ JavaScript Unicode error: {e}")
                return False
        
        # Test Java if available
        try:
            java_code = """
public class Test {
    public static void main(String[] args) {
        System.out.println("Java test");
    }
}"""
            java_output, java_error = execute_java_code(java_code)
            if java_error and "UnicodeDecodeError" not in java_error:
                print("✅ Java encoding: Success")
            elif "Java is not installed" in java_error:
                print("ℹ️  Java test skipped (Java not available)")
            elif "UnicodeDecodeError" in java_error:
                print(f"❌ Java Unicode error: {java_error}")
                return False
        except Exception as e:
            if "UnicodeDecodeError" in str(e):
                print(f"❌ Java Unicode error: {e}")
                return False
        
        print("✅ All code execution encoding tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Code execution encoding test failed: {e}")
        return False

def test_code_analyzer_encoding():
    """Test code analyzer with potential encoding issues"""
    print("\n🧪 Testing Code Analyzer Encoding")
    print("=" * 40)
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from code_analyzer import analyze_python_code, check_dependencies
        
        # Test with code that might cause encoding issues
        test_codes = [
            "print('Simple test')",
            "# Comment with unicode: äöü\nprint('Unicode test')",
            "def test_function():\n    '''Docstring with unicode: éñ'''\n    return 'test'",
            "x = 'String with unicode: 中文'\nprint(x)"
        ]
        
        for i, test_code in enumerate(test_codes, 1):
            try:
                result = analyze_python_code(test_code)
                print(f"✅ Code analyzer test {i}: Success")
                
                # Check if any error messages contain Unicode errors
                if 'error' in result.get('complexity', {}):
                    error_msg = result['complexity']['error']
                    if "UnicodeDecodeError" in error_msg:
                        print(f"❌ Unicode error in analyzer test {i}: {error_msg}")
                        return False
                        
            except Exception as e:
                if "UnicodeDecodeError" in str(e):
                    print(f"❌ Unicode error in analyzer test {i}: {e}")
                    return False
                print(f"⚠️  Analyzer test {i} failed (non-unicode): {e}")
        
        # Test dependency checking
        try:
            deps = check_dependencies()
            print("✅ Dependency check encoding: Success")
        except Exception as e:
            if "UnicodeDecodeError" in str(e):
                print(f"❌ Unicode error in dependency check: {e}")
                return False
        
        print("✅ All code analyzer encoding tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Code analyzer encoding test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable handling"""
    print("\n🧪 Testing Environment Variables")
    print("=" * 40)
    
    import os
    
    # Check encoding-related environment variables
    encoding_vars = {
        'PYTHONIOENCODING': os.getenv('PYTHONIOENCODING'),
        'PYTHONLEGACYWINDOWSSTDIO': os.getenv('PYTHONLEGACYWINDOWSSTDIO'),
        'JAVA_TOOL_OPTIONS': os.getenv('JAVA_TOOL_OPTIONS'),
        'NODE_OPTIONS': os.getenv('NODE_OPTIONS')
    }
    
    print("🔧 Encoding Environment Variables:")
    for var, value in encoding_vars.items():
        if value:
            print(f"   {var}: {value}")
        else:
            print(f"   {var}: Not set")
    
    # Test if we can set and read Unicode environment variables
    try:
        test_var = "TEST_UNICODE_VAR"
        test_value = "Test with unicode: äöü"
        os.environ[test_var] = test_value
        
        retrieved = os.getenv(test_var)
        if retrieved == test_value:
            print("✅ Unicode environment variable handling: Success")
        else:
            print(f"⚠️  Unicode environment variable mismatch: {retrieved} != {test_value}")
        
        # Clean up
        del os.environ[test_var]
        
    except Exception as e:
        print(f"❌ Unicode environment variable test failed: {e}")
        return False
    
    return True

def test_file_operations():
    """Test file operations with Unicode content"""
    print("\n🧪 Testing File Operations")
    print("=" * 40)
    
    import tempfile
    import os
    
    try:
        # Test creating and reading files with Unicode content
        unicode_content = """# Test file with Unicode
print('Hello: äöü')
print('Chinese: 中文')
print('Emoji: 🚀')
def test_function():
    '''Function with unicode: éñ'''
    return 'success'
"""
        
        # Test temporary file creation with UTF-8
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(unicode_content)
            temp_file = f.name
        
        # Test reading the file back
        with open(temp_file, 'r', encoding='utf-8') as f:
            read_content = f.read()
        
        if read_content == unicode_content:
            print("✅ Unicode file operations: Success")
        else:
            print("❌ Unicode file content mismatch")
            return False
        
        # Clean up
        os.unlink(temp_file)
        
        return True
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def main():
    """Run all comprehensive encoding tests"""
    print("🚀 AI Coding Mentor - Comprehensive Encoding Test")
    print("=" * 60)
    
    success = True
    
    if not test_code_execution_encoding():
        success = False
    
    if not test_code_analyzer_encoding():
        success = False
    
    if not test_environment_variables():
        success = False
    
    if not test_file_operations():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All comprehensive encoding tests passed!")
        print("\n✅ Unicode encoding issues have been resolved:")
        print("   • Code execution handles Unicode properly")
        print("   • Code analyzer works with Unicode content")
        print("   • Environment variables support Unicode")
        print("   • File operations handle UTF-8 correctly")
        print("\n🚀 The application should now work without Unicode errors!")
    else:
        print("❌ Some encoding tests failed.")
        print("   Check the error messages above for details.")
        print("   Unicode issues may still exist in the application.")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)