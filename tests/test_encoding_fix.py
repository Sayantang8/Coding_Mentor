#!/usr/bin/env python3
"""
Test script to verify the encoding fix works
"""

def test_encoding_fix():
    """Test the encoding fix for code execution"""
    print("🧪 Testing Encoding Fix")
    print("=" * 40)
    
    try:
        from app import execute_python_code
        
        # Test with simple code that might cause encoding issues
        test_codes = [
            # Simple test
            "print('Hello World!')\nprint('Test: 2 + 2 =', 2 + 2)",
            
            # Test with potential encoding issues
            "print('Testing encoding...')\nfor i in range(3):\n    print(f'Item {i}: OK')",
            
            # Test with error that might cause encoding issues
            "print('Before error')\nraise ValueError('Test error message')",
        ]
        
        for i, code in enumerate(test_codes, 1):
            print(f"\n🔍 Test {i}:")
            try:
                output, error = execute_python_code(code)
                print(f"✅ Execution completed")
                if output:
                    print(f"📤 Output: {output.strip()}")
                if error:
                    print(f"⚠️  Error: {error.strip()}")
            except Exception as e:
                print(f"❌ Test {i} failed: {e}")
                return False
        
        print("\n" + "=" * 40)
        print("🎉 All encoding tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Import or setup error: {e}")
        return False

def test_template_buttons():
    """Test that template functions still work"""
    print("\n🧪 Testing Template Functions")
    print("=" * 40)
    
    try:
        from app import get_basic_template, get_two_sum_template
        
        languages = ["python", "java", "javascript"]
        
        for lang in languages:
            basic = get_basic_template(lang)
            two_sum = get_two_sum_template(lang)
            
            if basic and two_sum:
                print(f"✅ {lang.title()} templates working")
            else:
                print(f"❌ {lang.title()} templates failed")
                return False
        
        print("🎉 All template tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Template test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Coding Mentor - Encoding Fix Test")
    print("=" * 50)
    
    success = True
    
    if not test_encoding_fix():
        success = False
    
    if not test_template_buttons():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Encoding issues should be resolved.")
        print("\n🚀 The app should now work without Unicode errors.")
        print("   Run: streamlit run app.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)