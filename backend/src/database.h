#pragma once
#include <sqlite3.h>
#include <string>
#include <vector>
#include <map>
#include <stdexcept>

using Row = std::map<std::string, std::string>;

class Database {
public:
    explicit Database(const std::string& filename);
    ~Database();

    void init();
    void execute(const std::string& sql);
    std::vector<Row> query(const std::string& sql);
    Row getUserByToken(const std::string& token);
    Row getUserByUsername(const std::string& username);
    int  getLastInsertId();

private:
    sqlite3* db_ = nullptr;
};
