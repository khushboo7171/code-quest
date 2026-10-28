"""Code Quest configuration and constants."""
import os

API_BASE = "http://localhost:8080/api"
TOKEN_FILE = os.path.expanduser("~/.codequest_token")
APP_VERSION = "1.0.0"

LEVELS = {
    "Novice":     (0,    99,   "🌱"),
    "Apprentice": (100,  299,  "⚔️"),
    "Warrior":    (300,  599,  "🛡️"),
    "Champion":   (600,  999,  "🏆"),
    "Master":     (1000, 1999, "🌟"),
    "Legend":     (2000, float("inf"), "👑"),
}

LEVEL_ORDER = ["Novice", "Apprentice", "Warrior", "Champion", "Master", "Legend"]

DIFFICULTY_COLORS = {
    "easy":   "#2ecc71",
    "medium": "#f39c12",
    "hard":   "#e74c3c",
}

DIFFICULTY_TAGS = {
    "easy":   ("Easy",   "success"),
    "medium": ("Medium", "warning"),
    "hard":   ("Hard",   "danger"),
}

XP_VALUES = {"easy": 10, "medium": 25, "hard": 50}

SAMPLE_PROBLEMS = [
    {"id": 1,  "title": "Two Sum",              "difficulty": "easy",   "category": "Arrays",     "xp": 10},
    {"id": 2,  "title": "Reverse String",        "difficulty": "easy",   "category": "Strings",    "xp": 10},
    {"id": 3,  "title": "FizzBuzz",              "difficulty": "easy",   "category": "Math",       "xp": 10},
    {"id": 4,  "title": "Palindrome Check",      "difficulty": "easy",   "category": "Strings",    "xp": 10},
    {"id": 5,  "title": "Fibonacci Number",      "difficulty": "easy",   "category": "Math",       "xp": 10},
    {"id": 6,  "title": "Count Vowels",          "difficulty": "easy",   "category": "Strings",    "xp": 10},
    {"id": 7,  "title": "Binary Search",         "difficulty": "medium", "category": "Algorithms", "xp": 25},
    {"id": 8,  "title": "Valid Parentheses",     "difficulty": "medium", "category": "Stacks",     "xp": 25},
    {"id": 9,  "title": "Anagram Check",         "difficulty": "medium", "category": "Strings",    "xp": 25},
    {"id": 10, "title": "Merge Sorted Arrays",   "difficulty": "hard",   "category": "Arrays",     "xp": 50},
]

SAMPLE_PROBLEM_DETAIL = {
    "id": 1,
    "title": "Two Sum",
    "difficulty": "easy",
    "category": "Arrays",
    "xp": 10,
    "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.\n\nYou may assume each input has exactly one solution. You may not use the same element twice.",
    "examples": ["Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: nums[0] + nums[1] = 9"],
    "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9"],
    "hints": ["Use a hash map to store seen values", "For each number, check if target - number is in the map"],
    "visible_tests": [
        {"input": "2 7 11 15\n9", "expected": "0 1"},
        {"input": "3 2 4\n6",     "expected": "1 2"},
    ],
}

LOCAL_TEST_CASES = {
    1: [{"input": "2 7 11 15\n9", "expected": "0 1"}, {"input": "3 2 4\n6", "expected": "1 2"}],
    2: [{"input": "hello", "expected": "olleh"}, {"input": "world", "expected": "dlrow"}],
    3: [{"input": "5", "expected": "1\n2\nFizz\n4\nBuzz"}, {"input": "3", "expected": "1\n2\nFizz"}],
    4: [{"input": "racecar", "expected": "true"}, {"input": "hello", "expected": "false"}, {"input": "A man a plan a canal Panama", "expected": "true"}],
    5: [{"input": "6", "expected": "8"}, {"input": "10", "expected": "55"}, {"input": "0", "expected": "0"}],
    6: [{"input": "hello world", "expected": "3"}, {"input": "aeiou", "expected": "5"}, {"input": "xyz", "expected": "0"}],
    7: [{"input": "1 3 5 7 9\n7", "expected": "3"}, {"input": "1 2 3 4 5\n6", "expected": "-1"}],
    8: [{"input": "()", "expected": "true"}, {"input": "()[]{}", "expected": "true"}, {"input": "(]", "expected": "false"}],
    9: [{"input": "anagram\nnagaram", "expected": "true"}, {"input": "rat\ncar", "expected": "false"}],
    10: [{"input": "1 3 5\n2 4 6", "expected": "1 2 3 4 5 6"}, {"input": "1\n2", "expected": "1 2"}],
}

STARTER_CODE = {
    "python": {
        "default": 'class Solution:\n    def solve(self):\n        pass\n',
        1:  'class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        # Write your code here\n        pass\n',
        2:  'class Solution:\n    def reverseString(self, s: str) -> str:\n        # Write your code here\n        pass\n',
        3:  'class Solution:\n    def fizzBuzz(self, n: int) -> List[str]:\n        # Write your code here\n        pass\n',
        4:  'class Solution:\n    def isPalindrome(self, s: str) -> bool:\n        # Write your code here\n        pass\n',
        5:  'class Solution:\n    def fib(self, n: int) -> int:\n        # Write your code here\n        pass\n',
        6:  'class Solution:\n    def countVowels(self, s: str) -> int:\n        # Write your code here\n        pass\n',
        7:  'class Solution:\n    def search(self, nums: List[int], target: int) -> int:\n        # Write your code here\n        pass\n',
        8:  'class Solution:\n    def isValid(self, s: str) -> bool:\n        # Write your code here\n        pass\n',
        9:  'class Solution:\n    def isAnagram(self, s: str, t: str) -> bool:\n        # Write your code here\n        pass\n',
        10: 'class Solution:\n    def merge(self, nums1: List[int], nums2: List[int]) -> List[int]:\n        # Write your code here\n        pass\n',
    },
    "cpp": {
        "default": 'class Solution {\npublic:\n    void solve() {\n        \n    }\n};\n',
        1:  'class Solution {\npublic:\n    vector<int> twoSum(vector<int>& nums, int target) {\n        // Write your code here\n        \n    }\n};\n',
        2:  'class Solution {\npublic:\n    string reverseString(string s) {\n        // Write your code here\n        \n    }\n};\n',
        3:  'class Solution {\npublic:\n    vector<string> fizzBuzz(int n) {\n        // Write your code here\n        \n    }\n};\n',
        4:  'class Solution {\npublic:\n    bool isPalindrome(string s) {\n        // Write your code here\n        \n    }\n};\n',
        5:  'class Solution {\npublic:\n    int fib(int n) {\n        // Write your code here\n        \n    }\n};\n',
        6:  'class Solution {\npublic:\n    int countVowels(string s) {\n        // Write your code here\n        \n    }\n};\n',
        7:  'class Solution {\npublic:\n    int search(vector<int>& nums, int target) {\n        // Write your code here\n        \n    }\n};\n',
        8:  'class Solution {\npublic:\n    bool isValid(string s) {\n        // Write your code here\n        \n    }\n};\n',
        9:  'class Solution {\npublic:\n    bool isAnagram(string s, string t) {\n        // Write your code here\n        \n    }\n};\n',
        10: 'class Solution {\npublic:\n    vector<int> merge(vector<int>& nums1, vector<int>& nums2) {\n        // Write your code here\n        \n    }\n};\n',
    },
    "c": {
        "default": 'void solve() {\n    \n}\n',
        1:  '/**\n * Note: The returned array must be malloced, assume caller calls free().\n */\nint* twoSum(int* nums, int numsSize, int target, int* returnSize) {\n    // Write your code here\n    \n}\n',
        2:  'char* reverseString(char* s) {\n    // Write your code here\n    \n}\n',
        3:  '/**\n * Note: The returned array must be malloced, assume caller calls free().\n */\nchar** fizzBuzz(int n, int* returnSize) {\n    // Write your code here\n    \n}\n',
        4:  'bool isPalindrome(char* s) {\n    // Write your code here\n    \n}\n',
        5:  'int fib(int n) {\n    // Write your code here\n    \n}\n',
        6:  'int countVowels(char* s) {\n    // Write your code here\n    \n}\n',
        7:  'int search(int* nums, int numsSize, int target) {\n    // Write your code here\n    \n}\n',
        8:  'bool isValid(char* s) {\n    // Write your code here\n    \n}\n',
        9:  'bool isAnagram(char* s, char* t) {\n    // Write your code here\n    \n}\n',
        10: '/**\n * Note: The returned array must be malloced, assume caller calls free().\n */\nint* merge(int* nums1, int m, int* nums2, int n, int* returnSize) {\n    // Write your code here\n    \n}\n',
    },
}

BADGES = {
    "first_solve":    ("🎯", "First Blood",     "Solve your first problem"),
    "easy_5":         ("⭐", "Easy Street",     "Solve 5 easy problems"),
    "medium_3":       ("🔥", "Getting Serious", "Solve 3 medium problems"),
    "hard_1":         ("💎", "Diamond Mind",    "Solve a hard problem"),
    "xp_100":         ("🏅", "Century",         "Earn 100 XP"),
    "xp_500":         ("🥇", "Gold Rush",       "Earn 500 XP"),
    "streak_3":       ("🌊", "On a Roll",       "3-day streak"),
    "all_easy":       ("🌟", "Easy Master",     "Solve all easy problems"),
}
