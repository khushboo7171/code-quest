#include "leaderboard.h"
#include <crow.h>
#include <nlohmann/json.hpp>

using json = nlohmann::json;

void LeaderboardHandler::setupRoutes(crow::SimpleApp& app, Database& db) {

    // GET /api/leaderboard
    CROW_ROUTE(app, "/api/leaderboard")
    ([&db](const crow::request&) {
        crow::response res;
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Content-Type", "application/json");

        try {
            auto rows = db.query(
                "SELECT username, xp, level, badges, solved_count "
                "FROM users ORDER BY xp DESC LIMIT 20;"
            );
            json arr = json::array();
            int rank = 1;
            for (const auto& row : rows) {
                // Count badges
                std::string badges = row.count("badges") ? row.at("badges") : "";
                int badgeCount = 0;
                for (char c : badges) if (c == ',') badgeCount++;
                if (!badges.empty()) badgeCount++;

                arr.push_back({
                    {"rank",        rank++},
                    {"username",    row.at("username")},
                    {"xp",          std::stoi(row.at("xp"))},
                    {"level",       row.at("level")},
                    {"badge_count", badgeCount},
                    {"solved_count",std::stoi(row.at("solved_count"))}
                });
            }
            res.body = arr.dump();
        } catch (const std::exception& e) {
            res.code = 500;
            res.body = json{{"error", e.what()}}.dump();
        }
        return res;
    });

    // GET /api/leaderboard/user?token=X
    CROW_ROUTE(app, "/api/leaderboard/user")
    ([&db](const crow::request& req) {
        crow::response res;
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Content-Type", "application/json");

        try {
            std::string token = req.url_params.get("token") ? req.url_params.get("token") : "";
            if (token.empty()) {
                res.code = 401;
                res.body = json{{"error", "Token required"}}.dump();
                return res;
            }

            auto user = db.getUserByToken(token);
            if (user.empty()) {
                res.code = 401;
                res.body = json{{"error", "Invalid token"}}.dump();
                return res;
            }

            int myXp = std::stoi(user["xp"]);
            // Count users with higher XP
            auto rows = db.query(
                "SELECT COUNT(*) as cnt FROM users WHERE xp > " + std::to_string(myXp) + ";"
            );
            int rank = rows.empty() ? 1 : std::stoi(rows[0].at("cnt")) + 1;

            res.body = json{
                {"username",     user["username"]},
                {"xp",           myXp},
                {"level",        user["level"]},
                {"rank",         rank},
                {"solved_count", std::stoi(user["solved_count"])},
                {"streak",       std::stoi(user["streak"])}
            }.dump();
        } catch (const std::exception& e) {
            res.code = 500;
            res.body = json{{"error", e.what()}}.dump();
        }
        return res;
    });
}
