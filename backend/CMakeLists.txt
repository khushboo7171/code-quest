cmake_minimum_required(VERSION 3.16)
project(CodeQuestBackend VERSION 1.0)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(Crow REQUIRED)
find_package(nlohmann_json REQUIRED)
find_package(SQLite3 REQUIRED)

add_executable(code_quest_backend
    src/main.cpp
    src/database.cpp
    src/auth.cpp
    src/problems.cpp
    src/judge.cpp
    src/leaderboard.cpp
)

target_link_libraries(code_quest_backend
    Crow::Crow
    nlohmann_json::nlohmann_json
    SQLite::SQLite3
)

target_include_directories(code_quest_backend PRIVATE src)

if(WIN32)
    target_compile_definitions(code_quest_backend PRIVATE _WIN32_WINNT=0x0601)
endif()
