#pragma once
#include "database.h"
#include <crow.h>
#include <string>

class AuthHandler {
public:
    static void setupRoutes(crow::SimpleApp& app, Database& db);
private:
    static std::string hashPassword(const std::string& password);
    static std::string generateToken(const std::string& username);
    static std::string calcLevel(int xp);
};
