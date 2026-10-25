# Contributing to Code Quest

Thank you for your interest in contributing! 🎮

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/code-quest.git`
3. Create a feature branch: `git checkout -b feature/my-feature`
4. Make your changes
5. Commit: `git commit -m "feat: add my feature"`
6. Push: `git push origin feature/my-feature`
7. Open a Pull Request

## 📚 Adding a New Problem

### Step 1: Add to `backend/src/problems.cpp`

Inside `loadProblems()`, add a new `Problem` struct:

```cpp
{
    11, "Your Problem Title",
    "Full problem description here.\n\nDetails...",
    "easy",   // "easy", "medium", or "hard"
    "Arrays", // Category
    10,       // XP reward (10/25/50)
    {"Hint 1", "Hint 2"},
    {"Input: ...\nOutput: ...\nExplanation: ..."},
    {"Constraint 1", "Constraint 2"},
    // Visible test cases
    {{"input_line1\ninput_line2", "expected_output"}},
    // Hidden test cases
    {{"hidden_input", "hidden_output"}}
}
```

### Step 2: Add Starter Code (optional)

In `frontend/utils/config.py`, add starter code for the problem ID:

```python
STARTER_CODE = {
    "python": {
        11: "# Your problem starter code\n",
    },
    "cpp": {
        11: "// C++ starter code\n",
    },
}
```

### Step 3: Test

Run both the backend and frontend, navigate to the problem, and verify it works correctly.

## 🐍 Python Style Guide

- Follow **PEP 8**
- Max line length: **120 characters**
- Use `f-strings` over `.format()`
- Add docstrings to classes and public methods
- Use type hints where possible

## ⚙️ C++ Style Guide

- Use **C++17** features
- Use `#pragma once` for headers
- Snake_case for variables, PascalCase for classes
- `const` and `constexpr` where possible
- Handle exceptions with `try/catch`

## 🐛 Bug Reports

Please open an issue with:
- OS and version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

## 💡 Feature Requests

Open an issue labeled `enhancement` describing:
- What problem it solves
- Proposed implementation
- Any alternatives considered

## 📝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help beginners learn
