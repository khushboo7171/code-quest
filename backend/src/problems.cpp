#include "problems.h"
#include <crow.h>
#include <nlohmann/json.hpp>
#include <ctime>
#include <algorithm>

using json = nlohmann::json;

ProblemsHandler::ProblemsHandler() {
    loadProblems();
}

void ProblemsHandler::loadProblems() {
    problems_ = {
        {
            1, "Two Sum", 
            "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nReturn the answer in any order.",
            "easy", "Arrays", 10,
            {"Try using a hash map to store values", "For each number, check if target - number exists in the map"},
            {"Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: nums[0] + nums[1] = 2 + 7 = 9",
             "Input: nums = [3,2,4], target = 6\nOutput: [1,2]"},
            {"2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "Only one valid answer exists"},
            {{"2 7 11 15\n9", "0 1"}, {"3 2 4\n6", "1 2"}},
            {{"1 5 3 7\n8", "1 3"}, {"2 6 4 1\n5", "2 3"}}
        },
        {
            2, "Reverse String",
            "Write a function that reverses a string. The input is given as a single line.\n\nReturn the reversed string.",
            "easy", "Strings", 10,
            {"Try reading the string character by character", "Use two pointers or a stack"},
            {"Input: hello\nOutput: olleh", "Input: Hannah\nOutput: hannaH"},
            {"1 <= s.length <= 10^5", "s consists of printable ASCII characters"},
            {{"hello", "olleh"}, {"world", "dlrow"}},
            {{"abcdef", "fedcba"}, {"racecar", "racecar"}}
        },
        {
            3, "FizzBuzz",
            "Given an integer n, return a string array where:\n- answer[i] == 'FizzBuzz' if i is divisible by 3 and 5\n- answer[i] == 'Fizz' if i is divisible by 3\n- answer[i] == 'Buzz' if i is divisible by 5\n- answer[i] == the number itself otherwise\n\nPrint each entry on a new line.",
            "easy", "Math", 10,
            {"Check divisibility by 15 first, then 3, then 5", "Use modulo operator %"},
            {"Input: 5\nOutput:\n1\n2\nFizz\n4\nBuzz"},
            {"1 <= n <= 10^4"},
            {{"5", "1\n2\nFizz\n4\nBuzz"}, {"3", "1\n2\nFizz"}},
            {{"15", "1\n2\nFizz\n4\nBuzz\nFizz\n7\n8\nFizz\nBuzz\n11\nFizz\n13\n14\nFizzBuzz"}}
        },
        {
            4, "Palindrome Check",
            "Given a string s, return 'true' if it is a palindrome, or 'false' otherwise.\n\nA palindrome is a string that reads the same forward and backward. Consider only alphanumeric characters and ignore cases.",
            "easy", "Strings", 10,
            {"Compare the string with its reverse", "Use two pointers from both ends"},
            {"Input: racecar\nOutput: true", "Input: hello\nOutput: false"},
            {"1 <= s.length <= 2 * 10^5"},
            {{"racecar", "true"}, {"hello", "false"}, {"A man a plan a canal Panama", "true"}},
            {{"Was it a car or a cat I saw", "true"}, {"never odd or even", "true"}}
        },
        {
            5, "Fibonacci Number",
            "Given n, return the nth Fibonacci number.\n\nF(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n > 1.",
            "easy", "Math", 10,
            {"Use dynamic programming or iteration", "Store previous two values to compute current"},
            {"Input: 6\nOutput: 8", "Input: 10\nOutput: 55"},
            {"0 <= n <= 30"},
            {{"6", "8"}, {"10", "55"}, {"0", "0"}},
            {{"15", "610"}, {"20", "6765"}}
        },
        {
            6, "Count Vowels",
            "Given a string s, count and return the number of vowels (a, e, i, o, u) in the string. Both uppercase and lowercase count.",
            "easy", "Strings", 10,
            {"Iterate through each character", "Use a set or condition to check vowels"},
            {"Input: hello world\nOutput: 3", "Input: Programming\nOutput: 3"},
            {"1 <= s.length <= 10^5"},
            {{"hello world", "3"}, {"aeiou", "5"}, {"xyz", "0"}},
            {{"Programming is fun", "5"}, {"AEIOU aeiou", "10"}}
        },
        {
            7, "Binary Search",
            "Given a sorted array of integers and a target value, return the index if the target is found. If not, return -1.\n\nYou must write an algorithm with O(log n) runtime complexity.\n\nInput format: First line is space-separated sorted array, second line is target.",
            "medium", "Algorithms", 25,
            {"Maintain left and right pointers", "Compute mid = (left + right) / 2 and compare with target"},
            {"Input: 1 3 5 7 9\n7\nOutput: 3", "Input: 1 2 3 4 5\n6\nOutput: -1"},
            {"1 <= nums.length <= 10^4", "All elements are unique and sorted in ascending order"},
            {{"1 3 5 7 9\n7", "3"}, {"1 2 3 4 5\n6", "-1"}, {"5\n5", "0"}},
            {{"2 4 6 8 10 12\n10", "4"}, {"1 3 5\n1", "0"}}
        },
        {
            8, "Valid Parentheses",
            "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n\nOutput 'true' or 'false'.",
            "medium", "Stacks", 25,
            {"Use a stack data structure", "Push opening brackets, pop and match on closing brackets"},
            {"Input: ()\nOutput: true", "Input: ()[]{}\nOutput: true", "Input: (]\nOutput: false"},
            {"1 <= s.length <= 10^4", "s consists of parentheses only '()[]{}'"},
            {{"()", "true"}, {"()[]{}", "true"}, {"(]", "false"}, {"{[]}", "true"}},
            {{"([)]", "false"}, {"((((", "false"}}
        },
        {
            9, "Anagram Check",
            "Given two strings s and t, return 'true' if t is an anagram of s, and 'false' otherwise.\n\nAn Anagram is a word or phrase formed by rearranging the letters of a different word, using all the original letters exactly once.\n\nInput: two lines, each a string.",
            "medium", "Strings", 25,
            {"Sort both strings and compare", "Use a frequency count map for each string"},
            {"Input: anagram\nnagaram\nOutput: true", "Input: rat\ncar\nOutput: false"},
            {"1 <= s.length, t.length <= 5 * 10^4", "s and t consist of lowercase English letters"},
            {{"anagram\nnagaram", "true"}, {"rat\ncar", "false"}, {"listen\nsilent", "true"}},
            {{"triangle\nintegral", "true"}, {"hello\nworld", "false"}}
        },
        {
            10, "Merge Sorted Arrays",
            "You are given two integer arrays nums1 and nums2, sorted in non-decreasing order.\n\nMerge nums2 into nums1 as one sorted array and print the result.\n\nInput format:\n- Line 1: space-separated integers for nums1\n- Line 2: space-separated integers for nums2",
            "hard", "Arrays", 50,
            {"Use two pointers starting from the beginning", "Compare elements from both arrays, pick the smaller"},
            {"Input: 1 3 5\n2 4 6\nOutput: 1 2 3 4 5 6"},
            {"0 <= nums1.length, nums2.length <= 200", "Both arrays are sorted"},
            {{"1 3 5\n2 4 6", "1 2 3 4 5 6"}, {"1\n2", "1 2"}, {"1 2 3\n", "1 2 3"}},
            {{"1 4 7 9\n2 5 6", "1 2 4 5 6 7 9"}, {"3\n1 2 4", "1 2 3 4"}}
        }
    };
}

const Problem* ProblemsHandler::getProblem(int id) const {
    for (const auto& p : problems_) {
        if (p.id == id) return &p;
    }
    return nullptr;
}

static json problemToJson(const Problem& p, bool includeTests = true) {
    json j;
    j["id"]          = p.id;
    j["title"]       = p.title;
    j["difficulty"]  = p.difficulty;
    j["category"]    = p.category;
    j["xp"]          = p.xp;
    j["description"] = p.description;
    j["hints"]       = p.hints;
    j["examples"]    = p.examples;
    j["constraints"] = p.constraints;
    if (includeTests) {
        json tests = json::array();
        for (const auto& tc : p.visible_tests) {
            tests.push_back({{"input", tc.input}, {"expected", tc.expected}});
        }
        j["visible_tests"] = tests;
    }
    return j;
}

void ProblemsHandler::setupRoutes(crow::SimpleApp& app, Database& db) {

    // GET /api/problems
    CROW_ROUTE(app, "/api/problems")
    ([this](const crow::request& req) {
        crow::response res;
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Content-Type", "application/json");

        std::string diff = req.url_params.get("difficulty") ? req.url_params.get("difficulty") : "";

        json arr = json::array();
        for (const auto& p : problems_) {
            if (!diff.empty() && p.difficulty != diff) continue;
            json item;
            item["id"]         = p.id;
            item["title"]      = p.title;
            item["difficulty"] = p.difficulty;
            item["category"]   = p.category;
            item["xp"]         = p.xp;
            arr.push_back(item);
        }
        res.body = arr.dump();
        return res;
    });

    // GET /api/problems/daily
    CROW_ROUTE(app, "/api/problems/daily")
    ([this](const crow::request&) {
        crow::response res;
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Content-Type", "application/json");

        std::time_t now = std::time(nullptr);
        std::tm* t = std::localtime(&now);
        int dayOfYear = t->tm_yday;
        int idx = dayOfYear % (int)problems_.size();
        res.body = problemToJson(problems_[idx], true).dump();
        return res;
    });

    // GET /api/problems/<id>
    CROW_ROUTE(app, "/api/problems/<int>")
    ([this](const crow::request&, int id) {
        crow::response res;
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Content-Type", "application/json");

        const Problem* p = getProblem(id);
        if (!p) {
            res.code = 404;
            res.body = json{{"error", "Problem not found"}}.dump();
            return res;
        }
        res.body = problemToJson(*p, true).dump();
        return res;
    });
}
