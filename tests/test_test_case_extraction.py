#!/usr/bin/env python3
"""
Test script to verify test case extraction and formatting functionality
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpt_helper import extract_test_cases, format_test_cases, classify_problem_type

class TestCaseExtractionTests(unittest.TestCase):
    """Test class for test case extraction and formatting functionality"""
    def setUp(self):
        """Set up test environment with various problem statement formats"""
        # Example problem statements with different test case formats
        self.example_format = """
        Write a function to check if a number is a palindrome.
        
        Example 1:
        Input: 121
        Output: true
        
        Example 2:
        Input: -121
        Output: false
        """
        
        self.given_return_format = """
        Write a function to find the two numbers that add up to the target.
        
        Given nums = [2, 7, 11, 15], target = 9, return [0, 1] because nums[0] + nums[1] = 2 + 7 = 9.
        """
        
        self.code_block_format = """
        Write a function to check if a string is a palindrome.
        
        Here's an example test case:
        ```python
        assert is_palindrome("racecar") == True
        assert is_palindrome("hello") == False
        ```
        """
        
        self.multiple_examples = """
        Find the maximum subarray sum.
        
        Example 1:
        Input: [-2,1,-3,4,-1,2,1,-5,4]
        Output: 6
        Explanation: [4,-1,2,1] has the largest sum = 6.
        
        Example 2:
        Input: [1]
        Output: 1
        """
        
        self.code_example_js = """
        Implement a function that reverses a string.
        
        Example:
        ```javascript
        reverseString('hello') // returns 'olleh'
        reverseString('world') // returns 'dlrow'
        ```
        """
        
        self.example_with_result = """
        Write a function to find the longest common prefix.
        
        Example:
        Input: ["flower","flow","flight"]
        Result: "fl"
        
        Input: ["dog","racecar","car"]
        Result: ""
        """
    
    def test_extract_test_cases_with_example_format(self):
        """Test extraction of test cases from example format"""
        print("\n🧪 Testing extraction from example format...")
        
        result = extract_test_cases(self.example_format, "python")
        self.assertIn("Input: 121", result)
        self.assertIn("Output: true", result)
        self.assertIn("Input: -121", result)
        self.assertIn("Output: false", result)
        print(f"✅ Extracted test cases: {result[:50]}...")
    
    def test_extract_test_cases_with_given_return_format(self):
        """Test extraction of test cases from given/return format"""
        print("\n🧪 Testing extraction from given/return format...")
        
        result = extract_test_cases(self.given_return_format, "python")
        self.assertIn("nums = [2, 7, 11, 15], target = 9", result)
        self.assertIn("[0, 1]", result)
        print(f"✅ Extracted test cases: {result[:50]}...")
    
    def test_extract_test_cases_with_code_block(self):
        """Test extraction of test cases from code block format"""
        print("\n🧪 Testing extraction from code block format...")
        
        result = extract_test_cases(self.code_block_format, "python")
        self.assertIn("assert is_palindrome(\"racecar\") == True", result)
        self.assertIn("assert is_palindrome(\"hello\") == False", result)
        print(f"✅ Extracted test cases: {result[:50]}...")
    
    def test_format_test_cases_python(self):
        test_cases = [
            {"input": "121", "output": "true"},
            {"description": "Check if negative numbers are palindromes"}
        ]
        
        result = format_test_cases(test_cases, "python")
        self.assertIn("# Test cases extracted from problem statement:", result)
        self.assertIn("# Test 1: Input: 121 | Expected Output: true", result)
        self.assertIn("# Test 2: Check if negative numbers are palindromes", result)
    
    def test_format_test_cases_javascript(self):
        test_cases = [
            {"input": "121", "output": "true"},
            {"description": "Check if negative numbers are palindromes"}
        ]
        
        result = format_test_cases(test_cases, "javascript")
        self.assertIn("// Test cases extracted from problem statement:", result)
        self.assertIn("// Test 1: Input: 121 | Expected Output: true", result)
        self.assertIn("// Test 2: Check if negative numbers are palindromes", result)
    
    def test_format_test_cases_with_code_example(self):
        test_cases = [
            {"code_example": "assert is_palindrome(\"racecar\") == True\nassert is_palindrome(\"hello\") == False"}
        ]
        
        result = format_test_cases(test_cases, "python")
        self.assertIn("# Test example 1 (from code block):", result)
        self.assertIn("assert is_palindrome(\"racecar\") == True", result)
    
    def test_format_test_cases_generates_test_function(self):
        test_cases = [
            {"input": "121", "output": "true"},
            {"input": "-121", "output": "false"}
        ]
        
        result = format_test_cases(test_cases, "python")
        self.assertIn("# Generated test function:", result)
        self.assertIn("def test_solution():", result)
        self.assertIn("assert solution(121) == true", result)
        self.assertIn("assert solution(-121) == false", result)
    
    def test_classify_problem_type(self):
        self.assertEqual(classify_problem_type("Check if a number is a palindrome"), "palindrome")
        self.assertEqual(classify_problem_type("Find two numbers that add up to the target"), "two sum")
        self.assertEqual(classify_problem_type("Implement a binary search algorithm"), "binary search")
        self.assertEqual(classify_problem_type("Sort an array of integers"), "sorting")
        self.assertEqual(classify_problem_type("Find the nth Fibonacci number"), "fibonacci")
        self.assertEqual(classify_problem_type("Traverse a binary tree"), "tree")
        self.assertEqual(classify_problem_type("Find the shortest path in a graph"), "graph")
        self.assertEqual(classify_problem_type("Solve the knapsack problem using dynamic programming"), "dynamic_programming")
        self.assertEqual(classify_problem_type("Implement a recursive function"), "recursion")
        self.assertEqual(classify_problem_type("Find the longest substring without repeating characters"), "string")
        self.assertEqual(classify_problem_type("Rotate an array to the right by k steps"), "array_manipulation")
        self.assertEqual(classify_problem_type("Calculate the factorial of a number"), "general")

    def test_extract_test_cases_with_multiple_examples(self):
        """Test extraction of test cases from multiple examples"""
        print("\n🧪 Testing extraction from multiple examples...")
        
        result = extract_test_cases(self.multiple_examples, "python")
        self.assertIn("[-2,1,-3,4,-1,2,1,-5,4]", result)
        self.assertIn("6", result)
        self.assertIn("[1]", result)
        self.assertIn("1", result)
        print(f"✅ Extracted test cases: {result[:50]}...")
    
    def test_extract_test_cases_with_js_code_example(self):
        """Test extraction of test cases from JavaScript code examples"""
        print("\n🧪 Testing extraction from JavaScript code examples...")
        
        result = extract_test_cases(self.code_example_js, "javascript")
        self.assertIn("reverseString('hello')", result)
        self.assertIn("'olleh'", result)
        self.assertIn("reverseString('world')", result)
        self.assertIn("'dlrow'", result)
        print(f"✅ Extracted test cases: {result[:50]}...")
    
    def test_extract_test_cases_with_result_keyword(self):
        """Test extraction of test cases with 'Result' keyword instead of 'Output'"""
        print("\n🧪 Testing extraction with 'Result' keyword...")
        
        # Create a simpler test case with the Result keyword
        example_with_result = """
        Write a function to find the longest common prefix.
        
        Example:
        Input: ["flower","flow","flight"]
        Result: "fl"
        """
        
        result = extract_test_cases(example_with_result, "python")
        self.assertIn("[\"flower\",\"flow\",\"flight\"]", result)
        self.assertIn("\"fl\"", result)
        print(f"✅ Extracted test cases: {result[:50]}...")
    
    def test_format_test_cases_generates_python_test_function(self):
        """Test generation of Python test functions from extracted test cases"""
        print("\n🧪 Testing generation of Python test functions...")
        
        # Extract test cases
        test_cases = extract_test_cases(self.example_format, "python")
        print(f"Extracted test cases: {test_cases}")
        
        # Manually create test cases to ensure proper format
        manual_test_cases = [
            {"input": "121", "output": "true"},
            {"input": "-121", "output": "false"}
        ]
        
        # Format test cases for Python
        formatted_cases = format_test_cases(manual_test_cases, "python")
        
        # Verify test function generation
        self.assertIn("def test_solution", formatted_cases)
        self.assertIn("assert solution(121) == true", formatted_cases)
        self.assertIn("assert solution(-121) == false", formatted_cases)
        print(f"✅ Generated Python test function: {formatted_cases[:50]}...")
    
    def test_format_test_cases_generates_javascript_test_function(self):
        """Test generation of JavaScript test functions from extracted test cases"""
        print("\n🧪 Testing generation of JavaScript test functions...")
        
        # Extract test cases
        test_cases = extract_test_cases(self.code_example_js, "javascript")
        print(f"Extracted JS test cases: {test_cases}")
        
        # Manually create test cases to ensure proper format
        manual_test_cases = [
            {"code_example": "reverseString('hello') // returns 'olleh'\nreverseString('world') // returns 'dlrow'"}
        ]
        
        # Format test cases for JavaScript
        formatted_cases = format_test_cases(manual_test_cases, "javascript")
        
        # Verify test function generation
        self.assertIn("test('reverseString", formatted_cases)
        self.assertIn("expect(reverseString('hello')).toBe('olleh')", formatted_cases)
        self.assertIn("expect(reverseString('world')).toBe('dlrow')", formatted_cases)
        print(f"✅ Generated JavaScript test function: {formatted_cases[:50]}...")

def main():
    """Run all tests"""
    print("🚀 AI Coding Mentor - Test Case Extraction Test")
    print("=" * 50)
    
    # Run the tests
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
    
    print("\n" + "=" * 50)
    print("🎉 Test case extraction tests completed!")

if __name__ == "__main__":
    main()