# Release Copy Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refresh the GitHub About sidebar and `v1.0.0` release copy so the repo is accurate, easier to scan, and better targeted to a broader Windows/WSL audience.

**Architecture:** This change is a GitHub metadata pass, not a code change. The work updates live repository metadata through `gh`, keeps a plan record in the repo, and verifies the final state by re-reading the repo description and release body from GitHub.

**Tech Stack:** Git, GitHub CLI (`gh`), Markdown

---

## File Structure

- Create: `docs/superpowers/plans/2026-04-21-release-copy-refresh.md`
- Read: `docs/superpowers/specs/2026-04-21-release-copy-design.md`
- Modify live GitHub metadata only:
  - Repository About description for `09ashishkapoor/WSLPathConverter`
  - Release `v1.0.0` title and body for `09ashishkapoor/WSLPathConverter`

### Task 1: Draft the final About and release copy

**Files:**
- Read: `docs/superpowers/specs/2026-04-21-release-copy-design.md`
- Modify: GitHub repository metadata only

- [ ] **Step 1: Confirm the approved copy direction from the spec**

Read: `docs/superpowers/specs/2026-04-21-release-copy-design.md`

Pull these exact targets from the spec:

```text
About description:
Convert Windows paths to WSL paths and back with a simple offline GUI and CLI for Windows.

Release title:
WSL Path Converter v1.0.0
```

- [ ] **Step 2: Draft the final release body with only verified claims**

Use this exact body:

```markdown
## What it does

WSL Path Converter helps you convert Windows paths to WSL paths and back from Windows.

It is useful when you copy a path from Explorer, VS Code, PowerShell, or Command Prompt and want to paste it into a WSL terminal without rewriting it by hand.

## Included in this release

- Simple Windows GUI for live path conversion
- Automatic detection for Windows and WSL-style paths
- Copy the converted path directly to the clipboard
- Copy a ready-to-paste `cd <path>` command
- CLI helper for Windows-to-WSL path conversion
- Fully offline operation with no telemetry or network access

## How to use it

- Download `WSLPathConverter.exe` from this release and run it on Windows
- Or run the GUI from source with `python wslpath_gui.py`
- Or use the CLI helper with `python wslpath_conv.py "C:\Users\name\project"`

## Privacy

This tool runs locally on your machine. It does not require an internet connection and does not send telemetry.
```

- [ ] **Step 3: Commit the plan record**

Run:

```bash
git add docs/superpowers/plans/2026-04-21-release-copy-refresh.md
git commit -m "add release copy refresh plan"
```

Expected:

```text
[main ...] add release copy refresh plan
```

### Task 2: Apply the GitHub About and release edits

**Files:**
- Modify: GitHub repository metadata only

- [ ] **Step 1: Update the repository About description**

Run:

```bash
gh repo edit 09ashishkapoor/WSLPathConverter --description "Convert Windows paths to WSL paths and back with a simple offline GUI and CLI for Windows."
```

Expected:

```text
Exit code 0
```

- [ ] **Step 2: Write the release body to a temporary file with real newlines**

Create `release-body-v1.0.0.md` with this exact content:

```markdown
## What it does

WSL Path Converter helps you convert Windows paths to WSL paths and back from Windows.

It is useful when you copy a path from Explorer, VS Code, PowerShell, or Command Prompt and want to paste it into a WSL terminal without rewriting it by hand.

## Included in this release

- Simple Windows GUI for live path conversion
- Automatic detection for Windows and WSL-style paths
- Copy the converted path directly to the clipboard
- Copy a ready-to-paste `cd <path>` command
- CLI helper for Windows-to-WSL path conversion
- Fully offline operation with no telemetry or network access

## How to use it

- Download `WSLPathConverter.exe` from this release and run it on Windows
- Or run the GUI from source with `python wslpath_gui.py`
- Or use the CLI helper with `python wslpath_conv.py "C:\Users\name\project"`

## Privacy

This tool runs locally on your machine. It does not require an internet connection and does not send telemetry.
```

- [ ] **Step 3: Update the release title and body**

Run:

```bash
gh release edit v1.0.0 --repo 09ashishkapoor/WSLPathConverter --title "WSL Path Converter v1.0.0" --notes-file release-body-v1.0.0.md
```

Expected:

```text
Exit code 0
```

- [ ] **Step 4: Remove the temporary release notes file**

Run:

```bash
rm release-body-v1.0.0.md
```

Expected:

```text
File removed locally
```

### Task 3: Verify the final live GitHub state

**Files:**
- Read: GitHub repository metadata only

- [ ] **Step 1: Re-read the About description from GitHub**

Run:

```bash
gh repo view 09ashishkapoor/WSLPathConverter --json description
```

Expected:

```json
{"description":"Convert Windows paths to WSL paths and back with a simple offline GUI and CLI for Windows."}
```

- [ ] **Step 2: Re-read the release title and body from GitHub**

Run:

```bash
gh release view v1.0.0 --repo 09ashishkapoor/WSLPathConverter --json name,body
```

Expected:

```json
{"name":"WSL Path Converter v1.0.0","body":"...updated markdown body..."}
```

- [ ] **Step 3: Confirm the release body contains no unsupported claims**

Check that the final body does not mention any of the following:

```text
--force
UNC
unicode crash fixes
performance optimizations
Windows 10/11 or WSL2 test claims
```

- [ ] **Step 4: Commit the plan record if it has not already been committed**

Run:

```bash
git status --short
```

Expected:

```text
No uncommitted plan-file changes related to this plan
```
