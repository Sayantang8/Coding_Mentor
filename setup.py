"""
Setup script for AI Coding Mentor
Helps install dependencies and check system requirements
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        # Set environment for proper encoding
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            env=env
        )
        print("✅ All packages installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def check_environment_file():
    """Check if .env file exists and guide user"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            print("⚠️  .env file not found")
            print("📋 Please copy .env.example to .env and add your OpenAI API key:")
            print("   cp .env.example .env")
            print("   # Then edit .env with your API key")
        else:
            print("⚠️  Environment files not found")
            print("🔑 You'll need to set OPENAI_API_KEY environment variable")
        return False
    else:
        print("✅ .env file found")
        return True

def check_tools():
    """Check if code analysis tools are available"""
    tools = ["flake8", "black", "radon"]
    available_tools = []
    
    # Set environment for proper encoding
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    
    for tool in tools:
        try:
            subprocess.run(
                [tool, "--version"], 
                capture_output=True, 
                check=True,
                text=True,
                encoding='utf-8',
                errors='replace',
                env=env
            )
            available_tools.append(tool)
            print(f"✅ {tool} is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"⚠️  {tool} not found (will be installed)")
    
    return available_tools

def main():
    """Main setup function"""
    print("🧠 AI Coding Mentor Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check tools after installation
    print("\n🔧 Checking code analysis tools...")
    check_tools()
    
    # Check environment setup
    print("\n🔐 Checking environment configuration...")
    env_ready = check_environment_file()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    
    if env_ready:
        print("🚀 You can now run: streamlit run app.py")
    else:
        print("⚠️  Don't forget to set up your .env file with OpenAI API key")
        print("🚀 Then run: streamlit run app.py")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()