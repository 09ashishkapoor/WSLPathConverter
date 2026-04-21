# Release Copy Refresh Design

## Goal

Improve the public-facing GitHub presentation for a broader Windows/WSL audience by making the About sidebar copy and latest release notes accurate, simpler, and easier to understand at a glance.

## Scope

This pass will update:

- The repository About description on GitHub
- The `v1.0.0` release title on GitHub
- The `v1.0.0` release body on GitHub

This pass will not update:

- Source code behavior
- README structure beyond what is already merged
- Topics, unless a mismatch is discovered while applying the copy
- Homepage URL, which will remain blank until a dedicated landing page exists

## Audience

Primary audience:

- Windows users who also use WSL
- Users copying paths between Explorer, editors, terminals, and shell commands
- People evaluating the repo quickly from GitHub search, a shared link, or the Releases page

Copy should assume technical familiarity with Windows and WSL, but not deep Python or packaging knowledge.

## Approach Options

### Option 1: Minimal correction

Only remove inaccurate release claims and keep the rest nearly unchanged.

Pros:

- Lowest editing risk

Cons:

- Weak improvement to discoverability and first impression

### Option 2: Balanced utility-first refresh

Tighten About copy and rewrite the release around current user value, with plain English and accurate feature framing.

Pros:

- Best balance of clarity, accuracy, and public-facing polish
- Appropriate for a small utility repo

Cons:

- Slightly more editorial work than a pure correction pass

### Option 3: Productized marketing pass

Rewrite the repo presentation with stronger promotional language and more ambitious product framing.

Pros:

- Can increase perceived polish

Cons:

- Higher risk of overselling the tool
- Less credible for a small repo if the claims outrun the implementation

## Selected Approach

Use Option 2.

Reasoning:

- The current problem is inaccurate and underspecified copy, not lack of marketing.
- The repo benefits more from trust and clarity than from aggressive positioning.
- A utility-first tone fits a public GitHub repo with a small, focused feature set.

## Proposed Copy Shape

### About description

One sentence, plain English, problem-first.

Target direction:

`Convert Windows paths to WSL paths and back with a simple offline GUI and CLI for Windows.`

### Release title

Keep it versioned and direct.

Target direction:

`WSL Path Converter v1.0.0`

### Release body

Use short sections with only verified claims:

- What it does
- Included in this release
- How to use it
- Privacy

Claims must match the current repo state:

- GUI available
- CLI helper available
- Offline/local operation
- Copy converted path or `cd` command
- No third-party runtime dependency for source usage beyond Python standard library

Claims that must not appear unless later verified in code:

- `--force` support
- UNC-specific support claims
- performance optimizations
- unicode bug fixes
- explicit Windows 10/11 or WSL2 test matrix statements

## Data Flow

The change flow is simple:

1. Read current About and release text from GitHub
2. Replace them with approved, accurate copy
3. Re-read GitHub metadata to confirm the final state

## Error Handling

- If GitHub API editing fails, preserve the drafted replacement copy locally and report the exact blocker
- If release editing succeeds but About editing fails, report partial completion explicitly
- Do not invent feature claims to fill missing sections

## Verification

Verification will consist of:

- `gh repo view ...` to confirm the final About description
- `gh release view v1.0.0 ...` to confirm the final release title and body
- Manual check that the final text matches current repo behavior and README positioning

## Success Criteria

- About copy is short, accurate, and understandable to a broader Windows/WSL audience
- Latest release notes no longer contain inaccurate claims
- Release page explains the tool in plain English and supports download confidence
- GitHub repo presentation is more trustworthy and easier to scan
