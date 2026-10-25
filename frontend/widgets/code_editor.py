"""Syntax-highlighted code editor widget."""
import tkinter as tk
from tkinter import font as tkfont


class CodeEditor(tk.Frame):
    """A custom monospace code editor with line numbers and syntax highlighting."""

    EDITOR_BG  = "#1e1e1e"
    EDITOR_FG  = "#d4d4d4"
    LINENO_BG  = "#252526"
    LINENO_FG  = "#858585"
    CURSOR_CLR = "#aeafad"
    SELECT_BG  = "#264f78"

    PYTHON_KEYWORDS = [
        "False","None","True","and","as","assert","async","await",
        "break","class","continue","def","del","elif","else","except",
        "finally","for","from","global","if","import","in","is",
        "lambda","nonlocal","not","or","pass","raise","return","try",
        "while","with","yield",
    ]
    CPP_KEYWORDS = [
        "int","float","double","char","bool","void","long","short",
        "unsigned","signed","auto","return","if","else","for","while",
        "do","switch","case","break","continue","class","struct","enum",
        "namespace","using","include","define","public","private","protected",
        "new","delete","nullptr","true","false","const","static","extern",
        "typedef","template","typename","virtual","override",
    ]

    COLORS = {
        "keyword":  "#569cd6",
        "string":   "#ce9178",
        "comment":  "#6a9955",
        "number":   "#b5cea8",
        "builtin":  "#dcdcaa",
        "operator": "#d4d4d4",
    }

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=self.EDITOR_BG, **kwargs)
        self.language = "python"
        self._build()
        self._bind_events()

    def _build(self):
        mono = tkfont.Font(family="Consolas", size=11)

        # Line numbers canvas
        self.lineno = tk.Canvas(self, width=48, bg=self.LINENO_BG,
                                highlightthickness=0, bd=0)
        self.lineno.pack(side=tk.LEFT, fill=tk.Y)

        # Scrollbars
        vscroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        hscroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        vscroll.pack(side=tk.RIGHT,  fill=tk.Y)
        hscroll.pack(side=tk.BOTTOM, fill=tk.X)

        # Main text widget
        self.text = tk.Text(
            self,
            bg=self.EDITOR_BG, fg=self.EDITOR_FG,
            insertbackground=self.CURSOR_CLR,
            selectbackground=self.SELECT_BG,
            font=mono, wrap=tk.NONE,
            undo=True, autoseparators=True, maxundo=-1,
            yscrollcommand=vscroll.set,
            xscrollcommand=hscroll.set,
            relief=tk.FLAT, bd=0,
            padx=6, pady=4,
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vscroll.config(command=self._on_scroll_y)
        hscroll.config(command=self.text.xview)

        # Syntax tag config
        for name, color in self.COLORS.items():
            self.text.tag_config(name, foreground=color)
        self.text.tag_config("lineno_highlight", background="#2d2d2d")

    def _on_scroll_y(self, *args):
        self.text.yview(*args)
        self._update_linenos()

    def _bind_events(self):
        self.text.bind("<KeyRelease>", self._on_key)
        self.text.bind("<Return>",     self._on_enter)
        self.text.bind("<Tab>",        self._on_tab)
        self.text.bind("<<Modified>>", self._on_modified)
        self.text.bind("<Configure>",  lambda e: self._update_linenos())

    def _on_tab(self, event):
        self.text.insert(tk.INSERT, "    ")
        return "break"

    def _on_enter(self, event):
        # Auto-indent
        line = self.text.get("insert linestart", "insert")
        indent = len(line) - len(line.lstrip())
        if line.rstrip().endswith(":"):
            indent += 4
        self.text.insert(tk.INSERT, "\n" + " " * indent)
        self._update_linenos()
        self._highlight()
        return "break"

    def _on_key(self, event):
        self._update_linenos()
        self._highlight()

    def _on_modified(self, event):
        self.text.edit_modified(False)
        self._update_linenos()

    def _update_linenos(self):
        self.lineno.delete("all")
        i = self.text.index("@0,0")
        while True:
            dline = self.text.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.lineno.create_text(
                40, y + 2, anchor="ne",
                text=linenum,
                fill=self.LINENO_FG,
                font=("Consolas", 10),
            )
            i = self.text.index(f"{i}+1line")
            if self.text.compare(i, ">=", "end"):
                break

    def _highlight(self):
        """Basic syntax highlighting."""
        content = self.text.get("1.0", tk.END)
        # Remove old tags
        for tag in self.COLORS:
            self.text.tag_remove(tag, "1.0", tk.END)

        keywords = self.PYTHON_KEYWORDS if self.language == "python" else self.CPP_KEYWORDS

        lines = content.split("\n")
        for lineno, line in enumerate(lines, start=1):
            # Comments
            comment_start = line.find("#") if self.language == "python" else line.find("//")
            if comment_start >= 0:
                self.text.tag_add("comment",
                    f"{lineno}.{comment_start}",
                    f"{lineno}.end")

            # Strings (simple)
            import re
            for m in re.finditer(r'(\".*?\"|\'.*?\')', line):
                self.text.tag_add("string", f"{lineno}.{m.start()}", f"{lineno}.{m.end()}")

            # Numbers
            for m in re.finditer(r'\b\d+\.?\d*\b', line):
                self.text.tag_add("number", f"{lineno}.{m.start()}", f"{lineno}.{m.end()}")

            # Keywords
            for kw in keywords:
                import re as _re
                for m in _re.finditer(r'\b' + kw + r'\b', line):
                    self.text.tag_add("keyword", f"{lineno}.{m.start()}", f"{lineno}.{m.end()}")

    # ── Public API ────────────────────────────────────────────────────────────

    def get_code(self) -> str:
        return self.text.get("1.0", tk.END)

    def set_code(self, code: str):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", code)
        self._update_linenos()
        self._highlight()

    def set_language(self, lang: str):
        self.language = lang
        self._highlight()

    def clear(self):
        self.text.delete("1.0", tk.END)
        self._update_linenos()
