#!/usr/bin/env python3
"""
Test script to verify template functions work correctly
"""

def test_templates():
    """Test the template functions"""
    print("🧪 Testing Template Functions")
    print("=" * 40)
    
    # Import the template functions
    try:
        from app import get_basic_template, get_two_sum_template
        print("✅ Successfully imported template functions")
    except ImportError as e:
        print(f"❌ Failed to import template functions: {e}")
        return False
    
    # Test basic templates
    languages = ["python", "java", "javascript"]
    
    for lang in languages:
        print(f"\n📝 Testing {lang.title()} Templates:")
        
        # Test basic template
        basic = get_basic_template(lang)
        if basic and len(basic) > 10:
            print(f"✅ Basic template for {lang}: {len(basic)} characters")
        else:
            print(f"❌ Basic template for {lang} failed")
            return False
        
        # Test Two Sum template
        two_sum = get_two_sum_template(lang)
        if two_sum and len(two_sum) > 50:
            print(f"✅ Two Sum template for {lang}: {len(two_sum)} characters")
        else:
            print(f"❌ Two Sum template for {lang} failed")
            return False
    
    print("\n" + "=" * 40)
    print("🎉 All template tests passed!")
    
    # Show sample outputs
    print("\n📋 Sample Templates:")
    print("\n🐍 Python Basic Template:")
    print("-" * 30)
    print(get_basic_template("python"))
    
    print("\n☕ Java Two Sum Template (first 200 chars):")
    print("-" * 30)
    print(get_two_sum_template("java")[:200] + "...")
    
    return True

if __name__ == "__main__":
    test_templates()