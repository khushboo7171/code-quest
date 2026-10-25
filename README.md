<div align="center">

```
  ██████╗ ██████╗ ██████╗ ███████╗     ██████╗ ██╗   ██╗███████╗███████╗████████╗
 ██╔════╝██╔═══██╗██╔══██╗██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
 ██║     ██║   ██║██║  ██║█████╗      ██║   ██║██║   ██║█████╗  ███████╗   ██║   
 ██║     ██║   ██║██║  ██║██╔══╝      ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║   
 ╚██████╗╚██████╔╝██████╔╝███████╗    ╚██████╔╝╚██████╔╝███████╗███████║   ██║   
  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝     ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝  
```

# 🎮 Code Quest: Programming Practice Playground

**A fully gamified programming practice platform — solve challenges, earn XP, level up, and compete!**

[![Python](https://img.shields.io/badge/Frontend-Python%20%2B%20ttkbootstrap-3776AB?logo=python&logoColor=white)](https://python.org)
[![C++](https://img.shields.io/badge/Backend-C%2B%2B17%20%2B%20Crow-00599C?logo=cplusplus&logoColor=white)](https://github.com/CrowCpp/Crow)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows)](https://github.com)

</div>

---

## ✨ Features

- 🎮 **Game-Like XP System** — Earn XP by solving problems and level up from Novice to Legend
- 📚 **10 Curated Problems** — Easy, Medium, and Hard challenges across Arrays, Strings, Algorithms
- ⚡ **Real Code Execution** — Your actual code runs in a sandboxed C++ judge engine (Python/C/C++)
- 🏆 **Live Leaderboard** — Compete globally with real-time XP rankings
- 🎯 **Daily Challenge** — A fresh problem every day to keep you sharp
- 💡 **Hints System** — Stuck? Unlock progressive hints
- 🏅 **Badges & Achievements** — Earn rewards for milestones
- 🔐 **User Authentication** — Register and track your progress
- 🌗 **Beautiful Dark UI** — Game-style ttkbootstrap interface with syntax highlighting
- 🌐 **Offline/Demo Mode** — Works without the backend for UI preview

---

## 🏗️ Architecture

```
┌─────────────────────────────────┐      HTTP/REST      ┌──────────────────────────────────┐
│   Python Frontend (tkinter)     │ ◄──────────────────► │  C++ Backend (Crow + SQLite)     │
│                                 │    localhost:8080     │                                  │
│  ┌──────────┐  ┌─────────────┐  │                       │  ┌────────┐  ┌───────────────┐  │
│  │ Sidebar  │  │ Code Editor │  │                       │  │  Auth  │  │ Judge Engine  │  │
│  └──────────┘  └─────────────┘  │                       │  └────────┘  └───────────────┘  │
│  ┌──────────────────────────┐   │                       │  ┌──────────┐  ┌────────────┐   │
│  │  Home | Arena | Profile  │   │                       │  │ Problems │  │ Leaderboard│   │
│  └──────────────────────────┘   │                       │  └──────────┘  └────────────┘   │
└─────────────────────────────────┘                       └──────────────────────────────────┘
                                                                           │
                                                                    ┌──────▼──────┐
                                                                    │  SQLite DB  │
                                                                    │ codequest.db│
                                                                    └─────────────┘
```

---

## 🎯 Level System

| Level | XP Range | Badge | Description |
|-------|----------|-------|-------------|
| Novice | 0 – 99 | 🌱 | Just starting out |
| Apprentice | 100 – 299 | ⚔️ | Getting the hang of it |
| Warrior | 300 – 599 | 🛡️ | Solid fundamentals |
| Champion | 600 – 999 | 🏆 | Consistent performer |
| Master | 1000 – 1999 | 🌟 | Elite problem solver |
| Legend | 2000+ | 👑 | Hall of Fame |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Python 3.10+, ttkbootstrap, tkinter, Pygments |
| **Backend** | C++17, Crow HTTP framework, nlohmann/json |
| **Database** | SQLite 3 |
| **Build System** | CMake 3.16+, vcpkg |
| **Code Execution** | Subprocess judge: g++ (C/C++), python |
| **CI/CD** | GitHub Actions |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** — [python.org](https://python.org)
- **g++ (MinGW or MSVC)** — for compiling the C++ backend and judging C/C++ submissions
- **CMake 3.16+** — [cmake.org](https://cmake.org)
- **vcpkg** — [vcpkg.io](https://vcpkg.io)

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/code-quest.git
cd code-quest
```

### 2. Run the Frontend (Python GUI)

> Works in offline/demo mode even without the backend!

```bash
cd frontend
pip install -r requirements.txt
python main.py
```

### 3. Build & Run the Backend (C++)

```bash
# Install vcpkg if you haven't
git clone https://github.com/microsoft/vcpkg.git C:\vcpkg
C:\vcpkg\bootstrap-vcpkg.bat
C:\vcpkg\vcpkg integrate install

# Build the backend
cd backend
cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=C:\vcpkg\scripts\buildsystems\vcpkg.cmake
cmake --build build --config Release

# Run it
.\build\Release\code_quest_backend.exe
```

The server starts on **http://localhost:8080**. Now relaunch the frontend to connect!

### 4. Use the Setup Script (Alternative)

```bash
python setup.py
```

---

## 📚 Supported Languages

| Language | Compile Command | Run |
|----------|----------------|-----|
| **Python** | *(interpreted)* | `python solution.py` |
| **C++** | `g++ -std=c++17 -o sol.exe sol.cpp` | `sol.exe` |
| **C** | `g++ -x c -o sol.exe sol.c` | `sol.exe` |

---

## 🗺️ Project Structure

```
code-quest/
├── backend/                    # C++ Crow HTTP backend
│   ├── src/
│   │   ├── main.cpp            # Server entry point
│   │   ├── database.h/cpp      # SQLite manager
│   │   ├── auth.h/cpp          # Register/Login/Profile
│   │   ├── problems.h/cpp      # Problem bank + routes
│   │   ├── judge.h/cpp         # Code execution engine
│   │   └── leaderboard.h/cpp   # Rankings
│   ├── problems/
│   │   └── problems.json       # Problem definitions
│   ├── CMakeLists.txt
│   ├── vcpkg.json
│   └── README.md
├── frontend/                   # Python ttkbootstrap GUI
│   ├── main.py                 # App entry point
│   ├── views/
│   │   ├── home.py             # Dashboard
│   │   ├── problems.py         # Problem browser
│   │   ├── arena.py            # Code editor + judge
│   │   ├── leaderboard.py      # Rankings view
│   │   ├── profile.py          # User profile
│   │   └── auth.py             # Login/Register dialog
│   ├── widgets/
│   │   ├── code_editor.py      # Syntax-highlighted editor
│   │   └── sidebar.py          # Navigation sidebar
│   ├── utils/
│   │   ├── api.py              # API client
│   │   └── config.py           # Constants & config
│   └── requirements.txt
├── .github/
│   └── workflows/ci.yml        # GitHub Actions CI
├── setup.py                    # Launcher helper
├── README.md
├── CONTRIBUTING.md
└── LICENSE
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding problems, features, and bug fixes.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Made with ❤️ | Python Frontend + C++ Backend | 2026
</div>
