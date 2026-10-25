"""
Code Quest: Programming Practice Playground
==========================================
Main entry point for the Python GUI application.

Frontend: Python + ttkbootstrap (dark game-style UI)
Backend:  C++ + Crow HTTP API (http://localhost:8080)
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading
import os
import sys

# Ensure frontend/ is on the path
sys.path.insert(0, os.path.dirname(__file__))

from utils.api import APIClient
from utils.config import TOKEN_FILE
from widgets.sidebar import Sidebar
from views.auth import AuthWindow
from views.home import HomeView
from views.problems import ProblemsView
from views.arena import ArenaView
from views.leaderboard import LeaderboardView
from views.profile import ProfileView


class CodeQuestApp(ttk.Window):
    """Main application window."""

    def __init__(self):
        super().__init__(themename="darkly")
        self.title("🎮 Code Quest: Programming Practice Playground")
        self.geometry("1280x800")
        self.minsize(1024, 680)

        self.api = APIClient()
        self.current_user = None

        self._setup_ui()
        self._show_splash()

    # ── UI setup ──────────────────────────────────────────────────────────────

    def _setup_ui(self):
        # Root layout
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=BOTH, expand=True)

        # Sidebar
        self.sidebar = Sidebar(self.main_frame, on_navigate=self.navigate)
        self.sidebar.pack(side=LEFT, fill=Y)

        # Thin separator
        ttk.Separator(self.main_frame, orient=VERTICAL).pack(side=LEFT, fill=Y)

        # Content area
        self.content = ttk.Frame(self.main_frame)
        self.content.pack(side=LEFT, fill=BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="⚡ Connecting to backend at http://localhost:8080 ...")
        status_bar = ttk.Label(self, textvariable=self.status_var,
                               font=("Segoe UI", 8), bootstyle="inverse-secondary",
                               anchor="w", padding=(8, 3))
        status_bar.pack(side=BOTTOM, fill=X)

        # Start backend health check
        threading.Thread(target=self._check_backend, daemon=True).start()

    def _check_backend(self):
        ok = self.api.check_health()
        msg = "✅ Backend connected — http://localhost:8080" if ok else \
              "⚠️  Backend offline — running in demo mode (start C++ backend for full features)"
        self.after(0, lambda: self.status_var.set(msg))

    # ── Splash screen ─────────────────────────────────────────────────────────

    def _show_splash(self):
        splash = tk.Toplevel(self)
        splash.overrideredirect(True)
        splash.configure(bg="#0f0f1a")

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = 520, 320
        splash.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        tk.Label(splash, text="🎮", font=("Segoe UI Emoji", 56),
                 bg="#0f0f1a", fg="#e94560").pack(pady=(30, 4))
        tk.Label(splash, text="CODE QUEST",
                 font=("Consolas", 28, "bold"), bg="#0f0f1a", fg="#e94560").pack()
        tk.Label(splash, text="Programming Practice Playground",
                 font=("Segoe UI", 12), bg="#0f0f1a", fg="#8888aa").pack(pady=4)
        tk.Label(splash, text="v1.0  |  Python + C++",
                 font=("Segoe UI", 9), bg="#0f0f1a", fg="#555577").pack(pady=(0, 20))

        bar = ttk.Progressbar(splash, length=380, mode="indeterminate",
                              bootstyle="danger")
        bar.pack()
        bar.start(12)

        tk.Label(splash, text="Loading...",
                 font=("Segoe UI", 9), bg="#0f0f1a", fg="#555577").pack(pady=8)

        self.after(2200, lambda: (splash.destroy(), self._check_auth()))

    # ── Auth check ────────────────────────────────────────────────────────────

    def _check_auth(self):
        if self.api.is_logged_in():
            profile = self.api.get_profile()
            if not profile.get("error"):
                self.current_user = profile
                self.sidebar.update_user(
                    profile.get("username", ""),
                    profile.get("xp", 0),
                    profile.get("level", "Novice"),
                )
                self.navigate("home")
                return
        # Show login window
        self.navigate("home")
        AuthWindow(self, self.api, self._on_login_success)

    def _on_login_success(self, user_data: dict):
        self.current_user = user_data
        self.sidebar.update_user(
            user_data.get("username", ""),
            user_data.get("xp", 0),
            user_data.get("level", "Novice"),
        )
        self.navigate("home")

    # ── Navigation ────────────────────────────────────────────────────────────

    def navigate(self, view_name: str, **kwargs):
        """Switch the main content area to a named view."""
        # Clear content
        for w in self.content.winfo_children():
            w.destroy()

        self.sidebar.set_active(view_name)

        if view_name == "home":
            view = HomeView(self.content, self.api, self.navigate)
        elif view_name == "problems":
            view = ProblemsView(self.content, self.api, self.navigate)
        elif view_name == "arena":
            view = ArenaView(self.content, self.api, self.navigate)
            problem_id = kwargs.get("problem_id")
            if problem_id:
                view.after(100, lambda: view.load_problem(problem_id))
        elif view_name == "leaderboard":
            view = LeaderboardView(self.content, self.api)
        elif view_name == "profile":
            view = ProfileView(self.content, self.api, self.navigate)
        else:
            view = HomeView(self.content, self.api, self.navigate)

        view.pack(fill=BOTH, expand=True)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = CodeQuestApp()
    app.mainloop()
