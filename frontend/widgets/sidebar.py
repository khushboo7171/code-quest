"""Animated sidebar navigation widget."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *


NAV_ITEMS = [
    ("home",        "🏠", "Home"),
    ("problems",    "📚", "Problems"),
    ("arena",       "⚔️",  "Arena"),
    ("leaderboard", "🏆", "Leaderboard"),
    ("profile",     "👤", "Profile"),
]


class Sidebar(tk.Frame):
    """Left navigation sidebar with game-style styling."""

    BG       = "#16213e"
    BTN_BG   = "#1a1a2e"
    BTN_ACT  = "#0f3460"
    FG       = "#e0e0e0"
    FG_MUT   = "#8888aa"
    LOGO_FG  = "#e94560"

    def __init__(self, parent, on_navigate, **kwargs):
        super().__init__(parent, bg=self.BG, width=200, **kwargs)
        self.pack_propagate(False)
        self.on_navigate = on_navigate
        self.active_view = None
        self.btn_map = {}
        self._build()

    def _build(self):
        # Logo
        logo_frame = tk.Frame(self, bg=self.BG, pady=20)
        logo_frame.pack(fill=tk.X)
        tk.Label(logo_frame, text="🎮", font=("Segoe UI Emoji", 28),
                 bg=self.BG, fg=self.LOGO_FG).pack()
        tk.Label(logo_frame, text="CODE QUEST", font=("Consolas", 12, "bold"),
                 bg=self.BG, fg=self.LOGO_FG).pack()
        tk.Label(logo_frame, text="Programming Playground", font=("Segoe UI", 8),
                 bg=self.BG, fg=self.FG_MUT).pack()

        # Separator
        tk.Frame(self, bg="#2a2a4a", height=1).pack(fill=tk.X, padx=16, pady=4)

        # Nav buttons
        nav_frame = tk.Frame(self, bg=self.BG)
        nav_frame.pack(fill=tk.X, pady=8)

        for view_id, icon, label in NAV_ITEMS:
            btn = tk.Button(
                nav_frame,
                text=f"  {icon}  {label}",
                font=("Segoe UI", 10),
                bg=self.BTN_BG, fg=self.FG,
                activebackground=self.BTN_ACT,
                activeforeground="#ffffff",
                relief=tk.FLAT, anchor="w",
                padx=12, pady=10, cursor="hand2",
                bd=0,
                command=lambda v=view_id: self.on_navigate(v),
            )
            btn.pack(fill=tk.X, padx=8, pady=2)
            self.btn_map[view_id] = btn

        # Spacer
        tk.Frame(self, bg=self.BG).pack(fill=tk.BOTH, expand=True)

        # Separator
        tk.Frame(self, bg="#2a2a4a", height=1).pack(fill=tk.X, padx=16, pady=4)

        # User info bar at bottom
        self.user_frame = tk.Frame(self, bg=self.BG, pady=10)
        self.user_frame.pack(fill=tk.X)

        self.user_avatar = tk.Label(self.user_frame, text="🌱",
                                    font=("Segoe UI Emoji", 18),
                                    bg=self.BG, fg=self.LOGO_FG)
        self.user_avatar.pack()

        self.user_label = tk.Label(self.user_frame, text="Guest",
                                   font=("Segoe UI", 9, "bold"),
                                   bg=self.BG, fg=self.FG)
        self.user_label.pack()

        self.level_label = tk.Label(self.user_frame, text="Novice | 0 XP",
                                    font=("Segoe UI", 8),
                                    bg=self.BG, fg=self.FG_MUT)
        self.level_label.pack()

        # Mini XP bar
        self.xp_canvas = tk.Canvas(self.user_frame, height=6, bg="#2a2a4a",
                                   highlightthickness=0)
        self.xp_canvas.pack(fill=tk.X, padx=12, pady=4)
        self._xp_bar_pct = 0
        self.xp_canvas.bind("<Configure>", self._draw_xp_bar)

    def _draw_xp_bar(self, event=None):
        self.xp_canvas.delete("all")
        w = self.xp_canvas.winfo_width()
        if w < 2:
            return
        fill_w = max(0, min(w, int(w * self._xp_bar_pct)))
        self.xp_canvas.create_rectangle(0, 0, fill_w, 6, fill="#e94560", outline="")

    def set_active(self, view_name: str):
        for vid, btn in self.btn_map.items():
            if vid == view_name:
                btn.config(bg=self.BTN_ACT, fg="#ffffff")
            else:
                btn.config(bg=self.BTN_BG, fg=self.FG)
        self.active_view = view_name

    def update_user(self, username: str, xp: int, level: str):
        from utils.config import LEVELS, LEVEL_ORDER
        self.user_label.config(text=username or "Guest")
        emoji = LEVELS.get(level, (0, 0, "🌱"))[2]
        self.user_avatar.config(text=emoji)

        # XP bar fraction
        lvl_data = LEVELS.get(level, (0, 99, "🌱"))
        lo, hi = lvl_data[0], lvl_data[1]
        if hi == float("inf"):
            hi = xp + 100
        span = max(hi - lo, 1)
        pct = min((xp - lo) / span, 1.0)
        self._xp_bar_pct = pct
        self.level_label.config(text=f"{level} | {xp} XP")
        self._draw_xp_bar()
