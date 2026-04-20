import sys
import os
import re

def windows_to_wsl(win_path):
    """
    Converts a Windows path to a WSL (Linux) path.
    Example: C:\\Users\\name -> /mnt/c/Users/name
    """
    # Remove surrounding quotes if any
    win_path = win_path.strip('"').strip("'")
    
    # Check for drive letter pattern (e.g., C:\ or C:/)
    match = re.match(r'^([a-zA-Z]):[\\/](.*)', win_path)
    if match:
        drive = match.group(1).lower()
        remainder = match.group(2).replace('\\', '/')
        res = f"/mnt/{drive}/{remainder}"
    
    # Handle paths already in a somewhat Linux-friendly format but with drive letter
    elif re.match(r'^([a-zA-Z]):(.*)', win_path):
        match_no_slash = re.match(r'^([a-zA-Z]):(.*)', win_path)
        drive = match_no_slash.group(1).lower()
        remainder = match_no_slash.group(2).replace('\\', '/')
        res = f"/mnt/{drive}{remainder}"
    else:
        res = win_path.replace('\\', '/')
    
    # Escape spaces and other special shell characters
    return res.replace(' ', '\\ ').replace('(', '\\(').replace(')', '\\)')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Re-join arguments in case spaces in path weren't quoted
        input_path = " ".join(sys.argv[1:])
        print(windows_to_wsl(input_path))
    else:
        print("Usage: python wslpath_conv.py <windows_path>")
        print("Example: python wslpath_conv.py C:\\Users\\username\\Documents\\my-project")
