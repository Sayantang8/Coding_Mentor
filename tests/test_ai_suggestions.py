#!/usr/bin/env python3
"""
Test script to verify AI suggestion functionality
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpt_helper import (
    generate_hint, 
    help_me_write, 
    generate_full_solution,
    get_openai_client,
    get_model_name,
    extract_test_cases,
    classify_problem_type
)

class TestAISuggestions(unittest.TestCase):
    """Test class for AI suggestion functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.problem_statement = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
        self.python_code = "def two_sum(nums, target):\n    pass"
        self.java_code = "public int[] twoSum(int[] nums, int target) {\n    return null;\n}"
        self.js_code = "function twoSum(nums, target) {\n    return null;\n}"
    
    @patch('gpt_helper.get_openai_client')
    def test_generate_hint(self, mock_get_client):
        """Test generate_hint function with mocked OpenAI client"""
        print("🧪 Testing generate_hint function...")
        
        # Mock the OpenAI client response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Consider using a hash map to store values you've seen."
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        # Test the function
        hint = generate_hint(self.problem_statement, self.python_code, "python")
        
        # Verify the result
        self.assertIsNotNone(hint)
        self.assertIn("hash map", hint)
        print(f"✅ generate_hint returned: {hint[:50]}...")
    
    @patch('gpt_helper.get_openai_client')
    def test_help_me_write(self, mock_get_client):
        """Test help_me_write function with mocked OpenAI client"""
        print("\n🧪 Testing help_me_write function...")
        
        # Mock the OpenAI client response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = """**Next Step:**
```python
def two_sum(nums, target):
    num_map = {}
```

**Why this step:**
A hash map allows us to look up complements in O(1) time."""
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        # Test the function
        suggestion = help_me_write(self.problem_statement, self.python_code, "python")
        
        # Verify the result
        self.assertIsNotNone(suggestion)
        self.assertIn("Next Step", suggestion)
        self.assertIn("num_map", suggestion)
        print(f"✅ help_me_write returned: {suggestion[:50]}...")
    
    @patch('gpt_helper.get_openai_client')
    def test_generate_full_solution(self, mock_get_client):
        """Test generate_full_solution function with mocked OpenAI client"""
        print("\n🧪 Testing generate_full_solution function...")
        
        # Mock the OpenAI client response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = """**Complete Solution:**
```python
def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    return []
```

**Explanation:**
We use a hash map to store each number and its index."""
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        # Test the function
        solution = generate_full_solution(self.problem_statement, self.python_code, "python")
        
        # Verify the result
        self.assertIsNotNone(solution)
        self.assertIn("Complete Solution", solution)
        self.assertIn("num_map", solution)
        print(f"✅ generate_full_solution returned: {solution[:50]}...")
    
    def test_fallback_responses(self):
        """Test fallback responses when OpenAI is not available"""
        print("\n🧪 Testing fallback responses...")
        
        # Temporarily unset OPENAI_API_KEY
        original_key = os.environ.get("OPENAI_API_KEY")
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        
        try:
            # Test fallback hint
            hint = generate_hint("two sum problem", self.python_code, "python")
            self.assertIsNotNone(hint)
            print(f"✅ Fallback hint: {hint[:50]}...")
            
            # Test fallback code help
            help_code = help_me_write("two sum problem", self.python_code, "python")
            self.assertIsNotNone(help_code)
            print(f"✅ Fallback code help: {help_code[:50]}...")
            
            # Test fallback full solution
            solution = generate_full_solution("two sum problem", self.python_code, "python")
            self.assertIsNotNone(solution)
            print(f"✅ Fallback solution: {solution[:50]}...")
            
        finally:
            # Restore original API key
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key
    
    def test_extract_test_cases(self):
        """Test the extract_test_cases function"""
        print("\n🧪 Testing test case extraction...")
        
        # Test with example format
        problem1 = "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\nExample: Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]"
        test_cases1 = extract_test_cases(problem1, "python")
        self.assertIn("nums = [2,7,11,15], target = 9", test_cases1)
        self.assertIn("[0,1]", test_cases1)
        print(f"✅ Extracted test cases from example format: {test_cases1[:50]}...")
        
        # Test with given/return format
        problem2 = "Given a string s, return true if it is a palindrome, or false otherwise.\nGiven s = 'racecar', return true\nGiven s = 'hello', return false"
        test_cases2 = extract_test_cases(problem2, "python")
        self.assertIn("s = 'racecar'", test_cases2)
        self.assertIn("true", test_cases2)
        self.assertIn("s = 'hello'", test_cases2)
        self.assertIn("false", test_cases2)
        print(f"✅ Extracted test cases from given/return format: {test_cases2[:50]}...")
        
        # Test with code block format
        problem3 = "Write a function to check if a number is prime.\n```\nassert is_prime(2) == True\nassert is_prime(4) == False\nassert is_prime(17) == True\n```"
        test_cases3 = extract_test_cases(problem3, "python")
        self.assertIn("is_prime(2) == True", test_cases3)
        self.assertIn("is_prime(4) == False", test_cases3)
        self.assertIn("is_prime(17) == True", test_cases3)
        print(f"✅ Extracted test cases from code block: {test_cases3[:50]}...")
    
    def test_classify_problem_type(self):
        """Test the classify_problem_type function"""
        print("\n🧪 Testing problem classification...")
        
        # Test with common problem types
        self.assertEqual(classify_problem_type("Check if a string is a palindrome"), "palindrome")
        self.assertEqual(classify_problem_type("Implement a function to find two numbers that add up to a target"), "two sum")
        self.assertEqual(classify_problem_type("Find the longest substring without repeating characters"), "string")
        self.assertEqual(classify_problem_type("Implement binary search algorithm"), "binary search")
        self.assertEqual(classify_problem_type("Implement merge sort algorithm"), "sorting")
        
        # Test with problem that doesn't match any specific type
        self.assertEqual(classify_problem_type("Create a function to calculate compound interest"), "general")
        
        print("✅ Problem classification tests passed")
    
    @patch('gpt_helper.get_openai_client')
    def test_retry_mechanism(self, mock_get_client):
        """Test the retry mechanism for OpenAI API calls"""
        print("\n🧪 Testing retry mechanism...")
        
        # Mock OpenAI client to fail on first call, succeed on second
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = [
            Exception("API Error"),  # First call fails
            MagicMock(choices=[MagicMock(message=MagicMock(content="Retry succeeded"))])  # Second call succeeds
        ]
        mock_get_client.return_value = mock_client
        
        # Test that retry works
        result = generate_hint("Test problem", "def test(): pass", "python")
        self.assertEqual(result, "Retry succeeded")
        self.assertEqual(mock_client.chat.completions.create.call_count, 2)  # Should have been called twice
        
        print("✅ Retry mechanism test passed")
    
    @patch('gpt_helper.get_openai_client')
    def test_integration_with_new_features(self, mock_get_client):
        """Test integration of test case extraction and problem classification"""
        print("\n🧪 Testing integration with new features...")
        
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Solution with test cases and classification"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        # Create a problem with test cases
        problem = "Write a function to check if a number is a palindrome. Example: Input: 121, Output: true"
        
        # Test generate_full_solution with the new features
        with patch('gpt_helper.extract_test_cases', return_value="Input: 121, Output: true") as mock_extract:
            with patch('gpt_helper.classify_problem_type', return_value="palindrome") as mock_classify:
                solution = generate_full_solution(problem, "def is_palindrome(x): pass", "python")
                
                # Verify the functions were called
                mock_extract.assert_called_once_with(problem, "python")
                mock_classify.assert_called_once_with(problem)
                
                # Verify the solution was returned
                self.assertEqual(solution, "Solution with test cases and classification")
                
                # Verify the extracted test cases and problem type were included in the prompt
                call_args = mock_client.chat.completions.create.call_args[1]
                messages = call_args['messages']
                user_message = [m for m in messages if m['role'] == 'user'][0]['content']
                self.assertIn("Input: 121, Output: true", user_message)
                self.assertIn("palindrome", user_message)
        
        print("✅ Integration test passed")

def main():
    """Run all tests"""
    print("🚀 AI Coding Mentor - AI Suggestions Test")
    print("=" * 50)
    
    # Run the tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    print("\n" + "=" * 50)
    print("🎉 AI suggestion tests completed!")

if __name__ == "__main__":
    main()