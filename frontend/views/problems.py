"""Problem browser view."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading


class ProblemsView(ttk.Frame):
    """Searchable, filterable problem list."""

    DIFF_COLORS = {"easy": "#2ecc71", "medium": "#f39c12", "hard": "#e74c3c"}

    def __init__(self, parent, api_client, on_navigate):
        super().__init__(parent, padding=24)
        self.api = api_client
        self.navigate = on_navigate
        self.problems = []
        self.filter_diff = "all"
        self._build()
        threading.Thread(target=self._load, daemon=True).start()

    def _build(self):
        # Header
        hdr = ttk.Frame(self)
        hdr.pack(fill=X, pady=(0, 16))
        ttk.Label(hdr, text="📚 Problem Library",
                  font=("Segoe UI", 18, "bold")).pack(side=LEFT)
        self.count_lbl = ttk.Label(hdr, text="Loading...",
                                   font=("Segoe UI", 10), bootstyle="secondary")
        self.count_lbl.pack(side=RIGHT, padx=8)

        # Search + filter row
        ctrl = ttk.Frame(self)
        ctrl.pack(fill=X, pady=(0, 12))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._apply_filter())
        ttk.Entry(ctrl, textvariable=self.search_var,
                  font=("Segoe UI", 11),
                  width=30).pack(side=LEFT, padx=(0, 12), ipady=4)
        ttk.Label(ctrl, text="🔍", font=("Segoe UI Emoji", 14)).pack(side=LEFT)

        ttk.Separator(ctrl, orient=VERTICAL).pack(side=LEFT, fill=Y, padx=16)

        diffs = [("All", "all"), ("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]
        self.diff_btns = {}
        for label, val in diffs:
            style = "primary" if val == "all" else "secondary-outline"
            b = ttk.Button(ctrl, text=label, bootstyle=style, width=8,
                           command=lambda v=val: self._set_diff(v))
            b.pack(side=LEFT, padx=2)
            self.diff_btns[val] = b

        # Treeview
        cols = ("id", "title", "difficulty", "category", "xp")
        self.tree = ttk.Treeview(self, columns=cols, show="headings",
                                  bootstyle="dark", height=20)
        self.tree.heading("id",         text="#")
        self.tree.heading("title",      text="Title")
        self.tree.heading("difficulty", text="Difficulty")
        self.tree.heading("category",   text="Category")
        self.tree.heading("xp",         text="XP")

        self.tree.column("id",         width=40,  anchor="center")
        self.tree.column("title",      width=300, anchor="w")
        self.tree.column("difficulty", width=100, anchor="center")
        self.tree.column("category",   width=140, anchor="center")
        self.tree.column("xp",         width=70,  anchor="center")

        # Scrollbar
        sb = ttk.Scrollbar(self, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        sb.pack(side=LEFT, fill=Y)

        # Tags for difficulty colours
        self.tree.tag_configure("easy",   foreground="#2ecc71")
        self.tree.tag_configure("medium", foreground="#f39c12")
        self.tree.tag_configure("hard",   foreground="#e74c3c")

        # Double-click to open
        self.tree.bind("<Double-1>", self._on_select)

        # Bottom bar
        bot = ttk.Frame(self)
        bot.pack(fill=X, pady=(12, 0))
        ttk.Button(bot, text="⚔️  Solve Selected", bootstyle="danger",
                   command=self._on_solve).pack(side=LEFT)
        ttk.Button(bot, text="🔄 Refresh", bootstyle="secondary-outline",
                   command=self.refresh).pack(side=LEFT, padx=8)

    def _load(self):
        problems = self.api.get_problems()
        self.after(0, lambda: self._populate(problems))

    def _populate(self, problems: list):
        self.problems = problems
        self._apply_filter()

    def _apply_filter(self):
        search = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        shown = 0
        for p in self.problems:
            if self.filter_diff != "all" and p["difficulty"] != self.filter_diff:
                continue
            if search and search not in p["title"].lower():
                continue
            diff = p["difficulty"]
            xp_str = f"+{p['xp']} XP"
            self.tree.insert("", END,
                             values=(p["id"], p["title"],
                                     diff.capitalize(), p["category"], xp_str),
                             tags=(diff,))
            shown += 1
        self.count_lbl.config(text=f"{shown} problem(s)")

    def _set_diff(self, val: str):
        self.filter_diff = val
        for v, btn in self.diff_btns.items():
            btn.configure(bootstyle="primary" if v == val else "secondary-outline")
        self._apply_filter()

    def _on_select(self, event):
        item = self.tree.focus()
        if item:
            pid = self.tree.item(item)["values"][0]
            self.navigate("arena", problem_id=int(pid))

    def _on_solve(self):
        item = self.tree.focus()
        if item:
            pid = self.tree.item(item)["values"][0]
            self.navigate("arena", problem_id=int(pid))

    def refresh(self):
        self.count_lbl.config(text="Loading...")
        threading.Thread(target=self._load, daemon=True).start()
