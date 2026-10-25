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

STARTER_CODE = {
    "python": {
        "default": '# Write your solution here\n\ndef solve():\n    pass\n\nsolve()\n',
        1:  'import sys\n\ndef two_sum(nums, target):\n    # Your code here\n    pass\n\ndata = sys.stdin.read().split()\nnums = list(map(int, data[:-1]))\ntarget = int(data[-1])\nresult = two_sum(nums, target)\nprint(*result)\n',
        2:  'import sys\n\ns = sys.stdin.read().strip()\nprint(s[::-1])\n',
        3:  'n = int(input())\nfor i in range(1, n+1):\n    if i % 15 == 0: print("FizzBuzz")\n    elif i % 3 == 0: print("Fizz")\n    elif i % 5 == 0: print("Buzz")\n    else: print(i)\n',
        4:  'import sys\ns = sys.stdin.read().strip()\nclean = "".join(c.lower() for c in s if c.isalnum())\nprint("true" if clean == clean[::-1] else "false")\n',
        5:  'n = int(input())\na, b = 0, 1\nfor _ in range(n):\n    a, b = b, a+b\nprint(a)\n',
        6:  'import sys\ns = sys.stdin.read().strip()\nprint(sum(1 for c in s if c.lower() in "aeiou"))\n',
    },
    "cpp": {
        "default": '#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    // Your code here\n    return 0;\n}\n',
    },
    "c": {
        "default": '#include <stdio.h>\n#include <stdlib.h>\n\nint main() {\n    // Your code here\n    return 0;\n}\n',
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
