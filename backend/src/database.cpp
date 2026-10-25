#include "database.h"
#include <iostream>
#include <sstream>

Database::Database(const std::string& filename) {
    if (sqlite3_open(filename.c_str(), &db_) != SQLITE_OK) {
        throw std::runtime_error("Cannot open database: " + std::string(sqlite3_errmsg(db_)));
    }
    // Enable WAL mode for better concurrency
    execute("PRAGMA journal_mode=WAL;");
    execute("PRAGMA foreign_keys=ON;");
}

Database::~Database() {
    if (db_) sqlite3_close(db_);
}

void Database::init() {
    execute(R"(
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            xp INTEGER DEFAULT 0,
            level TEXT DEFAULT 'Novice',
            streak INTEGER DEFAULT 0,
            badges TEXT DEFAULT '',
            solved_count INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    )");

    execute(R"(
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    )");

    execute(R"(
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            problem_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            language TEXT NOT NULL,
            status TEXT NOT NULL,
            runtime_ms INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    )");

    execute(R"(
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            badge_name TEXT NOT NULL,
            earned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    )");

    execute(R"(
        CREATE TABLE IF NOT EXISTS solved_problems (
            user_id INTEGER NOT NULL,
            problem_id INTEGER NOT NULL,
            PRIMARY KEY(user_id, problem_id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    )");

    std::cout << "[DB] Tables initialized.\n";
}

void Database::execute(const std::string& sql) {
    char* err = nullptr;
    if (sqlite3_exec(db_, sql.c_str(), nullptr, nullptr, &err) != SQLITE_OK) {
        std::string msg = err ? err : "Unknown error";
        sqlite3_free(err);
        throw std::runtime_error("SQL error: " + msg);
    }
}

static int rowCallback(void* data, int argc, char** argv, char** col_names) {
    auto* rows = static_cast<std::vector<Row>*>(data);
    Row row;
    for (int i = 0; i < argc; i++) {
        row[col_names[i]] = argv[i] ? argv[i] : "";
    }
    rows->push_back(row);
    return 0;
}

std::vector<Row> Database::query(const std::string& sql) {
    std::vector<Row> rows;
    char* err = nullptr;
    if (sqlite3_exec(db_, sql.c_str(), rowCallback, &rows, &err) != SQLITE_OK) {
        std::string msg = err ? err : "Unknown error";
        sqlite3_free(err);
        throw std::runtime_error("SQL query error: " + msg);
    }
    return rows;
}

Row Database::getUserByToken(const std::string& token) {
    std::string sql =
        "SELECT u.* FROM users u "
        "JOIN sessions s ON u.id = s.user_id "
        "WHERE s.token = '" + token + "' LIMIT 1;";
    auto rows = query(sql);
    return rows.empty() ? Row{} : rows[0];
}

Row Database::getUserByUsername(const std::string& username) {
    std::string sql = "SELECT * FROM users WHERE username = '" + username + "' LIMIT 1;";
    auto rows = query(sql);
    return rows.empty() ? Row{} : rows[0];
}

int Database::getLastInsertId() {
    return static_cast<int>(sqlite3_last_insert_rowid(db_));
}
