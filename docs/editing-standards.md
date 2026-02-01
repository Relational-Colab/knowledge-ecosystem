# Editing Standards: Indentation, Whitespace, and Cross‑Platform Safety

These rules ensure that all contributors work with clean, predictable, cross‑platform‑safe text files. They eliminate hidden characters, indentation drift, and Windows/Unix inconsistencies that can break Python scripts, Makefiles, and governance artifacts.

---

## 1. Indentation Rules

- **Use spaces only — never tabs.**
- **Indentation is exactly 4 spaces** for all Python, JSON, JSONL, Markdown, and documentation files.
- Makefiles are the only exception:
  - **Makefile commands must begin with a literal tab**, not spaces.
- Do not mix tabs and spaces in any file.

These rules are enforced by:
- `.editorconfig` in the repo root  
- `.vscode/settings.json` for VSCode users  

Both files are part of the repository and apply automatically.

---

## 2. Line Ending Rules

- All files must use **LF (`\n`) line endings**, even on Windows.
- CRLF (`\r\n`) line endings cause Python `IndentationError` and break diffs.
- VSCode is configured to enforce LF via `.vscode/settings.json`.

---

## 3. Whitespace Visibility

To avoid hidden characters:

- Editors should **render whitespace visibly** (VSCode does this automatically via project settings).
- Trailing whitespace is automatically trimmed by `.editorconfig`.
- No non‑breaking spaces, zero‑width spaces, or other invisible characters should appear in code or data files.

If in doubt, use:

```
:set list
```

in vim to inspect whitespace explicitly.

---

## 4. Formatting Behavior

To prevent accidental corruption:

- **Auto‑indentation guessing is disabled** in VSCode.
- **Format‑on‑paste is disabled** to avoid indentation shifts when pasting code.
- **Format‑on‑save is disabled** unless a project‑approved formatter is introduced later.

This ensures that contributors do not unintentionally reformat files.

---

## 5. Cross‑Platform Editing Discipline

Because this repository is edited on macOS, Linux, and Windows:

- Always ensure your editor respects `.editorconfig`.
- Avoid tools that silently rewrite indentation or line endings.
- When in doubt, use vim for inspection — it reveals the truth about whitespace.

---

## 6. Why These Rules Exist

This project is a governance‑grade ecosystem.  
Whitespace is not cosmetic — it is structural.

These rules:

- prevent Python `IndentationError`  
- prevent Makefile command failures  
- ensure reproducible diffs  
- eliminate cross‑platform drift  
- protect canonical data integrity  
- maintain contributor‑friendly clarity  

They are part of the system’s operational discipline.

## Editor Configuration (For All Contributors)

To ensure consistent, cross‑platform‑safe editing across macOS, Linux, and Windows, contributors should configure their editors to follow the project’s indentation and whitespace rules. These settings prevent hidden characters, indentation drift, and line‑ending mismatches that can break Python scripts, Makefiles, and governance artifacts.

### VSCode Users

This repository includes a `.vscode/settings.json` file that enforces:

- 4‑space indentation (no tabs)
- LF (`\n`) line endings
- disabled indentation guessing
- disabled format‑on‑paste
- visible whitespace rendering

VSCode applies these settings automatically when the workspace is opened. If files were already open before the settings were added, close and reopen them (or restart VSCode) to ensure the rules take effect.

### Other Editors

Most modern editors support `.editorconfig`, which is included in the repo root. Ensure your editor has EditorConfig support enabled so it can enforce:

- spaces instead of tabs  
- 4‑space indentation  
- LF line endings  
- trimmed trailing whitespace  

### When in Doubt

If you suspect hidden characters or indentation inconsistencies, open the file in `vim` and run:

```
:set list
```

This reveals tabs, non‑breaking spaces, trailing whitespace, and other invisible characters.

Following these guidelines ensures that all contributors work with clean, predictable files and helps maintain the integrity of the project’s governance‑grade ecosystem.
