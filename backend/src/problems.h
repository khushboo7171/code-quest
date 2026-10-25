#pragma once
#include "database.h"
#include <crow.h>
#include <string>
#include <vector>

struct TestCase {
    std::string input;
    std::string expected;
};

struct Problem {
    int id;
    std::string title;
    std::string description;
    std::string difficulty;
    std::string category;
    int xp;
    std::vector<std::string> hints;
    std::vector<std::string> examples;
    std::vector<std::string> constraints;
    std::vector<TestCase> visible_tests;
    std::vector<TestCase> hidden_tests;
};

class ProblemsHandler {
public:
    ProblemsHandler();
    void setupRoutes(crow::SimpleApp& app, Database& db);
    const Problem* getProblem(int id) const;
    const std::vector<Problem>& getAll() const { return problems_; }

private:
    std::vector<Problem> problems_;
    void loadProblems();
};
