#include "auth.h"
#include <crow.h>
#include <nlohmann/json.hpp>
#include <sstream>
#include <iomanip>
#include <chrono>
#include <functional>

using json = nlohmann::json;

std::string AuthHandler::hashPassword(const std::string& password) {
    // Simple djb2 hash (for demo; use bcrypt in production)
    unsigned long hash = 5381;
    for (char c : password) {
        hash = ((hash << 5) + hash) + (unsigned char)c;
    }
    std::ostringstream oss;
    oss << std::hex << std::setw(16) << std::setfill('0') << hash;
    return oss.str();
}

std::string AuthHandler::generateToken(const std::string& username) {
    auto now = std::chrono::system_clock::now().time_since_epoch().count();
    std::size_t h = std::hash<std::string>{}(username + std::to_string(now));
    std::ostringstream oss;
    oss << std::hex << std::setw(16) << std::setfill('0') << h;
    return "cq_" + oss.str();
}

std::string AuthHandler::calcLevel(int xp) {
    if (xp >= 2000) return "Legend";
    if (xp >= 1000) return "Master";
    if (xp >= 600)  return "Champion";
    if (xp >= 300)  return "Warrior";
    if (xp >= 100)  return "Apprentice";
    return "Novice";
}

void AuthHandler::setupRoutes(crow::SimpleApp& app, Database& db) {

    // POST /api/auth/register
    CROW_ROUTE(app, "/api/auth/register").methods(crow::HTTPMethod::POST)
    ([&db](const crow::request& req) {
        crow::response res;
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Content-Type", "application/json");
        try {
            auto body = json::parse(req.body);
            std::string username = body.value("username", "");
            std::string password = body.value("password", "");

            if (username.empty() || password.empty()) {
                res.code = 400;
                res.body = json{{"success", false}, {"error", "Username and password required"}}.dump();
                return res;
            }
            if (username.length() < 3 || username.length() > 20) {
                res.code = 400;
                res.body = json{{"success", false}, {"error", "Username must be 3-20 characters"}}.dump();
                return res;
            }

            // Check if user exists
            auto existing = db.getUserByUsername(username);
            if (!existing.empty()) {
                res.code = 409;
                res.body = json{{"success", false}, {"error", "Username already taken"}}.dump();
                return res;
            }

            std::string hash = AuthHandler::hashPassword(password);
            db.execute("INSERT INTO users (username, password_hash) VALUES ('" + username + "', '" + hash + "');");
            int userId = db.getLastInsertId();

            std::string token = AuthHandler::generateToken(username);
            db.execute("INSERT INTO sessions (token, user_id) VALUES ('" + token + "', " + std::to_string(userId) + ");");

            res.code = 200;
            res.body = json{
                {"success", true},
                {"token", token},
                {"username", username},
                {"xp", 0},
                {"level", "Novice"},
                {"message", "Welcome to Code Quest, " + username + "!"}
            }.dump();
        } catch (const std::exception& e) {
            res.code = 500;
            res.body = json{{"success", false}, {"error", e.what()}}.dump();
        }
        return res;
    });

    // POST /api/auth/login
    CROW_ROUTE(app, "/api/auth/login").methods(crow::HTTPMethod::POST)
    ([&db](const crow::request& req) {
        crow::response res;
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Content-Type", "application/json");
        try {
            auto body = json::parse(req.body);
            std::string username = body.value("username", "");
            std::string password = body.value("password", "");

            auto user = db.getUserByUsername(username);
            if (user.empty()) {
                res.code = 401;
                res.body = json{{"success", false}, {"error", "User not found"}}.dump();
                return res;
            }

            std::string hash = AuthHandler::hashPassword(password);
            if (user["password_hash"] != hash) {
                res.code = 401;
                res.body = json{{"success", false}, {"error", "Invalid password"}}.dump();
                return res;
            }

            std::string token = AuthHandler::generateToken(username);
            db.execute("INSERT OR REPLACE INTO sessions (token, user_id) VALUES ('" + token + "', " + user["id"] + ");");

            res.code = 200;
            res.body = json{
                {"success", true},
                {"token", token},
                {"username", user["username"]},
                {"xp", std::stoi(user["xp"])},
                {"level", user["level"]},
                {"badges", user["badges"]},
                {"streak", std::stoi(user["streak"])},
                {"solved_count", std::stoi(user["solved_count"])}
            }.dump();
        } catch (const std::exception& e) {
            res.code = 500;
            res.body = json{{"success", false}, {"error", e.what()}}.dump();
        }
        return res;
    });

    // GET /api/auth/profile
    CROW_ROUTE(app, "/api/auth/profile")
    ([&db](const crow::request& req) {
        crow::response res;
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Content-Type", "application/json");
        try {
            std::string token = req.url_params.get("token") ? req.url_params.get("token") : "";
            if (token.empty()) {
                res.code = 401;
                res.body = json{{"error", "No token provided"}}.dump();
                return res;
            }

            auto user = db.getUserByToken(token);
            if (user.empty()) {
                res.code = 401;
                res.body = json{{"error", "Invalid token"}}.dump();
                return res;
            }

            res.code = 200;
            res.body = json{
                {"username", user["username"]},
                {"xp", std::stoi(user["xp"])},
                {"level", user["level"]},
                {"streak", std::stoi(user["streak"])},
                {"badges", user["badges"]},
                {"solved_count", std::stoi(user["solved_count"])},
                {"created_at", user["created_at"]}
            }.dump();
        } catch (const std::exception& e) {
            res.code = 500;
            res.body = json{{"error", e.what()}}.dump();
        }
        return res;
    });

    // OPTIONS preflight for CORS
    CROW_ROUTE(app, "/api/auth/<path>").methods(crow::HTTPMethod::OPTIONS)
    ([](const crow::request&, const std::string&) {
        crow::response res(204);
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
        res.add_header("Access-Control-Allow-Headers", "Content-Type");
        return res;
    });
}
