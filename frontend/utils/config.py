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
        "default": '# Write your Python 3 solution here\nimport sys\n\ndef solve():\n    data = sys.stdin.read().strip()\n    print(data)\n\nsolve()\n',
        1:  'import sys\n\ndef two_sum(nums, target):\n    # Write your solution here\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []\n\ndata = sys.stdin.read().split()\nnums = list(map(int, data[:-1]))\ntarget = int(data[-1])\nresult = two_sum(nums, target)\nprint(*result)\n',
        2:  'import sys\ns = sys.stdin.read().strip()\nprint(s[::-1])\n',
        3:  'n = int(input())\nfor i in range(1, n+1):\n    if i % 15 == 0: print("FizzBuzz")\n    elif i % 3 == 0: print("Fizz")\n    elif i % 5 == 0: print("Buzz")\n    else: print(i)\n',
        4:  'import sys\ns = sys.stdin.read().strip()\nclean = "".join(c.lower() for c in s if c.isalnum())\nprint("true" if clean == clean[::-1] else "false")\n',
        5:  'n = int(input())\na, b = 0, 1\nfor _ in range(n):\n    a, b = b, a+b\nprint(a)\n',
        6:  'import sys\ns = sys.stdin.read().strip()\nprint(sum(1 for c in s if c.lower() in "aeiou"))\n',
        7:  'import sys\nlines = sys.stdin.read().strip().split("\\n")\nnums = list(map(int, lines[0].split()))\ntarget = int(lines[1])\nl, r = 0, len(nums) - 1\nans = -1\nwhile l <= r:\n    m = (l + r) // 2\n    if nums[m] == target: ans = m; break\n    elif nums[m] < target: l = m + 1\n    else: r = m - 1\nprint(ans)\n',
        8:  'import sys\ns = sys.stdin.read().strip()\nst = []\nmatch = {")": "(", "}": "{", "]": "["}\nok = True\nfor ch in s:\n    if ch in "({[": st.append(ch)\n    elif not st or st[-1] != match.get(ch): ok = False; break\n    else: st.pop()\nprint("true" if ok and not st else "false")\n',
        9:  'import sys\nlines = sys.stdin.read().strip().split("\\n")\nprint("true" if sorted(lines[0]) == sorted(lines[1]) else "false")\n',
        10: 'import sys\nlines = sys.stdin.read().strip().split("\\n")\na = list(map(int, lines[0].split())) if lines[0].strip() else []\nb = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []\nprint(*(sorted(a + b)))\n',
    },
    "cpp": {
        "default": '#include <iostream>\n#include <vector>\n#include <string>\nusing namespace std;\n\nint main() {\n    // Write your C++17 solution here\n    cout << "Hello Code Quest!" << endl;\n    return 0;\n}\n',
        1:  '#include <iostream>\n#include <vector>\n#include <sstream>\n#include <unordered_map>\nusing namespace std;\n\nint main() {\n    vector<int> nums;\n    string line;\n    getline(cin, line);\n    istringstream ss(line);\n    int val;\n    while (ss >> val) nums.push_back(val);\n    int target;\n    cin >> target;\n    \n    unordered_map<int, int> seen;\n    for (int i = 0; i < nums.size(); i++) {\n        int comp = target - nums[i];\n        if (seen.count(comp)) {\n            cout << seen[comp] << " " << i << endl;\n            return 0;\n        }\n        seen[nums[i]] = i;\n    }\n    return 0;\n}\n',
        2:  '#include <iostream>\n#include <string>\n#include <algorithm>\nusing namespace std;\n\nint main() {\n    string s;\n    getline(cin, s);\n    reverse(s.begin(), s.end());\n    cout << s << endl;\n    return 0;\n}\n',
    },
    "c": {
        "default": '#include <stdio.h>\n#include <stdlib.h>\n#include <string.h>\n\nint main() {\n    // Write your C solution here\n    printf("Hello Code Quest!\\n");\n    return 0;\n}\n',
        2:  '#include <stdio.h>\n#include <string.h>\n\nint main() {\n    char s[1000];\n    if (fgets(s, sizeof(s), stdin)) {\n        int len = strlen(s);\n        while (len > 0 && (s[len-1] == \'\\n\' || s[len-1] == \'\\r\')) len--;\n        for (int i = len - 1; i >= 0; i--) putchar(s[i]);\n        putchar(\'\\n\');\n    }\n    return 0;\n}\n',
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
