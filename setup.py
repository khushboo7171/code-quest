#!/usr/bin/env python3
"""
Code Quest — Setup & Launcher Script
=====================================
Checks prerequisites, installs dependencies, and launches the app.
"""
import subprocess
import sys
import os
import shutil
import platform


def banner():
    print("""
  ╔══════════════════════════════════════════╗
  ║   🎮  CODE QUEST  Setup & Launcher       ║
  ║      Programming Practice Playground     ║
  ╚══════════════════════════════════════════╝
""")


def check(cmd: str, name: str, install_hint: str = "") -> bool:
    if shutil.which(cmd):
        print(f"  ✅  {name} found")
        return True
    else:
        print(f"  ❌  {name} NOT found")
        if install_hint:
            print(f"       → {install_hint}")
        return False


def check_prerequisites():
    print("📋 Checking prerequisites...\n")
    ok = True
    ok &= check("python",  "Python 3",    "https://python.org")
    ok &= check("pip",     "pip",         "Comes with Python 3.4+")
    ok &= check("g++",     "g++ compiler","Install MinGW or MSYS2: https://www.mingw-w64.org")
    ok &= check("cmake",   "CMake",       "https://cmake.org/download")
    print()
    return ok


def install_python_deps():
    print("📦 Installing Python frontend dependencies...")
    req = os.path.join("frontend", "requirements.txt")
    if not os.path.exists(req):
        print(f"  ❌  {req} not found. Are you in the code-quest directory?")
        return False
    ret = subprocess.call([sys.executable, "-m", "pip", "install", "-r", req])
    if ret == 0:
        print("  ✅  Python dependencies installed!\n")
        return True
    else:
        print("  ❌  Failed to install dependencies.\n")
        return False


def build_backend_instructions():
    print("""
🔨 Building C++ Backend
=======================
Run these commands (requires vcpkg installed):

  # Install vcpkg (once)
  git clone https://github.com/microsoft/vcpkg.git C:\\vcpkg
  C:\\vcpkg\\bootstrap-vcpkg.bat
  C:\\vcpkg\\vcpkg integrate install

  # Build backend
  cd backend
  cmake -B build -S . -DCMAKE_TOOLCHAIN_FILE=C:\\vcpkg\\scripts\\buildsystems\\vcpkg.cmake
  cmake --build build --config Release

  # Run backend
  .\\build\\Release\\code_quest_backend.exe
""")


def run_frontend():
    print("🚀 Launching Code Quest Frontend...")
    os.chdir("frontend")
    subprocess.call([sys.executable, "main.py"])


def run_both():
    print("🚀 Launching backend + frontend...")
    backend_exe = os.path.join("..", "backend", "build", "Release", "code_quest_backend.exe")
    if not os.path.exists(backend_exe):
        print(f"  ⚠️   Backend executable not found at: {backend_exe}")
        print("       Please build the backend first (option 2).")
        input("  Press Enter to launch frontend in offline mode...")
    else:
        subprocess.Popen([backend_exe])
        print("  ✅  Backend started in background.")
        import time; time.sleep(1)
    run_frontend()


def main():
    banner()

    while True:
        print("What would you like to do?\n")
        print("  [1] Check prerequisites")
        print("  [2] Install Python frontend dependencies")
        print("  [3] Show backend build instructions")
        print("  [4] Run frontend only (offline/demo mode)")
        print("  [5] Run frontend + backend")
        print("  [0] Exit\n")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            check_prerequisites()
        elif choice == "2":
            install_python_deps()
        elif choice == "3":
            build_backend_instructions()
        elif choice == "4":
            if install_python_deps():
                run_frontend()
            break
        elif choice == "5":
            if install_python_deps():
                run_both()
            break
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("  Invalid choice. Try again.\n")


if __name__ == "__main__":
    # Must run from code-quest/ root
    if not os.path.isdir("frontend"):
        print("❌ Please run this script from the code-quest/ root directory.")
        sys.exit(1)
    main()
