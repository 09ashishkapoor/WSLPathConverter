# WSL Path Converter

WSL Path Converter is a lightweight Windows utility for converting Windows paths to WSL/Linux paths and back. It runs fully offline, uses only the Python standard library, and can copy a ready-to-paste `cd` command for your WSL terminal.

![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%2B%20WSL-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)
![Latest release](https://img.shields.io/github/v/release/09ashishkapoor/WSLPathConverter?display_name=tag)

![WSL Path Converter screenshot](Screenshot.png)

## Download

No Python required. Download the standalone Windows executable from the latest release:

-> **[Download WSLPathConverter.exe](../../releases/latest)**

If you already have Python 3.8+, you can also run the project from source.

## What Problem This Solves

If you work on Windows but run commands inside WSL, you constantly have to translate paths like:

- `C:\Users\name\project` -> `/mnt/c/Users/name/project`
- `/mnt/c/Users/name/project` -> `C:\Users\name\project`

That usually happens when copying paths from Explorer, VS Code, Cursor, PowerShell, or Command Prompt into a WSL terminal. Linux includes `wslpath`, but it only runs inside WSL. This project gives you a Windows-side path converter so you can prepare the path before you paste it into Bash, zsh, or a shell command.

## Features

- Windows path to WSL path conversion
- WSL path to Windows path conversion in the GUI
- Automatic direction detection for pasted input
- Live conversion as you type
- Copy the converted path or copy a full `cd <path>` command
- Optional shell escaping for spaces and parentheses
- Conversion history for the most recent 50 entries
- Fully offline operation with no telemetry and no third-party packages

## Common Use Cases

- Convert a Windows file path from Explorer into a WSL-ready path
- Turn a project folder into a ready-to-paste `cd` command
- Move quickly between Windows editors and WSL terminals
- Convert `/mnt/c/...` paths back into `C:\...` for Windows apps
- Use a simple `wslpath` alternative from the Windows side

## Requirements

- Windows
- WSL if you want to use the converted Linux-style paths in a WSL shell
- Python 3.8+ only when running from source

## Usage

### GUI

```bash
python wslpath_gui.py
```

| Action | How |
|---|---|
| Convert a path | Type or paste a path and the result updates live, or press `Enter` |
| Copy the converted path | Click `Copy` |
| Copy a shell command | Click `Copy as cd` |
| Reuse a previous conversion | Double-click an entry in the History panel |
| Clear the form | Press `Esc` or click `Clear` |

### CLI

The CLI helper currently converts Windows paths to WSL paths:

```bash
python wslpath_conv.py "C:\Users\name\Documents\My Project"
# -> /mnt/c/Users/name/Documents/My\ Project

python wslpath_conv.py C:\Users\name
# -> /mnt/c/Users/name
```

## Build A Standalone EXE

If you want to build the Windows executable yourself:

```bash
pip install pyinstaller
pyinstaller WSLPathConverter.spec
```

The generated executable will be written to `dist/`.

## Why Use This Instead Of `wslpath`?

- `wslpath` works inside WSL
- WSL Path Converter works from Windows
- The GUI is useful when you are copying paths from Windows tools into a WSL terminal
- The `Copy as cd` action removes another manual step from the workflow

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
