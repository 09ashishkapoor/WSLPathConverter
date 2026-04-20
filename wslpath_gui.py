import tkinter as tk
from tkinter import ttk, messagebox
import re


# ---------------------------------------------------------------------------
# Conversion logic
# ---------------------------------------------------------------------------

def windows_to_wsl(win_path: str, escape: bool = True) -> str:
    """Convert a Windows path to its WSL /mnt/… equivalent."""
    win_path = win_path.strip('"').strip("'").strip()
    if not win_path:
        return ""
    match = re.match(r'^([a-zA-Z]):[\\/](.*)', win_path)
    if match:
        drive = match.group(1).lower()
        remainder = match.group(2).replace('\\', '/')
        res = f"/mnt/{drive}/{remainder}"
    else:
        match2 = re.match(r'^([a-zA-Z]):(.*)', win_path)
        if match2:
            drive = match2.group(1).lower()
            remainder = match2.group(2).replace('\\', '/')
            res = f"/mnt/{drive}{remainder}"
        else:
            res = win_path.replace('\\', '/')
    if escape:
        res = res.replace(' ', '\\ ').replace('(', '\\(').replace(')', '\\)')
    return res


def wsl_to_windows(linux_path: str) -> str:
    """Convert a WSL /mnt/… path back to a Windows path."""
    linux_path = linux_path.strip()
    if not linux_path:
        return ""
    match = re.match(r'^/mnt/([a-zA-Z])(/.*)?$', linux_path)
    if match:
        drive = match.group(1).upper()
        rest = (match.group(2) or "").replace('/', '\\')
        return f"{drive}:{rest}"
    # plain Linux path: just flip slashes as best-effort
    return linux_path.replace('/', '\\')


def detect_and_convert(path: str, escape: bool = True) -> tuple[str, str]:
    """Auto-detect direction and return (result, direction_label)."""
    p = path.strip().strip('"').strip("'")
    if re.match(r'^[a-zA-Z]:[/\\]', p) or re.match(r'^[a-zA-Z]:', p):
        return windows_to_wsl(path, escape=escape), "Windows → WSL"
    elif re.match(r'^/mnt/[a-zA-Z]', p):
        return wsl_to_windows(p), "WSL → Windows"
    else:
        # default: treat as Windows
        return windows_to_wsl(path, escape=escape), "Windows → WSL"


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WSL Path Converter")
        self.geometry("680x460")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")

        self.history: list[tuple[str, str, str]] = []   # (input, output, direction)
        self.escape_var = tk.BooleanVar(value=True)

        self._build_ui()
        self._bind_keys()

    # ------------------------------------------------------------------
    def _build_ui(self):
        PAD = {"padx": 16, "pady": 6}
        BG  = "#1e1e2e"
        FG  = "#cdd6f4"
        ENTRY_BG = "#313244"
        BTN_BG   = "#89b4fa"
        BTN_FG   = "#1e1e2e"
        HIST_BG  = "#181825"

        # ── Title bar ──────────────────────────────────────────────────
        title_frame = tk.Frame(self, bg="#89b4fa")
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="  WSL Path Converter",
                 bg="#89b4fa", fg="#1e1e2e",
                 font=("Segoe UI", 13, "bold")).pack(side="left", pady=6)

        # ── Direction indicator ────────────────────────────────────────
        self.dir_label = tk.Label(self, text="Auto-detect direction",
                                  bg=BG, fg="#a6e3a1",
                                  font=("Segoe UI", 9, "italic"))
        self.dir_label.pack(anchor="w", **PAD)

        # ── Input ──────────────────────────────────────────────────────
        tk.Label(self, text="Input path:", bg=BG, fg=FG,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=16, pady=(0, 2))
        self.entry_in = tk.Entry(self, width=72, bg=ENTRY_BG, fg=FG,
                                 insertbackground=FG, relief="flat",
                                 font=("Cascadia Code", 10))
        self.entry_in.pack(padx=16, ipady=6)
        self.entry_in.insert(0, r"C:\Users\username\Documents\my-project")
        self.entry_in.bind("<KeyRelease>", self._on_type)

        # ── Options ────────────────────────────────────────────────────
        opt_frame = tk.Frame(self, bg=BG)
        opt_frame.pack(anchor="w", padx=16, pady=(6, 0))
        tk.Checkbutton(opt_frame, text="Escape spaces & parentheses",
                       variable=self.escape_var, command=self._on_type,
                       bg=BG, fg=FG, selectcolor=ENTRY_BG,
                       activebackground=BG, activeforeground=FG,
                       font=("Segoe UI", 9)).pack(side="left")

        # ── Buttons ────────────────────────────────────────────────────
        btn_frame = tk.Frame(self, bg=BG)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Convert  (Enter)", command=self._convert,
                  bg=BTN_BG, fg=BTN_FG, relief="flat", cursor="hand2",
                  font=("Segoe UI", 10, "bold"), padx=14, pady=4).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Clear", command=self._clear,
                  bg="#585b70", fg=FG, relief="flat", cursor="hand2",
                  font=("Segoe UI", 10), padx=14, pady=4).pack(side="left", padx=6)

        # ── Output ─────────────────────────────────────────────────────
        tk.Label(self, text="Converted path:", bg=BG, fg=FG,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=16, pady=(0, 2))
        out_frame = tk.Frame(self, bg=BG)
        out_frame.pack(padx=16, fill="x")
        self.entry_out = tk.Entry(out_frame, width=60, bg=ENTRY_BG, fg="#a6e3a1",
                                  insertbackground=FG, relief="flat",
                                  font=("Cascadia Code", 10), state="readonly")
        self.entry_out.pack(side="left", ipady=6, fill="x", expand=True)
        tk.Button(out_frame, text="Copy", command=self._copy,
                  bg="#a6e3a1", fg="#1e1e2e", relief="flat", cursor="hand2",
                  font=("Segoe UI", 10, "bold"), padx=14, pady=5).pack(side="left", padx=(6, 0))
        tk.Button(out_frame, text="Copy as cd", command=self._copy_as_cd,
                  bg="#f38ba8", fg="#1e1e2e", relief="flat", cursor="hand2",
                  font=("Segoe UI", 10, "bold"), padx=14, pady=5).pack(side="left", padx=(6, 0))

        # ── History ────────────────────────────────────────────────────
        tk.Label(self, text="History (click to reuse):", bg=BG, fg=FG,
                 font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=16, pady=(14, 2))
        hist_frame = tk.Frame(self, bg=HIST_BG, relief="flat")
        hist_frame.pack(padx=16, fill="both", expand=True, pady=(0, 12))
        scrollbar = tk.Scrollbar(hist_frame)
        scrollbar.pack(side="right", fill="y")
        self.hist_list = tk.Listbox(hist_frame, bg=HIST_BG, fg="#cdd6f4",
                                    selectbackground="#45475a",
                                    font=("Cascadia Code", 9), relief="flat",
                                    yscrollcommand=scrollbar.set,
                                    activestyle="none", height=6)
        self.hist_list.pack(fill="both", expand=True)
        scrollbar.config(command=self.hist_list.yview)
        self.hist_list.bind("<Double-Button-1>", self._reuse_history)
        self.hist_list.bind("<Return>", self._reuse_history)

    # ------------------------------------------------------------------
    def _bind_keys(self):
        self.bind("<Return>", lambda e: self._convert())
        self.bind("<Escape>", lambda e: self._clear())

    # ------------------------------------------------------------------
    def _set_output(self, text: str):
        self.entry_out.config(state="normal")
        self.entry_out.delete(0, tk.END)
        self.entry_out.insert(0, text)
        self.entry_out.config(state="readonly")

    def _on_type(self, event=None):
        """Live-convert as the user types."""
        raw = self.entry_in.get()
        if raw.strip():
            result, direction = detect_and_convert(raw, escape=self.escape_var.get())
            self._set_output(result)
            self.dir_label.config(text=f"Direction: {direction}")
        else:
            self._set_output("")
            self.dir_label.config(text="Auto-detect direction")

    def _convert(self):
        raw = self.entry_in.get().strip()
        if not raw:
            return
        result, direction = detect_and_convert(raw, escape=self.escape_var.get())
        self._set_output(result)
        self.dir_label.config(text=f"Direction: {direction}")
        # Add to history (avoid duplicates at top)
        entry = (raw, result, direction)
        if not self.history or self.history[0] != entry:
            self.history.insert(0, entry)
            self.hist_list.insert(0, f"[{direction}]  {result}")
            if len(self.history) > 50:
                self.history.pop()
                self.hist_list.delete(tk.END)

    def _copy(self):
        text = self.entry_out.get()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.dir_label.config(text="Copied to clipboard!")
            self.after(1500, lambda: self.dir_label.config(
                text=f"Direction: {detect_and_convert(self.entry_in.get())[1]}"))

    def _copy_as_cd(self):
        text = self.entry_out.get()
        if text:
            self.clipboard_clear()
            self.clipboard_append(f"cd {text}")
            self.dir_label.config(text="Copied as 'cd <path>'!")
            self.after(1500, lambda: self.dir_label.config(
                text=f"Direction: {detect_and_convert(self.entry_in.get())[1]}"))

    def _clear(self):
        self.entry_in.delete(0, tk.END)
        self._set_output("")
        self.dir_label.config(text="Auto-detect direction")
        self.entry_in.focus()

    def _reuse_history(self, event=None):
        sel = self.hist_list.curselection()
        if not sel:
            return
        idx = sel[0]
        original_input, _, _ = self.history[idx]
        self.entry_in.delete(0, tk.END)
        self.entry_in.insert(0, original_input)
        self._convert()


if __name__ == "__main__":
    app = App()
    app.mainloop()

