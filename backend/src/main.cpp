#include <crow.h>
#include <iostream>
#include "database.h"
#include "auth.h"
#include "problems.h"
#include "judge.h"
#include "leaderboard.h"

void printBanner() {
    std::cout << R"(
  ____  _____  ____  _____     ___  _   _ _____  ____  _____
 / ___||  _  \|  _ \| ____|   / _ \| | | | ____|/ ___|_   _|
| |    | | | || | | |  _|    | | | | | | |  _| \___ \ | |
| |___ | |_| || |_| | |___   | |_| | |_| | |___ ___) || |
 \____||_____/|____/|_____|   \__\_\\___/|_____|____/ |_|

  🎮  Programming Practice Playground  v1.0
  ⚡  C++ Backend | Crow HTTP | SQLite DB
  🌐  Listening on http://localhost:8080
)" << std::endl;
}

int main() {
    printBanner();

    // Initialize database
    Database db("codequest.db");
    db.init();
    std::cout << "[Main] Database ready.\n";

    // Create handlers
    ProblemsHandler problemsHandler;
    std::cout << "[Main] Loaded " << problemsHandler.getAll().size() << " problems.\n";

    crow::SimpleApp app;

    // Health check
    CROW_ROUTE(app, "/api/health")
    ([]() {
        crow::response res;
        res.add_header("Access-Control-Allow-Origin", "*");
        res.add_header("Content-Type", "application/json");
        res.body = R"({"status":"ok","service":"Code Quest Backend","version":"1.0.0"})";
        return res;
    });

    // Root
    CROW_ROUTE(app, "/")
    ([]() {
        return "Code Quest Backend is running! Use /api/health to check status.";
    });

    // Setup all routes
    AuthHandler::setupRoutes(app, db);
    problemsHandler.setupRoutes(app, db);
    JudgeHandler::setupRoutes(app, db, problemsHandler);
    LeaderboardHandler::setupRoutes(app, db);

    std::cout << "[Main] All routes registered.\n";
    std::cout << "[Main] Starting server on port 8080...\n\n";

    app.port(8080).multithreaded().run();
    return 0;
}
