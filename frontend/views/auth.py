"""Login / Register view."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading


class AuthWindow(tk.Toplevel):
    """Floating login/register dialog."""

    def __init__(self, parent, api_client, on_success):
        super().__init__(parent)
        self.api = api_client
        self.on_success = on_success
        self.title("🎮 Code Quest — Login")
        self.geometry("440x520")
        self.resizable(False, False)
        self.configure(bg="#16213e")
        self.grab_set()
        self._build()

    def _build(self):
        # Header
        tk.Label(self, text="🎮", font=("Segoe UI Emoji", 40),
                 bg="#16213e", fg="#e94560").pack(pady=(30, 4))
        tk.Label(self, text="CODE QUEST", font=("Consolas", 18, "bold"),
                 bg="#16213e", fg="#e94560").pack()
        tk.Label(self, text="Programming Practice Playground",
                 font=("Segoe UI", 9), bg="#16213e", fg="#8888aa").pack(pady=(0, 20))

        # Notebook
        nb = ttk.Notebook(self, bootstyle="dark")
        nb.pack(fill=BOTH, expand=True, padx=24, pady=0)

        self._build_login_tab(nb)
        self._build_register_tab(nb)

        # Status
        self.status_var = tk.StringVar()
        self.status_lbl = tk.Label(self, textvariable=self.status_var,
                                   font=("Segoe UI", 9), bg="#16213e", fg="#e74c3c")
        self.status_lbl.pack(pady=6)

    def _make_entry(self, parent, label: str, show: str = "") -> ttk.Entry:
        tk.Label(parent, text=label, font=("Segoe UI", 10),
                 bg="#1a1a2e", fg="#e0e0e0", anchor="w").pack(fill=X, pady=(10, 2))
        e = ttk.Entry(parent, font=("Segoe UI", 11), show=show, bootstyle="dark")
        e.pack(fill=X, ipady=6)
        return e

    def _build_login_tab(self, nb: ttk.Notebook):
        f = tk.Frame(nb, bg="#1a1a2e", padx=20, pady=16)
        nb.add(f, text="  🔑 Login  ")

        self.login_user = self._make_entry(f, "Username")
        self.login_pass = self._make_entry(f, "Password", show="●")

        ttk.Button(f, text="Login  ▶", bootstyle="danger",
                   command=self._do_login, width=24).pack(pady=14)

        ttk.Button(f, text="🎮 Quick Demo (no server)",
                   bootstyle="secondary-outline",
                   command=self._demo_login, width=24).pack()

    def _build_register_tab(self, nb: ttk.Notebook):
        f = tk.Frame(nb, bg="#1a1a2e", padx=20, pady=16)
        nb.add(f, text="  ✨ Register  ")

        self.reg_user  = self._make_entry(f, "Username (3–20 chars)")
        self.reg_pass  = self._make_entry(f, "Password", show="●")
        self.reg_pass2 = self._make_entry(f, "Confirm Password", show="●")

        ttk.Button(f, text="Create Account  ▶", bootstyle="success",
                   command=self._do_register, width=24).pack(pady=14)

    def _set_status(self, msg: str, color: str = "#e74c3c"):
        self.status_var.set(msg)
        self.status_lbl.config(fg=color)

    def _do_login(self):
        u = self.login_user.get().strip()
        p = self.login_pass.get().strip()
        if not u or not p:
            self._set_status("⚠️  Please fill in all fields.")
            return
        self._set_status("⏳ Logging in...", "#f39c12")
        threading.Thread(target=self._login_thread, args=(u, p), daemon=True).start()

    def _login_thread(self, u: str, p: str):
        result = self.api.login(u, p)
        self.after(0, lambda: self._handle_auth_result(result))

    def _do_register(self):
        u  = self.reg_user.get().strip()
        p  = self.reg_pass.get().strip()
        p2 = self.reg_pass2.get().strip()
        if not u or not p:
            self._set_status("⚠️  Please fill in all fields.")
            return
        if p != p2:
            self._set_status("⚠️  Passwords don't match.")
            return
        if len(u) < 3:
            self._set_status("⚠️  Username too short.")
            return
        self._set_status("⏳ Creating account...", "#f39c12")
        threading.Thread(target=self._register_thread, args=(u, p), daemon=True).start()

    def _register_thread(self, u: str, p: str):
        result = self.api.register(u, p)
        self.after(0, lambda: self._handle_auth_result(result))

    def _handle_auth_result(self, result: dict):
        if result.get("success"):
            self._set_status("✅ Success!", "#2ecc71")
            self.after(400, lambda: (self.destroy(), self.on_success(result)))
        else:
            err = result.get("error", "Unknown error")
            self._set_status(f"❌ {err}")

    def _demo_login(self):
        """Bypass auth for offline/demo mode."""
        demo = {
            "success": True, "token": "demo_token",
            "username": "demo_player",
            "xp": 150, "level": "Apprentice",
            "badges": "", "streak": 3, "solved_count": 5,
        }
        self.api.token = "demo_token"
        self.destroy()
        self.on_success(demo)
