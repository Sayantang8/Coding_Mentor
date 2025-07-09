#!/usr/bin/env python3
"""
Demo Example: Two Sum Problem
This demonstrates how the new AI Coding Mentor features work
"""

# Example problem statement for testing:
PROBLEM_STATEMENT = """
Two Sum Problem:
Given an array of integers nums and an integer target, 
return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, 
and you may not use the same element twice.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Because nums[0] + nums[1] = 2 + 7 = 9
"""

# Example progression using "Next Steps" button:

# Step 1: User starts with basic structure
CODE_STEP_1 = """
def two_sum(nums, target):
    # Need to find two numbers that add up to target
    pass

# Test
nums = [2, 7, 11, 15]
target = 9
result = two_sum(nums, target)
print(result)
"""

# After "Next Steps" guidance, user might add:
CODE_STEP_2 = """
def two_sum(nums, target):
    # Need to find two numbers that add up to target
    for i in range(len(nums)):
        # Check each number
        pass

# Test
nums = [2, 7, 11, 15]
target = 9
result = two_sum(nums, target)
print(result)
"""

# After more "Next Steps" guidance:
CODE_STEP_3 = """
def two_sum(nums, target):
    # Need to find two numbers that add up to target
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            # Check if two numbers add up to target
            pass

# Test
nums = [2, 7, 11, 15]
target = 9
result = two_sum(nums, target)
print(result)
"""

# Final step with "Next Steps":
CODE_STEP_4 = """
def two_sum(nums, target):
    # Need to find two numbers that add up to target
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

# Test
nums = [2, 7, 11, 15]
target = 9
result = two_sum(nums, target)
print(result)
"""

# What "Full Solution" button would provide:
FULL_SOLUTION_EXAMPLE = """
**Complete Solution:**
```python
def two_sum(nums, target):
    # Optimal approach using hash map
    num_map = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num] = i
    
    return []  # No solution found

# Test cases
def test_two_sum():
    # Test case 1
    nums1 = [2, 7, 11, 15]
    target1 = 9
    result1 = two_sum(nums1, target1)
    print(f"Test 1: {result1}")  # Expected: [0, 1]
    
    # Test case 2
    nums2 = [3, 2, 4]
    target2 = 6
    result2 = two_sum(nums2, target2)
    print(f"Test 2: {result2}")  # Expected: [1, 2]

test_two_sum()
```

**Explanation:**
1. We use a hash map (dictionary) to store numbers we've seen and their indices
2. For each number, we calculate its complement (target - current number)
3. If the complement exists in our hash map, we found our pair
4. Otherwise, we store the current number and its index for future lookups

**Key Concepts:**
- Hash map for O(1) lookup time
- Single pass through the array
- Space-time tradeoff optimization

**Complexity:**
- Time: O(n) - single pass through array
- Space: O(n) - hash map storage

**Learning Notes:**
- This is more efficient than the O(n²) brute force approach
- Hash maps are powerful for "find complement" problems
- Always consider edge cases and test with multiple inputs
"""

def main():
    print("🧠 AI Coding Mentor - Demo Example")
    print("=" * 50)
    print("\n📝 Problem Statement:")
    print(PROBLEM_STATEMENT)
    
    print("\n🎯 Learning Progression with 'Next Steps' Button:")
    print("\nStep 1 - Initial structure:")
    print(CODE_STEP_1)
    
    print("\nStep 2 - After first 'Next Steps' guidance:")
    print(CODE_STEP_2)
    
    print("\nStep 3 - After second 'Next Steps' guidance:")
    print(CODE_STEP_3)
    
    print("\nStep 4 - Final working solution:")
    print(CODE_STEP_4)
    
    print("\n🤖 What 'Full Solution' Button Provides:")
    print(FULL_SOLUTION_EXAMPLE)
    
    print("\n" + "=" * 50)
    print("🎓 Educational Benefits:")
    print("✅ Next Steps: Builds understanding incrementally")
    print("✅ Full Solution: Shows optimal approach and best practices")
    print("✅ Run Code: Tests each step immediately")
    print("✅ AI Context: Considers execution results for better guidance")

if __name__ == "__main__":
    main()