#!/usr/bin/env python3
"""
Quick test to verify the app can start without errors
"""

import sys
import os

def test_app_imports():
    """Test that the app can be imported without errors"""
    print("🧪 Testing App Imports...")
    
    try:
        # Test basic imports
        import streamlit as st
        print("✅ Streamlit imported")
        
        import streamlit_ace
        print("✅ Streamlit-ace imported")
        
        # Test our modules
        from gpt_helper import generate_hint, help_me_write, generate_full_solution
        print("✅ GPT helper functions imported")
        
        from code_analyzer import analyze_python_code
        print("✅ Code analyzer imported")
        
        from utils import export_report, get_language_mode
        print("✅ Utils imported")
        
        from config import get_config
        print("✅ Config imported")
        
        # Test template functions
        from app import get_basic_template, get_two_sum_template
        print("✅ Template functions imported")
        
        # Test template content
        basic_py = get_basic_template("python")
        two_sum_py = get_two_sum_template("python")
        
        if basic_py and two_sum_py:
            print("✅ Template functions working")
        else:
            print("❌ Template functions not working")
            return False
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_execution_functions():
    """Test code execution functions"""
    print("\n🧪 Testing Code Execution...")
    
    try:
        from app import execute_python_code
        
        # Test simple Python code
        test_code = "print('Hello from test!')\nresult = 2 + 2\nprint(f'2 + 2 = {result}')"
        output, error = execute_python_code(test_code)
        
        if "Hello from test!" in output and "2 + 2 = 4" in output:
            print("✅ Python execution working")
            return True
        else:
            print(f"❌ Python execution failed. Output: {output}, Error: {error}")
            return False
            
    except Exception as e:
        print(f"❌ Execution test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Coding Mentor - Quick Test")
    print("=" * 40)
    
    success = True
    
    if not test_app_imports():
        success = False
    
    if not test_execution_functions():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 All tests passed! App should work correctly.")
        print("\n🚀 To start the app, run:")
        print("   streamlit run app.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)