# 🧪 AI Coding Mentor Test Suite

This directory contains comprehensive tests and validation tools for the AI Coding Mentor project.

## 🔍 Test Files Overview

### 🚀 System Tests
- **[test_app.py](test_app.py)** - Main application functionality tests
- **[quick_test.py](quick_test.py)** - Fast system health check and verification
- **[test_encoding_fix.py](test_encoding_fix.py)** - Unicode encoding compatibility tests (Windows focus)
- **[test_templates.py](test_templates.py)** - Template system functionality validation
- **[test_model_config.py](test_model_config.py)** - Model configuration and GPT-4o-mini setup verification
- **[test_ui_layout.py](test_ui_layout.py)** - UI layout improvements and workflow verification
- **[test_embedded_output.py](test_embedded_output.py)** - Embedded output integration and styling verification

### 📚 Demonstrations
- **[demo_example.py](demo_example.py)** - Interactive feature showcase and examples

## 🎯 Running Tests

### Quick Verification
```bash
# Fast system check (recommended first step)
python tests/quick_test.py
```

### Comprehensive Testing
```bash
# Full application test suite
python tests/test_app.py

# Encoding compatibility (especially important on Windows)
python tests/test_encoding_fix.py

# Template functionality
python tests/test_templates.py

# Model configuration verification
python tests/test_model_config.py

# UI layout and workflow verification
python tests/test_ui_layout.py

# Embedded output integration verification
python tests/test_embedded_output.py
```

### Feature Demonstration
```bash
# View feature examples and use cases
python tests/demo_example.py
```

## 📊 Test Coverage

### ✅ Core Functionality
- **Application Startup**: Verifies all modules load correctly
- **Import Dependencies**: Checks all required packages are available
- **Configuration Loading**: Tests environment variable handling
- **Template Generation**: Validates code templates for all languages

### ✅ Code Execution
- **Python Execution**: Tests Python code running with proper output capture
- **Error Handling**: Verifies graceful error handling and reporting
- **Encoding Compatibility**: Ensures Unicode characters work on all platforms
- **Timeout Protection**: Tests execution time limits

### ✅ AI Integration
- **Function Loading**: Verifies AI helper functions import correctly
- **Fallback Modes**: Tests operation without OpenAI API
- **Template Functions**: Validates AI prompt generation

### ✅ Platform Compatibility
- **Windows Encoding**: Comprehensive Unicode handling tests
- **Cross-Platform**: File handling and path management
- **Environment Variables**: Configuration loading across platforms

## 🔧 Test Details

### test_app.py
**Purpose**: Main application integration testing
**Coverage**:
- Module imports and dependencies
- Core functionality verification
- Template system validation
- Basic execution testing

### quick_test.py
**Purpose**: Fast system health check
**Coverage**:
- Essential imports
- Basic functionality
- Quick execution test
- Dependency verification

### test_encoding_fix.py
**Purpose**: Unicode encoding compatibility
**Coverage**:
- Windows cp1252 encoding issues
- UTF-8 handling
- Error message encoding
- Multi-language output

### test_templates.py
**Purpose**: Template system validation
**Coverage**:
- Template generation for all languages
- Content validation
- Function availability
- Template completeness

### demo_example.py
**Purpose**: Feature demonstration
**Coverage**:
- Two Sum problem walkthrough
- Step-by-step learning progression
- AI assistance examples
- Educational workflow demonstration

## 🎯 Test Results Interpretation

### ✅ Success Indicators
- All imports successful
- Template functions working
- Code execution without errors
- Proper encoding handling

### ⚠️ Warning Signs
- Missing optional dependencies
- API key not configured
- Platform-specific issues
- Performance concerns

### ❌ Failure Indicators
- Import errors
- Template generation failures
- Encoding crashes
- Execution timeouts

## 🚀 Continuous Testing

### Before Each Release
```bash
# Run full test suite
python tests/test_app.py
python tests/test_encoding_fix.py
python tests/test_templates.py
```

### Development Workflow
```bash
# Quick check during development
python tests/quick_test.py

# Feature-specific testing
python tests/test_templates.py  # When working on templates
python tests/test_encoding_fix.py  # When modifying execution
```

### User Verification
```bash
# New installation verification
python tests/quick_test.py

# Troubleshooting
python tests/test_app.py  # For detailed diagnostics
```

## 📋 Test Maintenance

### Adding New Tests
1. Follow existing test patterns
2. Include both positive and negative test cases
3. Test error conditions and edge cases
4. Update this README with new test descriptions

### Test Dependencies
- Tests should work without external API keys
- Use fallback modes when possible
- Include clear error messages for missing dependencies
- Test both success and failure scenarios

---

**Note**: These tests are designed to work offline and don't require API keys for basic functionality verification.