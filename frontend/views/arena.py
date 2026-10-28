"""Arena view — LeetCode-style problem description + code editor + judge."""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import threading

from widgets.code_editor import CodeEditor
from utils.config import STARTER_CODE, SAMPLE_PROBLEM_DETAIL, LOCAL_TEST_CASES
from utils.harness import wrap_user_code


LANG_DISPLAY = {
    "python": "🐍 Python 3",
    "cpp":    "⚡ C++17",
    "c":      "🔧 C",
}

VERDICT_STYLES = {
    "AC":    ("#2ecc71", "✅ Accepted"),
    "WA":    ("#e74c3c", "❌ Wrong Answer"),
    "CE":    ("#e67e22", "💥 Compile Error"),
    "TLE":   ("#f39c12", "⏰ Time Limit Exceeded"),
    "RE":    ("#e74c3c", "💥 Runtime Error"),
    "ERROR": ("#e74c3c", "⚠️ System Error"),
}


class ArenaView(ttk.Frame):
    """The main code editor + judging arena with LeetCode-style layout."""

    def __init__(self, parent, api_client, on_navigate):
        super().__init__(parent)
        self.api = api_client
        self.navigate = on_navigate
        self.current_problem = None
        self.language = tk.StringVar(value="python")
        self.active_testcase_idx = 0
        self.example_cards = []
        self._build()

    def _build(self):
        # ── Top toolbar ────────────────────────────────────────────────────────
        toolbar = tk.Frame(self, bg="#16213e", height=44)
        toolbar.pack(fill=X, side=TOP)
        toolbar.pack_propagate(False)

        ttk.Label(toolbar, text="⚔️  Code Arena",
                  font=("Segoe UI", 13, "bold"),
                  background="#16213e", foreground="#e94560").pack(side=LEFT, padx=16, pady=8)

        self.lang_status_lbl = ttk.Label(toolbar, text="Active: 🐍 Python 3",
                                         font=("Segoe UI", 9, "bold"),
                                         bootstyle="info",
                                         background="#16213e")
        self.lang_status_lbl.pack(side=RIGHT, padx=16, pady=8)

        # ── Main horizontal PanedWindow ───────────────────────────────────────
        pane = tk.PanedWindow(self, orient=HORIZONTAL, sashwidth=6,
                              bg="#0f0f1a", bd=0)
        pane.pack(fill=BOTH, expand=True)

        # ── LEFT: Problem Description ─────────────────────────────────────────
        left = ttk.Frame(pane, padding=0)
        pane.add(left, minsize=320, width=460)

        # Problem Header Card
        prob_hdr = tk.Frame(left, bg="#1a1a2e", pady=12, padx=16)
        prob_hdr.pack(fill=X)

        self.prob_title = tk.Label(prob_hdr, text="Select a Problem",
                                   font=("Segoe UI", 14, "bold"),
                                   bg="#1a1a2e", fg="#ffffff", anchor="w")
        self.prob_title.pack(fill=X)

        # Badges row
        self.badges_row = tk.Frame(prob_hdr, bg="#1a1a2e")
        self.badges_row.pack(fill=X, pady=(6, 0))

        self.diff_badge = ttk.Label(self.badges_row, text="Easy", bootstyle="success",
                                    font=("Segoe UI", 8, "bold"))
        self.diff_badge.pack(side=LEFT, padx=(0, 6))

        self.cat_badge = ttk.Label(self.badges_row, text="Arrays", bootstyle="secondary",
                                   font=("Segoe UI", 8))
        self.cat_badge.pack(side=LEFT, padx=(0, 6))

        self.xp_badge = ttk.Label(self.badges_row, text="+10 XP", bootstyle="warning",
                                  font=("Segoe UI", 8, "bold"))
        self.xp_badge.pack(side=LEFT)

        # Scrollable text container for description & examples
        prob_scroll = ttk.Scrollbar(left, orient=VERTICAL)
        prob_scroll.pack(side=RIGHT, fill=Y)

        self.prob_text = tk.Text(left, wrap=WORD, font=("Segoe UI", 10),
                                 bg="#151522", fg="#dcdcdc",
                                 yscrollcommand=prob_scroll.set,
                                 relief=FLAT, padx=16, pady=12,
                                 state=DISABLED, cursor="arrow")
        self.prob_text.pack(fill=BOTH, expand=True)
        prob_scroll.config(command=self.prob_text.yview)

        # Text tags styling
        self.prob_text.tag_config("heading", font=("Segoe UI", 11, "bold"), foreground="#e94560")
        self.prob_text.tag_config("desc", font=("Segoe UI", 10), foreground="#e0e0e0")
        self.prob_text.tag_config("constraint_bullet", font=("Segoe UI", 10, "bold"), foreground="#f39c12")
        self.prob_text.tag_config("constraint_text", font=("Consolas", 9), foreground="#bbbbbb")

        # ── RIGHT: Editor + LeetCode-style Tabs ────────────────────────────────
        right = ttk.Frame(pane, padding=0)
        pane.add(right, minsize=420)

        right_pane = tk.PanedWindow(right, orient=VERTICAL, sashwidth=5,
                                    bg="#0f0f1a", bd=0)
        right_pane.pack(fill=BOTH, expand=True)

        # Editor Frame
        editor_frame = ttk.Frame(right_pane, padding=0)
        right_pane.add(editor_frame, minsize=220, height=440)

        # Editor toolbar
        ed_bar = tk.Frame(editor_frame, bg="#252526", height=42)
        ed_bar.pack(fill=X)
        ed_bar.pack_propagate(False)

        ttk.Button(ed_bar, text="▶  Run Code", bootstyle="success",
                   command=self._run_code).pack(side=LEFT, padx=8, pady=5)
        ttk.Button(ed_bar, text="🔄 Reset", bootstyle="secondary-outline",
                   command=self._reset_code).pack(side=LEFT, pady=5)
        ttk.Button(ed_bar, text="💡 Hint", bootstyle="warning-outline",
                   command=self._show_hint).pack(side=LEFT, padx=8, pady=5)

        # Prominent Language Selection Bar
        lang_box = tk.Frame(ed_bar, bg="#252526")
        lang_box.pack(side=RIGHT, padx=8)

        tk.Label(lang_box, text="Language:", bg="#252526", fg="#aaaaaa",
                 font=("Segoe UI", 9, "bold")).pack(side=LEFT, padx=(0, 6))

        self.lang_btns = {}
        for l_key, l_title in [("python", "🐍 Python 3"), ("cpp", "⚡ C++17"), ("c", "🔧 C")]:
            btn = ttk.Button(lang_box, text=l_title,
                             bootstyle="info" if l_key == self.language.get() else "secondary-outline",
                             command=lambda k=l_key: self.set_language(k))
            btn.pack(side=LEFT, padx=3, pady=5)
            self.lang_btns[l_key] = btn

        self.editor = CodeEditor(editor_frame)
        self.editor.pack(fill=BOTH, expand=True)
        self.editor.set_code("# Select a problem from the Problems tab to start!\n")

        # ── BOTTOM: LeetCode-style Notebook (Testcase / Result) ──────────────
        bottom_frame = tk.Frame(right_pane, bg="#1e1e1e")
        right_pane.add(bottom_frame, minsize=140, height=220)

        self.bottom_nb = ttk.Notebook(bottom_frame, bootstyle="dark")
        self.bottom_nb.pack(fill=BOTH, expand=True)

        self._build_testcase_tab()
        self._build_result_tab()

        # XP animation label (hidden initially)
        self.xp_lbl = tk.Label(self, text="+0 XP! 🎉",
                                font=("Segoe UI", 20, "bold"),
                                bg="#16213e", fg="#2ecc71")

    def _build_testcase_tab(self):
        """LeetCode-style interactive Testcase Tab."""
        self.testcase_tab = tk.Frame(self.bottom_nb, bg="#1e1e1e", padx=12, pady=8)
        self.bottom_nb.add(self.testcase_tab, text="  🧪 Testcase  ")

        # Top row: Case buttons (Case 1, Case 2, Case 3)
        self.tc_buttons_frame = tk.Frame(self.testcase_tab, bg="#1e1e1e")
        self.tc_buttons_frame.pack(fill=X, pady=(0, 6))

        self.tc_feedback_lbl = tk.Label(self.testcase_tab, text="", font=("Segoe UI", 8),
                                        bg="#1e1e1e", fg="#2ecc71", anchor="w")
        self.tc_feedback_lbl.pack(fill=X, pady=(0, 4))

        # Testcase Details Box
        tc_box = tk.Frame(self.testcase_tab, bg="#252526", padx=10, pady=8, relief=FLAT)
        tc_box.pack(fill=BOTH, expand=True)

        tk.Label(tc_box, text="Input:", font=("Segoe UI", 9, "bold"),
                 bg="#252526", fg="#8888aa", anchor="w").pack(fill=X)

        self.tc_input_text = tk.Text(tc_box, height=2, font=("Consolas", 10),
                                     bg="#1e1e1e", fg="#9cdcfe", relief=FLAT, padx=6, pady=4)
        self.tc_input_text.pack(fill=X, pady=(2, 6))

        tk.Label(tc_box, text="Expected Output:", font=("Segoe UI", 9, "bold"),
                 bg="#252526", fg="#8888aa", anchor="w").pack(fill=X)

        self.tc_expected_text = tk.Text(tc_box, height=1, font=("Consolas", 10),
                                        bg="#1e1e1e", fg="#ce9178", relief=FLAT, padx=6, pady=4)
        self.tc_expected_text.pack(fill=X, pady=(2, 0))

    def _build_result_tab(self):
        """LeetCode-style Test Result Tab."""
        self.result_tab = tk.Frame(self.bottom_nb, bg="#1e1e1e", padx=12, pady=6)
        self.bottom_nb.add(self.result_tab, text="  📤 Test Result  ")

        # Result Header bar
        res_hdr = tk.Frame(self.result_tab, bg="#1e1e1e")
        res_hdr.pack(fill=X, pady=(0, 4))

        self.verdict_lbl = tk.Label(res_hdr, text="No submissions yet",
                                    font=("Segoe UI", 11, "bold"),
                                    bg="#1e1e1e", fg="#8888aa")
        self.verdict_lbl.pack(side=LEFT)

        self.runtime_lbl = tk.Label(res_hdr, text="",
                                    font=("Segoe UI", 9),
                                    bg="#1e1e1e", fg="#aaaaaa")
        self.runtime_lbl.pack(side=RIGHT)

        # Output text box
        self.output_text = tk.Text(self.result_tab, font=("Consolas", 10),
                                   bg="#181818", fg="#d4d4d4",
                                   relief=FLAT, padx=10, pady=8,
                                   state=DISABLED)
        self.output_text.pack(fill=BOTH, expand=True)

    # ── Problem Loading & Display ─────────────────────────────────────────────

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

        # Badges
        diff = prob.get("difficulty", "easy").lower()
        diff_bootstyles = {"easy": "success", "medium": "warning", "hard": "danger"}
        self.prob_title.config(text=f"{pid}. {prob.get('title', 'Unknown')}")
        self.diff_badge.config(text=diff.capitalize(), bootstyle=diff_bootstyles.get(diff, "info"))
        self.cat_badge.config(text=prob.get("category", "General"))
        self.xp_badge.config(text=f"+{prob.get('xp', 10)} XP")

        # ── Render Problem Text & Interactive Examples ───────────────────────
        self.prob_text.config(state=NORMAL)
        self.prob_text.delete("1.0", END)

        # Description
        self.prob_text.insert(END, prob.get("description", "") + "\n\n", "desc")

        # Examples section
        raw_examples = prob.get("examples", [])
        if raw_examples:
            self.prob_text.insert(END, "Examples\n", "heading")
            self.example_cards.clear()

            for i, raw_ex in enumerate(raw_examples, 1):
                ex_data = self._normalize_example(raw_ex)
                card = self._create_example_card(i, ex_data)
                self.example_cards.append(card)

                self.prob_text.insert(END, "\n")
                self.prob_text.window_create(END, window=card)
                self.prob_text.insert(END, "\n")

            self.prob_text.insert(END, "\n")

        # Constraints
        constraints = prob.get("constraints", [])
        if constraints:
            self.prob_text.insert(END, "Constraints:\n", "heading")
            for c in constraints:
                self.prob_text.insert(END, "  • ", "constraint_bullet")
                self.prob_text.insert(END, f"{c}\n", "constraint_text")
            self.prob_text.insert(END, "\n")

        self.prob_text.config(state=DISABLED)

        # ── Build Testcase Tabs ──────────────────────────────────────────────
        self._populate_testcase_tabs(prob)

        # ── Load LeetCode Starter Code ───────────────────────────────────────
        lang = self.language.get()
        starters = STARTER_CODE.get(lang, {})
        code = starters.get(pid) or starters.get("default", "class Solution:\n    pass\n")
        self.editor.set_code(code)
        self.editor.set_language(lang)

        self._set_output("✅ Problem loaded. Write your function and click ▶ Run Code!")

    def _normalize_example(self, ex) -> dict:
        """Normalizes example from string or dictionary into {input, output, explanation}."""
        if isinstance(ex, dict):
            return {
                "input": str(ex.get("input", "")),
                "output": str(ex.get("output", "")),
                "explanation": str(ex.get("explanation", "")),
            }
        elif isinstance(ex, str):
            inp, out, exp = "", "", ""
            for line in ex.split("\n"):
                line_str = line.strip()
                if line_str.startswith("Input:"):
                    inp = line_str.replace("Input:", "").strip()
                elif line_str.startswith("Output:"):
                    out = line_str.replace("Output:", "").strip()
                elif line_str.startswith("Explanation:"):
                    exp = line_str.replace("Explanation:", "").strip()
                elif not inp:
                    inp = line_str
            return {"input": inp, "output": out, "explanation": exp}
        return {"input": str(ex), "output": "", "explanation": ""}

    def _create_example_card(self, idx: int, ex_data: dict) -> tk.Frame:
        """Builds a clickable, beautiful LeetCode-style example card."""
        card = tk.Frame(self.prob_text, bg="#1a1a2e", padx=12, pady=10,
                        relief=FLAT, highlightthickness=1, highlightbackground="#2e2e4a")

        # Header with clickable Load button
        hdr = tk.Frame(card, bg="#1a1a2e")
        hdr.pack(fill=X, pady=(0, 6))

        tk.Label(hdr, text=f"Example {idx}:", font=("Segoe UI", 10, "bold"),
                 bg="#1a1a2e", fg="#ffffff").pack(side=LEFT)

        btn = ttk.Button(hdr, text="📋 Test this Case", bootstyle="info-outline", width=14,
                         command=lambda: self.select_testcase(idx - 1))
        btn.pack(side=RIGHT)

        # Content container
        body = tk.Frame(card, bg="#1a1a2e")
        body.pack(fill=X)

        # Input row
        r1 = tk.Frame(body, bg="#1a1a2e")
        r1.pack(fill=X, anchor="w", pady=1)
        tk.Label(r1, text="Input: ", font=("Segoe UI", 9, "bold"),
                 bg="#1a1a2e", fg="#aaaaaa").pack(side=LEFT)
        tk.Label(r1, text=ex_data.get("input", ""), font=("Consolas", 9),
                 bg="#1a1a2e", fg="#9cdcfe", wraplength=340, justify=LEFT).pack(side=LEFT)

        # Output row
        r2 = tk.Frame(body, bg="#1a1a2e")
        r2.pack(fill=X, anchor="w", pady=1)
        tk.Label(r2, text="Output: ", font=("Segoe UI", 9, "bold"),
                 bg="#1a1a2e", fg="#aaaaaa").pack(side=LEFT)
        tk.Label(r2, text=ex_data.get("output", ""), font=("Consolas", 9),
                 bg="#1a1a2e", fg="#ce9178", wraplength=340, justify=LEFT).pack(side=LEFT)

        # Explanation row
        if ex_data.get("explanation"):
            r3 = tk.Frame(body, bg="#1a1a2e")
            r3.pack(fill=X, anchor="w", pady=1)
            tk.Label(r3, text="Explanation: ", font=("Segoe UI", 9, "bold"),
                     bg="#1a1a2e", fg="#aaaaaa").pack(side=LEFT)
            tk.Label(r3, text=ex_data.get("explanation", ""), font=("Segoe UI", 9),
                     bg="#1a1a2e", fg="#999999", wraplength=320, justify=LEFT).pack(side=LEFT)

        # Click card anywhere to load that testcase
        def _card_clicked(e):
            self.select_testcase(idx - 1)
        card.bind("<Button-1>", _card_clicked)
        card.config(cursor="hand2")

        return card

    def _populate_testcase_tabs(self, prob: dict):
        """Populates the Case 1, Case 2 buttons in the bottom Testcase tab."""
        for w in self.tc_buttons_frame.winfo_children():
            w.destroy()

        tests = prob.get("visible_tests", [])
        if not tests:
            pid = prob.get("id", 1)
            tests = LOCAL_TEST_CASES.get(pid, [{"input": "", "expected": ""}])

        self.current_tests = tests
        self.tc_btns = []

        for i, _ in enumerate(tests):
            btn = ttk.Button(self.tc_buttons_frame, text=f"Case {i+1}",
                             bootstyle="info" if i == 0 else "secondary-outline",
                             width=8,
                             command=lambda idx=i: self.select_testcase(idx))
            btn.pack(side=LEFT, padx=3)
            self.tc_btns.append(btn)

        self.select_testcase(0)

    def select_testcase(self, idx: int):
        """Selects a testcase and switches to the Testcase tab."""
        if not hasattr(self, "current_tests") or not self.current_tests:
            return
        idx = max(0, min(idx, len(self.current_tests) - 1))
        self.active_testcase_idx = idx

        # Highlight button
        for i, b in enumerate(getattr(self, "tc_btns", [])):
            b.configure(bootstyle="info" if i == idx else "secondary-outline")

        # Highlight corresponding example card if present
        for i, c in enumerate(getattr(self, "example_cards", [])):
            if i == idx:
                c.configure(highlightbackground="#3498db", highlightthickness=2)
            else:
                c.configure(highlightbackground="#2e2e4a", highlightthickness=1)

        # Update input and expected fields
        tc = self.current_tests[idx]
        self.tc_input_text.delete("1.0", END)
        self.tc_input_text.insert("1.0", tc.get("input", ""))

        self.tc_expected_text.delete("1.0", END)
        self.tc_expected_text.insert("1.0", tc.get("expected", ""))

        self.tc_feedback_lbl.config(text=f"Selected Case {idx + 1}")

        # Switch notebook to Testcase tab
        self.bottom_nb.select(self.testcase_tab)

    # ── Language & Code Execution ─────────────────────────────────────────────

    def set_language(self, lang: str):
        self.language.set(lang)
        self._on_lang_change()

    def _on_lang_change(self, event=None):
        lang = self.language.get()
        names = {"python": "🐍 Python 3", "cpp": "⚡ C++17", "c": "🔧 C"}
        if hasattr(self, "lang_status_lbl"):
            self.lang_status_lbl.config(text=f"Active: {names.get(lang, lang)}")
        for k, btn in getattr(self, "lang_btns", {}).items():
            btn.configure(bootstyle="info" if k == lang else "secondary-outline")
        self.editor.set_language(lang)
        if self.current_problem:
            pid = self.current_problem.get("id", 0)
            starters = STARTER_CODE.get(lang, {})
            code = starters.get(pid) or starters.get("default", "class Solution:\n    pass\n")
            self.editor.set_code(code)

    def _run_code(self):
        if not self.current_problem:
            self._set_output("⚠️  Please select a problem first!")
            return
        code = self.editor.get_code().strip()
        if not code:
            self._set_output("⚠️  Write some code first!")
            return

        # Switch to Test Result tab immediately
        self.bottom_nb.select(self.result_tab)
        self._set_output("⏳ Judging your solution against all test cases...")
        self.verdict_lbl.config(text="⏳ Running...", fg="#f39c12")
        self.runtime_lbl.config(text="")

        pid = self.current_problem["id"]
        lang = self.language.get()
        threading.Thread(target=self._judge_thread,
                         args=(pid, code, lang), daemon=True).start()

    def _judge_thread(self, pid: int, code: str, lang: str):
        # Automatically wrap user solution with driver harness
        wrapped_code = wrap_user_code(pid, code, lang)

        result = self.api.submit_code(pid, wrapped_code, lang)
        # Fallback to local offline judge if backend is offline
        if result.get("offline") or result.get("error"):
            result = self._run_local_judge(pid, wrapped_code, lang)

        self.after(0, lambda: self._show_result(result))

    def _run_local_judge(self, pid: int, wrapped_code: str, lang: str):
        import subprocess, tempfile, os, time, sys

        tests = getattr(self, "current_tests", [])
        if not tests:
            tests = LOCAL_TEST_CASES.get(pid, [{"input": "", "expected": ""}])

        passed = 0
        total = len(tests)
        last_out = ""
        last_err = ""
        total_time = 0

        tmp_dir = tempfile.mkdtemp(prefix="codequest_")
        exe_path = None
        src_path = None

        try:
            if lang == "python":
                src_path = os.path.join(tmp_dir, "solution.py")
                with open(src_path, "w", encoding="utf-8") as f:
                    f.write(wrapped_code)
                run_cmd = [sys.executable, src_path]
            else:
                ext = ".cpp" if lang == "cpp" else ".c"
                src_path = os.path.join(tmp_dir, f"solution{ext}")
                exe_path = os.path.join(tmp_dir, "solution.exe")
                with open(src_path, "w", encoding="utf-8") as f:
                    f.write(wrapped_code)

                std_flag = "-std=c++17" if lang == "cpp" else "-std=c11"
                compile_cmd = ["g++", std_flag, "-O2", "-o", exe_path, src_path]
                comp = subprocess.run(compile_cmd, capture_output=True, text=True, timeout=12)
                if comp.returncode != 0:
                    return {
                        "status": "CE",
                        "passed": 0,
                        "total": total,
                        "runtime_ms": 0,
                        "output": "",
                        "error": comp.stderr.strip() or "Compilation failed",
                        "xp_earned": 0,
                    }
                run_cmd = [exe_path]

            # Execute against test cases
            for tc in tests:
                t_in = tc.get("input", "")
                t_exp = tc.get("expected", "").strip()

                start = time.perf_counter()
                try:
                    proc = subprocess.run(
                        run_cmd,
                        input=t_in,
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )
                except subprocess.TimeoutExpired:
                    return {
                        "status": "TLE",
                        "passed": passed,
                        "total": total,
                        "runtime_ms": 5000,
                        "output": "",
                        "error": "Time Limit Exceeded (> 5.0 seconds)",
                        "xp_earned": 0,
                    }

                elapsed_ms = int((time.perf_counter() - start) * 1000)
                total_time += elapsed_ms

                out = proc.stdout.strip()
                last_out = out
                last_err = proc.stderr.strip()

                if proc.returncode != 0 and not out:
                    return {
                        "status": "RE",
                        "passed": passed,
                        "total": total,
                        "runtime_ms": elapsed_ms,
                        "output": out,
                        "error": last_err or f"Runtime error (exit code {proc.returncode})",
                        "xp_earned": 0,
                    }

                if out == t_exp:
                    passed += 1

            status = "AC" if passed == total else "WA"
            avg_ms = int(total_time / max(total, 1))
            xp = self.current_problem.get("xp", 10) if status == "AC" else 0

            return {
                "status": status,
                "passed": passed,
                "total": total,
                "runtime_ms": avg_ms,
                "output": last_out,
                "error": last_err,
                "xp_earned": xp,
            }

        except Exception as e:
            return {
                "status": "ERROR",
                "passed": 0,
                "total": total,
                "runtime_ms": 0,
                "output": "",
                "error": str(e),
                "xp_earned": 0,
            }
        finally:
            try:
                import shutil
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except Exception:
                pass

    def _show_result(self, result: dict):
        status = result.get("status", "WA")
        passed = result.get("passed", 0)
        total = result.get("total", 0)
        ms = result.get("runtime_ms", 0)
        output = result.get("output", "")
        error = result.get("error", "")
        xp = result.get("xp_earned", 0)

        color, label = VERDICT_STYLES.get(status, ("#888", f"❓ {status}"))
        self.verdict_lbl.config(text=label, fg=color)
        self.runtime_lbl.config(text=f"Runtime: {ms} ms")

        lines = [f"{label}\n", f"Test Cases: {passed}/{total} passed\n",
                 f"Runtime:    {ms} ms\n"]
        if output:
            lines += ["\n── Last Output ──\n", output]
        if error:
            lines += ["\n── Error Details ──\n", error]
        if xp > 0:
            lines += [f"\n🎉 +{xp} XP earned! Great job!"]

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
        y = 0.6 - step * 0.01
        self.xp_lbl.place(relx=0.7, rely=y)
        self.after(40, lambda: self._xp_anim_step(step + 1))

    def _reset_code(self):
        if self.current_problem:
            self._on_lang_change(None)
        else:
            self.editor.set_code("class Solution:\n    pass\n")

    def _show_hint(self):
        if not self.current_problem:
            return
        hints = self.current_problem.get("hints", [])
        if hints:
            self.bottom_nb.select(self.result_tab)
            self._set_output("💡 Hints:\n\n" + "\n".join(f"  {i+1}. {h}" for i, h in enumerate(hints)))
        else:
            self._set_output("No hints available for this problem.")
