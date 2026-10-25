#include "judge.h"
#include <crow.h>
#include <nlohmann/json.hpp>
#include <fstream>
#include <sstream>
#include <chrono>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <cctype>
#include <filesystem>

using json = nlohmann::json;
namespace fs = std::filesystem;

std::string JudgeHandler::calcLevel(int xp) {
    if (xp >= 2000) return "Legend";
    if (xp >= 1000) return "Master";
    if (xp >= 600)  return "Champion";
    if (xp >= 300)  return "Warrior";
    if (xp >= 100)  return "Apprentice";
    return "Novice";
}

std::string JudgeHandler::trim(const std::string& s) {
    size_t start = s.find_first_not_of(" \t\n\r");
    if (start == std::string::npos) return "";
    size_t end = s.find_last_not_of(" \t\n\r");
    return s.substr(start, end - start + 1);
}

bool JudgeHandler::runCode(const std::string& code, const std::string& language,
                            const std::string& input, std::string& output,
                            std::string& error, long long& runtime_ms) {
    // Create temp directory
    std::string tmpDir = "C:\\temp\\codequest\\";
    fs::create_directories(tmpDir);

    std::string srcFile, exeFile, compileCmd, runCmd;

    if (language == "python") {
        srcFile = tmpDir + "solution.py";
        runCmd  = "python \"" + srcFile + "\"";
    } else if (language == "c") {
        srcFile   = tmpDir + "solution.c";
        exeFile   = tmpDir + "solution.exe";
        compileCmd = "g++ -x c -O2 -o \"" + exeFile + "\" \"" + srcFile + "\" 2> \"" + tmpDir + "compile_err.txt\"";
        runCmd     = "\"" + exeFile + "\"";
    } else { // cpp
        srcFile   = tmpDir + "solution.cpp";
        exeFile   = tmpDir + "solution.exe";
        compileCmd = "g++ -std=c++17 -O2 -o \"" + exeFile + "\" \"" + srcFile + "\" 2> \"" + tmpDir + "compile_err.txt\"";
        runCmd     = "\"" + exeFile + "\"";
    }

    std::string inputFile  = tmpDir + "input.txt";
    std::string outputFile = tmpDir + "output.txt";
    std::string errFile    = tmpDir + "stderr.txt";

    // Write source
    { std::ofstream f(srcFile); f << code; }
    // Write input
    { std::ofstream f(inputFile); f << input; }

    // Compile if needed
    if (!compileCmd.empty()) {
        int ret = system(compileCmd.c_str());
        if (ret != 0) {
            std::ifstream ef(tmpDir + "compile_err.txt");
            error = std::string(std::istreambuf_iterator<char>(ef), {});
            output = "";
            runtime_ms = 0;
            return false; // CE
        }
    }

    // Run
    std::string fullRun = runCmd + " < \"" + inputFile + "\" > \"" + outputFile + "\" 2> \"" + errFile + "\"";
    auto start = std::chrono::high_resolution_clock::now();
    int ret = system(fullRun.c_str());
    auto end = std::chrono::high_resolution_clock::now();
    runtime_ms = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();

    { std::ifstream f(outputFile); output = std::string(std::istreambuf_iterator<char>(f), {}); }
    { std::ifstream f(errFile);    error  = std::string(std::istreambuf_iterator<char>(f), {}); }

    return true;
}

void JudgeHandler::setupRoutes(crow::SimpleApp& app, Database& db, ProblemsHandler& problems) {

    CROW_ROUTE(app, "/api/judge/run").methods(crow::HTTPMethod::POST)
    ([&db, &problems](const crow::request& req) {
        crow::response res;
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Content-Type", "application/json");

        try {
            auto body = json::parse(req.body);
            int    problemId = body.value("problem_id", 0);
            std::string code = body.value("code", "");
            std::string lang = body.value("language", "python");
            std::string token= body.value("token", "");

            const Problem* prob = problems.getProblem(problemId);
            if (!prob) {
                res.code = 404;
                res.body = json{{"error", "Problem not found"}}.dump();
                return res;
            }
            if (code.empty()) {
                res.code = 400;
                res.body = json{{"error", "No code provided"}}.dump();
                return res;
            }

            // Collect all test cases
            std::vector<TestCase> allTests;
            for (const auto& tc : prob->visible_tests) allTests.push_back(tc);
            for (const auto& tc : prob->hidden_tests)  allTests.push_back(tc);

            int passed = 0, total = (int)allTests.size();
            long long totalMs = 0;
            std::string lastOutput, lastError;
            std::string verdict = "AC";
            bool ceFlag = false;

            for (const auto& tc : allTests) {
                std::string output, error;
                long long ms = 0;
                bool compiled = JudgeHandler::runCode(code, lang, tc.input, output, error, ms);

                if (!compiled) {
                    verdict  = "CE";
                    lastError = error;
                    ceFlag = true;
                    break;
                }
                if (ms > 5000) {
                    verdict = "TLE";
                    break;
                }

                totalMs += ms;
                lastOutput = output;
                lastError  = error;

                std::string got = JudgeHandler::trim(output);
                std::string exp = JudgeHandler::trim(tc.expected);
                if (got == exp) passed++;
                else if (verdict == "AC") verdict = "WA";
            }

            long long avgMs = total > 0 ? totalMs / total : 0;
            int xpEarned = 0;

            if (!ceFlag && verdict == "AC" && passed == total) {
                xpEarned = prob->xp;
                // Award XP if user is logged in
                if (!token.empty()) {
                    auto user = db.getUserByToken(token);
                    if (!user.empty()) {
                        int userId  = std::stoi(user["id"]);
                        int newXp   = std::stoi(user["xp"]) + xpEarned;
                        std::string newLevel = JudgeHandler::calcLevel(newXp);

                        db.execute("UPDATE users SET xp=" + std::to_string(newXp) +
                                   ", level='" + newLevel + "'"
                                   ", solved_count=solved_count+1"
                                   " WHERE id=" + std::to_string(userId) + ";");

                        // Record submission
                        db.execute("INSERT INTO submissions (user_id,problem_id,code,language,status,runtime_ms)"
                                   " VALUES(" + std::to_string(userId) + "," +
                                   std::to_string(problemId) + ",'" +
                                   code + "','" + lang + "','AC'," +
                                   std::to_string(avgMs) + ");");

                        // Mark problem solved
                        db.execute("INSERT OR IGNORE INTO solved_problems (user_id,problem_id) VALUES(" +
                                   std::to_string(userId) + "," + std::to_string(problemId) + ");");
                    }
                }
            }

            res.body = json{
                {"status",     verdict},
                {"passed",     passed},
                {"total",      total},
                {"runtime_ms", avgMs},
                {"output",     JudgeHandler::trim(lastOutput)},
                {"error",      JudgeHandler::trim(lastError)},
                {"xp_earned",  xpEarned}
            }.dump();

        } catch (const std::exception& e) {
            res.code = 500;
            res.body = json{{"error", e.what()}}.dump();
        }
        return res;
    });

    CROW_ROUTE(app, "/api/judge/run").methods(crow::HTTPMethod::OPTIONS)
    ([](const crow::request&) {
        crow::response res(204);
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Access-Control-Allow-Methods", "POST, OPTIONS");
        res.add_header("Access-Control-Allow-Headers", "Content-Type");
        return res;
    });
}
