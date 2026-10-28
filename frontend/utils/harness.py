"""
LeetCode-style code harness and driver wrappers.
Wraps user's Solution class or function with standard library imports
and a test driver so users only write the function logic.
"""

def wrap_user_code(problem_id: int, user_code: str, language: str) -> str:
    """Wraps user code with driver code if not already providing a main."""
    user_code_stripped = user_code.strip()

    if language == "python":
        # If user wrote manual sys.stdin / script execution, don't double-wrap
        if "sys.stdin" in user_code and "class Solution" not in user_code:
            return user_code
        return _wrap_python(problem_id, user_code)

    elif language == "cpp":
        if "int main(" in user_code and "class Solution" not in user_code:
            return user_code
        return _wrap_cpp(problem_id, user_code)

    elif language == "c":
        if "int main(" in user_code:
            return user_code
        return _wrap_c(problem_id, user_code)

    return user_code


def _wrap_python(pid: int, code: str) -> str:
    headers = "from typing import List, Dict, Tuple, Set, Optional\nimport sys, math, collections, heapq\n\n"
    
    drivers = {
        1: """
def _driver():
    data = sys.stdin.read().split()
    if not data: return
    nums = list(map(int, data[:-1]))
    target = int(data[-1])
    sol = Solution()
    res = sol.twoSum(nums, target)
    if res is not None:
        print(*(sorted(res)))
_driver()
""",
        2: """
def _driver():
    s = sys.stdin.read().strip()
    sol = Solution()
    res = sol.reverseString(s)
    print(res)
_driver()
""",
        3: """
def _driver():
    line = sys.stdin.read().strip()
    if not line: return
    n = int(line)
    sol = Solution()
    res = sol.fizzBuzz(n)
    if res:
        for x in res:
            print(x)
_driver()
""",
        4: """
def _driver():
    s = sys.stdin.read().strip()
    sol = Solution()
    res = sol.isPalindrome(s)
    print("true" if res else "false")
_driver()
""",
        5: """
def _driver():
    line = sys.stdin.read().strip()
    if not line: return
    n = int(line)
    sol = Solution()
    print(sol.fib(n))
_driver()
""",
        6: """
def _driver():
    s = sys.stdin.read().strip()
    sol = Solution()
    print(sol.countVowels(s))
_driver()
""",
        7: """
def _driver():
    lines = sys.stdin.read().strip().split("\\n")
    if not lines or not lines[0]: return
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    sol = Solution()
    print(sol.search(nums, target))
_driver()
""",
        8: """
def _driver():
    s = sys.stdin.read().strip()
    sol = Solution()
    print("true" if sol.isValid(s) else "false")
_driver()
""",
        9: """
def _driver():
    lines = sys.stdin.read().strip().split("\\n")
    if len(lines) < 2: return
    s, t = lines[0].strip(), lines[1].strip()
    sol = Solution()
    print("true" if sol.isAnagram(s, t) else "false")
_driver()
""",
        10: """
def _driver():
    lines = sys.stdin.read().strip().split("\\n")
    a = list(map(int, lines[0].split())) if lines and lines[0].strip() else []
    b = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []
    sol = Solution()
    res = sol.merge(a, b)
    if res:
        print(*res)
_driver()
""",
    }

    driver = drivers.get(pid, """
def _driver():
    s = sys.stdin.read().strip()
    sol = Solution()
    for method in dir(sol):
        if not method.startswith('_'):
            fn = getattr(sol, method)
            try:
                print(fn(s))
                return
            except Exception:
                pass
_driver()
""")
    return headers + code + "\n\n" + driver


def _wrap_cpp(pid: int, code: str) -> str:
    headers = """#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <map>
#include <set>
#include <queue>
#include <stack>
#include <cmath>
using namespace std;

"""

    drivers = {
        1: """
int main() {
    string line;
    if (!getline(cin, line)) return 0;
    istringstream ss(line);
    vector<int> nums;
    int x;
    while (ss >> x) nums.push_back(x);
    int target;
    if (!(cin >> target)) return 0;
    Solution sol;
    vector<int> res = sol.twoSum(nums, target);
    sort(res.begin(), res.end());
    for (int i = 0; i < (int)res.size(); i++) {
        if (i) cout << " ";
        cout << res[i];
    }
    cout << endl;
    return 0;
}
""",
        2: """
int main() {
    string s;
    if (getline(cin, s)) {
        Solution sol;
        cout << sol.reverseString(s) << endl;
    }
    return 0;
}
""",
        3: """
int main() {
    int n;
    if (cin >> n) {
        Solution sol;
        vector<string> res = sol.fizzBuzz(n);
        for (const auto& s : res) cout << s << endl;
    }
    return 0;
}
""",
        4: """
int main() {
    string s;
    if (getline(cin, s)) {
        Solution sol;
        cout << (sol.isPalindrome(s) ? "true" : "false") << endl;
    }
    return 0;
}
""",
        5: """
int main() {
    int n;
    if (cin >> n) {
        Solution sol;
        cout << sol.fib(n) << endl;
    }
    return 0;
}
""",
        6: """
int main() {
    string s;
    if (getline(cin, s)) {
        Solution sol;
        cout << sol.countVowels(s) << endl;
    }
    return 0;
}
""",
        7: """
int main() {
    string line;
    if (!getline(cin, line)) return 0;
    istringstream ss(line);
    vector<int> nums;
    int x;
    while (ss >> x) nums.push_back(x);
    int target;
    if (!(cin >> target)) return 0;
    Solution sol;
    cout << sol.search(nums, target) << endl;
    return 0;
}
""",
        8: """
int main() {
    string s;
    if (getline(cin, s)) {
        Solution sol;
        cout << (sol.isValid(s) ? "true" : "false") << endl;
    }
    return 0;
}
""",
        9: """
int main() {
    string s, t;
    if (getline(cin, s) && getline(cin, t)) {
        Solution sol;
        cout << (sol.isAnagram(s, t) ? "true" : "false") << endl;
    }
    return 0;
}
""",
        10: """
int main() {
    string l1, l2;
    getline(cin, l1);
    getline(cin, l2);
    vector<int> a, b;
    int x;
    istringstream s1(l1), s2(l2);
    while (s1 >> x) a.push_back(x);
    while (s2 >> x) b.push_back(x);
    Solution sol;
    vector<int> res = sol.merge(a, b);
    for (int i = 0; i < (int)res.size(); i++) {
        if (i) cout << " ";
        cout << res[i];
    }
    cout << endl;
    return 0;
}
""",
    }

    driver = drivers.get(pid, "int main() { return 0; }\n")
    return headers + code + "\n\n" + driver


def _wrap_c(pid: int, code: str) -> str:
    headers = """#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

"""

    drivers = {
        1: """
int main() {
    int nums[10000];
    int n = 0;
    char line[10000];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    char* tok = strtok(line, " \\t\\r\\n");
    while (tok) {
        nums[n++] = atoi(tok);
        tok = strtok(NULL, " \\t\\r\\n");
    }
    int target;
    if (scanf("%d", &target) != 1) return 0;
    int retSize = 0;
    int* res = twoSum(nums, n, target, &retSize);
    if (res && retSize >= 2) {
        if (res[0] > res[1]) { int t = res[0]; res[0] = res[1]; res[1] = t; }
        printf("%d %d\\n", res[0], res[1]);
        free(res);
    }
    return 0;
}
""",
        2: """
int main() {
    char s[100000];
    if (fgets(s, sizeof(s), stdin)) {
        int len = strlen(s);
        while (len > 0 && (s[len-1] == '\\n' || s[len-1] == '\\r')) s[--len] = '\\0';
        char* res = reverseString(s);
        printf("%s\\n", res ? res : s);
    }
    return 0;
}
""",
        3: """
int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        int retSize = 0;
        char** res = fizzBuzz(n, &retSize);
        for (int i = 0; i < retSize; i++) {
            printf("%s\\n", res[i]);
            free(res[i]);
        }
        if (res) free(res);
    }
    return 0;
}
""",
        4: """
int main() {
    char s[200000];
    if (fgets(s, sizeof(s), stdin)) {
        int len = strlen(s);
        while (len > 0 && (s[len-1] == '\\n' || s[len-1] == '\\r')) s[--len] = '\\0';
        printf("%s\\n", isPalindrome(s) ? "true" : "false");
    }
    return 0;
}
""",
        5: """
int main() {
    int n;
    if (scanf("%d", &n) == 1) {
        printf("%d\\n", fib(n));
    }
    return 0;
}
""",
        6: """
int main() {
    char s[200000];
    if (fgets(s, sizeof(s), stdin)) {
        int len = strlen(s);
        while (len > 0 && (s[len-1] == '\\n' || s[len-1] == '\\r')) s[--len] = '\\0';
        printf("%d\\n", countVowels(s));
    }
    return 0;
}
""",
        7: """
int main() {
    int nums[20000];
    int n = 0;
    char line[20000];
    if (!fgets(line, sizeof(line), stdin)) return 0;
    char* tok = strtok(line, " \\t\\r\\n");
    while (tok) {
        nums[n++] = atoi(tok);
        tok = strtok(NULL, " \\t\\r\\n");
    }
    int target;
    if (scanf("%d", &target) != 1) return 0;
    printf("%d\\n", search(nums, n, target));
    return 0;
}
""",
        8: """
int main() {
    char s[20000];
    if (fgets(s, sizeof(s), stdin)) {
        int len = strlen(s);
        while (len > 0 && (s[len-1] == '\\n' || s[len-1] == '\\r')) s[--len] = '\\0';
        printf("%s\\n", isValid(s) ? "true" : "false");
    }
    return 0;
}
""",
        9: """
int main() {
    char s[50000], t[50000];
    if (fgets(s, sizeof(s), stdin) && fgets(t, sizeof(t), stdin)) {
        int l1 = strlen(s), l2 = strlen(t);
        while (l1 > 0 && (s[l1-1] == '\\n' || s[l1-1] == '\\r')) s[--l1] = '\\0';
        while (l2 > 0 && (t[l2-1] == '\\n' || t[l2-1] == '\\r')) t[--l2] = '\\0';
        printf("%s\\n", isAnagram(s, t) ? "true" : "false");
    }
    return 0;
}
""",
        10: """
int main() {
    int a[1000], b[1000];
    int n1 = 0, n2 = 0;
    char l1[5000], l2[5000];
    if (fgets(l1, sizeof(l1), stdin)) {
        char* t = strtok(l1, " \\t\\r\\n");
        while (t) { a[n1++] = atoi(t); t = strtok(NULL, " \\t\\r\\n"); }
    }
    if (fgets(l2, sizeof(l2), stdin)) {
        char* t = strtok(l2, " \\t\\r\\n");
        while (t) { b[n2++] = atoi(t); t = strtok(NULL, " \\t\\r\\n"); }
    }
    int retSize = 0;
    int* res = merge(a, n1, b, n2, &retSize);
    for (int i = 0; i < retSize; i++) {
        if (i) printf(" ");
        printf("%d", res[i]);
    }
    printf("\\n");
    if (res) free(res);
    return 0;
}
""",
    }

    driver = drivers.get(pid, "int main() { return 0; }\n")
    return headers + code + "\n\n" + driver
