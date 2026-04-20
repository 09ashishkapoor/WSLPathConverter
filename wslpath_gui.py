import tkinter as tk
from tkinter import messagebox
import re

def windows_to_wsl(win_path):
    """Converts Windows path to WSL path."""
    win_path = win_path.strip('"').strip("'").strip()
    if not win_path:
        return ""
    
    # Check for drive letter pattern (e.g., C:\ or C:/)
    match = re.match(r'^([a-zA-Z]):[\\/](.*)', win_path)
    if match:
        drive = match.group(1).lower()
        remainder = match.group(2).replace('\\', '/')
        res = f"/mnt/{drive}/{remainder}"
    
    # Handle paths with drive letter but no immediate slash
    elif re.match(r'^([a-zA-Z]):(.*)', win_path):
        match_no_slash = re.match(r'^([a-zA-Z]):(.*)', win_path)
        drive = match_no_slash.group(1).lower()
        remainder = match_no_slash.group(2).replace('\\', '/')
        res = f"/mnt/{drive}{remainder}"
    else:
        res = win_path.replace('\\', '/')

    # Escape spaces and parentheses for Linux shell consumption
    return res.replace(' ', '\\ ').replace('(', '\\(').replace(')', '\\)')

def convert_action():
    input_text = entry_in.get()
    result = windows_to_wsl(input_text)
    entry_out.delete(0, tk.END)
    entry_out.insert(0, result)

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(entry_out.get())
    messagebox.showinfo("Success", "Path copied to clipboard!")

# UI Setup
root = tk.Tk()
root.title("WSL Path Converter")
root.geometry("500x200")
root.resizable(False, False)

tk.Label(root, text="Windows Path:").pack(pady=(10, 0))
entry_in = tk.Entry(root, width=60)
entry_in.pack(pady=5)
# Set default example
entry_in.insert(0, r"C:\Users\kalbhairav\Documents\New project")

btn_convert = tk.Button(root, text="Convert to WSL", command=convert_action)
btn_convert.pack(pady=5)

tk.Label(root, text="WSL Path:").pack(pady=(10, 0))
entry_out = tk.Entry(root, width=60)
entry_out.pack(pady=5)

btn_copy = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
btn_copy.pack(pady=5)

if __name__ == "__main__":
    root.mainloop()
