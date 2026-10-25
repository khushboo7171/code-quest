# Code Quest — C++ Backend

## Overview

A high-performance REST API built with **C++17 + Crow** that powers:
- User authentication (register/login/profile)
- Problem bank (10 curated challenges)
- Code execution judge (C, C++, Python)
- XP & level system
- Global leaderboard

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| g++ (MinGW/MSVC) | GCC 10+ | [mingw-w64.org](https://www.mingw-w64.org) |
| CMake | 3.16+ | [cmake.org](https://cmake.org) |
| vcpkg | latest | [vcpkg.io](https://vcpkg.io) |

## Build on Windows

```powershell
# 1. Install vcpkg (once)
git clone https://github.com/microsoft/vcpkg.git C:\vcpkg
C:\vcpkg\bootstrap-vcpkg.bat
C:\vcpkg\vcpkg integrate install

# 2. Build
cd backend
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=C:\vcpkg\scripts\buildsystems\vcpkg.cmake
cmake --build build --config Release

# 3. Run
.\build\Release\code_quest_backend.exe
```

The server starts on **http://localhost:8080**.

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register `{username, password}` |
| POST | `/api/auth/login` | Login `{username, password}` |
| GET  | `/api/auth/profile?token=X` | Get user profile |

### Problems
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/problems` | List all problems |
| GET | `/api/problems?difficulty=easy` | Filter by difficulty |
| GET | `/api/problems/{id}` | Get problem details |
| GET | `/api/problems/daily` | Today's daily challenge |

### Judge
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/judge/run` | Submit `{problem_id, code, language, token}` |

**Response:**
```json
{
  "status": "AC",
  "passed": 4,
  "total": 4,
  "runtime_ms": 12,
  "output": "0 1",
  "error": "",
  "xp_earned": 10
}
```

Status codes: `AC` (Accepted), `WA` (Wrong Answer), `CE` (Compile Error), `TLE` (Time Limit Exceeded)

### Leaderboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/leaderboard` | Top 20 users by XP |
| GET | `/api/leaderboard/user?token=X` | Current user's rank |

### Health
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Server health check |

## Database Schema

```sql
users        (id, username, password_hash, xp, level, streak, badges, solved_count, created_at)
sessions     (token, user_id, created_at)
submissions  (id, user_id, problem_id, code, language, status, runtime_ms, created_at)
achievements (id, user_id, badge_name, earned_at)
solved_problems (user_id, problem_id)
```

## Level Thresholds

| Level | XP |
|-------|----|
| Novice | 0 |
| Apprentice | 100 |
| Warrior | 300 |
| Champion | 600 |
| Master | 1000 |
| Legend | 2000 |
