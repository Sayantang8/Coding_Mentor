# 🧠 AI Coding Mentor

An advanced interactive web application built with Streamlit that helps users solve coding problems with AI assistance, real-time code execution, analysis, and intelligent suggestions.

## 🌟 Features

### 🎯 Core Functionality
- **Multi-language Support**: Python, Java, JavaScript with syntax highlighting
- **Interactive Code Editor**: Monaco/Ace editor with dark theme and professional styling
- **Real-time Code Execution**: Run code directly in the browser with immediate output
- **Embedded Output Display**: Results appear seamlessly below the editor
- **Problem Statement Input**: Clear description area for coding challenges
- **Template System**: Quick-start templates for common problems

### 🤖 AI-Powered Assistance (GPT-4o-mini)
- **💡 Get Hint**: Conceptual guidance without giving away solutions
- **✍️ Next Steps**: AI-suggested next 1-2 lines with explanations
- **🤖 Full Solution**: Complete reference solutions for learning
- **Context-Aware**: AI considers your code and execution results
- **Educational Focus**: Designed for learning, not just answers

### 🔍 Code Analysis (Python)
- **Linting**: Flake8 integration for code quality checks
- **Formatting**: Black formatter with before/after comparison
- **Complexity Analysis**: Radon-powered complexity and maintainability metrics
- **Real-time Feedback**: Instant analysis results

### 📊 Advanced Features
- **Export Reports**: Comprehensive JSON reports with all analysis and AI interactions
- **Session History**: Track your coding journey and AI responses
- **Unicode Support**: Full international character support across all platforms
- **Cross-Platform**: Windows, Mac, and Linux compatibility
- **Template Loading**: Basic templates and Two Sum problem examples

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (for AI features)

### Installation

1. **Clone or download the project**
```bash
cd "AI Mentor"
```

2. **Run the automated setup**
```bash
python setup.py
```

3. **Configure your API key**
```bash
cp .env.example .env
# Edit .env and add your API key (see Configuration section below)
```

4. **Verify installation (optional)**
```bash
# Quick system test
python tests/quick_test.py

# Full verification
python tests/test_app.py
```

5. **Start the application**
```bash
streamlit run app.py
```

### Manual Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export OPENAI_API_KEY=your_api_key_here  # Linux/Mac
set OPENAI_API_KEY=your_api_key_here     # Windows

# Run the app
streamlit run app.py
```

## 📁 Project Structure

```
AI Mentor/
├── 📄 Core Application
│   ├── app.py                 # Main Streamlit application with embedded output
│   ├── gpt_helper.py         # AI/GPT integration (GPT-4o-mini)
│   ├── code_analyzer.py      # Python code analysis tools
│   ├── utils.py              # Utility functions and helpers
│   └── config.py             # Configuration management
│
├── 🧪 tests/                 # Comprehensive Testing Suite
│   ├── test_app.py           # Main application functionality tests
│   ├── test_encoding_fix.py  # Unicode encoding compatibility tests
│   ├── test_templates.py     # Template system validation
│   ├── test_model_config.py  # GPT-4o-mini configuration tests
│   ├── test_ui_layout.py     # UI layout and workflow tests
│   ├── quick_test.py         # Fast system verification
│   └── demo_example.py       # Feature demonstration examples
│
├── ⚙️ Configuration
│   ├── requirements.txt      # Python dependencies
│   ├── setup.py             # Automated setup script
│   ├── .env.example         # Environment variables template
│   └── .env                 # Your environment variables (create this)
│
└── 📖 README.md             # Complete documentation (you're reading it!)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with your preferred configuration. The application now features a simplified interface that only displays API configuration status for enhanced privacy and cleaner UI.

#### OpenAI Official API (Recommended):
```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini
```

#### Optional Settings:
```env
OPENAI_ORG_ID=your_org_id_here
DEBUG=False
LOG_LEVEL=INFO
```

### Model Options

The application supports multiple AI models:
- **gpt-4o-mini** (default): Most cost-effective, excellent for coding
- **gpt-3.5-turbo**: Legacy option, good performance
- **gpt-4o**: Highest performance, more expensive

## 💡 Usage Guide

### 🎯 Getting Started Workflow

1. **Enter Problem Statement**
   - Describe your coding challenge clearly
   - Example: "Two Sum problem - find two numbers that add up to target"

2. **Choose Programming Language**
   - Select Python, Java, or JavaScript
   - Editor automatically adjusts syntax highlighting

3. **Write or Load Code**
   - Use the integrated code editor with dark theme
   - Load templates: Basic Template or Two Sum example
   - Code auto-saves as you type

4. **Run and Test**
   - Click "▶️ Run Code" (embedded below editor)
   - See output immediately in styled container
   - Clear output with 🗑️ button

5. **Get AI Assistance**
   - **💡 Get Hint**: Conceptual guidance for approach
   - **✍️ Next Steps**: Specific next lines with explanations
   - **🤖 Full Solution**: Complete reference implementation

6. **Analyze Code (Python)**
   - **🔍 Analyze Code**: Get linting, formatting, complexity analysis
   - View results in organized tabs

7. **Export Results**
   - **📄 Export Report**: Download comprehensive JSON report
   - Includes all code, analysis, and AI interactions

### 🎨 User Interface Features

#### Simplified Configuration Panel
- **Minimal Sidebar**: Clean interface with only essential information
- **API Status Indicator**: Simple ✅/❌ indicator for API configuration
- **Enhanced Privacy**: No detailed API information displayed
- **More Screen Space**: Maximized area for coding and problem-solving

#### Embedded Output Design
- **Seamless Integration**: Output appears directly below editor
- **Dark Theme**: Matches editor styling (#1e1e1e background)
- **Color Coding**: Green for success, red for errors
- **Monospace Font**: Courier New for code-like appearance
- **No Scrolling**: Results exactly where expected

#### AI Response Management
- **Newest First**: Latest AI responses appear at top
- **Smart Expansion**: Only newest response expanded by default
- **Clear History**: Remove all AI responses with one click
- **Timestamped**: All responses include creation time

#### Template System
- **📝 Basic Template**: Language-specific boilerplate code
- **🔄 Two Sum**: Complete problem setup with test cases
- **🧹 Clear Editor**: Reset editor content
- **🗑️ Clear Output**: Remove execution results

## 🛠️ Technical Implementation

### 🤖 AI Integration (GPT-4o-mini)
- **Context-Aware**: AI considers your code and execution results
- **Educational Focus**: Provides learning-oriented responses
- **Fallback Support**: Works without API key (limited functionality)
- **Error Handling**: Robust error handling with user-friendly messages

### ⚡ Code Execution Engine
- **Multi-Language**: Python, JavaScript (Node.js), Java
- **Unicode Safe**: Comprehensive encoding handling for all platforms
- **Timeout Protection**: 10-second execution limit
- **Error Capture**: Both stdout and stderr captured
- **Environment Setup**: Proper encoding configuration

### 🔍 Code Analysis (Python)
- **Flake8 Linting**: Style and error checking
- **Black Formatting**: Code formatting suggestions
- **Radon Complexity**: Cyclomatic complexity and maintainability
- **AST Fallback**: Basic analysis when tools unavailable

### 🎨 UI/UX Design
- **Responsive Layout**: Works on different screen sizes
- **Professional Styling**: IDE-like appearance
- **Embedded Output**: Seamless editor integration
- **Compact Controls**: Efficient space usage
- **Visual Hierarchy**: Clear information organization

## 🧪 Testing & Quality Assurance

### Comprehensive Test Suite

```bash
# System Integration Tests
python tests/test_app.py                    # Core functionality
python tests/test_encoding_fix.py           # Unicode compatibility
python tests/test_templates.py             # Template system
python tests/test_model_config.py          # GPT-4o-mini setup
python tests/test_ui_layout.py             # UI improvements

# Quick Verification
python tests/quick_test.py                  # Fast health check

# Feature Demonstrations
python tests/demo_example.py               # Interactive examples
```

### Test Coverage
- ✅ **Code Execution**: All languages with Unicode content
- ✅ **AI Integration**: Hint generation and response handling
- ✅ **Template System**: Loading and editor state management
- ✅ **Code Analysis**: Linting, formatting, complexity
- ✅ **UI Components**: Layout, styling, embedded output
- ✅ **Cross-Platform**: Windows, Mac, Linux compatibility
- ✅ **Error Handling**: Graceful degradation and fallbacks

### Quality Features
- **Unicode Support**: Full international character support
- **Error Recovery**: Robust error handling throughout
- **Performance**: Optimized for responsive user experience
- **Accessibility**: Clear visual hierarchy and intuitive controls

## 🔧 Development & Customization

### Adding New Features

The modular architecture supports easy extension:

```python
# AI Features (gpt_helper.py)
def new_ai_feature(problem, code, language):
    # Add new AI capabilities
    pass

# Code Analysis (code_analyzer.py)
def analyze_new_language(code):
    # Add support for new languages
    pass

# UI Components (app.py)
def new_ui_component():
    # Add new interface elements
    pass
```

### Configuration Options
- **Model Selection**: Easy switching between AI models
- **Theme Customization**: Modify editor and output styling
- **Language Support**: Add new programming languages
- **Analysis Tools**: Integrate additional code analysis tools

## 🔍 Troubleshooting

### Common Issues & Solutions

#### 1. API Configuration
```bash
# Check API key
echo $OPENAI_API_KEY  # Should show your key

# Test configuration
python tests/test_model_config.py
```

#### 2. Dependencies
```bash
# Install missing tools
pip install flake8 black radon

# Verify installation
python -c "from code_analyzer import check_dependencies; print(check_dependencies())"
```

#### 3. Unicode Issues (Windows)
```bash
# Test encoding fixes
python tests/test_encoding_fix.py

# Should show: "All encoding tests passed!"
```

#### 4. Streamlit Issues
```bash
# Update Streamlit
pip install --upgrade streamlit

# Clear cache
rm -rf .streamlit/  # Linux/Mac
rmdir /s .streamlit  # Windows

# Check port
netstat -an | grep 8501
```

### Fallback Modes
- **No API Key**: Basic functionality without AI features
- **Missing Tools**: AST-based analysis when linting tools unavailable
- **Network Issues**: Cached responses and offline operation
- **Platform Issues**: Cross-platform compatibility layers

## 📊 Dependencies & Requirements

### Core Dependencies
```
streamlit>=1.28.0          # Web application framework
streamlit-ace>=0.1.1       # Code editor component
openai>=1.0.0              # AI integration
python-dotenv>=1.0.0       # Environment management
```

### Code Analysis Tools
```
flake8>=6.0.0              # Python linting
black>=23.0.0              # Code formatting
radon>=6.0.0               # Complexity analysis
```

### System Requirements
- **Python**: 3.8 or higher
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB free space
- **Network**: Internet connection for AI features
- **Optional**: Node.js for JavaScript execution, Java for Java execution

## 🎯 Key Improvements & Features

### Recent Enhancements
- ✅ **GPT-4o-mini Integration**: Better performance at lower cost
- ✅ **Embedded Output**: Seamless editor integration
- ✅ **Unicode Compatibility**: Full Windows/international support
- ✅ **Template System**: Working template buttons with proper state management
- ✅ **UI Improvements**: Newest AI responses first, compact layout
- ✅ **Simplified Sidebar**: Minimal configuration display with enhanced privacy
- ✅ **Comprehensive Testing**: Full test suite with verification
- ✅ **Professional Styling**: IDE-like appearance with dark theme

### Educational Focus
- **Step-by-Step Learning**: AI provides educational guidance
- **Multiple Assistance Levels**: Hints, next steps, full solutions
- **Context Awareness**: AI considers execution results
- **Progress Tracking**: Session history and export capabilities

## 🚀 Getting Started Examples

### Example 1: Two Sum Problem
1. Click "🔄 Two Sum" to load template
2. Click "▶️ Run Code" to see initial output
3. Click "💡 Get Hint" for algorithmic guidance
4. Implement solution step by step
5. Use "✍️ Next Steps" for specific help
6. Click "🤖 Full Solution" for reference

### Example 2: Custom Problem
1. Enter problem in "Problem Statement" area
2. Choose your preferred language
3. Start coding in the editor
4. Run code frequently to test
5. Get AI assistance when stuck
6. Analyze code quality (Python)
7. Export final report

## 📄 License & Support

### License
This project is open source. Feel free to use, modify, and distribute.

### Support
- **Documentation**: This comprehensive README
- **Testing**: Run test suite for diagnostics
- **Issues**: Check troubleshooting section
- **Community**: Contribute improvements and bug fixes

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all tests pass
5. Submit a pull request

---

## 🎉 Summary

**AI Coding Mentor v2.0** is a comprehensive, professional-grade coding education platform featuring:

- 🤖 **GPT-4o-mini AI assistance** with educational focus
- ⚡ **Real-time code execution** for Python, Java, JavaScript
- 🎨 **Embedded output display** with professional styling
- 🔍 **Advanced code analysis** with linting and complexity metrics
- 🌍 **Full Unicode support** across all platforms
- 🧪 **Comprehensive testing** with quality assurance
- 🔒 **Privacy-focused UI** with simplified configuration display
- 📚 **Educational workflow** designed for learning

**Ready to enhance your coding skills with AI assistance!** 🚀

```bash
streamlit run app.py
```

### LICENSE

This project is licensed under the MIT License. For more details, please see the `LICENSE` file included in this repository.
