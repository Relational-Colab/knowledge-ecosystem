## Pre‑Commit Ritual (Governance Checkpoint)

Before committing or pushing changes, contributors should run the **pre‑commit** ritual to ensure the repository remains in a clean, valid, and governance‑aligned state. This ritual acts as a safeguard against malformed data, stale artifacts, or workflow drift entering the canonical history.

The pre‑commit ritual performs four checks:

1. **Canonical Data Validation**  
   Ensures all JSONL files conform to the schema registry and contain no structural or formatting errors. This protects the integrity of the ecosystem and prevents downstream failures.

2. **Kanban Regeneration**  
   Rebuilds the current sprint’s Kanban board to ensure it reflects the latest canonical data. This guarantees that contributors never commit outdated or inconsistent workflow views.

3. **Metrics Extraction (T02)**  
   Runs the metrics pipeline to confirm that the sprint’s analytical layer is still valid and that no recent changes have broken the metrics extractor.

4. **Time‑Series Consolidation (T03)**  
   Rebuilds the cumulative metrics time‑series dataset, ensuring that historical analytics remain consistent and that the repository is ready for sprint review, dashboards, and MLflow logging.

### Why This Ritual Matters

The pre‑commit ritual is a governance checkpoint designed to:

- prevent accidental corruption of canonical data  
- ensure all workflow artifacts are fresh and reproducible  
- maintain analytical continuity across sprints  
- support clean sprint transitions  
- reinforce contributor discipline and operational clarity  

Running this ritual before committing helps maintain the ecosystem’s reliability, auditability, and long‑term analytical value.

### How to Run It

From the repository root:

```
make pre-commit
```

If all checks pass, contributors can commit with confidence that the repository is in a clean, governance‑grade state.

## Tab Sentinel (Makefile Indentation Sniff Test)

Makefiles are uniquely strict about indentation: **every command must begin with a literal tab**, and **spaces cause fatal errors**. Modern editors often convert tabs to spaces automatically, which can silently break Makefile targets.

To protect the workflow from accidental indentation drift, the repository includes a **tab sentinel** at the top of the Makefile:

```makefile
# TAB SENTINEL — this command *must* start with a real tab
sentinel:
    @echo "Tab indentation is working."
```

The sentinel provides a quick **sniff test** to verify that your editor is inserting real tabs. Running:

```
make sentinel
```

should print:

```
Tab indentation is working.
```

If instead you see an error such as:

```
Makefile:<line>: *** missing separator.  Stop.
```

this indicates that your editor has replaced tabs with spaces somewhere in the Makefile.  
Fix the indentation before running any other Makefile targets.

### Why This Ritual Matters

- Makefiles are the only part of the ecosystem where tabs are mandatory.  
- Editors often “helpfully” convert tabs to spaces, breaking the file.  
- The sentinel provides a fast, safe way to confirm indentation integrity.  
- It prevents contributors from running broken workflow rituals (e.g., `make metrics`, `make review`) on a malformed Makefile.  
- It reinforces the project’s commitment to transparency, reproducibility, and editing discipline.

### When to Use It

Run the sentinel:

- after editing the Makefile  
- after updating VSCode settings  
- after pulling changes that modify Makefile targets  
- before running any major workflow ritual (optional but recommended)

The sentinel is intentionally simple, visible, and easy to run. It is part of the governance philosophy that protects the ecosystem from subtle, editor‑induced breakage.

## Appendix: Troubleshooting Makefile Indentation Issues

Makefiles are extremely sensitive to indentation. Every command must begin with a **literal tab**, and any accidental spaces will cause errors such as:

```
*** missing separator.  Stop.
```

Modern editors often convert tabs to spaces automatically, so indentation issues can appear even when the file *looks* correct. This appendix provides quick, reliable steps to diagnose and repair Makefile indentation problems.

### Common Symptoms

- `make` fails with “missing separator”
- A target that previously worked suddenly breaks
- VSCode or another editor silently reformats indentation
- Tabs appear as spaces when whitespace is rendered

### How to Diagnose

1. **Run the tab sentinel:**

   ```
   make sentinel
   ```

   If it fails, indentation drift has occurred somewhere in the Makefile.

2. **Enable whitespace rendering** in your editor so tabs and spaces are visually distinct.

3. **Inspect command lines** (the lines under each target).  
   Only these lines must begin with a literal tab.

### How to Fix Indentation Quickly

If your editor has replaced tabs with spaces:

1. Open the Makefile.
2. Use “Find and Replace” to convert leading spaces to tabs:
   - Replace four spaces → tab
   - Replace two spaces → tab
   - Replace eight spaces → tab
3. Save the file.
4. Re-run:

   ```
   make sentinel
   ```

   If it prints “Tab indentation is working.” the file is repaired.

### Preventing Future Issues

To avoid recurring indentation drift:

- Configure your editor to use **tabs** specifically for Makefiles.  
  For VSCode, add this to `settings.json`:

  ```json
  "[makefile]": {
    "editor.insertSpaces": false,
    "editor.detectIndentation": false,
    "editor.tabSize": 4
  }
  ```

- Run the sentinel after any Makefile edits.
- Avoid copying Makefile content from sources that may contain spaces.

### Why This Matters

Makefile indentation errors are subtle but can break core workflow rituals such as:

- `make metrics`
- `make timeseries`
- `make review`
- `make pre-commit`

Maintaining correct indentation ensures the reliability of the entire governance pipeline and protects contributors from confusing, hard-to-diagnose failures.

## Sprint Review Ritual (T04)

The sprint review ritual produces a complete, reproducible review artifact that combines:

- fresh sprint metrics  
- updated time‑series data  
- a JSON review snapshot  
- a Markdown narrative review  

This ritual is fully automated and should be run at the end of each sprint.

### How to run the sprint review ritual

```
make review sprint=<sprint-name>
```

This command performs the following steps in order:

1. Runs the metrics extraction ritual (`make metrics`)  
2. Updates the longitudinal time‑series (`make timeseries`)  
3. Generates the sprint review artifacts using `scripts/generate-review.py`  
4. Writes both JSON and Markdown review files to:  
   ```
   reports/<sprint>/review/
   ```

### When to run it

- At the end of each sprint  
- During sprint review ceremonies  
- Whenever a contributor needs a fresh, consolidated snapshot of sprint health  

The review ritual ensures that every sprint leaves behind a clear, auditable, and narrative‑ready record of progress.
