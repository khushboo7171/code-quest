#pragma once
#include "database.h"
#include "problems.h"
#include <crow.h>
#include <string>

class JudgeHandler {
public:
    static void setupRoutes(crow::SimpleApp& app, Database& db, ProblemsHandler& problems);

private:
    static std::string calcLevel(int xp);
    static std::string trim(const std::string& s);
    static bool runCode(const std::string& code, const std::string& language,
                        const std::string& input, std::string& output,
                        std::string& error, long long& runtime_ms);
};
