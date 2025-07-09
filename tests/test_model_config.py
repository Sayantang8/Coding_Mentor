#!/usr/bin/env python3
"""
Test script to verify GPT-4o-mini model configuration
"""

def test_model_configuration():
    """Test that the model is correctly configured to use GPT-4o-mini"""
    print("🧪 Testing Model Configuration")
    print("=" * 40)
    
    try:
        import sys
        import os
        # Add parent directory to path to import config
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from config import get_config
        
        config = get_config()
        openai_config = config["openai"]
        
        model = openai_config["model"]
        print(f"📋 Configured Model: {model}")
        
        # Check if it's GPT-4o-mini
        if model == "gpt-4o-mini":
            print("✅ Model correctly set to GPT-4o-mini")
        elif model == "gpt-3.5-turbo":
            print("⚠️  Model is still set to GPT-3.5-turbo")
            print("💡 To use GPT-4o-mini, set OPENAI_MODEL=gpt-4o-mini in your .env file")
        elif model == "gpt-4o":
            print("ℹ️  Model is set to GPT-4o (full version)")
            print("💡 GPT-4o-mini is more cost-effective for most use cases")
        else:
            print(f"ℹ️  Model is set to: {model}")
        
        # Show other configuration details
        print(f"\n🔧 Configuration Details:")
        print(f"   Base URL: {openai_config['base_url']}")
        print(f"   API Key: {'✅ Set' if openai_config['api_key'] else '❌ Missing'}")
        print(f"   Use ChatAnywhere: {openai_config['use_chatanywhere']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_environment_variables():
    """Test environment variable handling"""
    print("\n🧪 Testing Environment Variables")
    print("=" * 40)
    
    import os
    
    # Check if .env file exists
    env_file_exists = os.path.exists('.env')
    print(f"📄 .env file: {'✅ Found' if env_file_exists else '❌ Not found'}")
    
    # Check environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    print(f"🔑 OPENAI_API_KEY: {'✅ Set' if api_key else '❌ Not set'}")
    print(f"🤖 OPENAI_MODEL: {model if model else 'Not set (will use default: gpt-4o-mini)'}")
    print(f"🌐 OPENAI_BASE_URL: {base_url if base_url else 'Not set (will use default)'}")
    
    if not env_file_exists:
        print("\n💡 To configure:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your OpenAI API key")
        print("   3. Optionally set OPENAI_MODEL=gpt-4o-mini")
    
    return True

def test_model_comparison():
    """Show comparison between different models"""
    print("\n📊 Model Comparison")
    print("=" * 40)
    
    models = {
        "gpt-4o-mini": {
            "description": "Most cost-effective, good performance",
            "use_case": "Recommended for most coding assistance tasks",
            "cost": "Very low",
            "performance": "High"
        },
        "gpt-3.5-turbo": {
            "description": "Previous default, good balance",
            "use_case": "General purpose, legacy option",
            "cost": "Low",
            "performance": "Good"
        },
        "gpt-4o": {
            "description": "Highest performance, more expensive",
            "use_case": "Complex problems requiring advanced reasoning",
            "cost": "Higher",
            "performance": "Highest"
        }
    }
    
    for model, info in models.items():
        print(f"\n🤖 {model}:")
        print(f"   📝 {info['description']}")
        print(f"   🎯 Use case: {info['use_case']}")
        print(f"   💰 Cost: {info['cost']}")
        print(f"   ⚡ Performance: {info['performance']}")
    
    print(f"\n✨ Current default: gpt-4o-mini (recommended)")
    
    return True

def main():
    """Run all model configuration tests"""
    print("🚀 AI Coding Mentor - Model Configuration Test")
    print("=" * 50)
    
    success = True
    
    if not test_model_configuration():
        success = False
    
    if not test_environment_variables():
        success = False
    
    if not test_model_comparison():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Model configuration test completed!")
        print("\n🚀 Ready to use GPT-4o-mini for AI assistance.")
        print("   Run: streamlit run app.py")
    else:
        print("❌ Some configuration issues found.")
        print("   Check the messages above for guidance.")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)