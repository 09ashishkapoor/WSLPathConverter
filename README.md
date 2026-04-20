# WSL Path Converter

This is a completely offline tool to convert Windows file paths to Linux paths compatible with WSL.

## Usage

### GUI Version (Recommended)
Run the GUI tool to convert paths with a window:
```bash
python wslpath_gui.py
```

### CLI Version
Run the script from your terminal:
```bash
python wslpath_conv.py "C:\Users\name\Documents"
```

Output:
`/mnt/c/Users/name/Documents`

## How it works
The script:
1. Detects the drive letter (e.g., `C:`) and converts it to `/mnt/c/`.
2. Replaces all backslashes (`\`) with forward slashes (`/`).
3. Handles paths with spaces correctly when quoted.
