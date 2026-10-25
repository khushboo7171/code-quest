"""Arena view — problem description + code editor + judge."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading

from widgets.code_editor import CodeEditor
from utils.config import STARTER_CODE, SAMPLE_PROBLEM_DETAIL


LANG_DISPLAY = {
    "python": "Python 3",
    "cpp":    "C++17",
    "c":      "C",
}

VERDICT_STYLES = {
    "AC":  ("#2ecc71", "✅ Accepted"),
    "WA":  ("#e74c3c", "❌ Wrong Answer"),
    "CE":  ("#e67e22", "💥 Compile Error"),
    "TLE": ("#f39c12", "⏰ Time Limit Exceeded"),
}


class ArenaView(ttk.Frame):
    """The main code editor + judging arena."""

    def __init__(self, parent, api_client, on_navigate):
        super().__init__(parent)
        self.api = api_client
        self.navigate = on_navigate
        self.current_problem = None
        self.language = tk.StringVar(value="python")
        self._build()

    def _build(self):
        # Top toolbar
        toolbar = tk.Frame(self, bg="#16213e", height=44)
        toolbar.pack(fill=X, side=TOP)
        toolbar.pack_propagate(False)

        ttk.Label(toolbar, text="⚔️  Code Arena",
                  font=("Segoe UI", 13, "bold"),
                  background="#16213e", foreground="#e94560").pack(side=LEFT, padx=16, pady=8)

        # Language selector
        ttk.Label(toolbar, text="Language:",
                  background="#16213e", foreground="#e0e0e0").pack(side=RIGHT, padx=(0, 4), pady=8)
        lang_cb = ttk.Combobox(toolbar, textvariable=self.language,
                                values=["python", "cpp", "c"],
                                state="readonly", width=10, bootstyle="dark")
        lang_cb.pack(side=RIGHT, padx=8, pady=8)
        lang_cb.bind("<<ComboboxSelected>>", self._on_lang_change)

        # Main paned window (left: problem, right: editor)
        pane = tk.PanedWindow(self, orient=HORIZONTAL, sashwidth=6,
                              bg="#0f0f1a", bd=0)
        pane.pack(fill=BOTH, expand=True)

        # ── LEFT: Problem Description ─────────────────────────────────────────
        left = ttk.Frame(pane, padding=0)
        pane.add(left, minsize=300, width=420)

        prob_hdr = tk.Frame(left, bg="#1a1a2e", pady=12, padx=16)
        prob_hdr.pack(fill=X)
        self.prob_title = tk.Label(prob_hdr, text="Select a Problem",
                                   font=("Segoe UI", 14, "bold"),
                                   bg="#1a1a2e", fg="#e0e0e0", anchor="w")
        self.prob_title.pack(fill=X)
        self.prob_diff  = tk.Label(prob_hdr, text="",
                                   font=("Segoe UI", 10),
                                   bg="#1a1a2e", fg="#8888aa", anchor="w")
        self.prob_diff.pack(fill=X)

        prob_scroll = ttk.Scrollbar(left, orient=VERTICAL)
        prob_scroll.pack(side=RIGHT, fill=Y)
        self.prob_text = tk.Text(left, wrap=WORD, font=("Segoe UI", 10),
                                  bg="#1a1a2e", fg="#d0d0d0",
                                  yscrollcommand=prob_scroll.set,
                                  relief=FLAT, padx=16, pady=12,
                                  state=DISABLED, cursor="arrow")
        self.prob_text.pack(fill=BOTH, expand=True)
        prob_scroll.config(command=self.prob_text.yview)

        # Tags for description styling
        self.prob_text.tag_config("section",  font=("Segoe UI", 11, "bold"), foreground="#e94560")
        self.prob_text.tag_config("example",  font=("Courier New", 9),        foreground="#b5cea8",
                                              background="#252526")
        self.prob_text.tag_config("hint",     foreground="#f39c12")
        self.prob_text.tag_config("constraint", foreground="#8888aa")

        # ── RIGHT: Editor + Output ────────────────────────────────────────────
        right = ttk.Frame(pane, padding=0)
        pane.add(right, minsize=400)

        right_pane = tk.PanedWindow(right, orient=VERTICAL, sashwidth=5,
                                    bg="#0f0f1a", bd=0)
        right_pane.pack(fill=BOTH, expand=True)

        # Editor
        editor_frame = ttk.Frame(right_pane, padding=0)
        right_pane.add(editor_frame, minsize=200, height=420)

        # Editor toolbar
        ed_bar = tk.Frame(editor_frame, bg="#252526", height=36)
        ed_bar.pack(fill=X)
        ed_bar.pack_propagate(False)

        ttk.Button(ed_bar, text="▶  Run Code", bootstyle="success",
                   command=self._run_code).pack(side=LEFT, padx=8, pady=4)
        ttk.Button(ed_bar, text="🔄 Reset", bootstyle="secondary-outline",
                   command=self._reset_code).pack(side=LEFT, pady=4)
        ttk.Button(ed_bar, text="💡 Hint", bootstyle="warning-outline",
                   command=self._show_hint).pack(side=LEFT, padx=8, pady=4)

        self.editor = CodeEditor(editor_frame)
        self.editor.pack(fill=BOTH, expand=True)
        self.editor.set_code("# Select a problem from the Problems tab to start!\n")

        # Output panel
        out_frame = tk.Frame(right_pane, bg="#1e1e1e")
        right_pane.add(out_frame, minsize=120, height=200)

        out_hdr = tk.Frame(out_frame, bg="#252526", height=32)
        out_hdr.pack(fill=X)
        out_hdr.pack_propagate(False)
        tk.Label(out_hdr, text="📤 Output", font=("Segoe UI", 10, "bold"),
                 bg="#252526", fg="#e0e0e0").pack(side=LEFT, padx=12, pady=6)

        self.verdict_lbl = tk.Label(out_hdr, text="",
                                    font=("Segoe UI", 10, "bold"),
                                    bg="#252526")
        self.verdict_lbl.pack(side=RIGHT, padx=12, pady=6)

        self.runtime_lbl = tk.Label(out_hdr, text="",
                                    font=("Segoe UI", 9),
                                    bg="#252526", fg="#8888aa")
        self.runtime_lbl.pack(side=RIGHT, padx=8, pady=6)

        self.output_text = tk.Text(out_frame, font=("Consolas", 10),
                                    bg="#1e1e1e", fg="#d4d4d4",
                                    relief=FLAT, padx=10, pady=8,
                                    state=DISABLED)
        self.output_text.pack(fill=BOTH, expand=True)

        # XP animation label (hidden)
        self.xp_lbl = tk.Label(self, text="+0 XP! 🎉",
                                font=("Segoe UI", 20, "bold"),
                                bg="#16213e", fg="#2ecc71")

    def load_problem(self, problem_id: int):
        """Load a problem into the view."""
        self._set_output("⏳ Loading problem...")
        threading.Thread(target=self._fetch_problem,
                         args=(problem_id,), daemon=True).start()

    def _fetch_problem(self, pid: int):
        prob = self.api.get_problem(pid)
        self.after(0, lambda: self._display_problem(prob))

    def _display_problem(self, prob: dict):
        self.current_problem = prob
        pid = prob.get("id", 0)

        # Title
        diff = prob.get("difficulty", "easy")
        diff_colors = {"easy": "#2ecc71", "medium": "#f39c12", "hard": "#e74c3c"}
        self.prob_title.config(text=prob.get("title", "Unknown"))
        self.prob_diff.config(
            text=f"{diff.capitalize()}  |  Category: {prob.get('category', '—')}  |  +{prob.get('xp', 0)} XP",
            fg=diff_colors.get(diff, "#e0e0e0"))

        # Description text
        self.prob_text.config(state=NORMAL)
        self.prob_text.delete("1.0", END)

        self._append_prob("📄 Description\n", "section")
        self._append_prob(prob.get("description", "") + "\n\n")

        examples = prob.get("examples", [])
        if examples:
            self._append_prob("📌 Examples\n", "section")
            for ex in examples:
                self._append_prob(ex + "\n\n", "example")

        constraints = prob.get("constraints", [])
        if constraints:
            self._append_prob("⚖️  Constraints\n", "section")
            for c in constraints:
                self._append_prob(f"  • {c}\n", "constraint")
            self._append_prob("\n")

        vis_tests = prob.get("visible_tests", [])
        if vis_tests:
            self._append_prob("🧪 Sample Test Cases\n", "section")
            for i, tc in enumerate(vis_tests, 1):
                self._append_prob(f"  Case {i}:\n", "hint")
                self._append_prob(f"  Input:    {tc.get('input', '')}\n", "example")
                self._append_prob(f"  Expected: {tc.get('expected', '')}\n\n", "example")

        self.prob_text.config(state=DISABLED)

        # Load starter code
        lang = self.language.get()
        starters = STARTER_CODE.get(lang, {})
        code = starters.get(pid) or starters.get("default", "# Write your solution here\n")
        self.editor.set_code(code)
        self.editor.set_language(lang)
        self._set_output("✅ Problem loaded. Write your solution and click ▶ Run Code!")

    def _append_prob(self, text: str, tag: str = None):
        if tag:
            self.prob_text.insert(END, text, tag)
        else:
            self.prob_text.insert(END, text)

    def _on_lang_change(self, event):
        lang = self.language.get()
        self.editor.set_language(lang)
        if self.current_problem:
            pid = self.current_problem.get("id", 0)
            starters = STARTER_CODE.get(lang, {})
            code = starters.get(pid) or starters.get("default", "// Write your solution here\n")
            self.editor.set_code(code)

    def _run_code(self):
        if not self.current_problem:
            self._set_output("⚠️  Please select a problem first!")
            return
        code = self.editor.get_code().strip()
        if not code:
            self._set_output("⚠️  Write some code first!")
            return
        self._set_output("⏳ Judging your solution...")
        self.verdict_lbl.config(text="⏳ Running...", fg="#f39c12")
        pid  = self.current_problem["id"]
        lang = self.language.get()
        threading.Thread(target=self._judge_thread,
                         args=(pid, code, lang), daemon=True).start()

    def _judge_thread(self, pid, code, lang):
        result = self.api.submit_code(pid, code, lang)
        self.after(0, lambda: self._show_result(result))

    def _show_result(self, result: dict):
        if result.get("error") and result.get("offline"):
            self._set_output(f"⚠️  Backend offline.\n\nError: {result['error']}\n\n"
                             "Start the C++ backend first, or use demo mode.")
            self.verdict_lbl.config(text="⚠️ Offline", fg="#f39c12")
            return

        status  = result.get("status", "WA")
        passed  = result.get("passed", 0)
        total   = result.get("total", 0)
        ms      = result.get("runtime_ms", 0)
        output  = result.get("output", "")
        error   = result.get("error", "")
        xp      = result.get("xp_earned", 0)

        color, label = VERDICT_STYLES.get(status, ("#888", f"❓ {status}"))
        self.verdict_lbl.config(text=label, fg=color)
        self.runtime_lbl.config(text=f"{ms}ms")

        lines = [f"{label}\n", f"Test Cases: {passed}/{total} passed\n",
                 f"Runtime:    {ms} ms\n"]
        if output:
            lines += ["\n── Output ──\n", output]
        if error:
            lines += ["\n── Error ──\n", error]
        if xp > 0:
            lines += [f"\n🎉 +{xp} XP earned!"]

        self._set_output("".join(lines))

        if xp > 0:
            self._animate_xp(xp)

    def _set_output(self, text: str):
        self.output_text.config(state=NORMAL)
        self.output_text.delete("1.0", END)
        self.output_text.insert("1.0", text)
        self.output_text.config(state=DISABLED)

    def _animate_xp(self, xp: int):
        self.xp_lbl.config(text=f"+{xp} XP! 🎉")
        self.xp_lbl.place(relx=0.7, rely=0.6)
        self._xp_anim_step(0)

    def _xp_anim_step(self, step: int):
        if step > 20:
            self.xp_lbl.place_forget()
            return
        alpha = max(0, 1.0 - step / 20)
        y = 0.6 - step * 0.01
        self.xp_lbl.place(relx=0.7, rely=y)
        self.after(40, lambda: self._xp_anim_step(step + 1))

    def _reset_code(self):
        if self.current_problem:
            self._on_lang_change(None)
        else:
            self.editor.set_code("# Write your solution here\n")

    def _show_hint(self):
        if not self.current_problem:
            return
        hints = self.current_problem.get("hints", [])
        if hints:
            self._set_output("💡 Hints:\n\n" + "\n".join(f"  {i+1}. {h}" for i, h in enumerate(hints)))
        else:
            self._set_output("No hints available for this problem.")
