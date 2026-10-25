#pragma once
#include "database.h"
#include <crow.h>

class LeaderboardHandler {
public:
    static void setupRoutes(crow::SimpleApp& app, Database& db);
};
