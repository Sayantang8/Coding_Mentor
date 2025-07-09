#!/usr/bin/env python3
"""
Simple test script to verify the AI Coding Mentor functionality
"""

import sys
import os
import tempfile
import subprocess

def test_python_execution():
    """Test Python code execution"""
    print("Testing Python code execution...")
    
    test_code = """
print("Hello, World!")
x = 5 + 3
print(f"5 + 3 = {x}")
"""
    
    try:
        # Create a temporary file with UTF-8 encoding
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(test_code)
            temp_file = f.name
        
        # Execute the code with proper encoding handling
        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            timeout=10
        )
        
        # Clean up
        os.unlink(temp_file)
        
        print("✅ Python execution successful!")
        print(f"Output: {result.stdout}")
        if result.stderr:
            print(f"Errors: {result.stderr}")
        
        return True
        
    except Exception as e:
        print(f"❌ Python execution failed: {e}")
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    modules = [
        'streamlit',
        'streamlit_ace', 
        'openai',
        'flake8',
        'black',
        'radon'
    ]
    
    success = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            success = False
    
    return success

def main():
    """Run all tests"""
    print("🧠 AI Coding Mentor - System Test")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    print()
    
    # Test Python execution
    if not test_python_execution():
        all_passed = False
    
    print()
    print("=" * 40)
    
    if all_passed:
        print("🎉 All tests passed! The AI Coding Mentor should work correctly.")
        print("Run: streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)