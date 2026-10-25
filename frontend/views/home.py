"""Home dashboard view."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading


class HomeView(ttk.Frame):
    """Game-like home dashboard shown after login."""

    def __init__(self, parent, api_client, on_navigate):
        super().__init__(parent)
        self.api = api_client
        self.navigate = on_navigate
        self.user = {}
        self.daily = {}
        self._build()
        threading.Thread(target=self._load_data, daemon=True).start()

    def _build(self):
        self.configure(padding=0)

        # Scrollable canvas
        canvas = tk.Canvas(self, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.inner = ttk.Frame(canvas, padding=24)
        self.inner_id = canvas.create_window((0, 0), window=self.inner, anchor="nw")

        def _resize(e):
            canvas.itemconfig(self.inner_id, width=e.width)
        canvas.bind("<Configure>", _resize)
        self.inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        self._build_header()
        self._build_stats()
        self._build_daily()
        self._build_quick_actions()

    def _build_header(self):
        hdr = ttk.Frame(self.inner, padding=(0, 0, 0, 16))
        hdr.pack(fill=X)

        # Welcome
        self.welcome_lbl = ttk.Label(hdr,
            text="Welcome to Code Quest! 🎮",
            font=("Segoe UI", 20, "bold"), bootstyle="inverse-dark")
        self.welcome_lbl.pack(anchor="w")

        self.sub_lbl = ttk.Label(hdr,
            text="Level up your programming skills through fun challenges!",
            font=("Segoe UI", 11), bootstyle="secondary")
        self.sub_lbl.pack(anchor="w", pady=(4, 0))

        # XP bar
        xp_row = ttk.Frame(self.inner)
        xp_row.pack(fill=X, pady=(0, 16))

        self.level_lbl = ttk.Label(xp_row, text="🌱 Novice",
                                   font=("Segoe UI", 12, "bold"))
        self.level_lbl.pack(side=LEFT)

        self.xp_lbl = ttk.Label(xp_row, text="0 XP",
                                 font=("Segoe UI", 10), bootstyle="secondary")
        self.xp_lbl.pack(side=RIGHT)

        self.xp_bar = ttk.Progressbar(self.inner, value=0,
                                       bootstyle="danger-striped", length=400)
        self.xp_bar.pack(fill=X, pady=(0, 20))

        ttk.Separator(self.inner).pack(fill=X, pady=8)

    def _build_stats(self):
        ttk.Label(self.inner, text="📊 Your Stats",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(8, 8))

        grid = ttk.Frame(self.inner)
        grid.pack(fill=X, pady=(0, 16))

        self.stat_cards = {}
        stats = [
            ("solved",  "✅", "Solved",      "0",   "success"),
            ("streak",  "🔥", "Streak",      "0d",  "warning"),
            ("rank",    "🏆", "Global Rank", "#—",  "primary"),
            ("badges",  "🎖️", "Badges",      "0",   "danger"),
        ]
        for i, (key, icon, label, default, style) in enumerate(stats):
            card = self._make_stat_card(grid, icon, label, default, style)
            card.grid(row=0, column=i, padx=6, pady=4, sticky="nsew")
            grid.columnconfigure(i, weight=1)
            self.stat_cards[key] = card

    def _make_stat_card(self, parent, icon, label, value, style):
        card = ttk.Frame(parent, bootstyle=style, padding=16)
        tk.Label(card, text=icon, font=("Segoe UI Emoji", 22),
                 bg=card.cget("background") if hasattr(card, 'cget') else "#fff").pack()
        lbl = ttk.Label(card, text=value, font=("Segoe UI", 18, "bold"))
        lbl.pack()
        ttk.Label(card, text=label, font=("Segoe UI", 9)).pack()
        card._value_label = lbl
        return card

    def _build_daily(self):
        ttk.Label(self.inner, text="⚡ Daily Challenge",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(8, 8))

        self.daily_card = ttk.Frame(self.inner, bootstyle="dark", padding=20)
        self.daily_card.pack(fill=X, pady=(0, 16))

        self.daily_title = ttk.Label(self.daily_card,
            text="Loading daily challenge...",
            font=("Segoe UI", 14, "bold"))
        self.daily_title.pack(anchor="w")

        self.daily_diff = ttk.Label(self.daily_card, text="",
                                    font=("Segoe UI", 10))
        self.daily_diff.pack(anchor="w", pady=4)

        ttk.Button(self.daily_card, text="Play Daily Challenge  ⚔️",
                   bootstyle="danger", command=self._open_daily).pack(anchor="w", pady=8)

    def _build_quick_actions(self):
        ttk.Label(self.inner, text="🚀 Quick Actions",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(8, 8))

        btns = ttk.Frame(self.inner)
        btns.pack(fill=X)

        actions = [
            ("📚 Browse Problems",  "primary",   "problems"),
            ("⚔️  Enter Arena",     "danger",    "arena"),
            ("🏆 Leaderboard",      "warning",   "leaderboard"),
            ("👤 My Profile",       "secondary", "profile"),
        ]
        for i, (label, style, view) in enumerate(actions):
            ttk.Button(btns, text=label, bootstyle=style,
                       command=lambda v=view: self.navigate(v),
                       width=18).grid(row=0, column=i, padx=6)
            btns.columnconfigure(i, weight=1)

    # ── Data loading ──────────────────────────────────────────────────────────

    def _load_data(self):
        profile = self.api.get_profile()
        daily   = self.api.get_daily()
        self.after(0, lambda: self._update_ui(profile, daily))

    def _update_ui(self, profile: dict, daily: dict):
        from utils.config import LEVELS

        if not profile.get("error"):
            self.user = profile
            username = profile.get("username", "Player")
            xp       = profile.get("xp", 0)
            level    = profile.get("level", "Novice")
            solved   = profile.get("solved_count", 0)
            streak   = profile.get("streak", 0)

            self.welcome_lbl.config(text=f"Welcome back, {username}! 🎮")
            emoji = LEVELS.get(level, (0, 0, "🌱"))[2]
            self.level_lbl.config(text=f"{emoji} {level}")
            self.xp_lbl.config(text=f"{xp} XP")

            # XP bar
            lvl_data = LEVELS.get(level, (0, 99, "🌱"))
            lo, hi = lvl_data[0], lvl_data[1]
            if hi == float("inf"):
                hi = xp + 200
            pct = min(100, int((xp - lo) / max(hi - lo, 1) * 100))
            self.xp_bar["value"] = pct

            # Stats
            self.stat_cards["solved"]._value_label.config(text=str(solved))
            self.stat_cards["streak"]._value_label.config(text=f"{streak}d")

        if not daily.get("error"):
            self.daily = daily
            self.daily_title.config(text=daily.get("title", "—"))
            diff = daily.get("difficulty", "easy")
            self.daily_diff.config(
                text=f"Difficulty: {diff.capitalize()}  |  XP: +{daily.get('xp', 10)}")

    def _open_daily(self):
        pid = self.daily.get("id", 1)
        self.navigate("arena", problem_id=pid)
