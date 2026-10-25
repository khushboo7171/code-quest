"""Leaderboard view."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading


PODIUM_COLORS = {1: "#FFD700", 2: "#C0C0C0", 3: "#CD7F32"}
LEVEL_EMOJI = {
    "Novice": "🌱", "Apprentice": "⚔️", "Warrior": "🛡️",
    "Champion": "🏆", "Master": "🌟", "Legend": "👑",
}


class LeaderboardView(ttk.Frame):
    """Live leaderboard with podium and ranked table."""

    def __init__(self, parent, api_client):
        super().__init__(parent, padding=24)
        self.api = api_client
        self.leaders = []
        self.my_username = ""
        self._build()
        threading.Thread(target=self._load, daemon=True).start()

    def _build(self):
        # Header
        hdr = ttk.Frame(self)
        hdr.pack(fill=X, pady=(0, 16))
        ttk.Label(hdr, text="🏆 Global Leaderboard",
                  font=("Segoe UI", 18, "bold")).pack(side=LEFT)
        ttk.Button(hdr, text="🔄 Refresh", bootstyle="secondary-outline",
                   command=self.refresh).pack(side=RIGHT)

        # Podium
        ttk.Label(self, text="🥇 Top 3 Players",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))
        self.podium_frame = ttk.Frame(self)
        self.podium_frame.pack(fill=X, pady=(0, 16))

        # Table
        ttk.Label(self, text="📋 Full Rankings",
                  font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0, 8))

        cols = ("rank", "username", "level", "xp", "solved", "badges")
        self.tree = ttk.Treeview(self, columns=cols, show="headings",
                                  bootstyle="dark", height=16)
        self.tree.heading("rank",     text="Rank")
        self.tree.heading("username", text="Player")
        self.tree.heading("level",    text="Level")
        self.tree.heading("xp",       text="XP")
        self.tree.heading("solved",   text="Solved")
        self.tree.heading("badges",   text="Badges")

        self.tree.column("rank",     width=60,  anchor="center")
        self.tree.column("username", width=200, anchor="w")
        self.tree.column("level",    width=130, anchor="center")
        self.tree.column("xp",       width=100, anchor="center")
        self.tree.column("solved",   width=80,  anchor="center")
        self.tree.column("badges",   width=80,  anchor="center")

        sb = ttk.Scrollbar(self, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        sb.pack(side=LEFT, fill=Y)

        self.tree.tag_configure("me",    background="#1a3a5c", foreground="#f0f0f0")
        self.tree.tag_configure("gold",  foreground="#FFD700")
        self.tree.tag_configure("silver",foreground="#C0C0C0")
        self.tree.tag_configure("bronze",foreground="#CD7F32")

    def _build_podium(self):
        for w in self.podium_frame.winfo_children():
            w.destroy()

        order = [1, 0, 2]  # 2nd, 1st, 3rd for podium shape
        heights = [80, 110, 60]

        for i, idx in enumerate(order):
            if idx >= len(self.leaders):
                continue
            p = self.leaders[idx]
            rank = p.get("rank", idx + 1)
            color = PODIUM_COLORS.get(rank, "#888")
            username = p.get("username", "—")
            xp = p.get("xp", 0)
            level = p.get("level", "Novice")
            emoji = LEVEL_EMOJI.get(level, "🌱")

            col = tk.Frame(self.podium_frame, bg="#16213e")
            col.pack(side=LEFT, expand=True)

            tk.Label(col, text=emoji, font=("Segoe UI Emoji", 24),
                     bg="#16213e").pack()
            tk.Label(col, text=username, font=("Segoe UI", 11, "bold"),
                     bg="#16213e", fg=color).pack()
            tk.Label(col, text=f"{xp} XP", font=("Segoe UI", 9),
                     bg="#16213e", fg="#8888aa").pack()

            podium_box = tk.Frame(col, bg=color, height=heights[i])
            podium_box.pack(fill=X, padx=12, pady=4)

            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, "")
            tk.Label(podium_box, text=medal, font=("Segoe UI Emoji", 20),
                     bg=color).pack(expand=True)

    def _populate_table(self):
        self.tree.delete(*self.tree.get_children())

        # Get my username
        profile = self.api.get_profile()
        self.my_username = profile.get("username", "") if not profile.get("error") else ""

        for p in self.leaders:
            rank     = p.get("rank", "—")
            username = p.get("username", "—")
            level    = p.get("level", "Novice")
            xp       = p.get("xp", 0)
            solved   = p.get("solved_count", 0)
            badges   = p.get("badge_count", 0)

            emoji = LEVEL_EMOJI.get(level, "")
            medal_map = {1: "🥇", 2: "🥈", 3: "🥉"}
            rank_str = medal_map.get(rank, f"#{rank}")

            tag = "me" if username == self.my_username else \
                  "gold" if rank == 1 else \
                  "silver" if rank == 2 else \
                  "bronze" if rank == 3 else ""

            self.tree.insert("", END,
                             values=(rank_str, username,
                                     f"{emoji} {level}", xp, solved, badges),
                             tags=(tag,))

    def _load(self):
        leaders = self.api.get_leaderboard()
        self.after(0, lambda: self._update(leaders))

    def _update(self, leaders: list):
        self.leaders = leaders
        self._build_podium()
        self._populate_table()

    def refresh(self):
        threading.Thread(target=self._load, daemon=True).start()
