"""User profile view."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading


LEVEL_EMOJI = {
    "Novice": "🌱", "Apprentice": "⚔️", "Warrior": "🛡️",
    "Champion": "🏆", "Master": "🌟", "Legend": "👑",
}
BADGES_INFO = {
    "first_solve": ("🎯", "First Blood",     "Solved your first problem"),
    "easy_5":      ("⭐", "Easy Street",     "Solved 5 easy problems"),
    "medium_3":    ("🔥", "Getting Serious", "Solved 3 medium problems"),
    "hard_1":      ("💎", "Diamond Mind",    "Solved a hard problem"),
    "xp_100":      ("🏅", "Century",         "Earned 100 XP"),
    "xp_500":      ("🥇", "Gold Rush",       "Earned 500 XP"),
    "streak_3":    ("🌊", "On a Roll",       "3-day streak"),
}


class ProfileView(ttk.Frame):
    """User profile with stats, badges and submission history."""

    def __init__(self, parent, api_client, on_navigate):
        super().__init__(parent, padding=24)
        self.api = api_client
        self.navigate = on_navigate
        self._build()
        threading.Thread(target=self._load, daemon=True).start()

    def _build(self):
        # Scrollable
        canvas = tk.Canvas(self, highlightthickness=0)
        sb = ttk.Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        self.inner = ttk.Frame(canvas, padding=8)
        win = canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        self.inner.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))

        # Avatar + name row
        top = ttk.Frame(self.inner)
        top.pack(fill=X, pady=(0, 20))

        self.avatar_lbl = tk.Label(top, text="🌱",
                                   font=("Segoe UI Emoji", 52),
                                   bg=self.inner.cget("background") if hasattr(self.inner, 'cget') else "#fff")
        self.avatar_lbl.pack(side=LEFT, padx=(0, 20))

        info = ttk.Frame(top)
        info.pack(side=LEFT, fill=Y)

        self.name_lbl = ttk.Label(info, text="Loading...",
                                  font=("Segoe UI", 20, "bold"))
        self.name_lbl.pack(anchor="w")

        self.level_lbl = ttk.Label(info, text="Novice",
                                   font=("Segoe UI", 12), bootstyle="secondary")
        self.level_lbl.pack(anchor="w")

        self.xp_bar = ttk.Progressbar(info, value=0, length=260,
                                       bootstyle="danger-striped")
        self.xp_bar.pack(anchor="w", pady=6)

        self.xp_detail = ttk.Label(info, text="0 XP",
                                   font=("Segoe UI", 9), bootstyle="secondary")
        self.xp_detail.pack(anchor="w")

        ttk.Separator(self.inner).pack(fill=X, pady=12)

        # Stats
        ttk.Label(self.inner, text="📊 Statistics",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 8))

        stats_row = ttk.Frame(self.inner)
        stats_row.pack(fill=X, pady=(0, 16))
        self.stat_widgets = {}
        for i, (key, icon, label, style) in enumerate([
            ("solved",  "✅", "Solved",  "success"),
            ("streak",  "🔥", "Streak",  "warning"),
            ("xp",      "⚡", "XP",      "danger"),
        ]):
            f = ttk.Frame(stats_row, bootstyle=style, padding=14)
            f.grid(row=0, column=i, padx=6, sticky="nsew")
            stats_row.columnconfigure(i, weight=1)
            tk.Label(f, text=icon, font=("Segoe UI Emoji", 20),
                     bg=f.cget("background") if hasattr(f, 'cget') else "#fff").pack()
            val = ttk.Label(f, text="—", font=("Segoe UI", 18, "bold"))
            val.pack()
            ttk.Label(f, text=label, font=("Segoe UI", 9)).pack()
            self.stat_widgets[key] = val

        ttk.Separator(self.inner).pack(fill=X, pady=12)

        # Badges
        ttk.Label(self.inner, text="🎖️ Badges",
                  font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 8))
        self.badges_frame = ttk.Frame(self.inner)
        self.badges_frame.pack(fill=X, pady=(0, 16))

        ttk.Separator(self.inner).pack(fill=X, pady=12)

        # Logout
        ttk.Button(self.inner, text="🚪 Logout", bootstyle="danger-outline",
                   command=self._logout).pack(anchor="w")

    def _load(self):
        profile = self.api.get_profile()
        self.after(0, lambda: self._update(profile))

    def _update(self, profile: dict):
        from utils.config import LEVELS
        if profile.get("error"):
            self.name_lbl.config(text="Not logged in")
            return

        username = profile.get("username", "—")
        xp       = profile.get("xp", 0)
        level    = profile.get("level", "Novice")
        solved   = profile.get("solved_count", 0)
        streak   = profile.get("streak", 0)
        badges   = profile.get("badges", "")

        emoji = LEVEL_EMOJI.get(level, "🌱")
        self.avatar_lbl.config(text=emoji)
        self.name_lbl.config(text=username)
        self.level_lbl.config(text=f"{emoji} {level}")
        self.xp_detail.config(text=f"{xp} XP total")

        # XP bar
        lvl_data = LEVELS.get(level, (0, 99, "🌱"))
        lo, hi = lvl_data[0], lvl_data[1]
        if hi == float("inf"):
            hi = xp + 200
        pct = min(100, int((xp - lo) / max(hi - lo, 1) * 100))
        self.xp_bar["value"] = pct

        self.stat_widgets["solved"].config(text=str(solved))
        self.stat_widgets["streak"].config(text=f"{streak}d")
        self.stat_widgets["xp"].config(text=str(xp))

        # Badges
        for w in self.badges_frame.winfo_children():
            w.destroy()
        badge_list = [b.strip() for b in badges.split(",") if b.strip()] if badges else []
        if not badge_list:
            ttk.Label(self.badges_frame,
                      text="No badges yet — solve problems to earn them! 🎯",
                      font=("Segoe UI", 10), bootstyle="secondary").pack(anchor="w")
        else:
            for i, badge in enumerate(badge_list):
                info = BADGES_INFO.get(badge, ("🏅", badge, ""))
                f = ttk.Frame(self.badges_frame, bootstyle="dark", padding=10)
                f.grid(row=i // 4, column=i % 4, padx=6, pady=4)
                tk.Label(f, text=info[0], font=("Segoe UI Emoji", 22)).pack()
                ttk.Label(f, text=info[1], font=("Segoe UI", 8, "bold")).pack()

    def _logout(self):
        self.api.logout()
        self.navigate("home")
