# Contributing to the Knowledge Ecosystem
# Contributor Quickstart

Welcome. This repository uses a set of lightweight, governance‑aligned rituals to keep the ecosystem clean, reproducible, and contributor‑friendly.  
If you want to contribute, these are the three steps you need to know:

### 1. Run the tab sentinel (Makefile safety check)

Before running any workflow:

```
make sentinel
```

If it prints:

```
Tab indentation is working.
```

you’re good to proceed.  
If it fails, fix Makefile indentation before continuing.

### 2. Validate the repository

Always validate before committing:

```
make validate
```

This checks canonical data, schemas, workflow states, and JSONL formatting.

### 3. Use the pre‑commit ritual

Before every commit:

```
make pre-commit
```

This runs validation, metrics extraction, and time‑series consolidation.  
If it passes, your contribution is safe to commit.

That’s it.  
The rest of this document explains the full workflow in more detail, but these three steps will carry you through 95% of contributions.

Every contribution—large or small—participates in a set of rituals designed to keep the system transparent, reproducible, and contributor‑friendly.

This document explains how to contribute safely, how to run the workflow rituals, and how to avoid common pitfalls (especially around Makefile indentation).

---

## 1. Core Principles

Contributions follow these principles:

- **Transparency** — every change is visible, explainable, and auditable.  
- **Reproducibility** — all workflows run cleanly from a fresh checkout.  
- **Discipline** — indentation, whitespace, and schema alignment matter.  
- **Teachability** — every artifact should help future contributors understand the system.  
- **Minimal friction** — contributors should be able to operate without surprises.

If you follow the rituals in this document, you will stay aligned with the ecosystem’s governance philosophy.

---

## 2. Repository Structure (Contributor View)

Key directories:

- `data/` — canonical data, schemas, and time‑series artifacts  
- `reports/` — sprint‑level metrics and generated outputs  
- `scripts/` — Python scripts for validation, metrics, and consolidation  
- `docs/` — governance documentation and workflow rituals  
- `Makefile` — the operational interface for all contributor workflows  

---

## 3. Required Tools

Contributors need:

- Python 3.10+  
- A WSL‑native editor (VSCode with WSL integration is fine)  
- A terminal capable of running Makefile targets  
- Git  

No additional dependencies are required beyond what the scripts install automatically.

---

## 4. Workflow Rituals

All contributor workflows are orchestrated through the Makefile.  
Before running any target, run the **tab sentinel**:

```
make sentinel
```

If it prints:

```
Tab indentation is working.
```

you may proceed.  
If it fails, fix Makefile indentation before continuing.

### 4.1 Validate the Repository

Run:

```
make validate
```

This checks:

- canonical data  
- schema alignment  
- status history  
- workflow states  
- JSONL formatting  

All contributions must pass validation before commit.

---

### 4.2 Generate Metrics (T02)

To extract metrics for the current sprint:

```
make metrics
```

This produces:

- a timestamped metrics file under `reports/<sprint>/metrics/`  
- a clean, reproducible snapshot of sprint health  

---

### 4.3 Consolidate Time‑Series (T03)

To update the longitudinal metrics files:

```
make timeseries
```

This generates:

- `data/metrics_timeseries.jsonl`  
- `data/metrics_timeseries.parquet`  

These files power analytics and historical review.

---

### 4.4 Full Sprint Review Ritual

To run metrics + time‑series together:

```
make review
```

This is used during sprint transitions and review ceremonies.

---

### 4.5 Pre‑Commit Ritual

Before committing any change:

```
make pre-commit
```

This runs:

- validation  
- metrics extraction  
- time‑series consolidation  

If this passes, your contribution is safe to commit.

---

## 5. Editing Standards

### 5.1 Makefile Indentation (Critical)

Makefiles require **literal tabs** for command lines.  
Spaces will break the workflow.

To verify indentation:

```
make sentinel
```

If it fails, repair indentation before running any other target.

### 5.2 VSCode Configuration

VSCode must be configured to use tabs for Makefiles:

```json
"[makefile]": {
  "editor.insertSpaces": false,
  "editor.detectIndentation": false,
  "editor.tabSize": 4
}
```

### 5.3 Clipboard Safety

Copying Makefile content from HTML (e.g., browsers, chat interfaces) may convert tabs to spaces.  
To avoid this:

- paste into a WSL‑native editor (vim/nano) first  
- then copy from WSL → VSCode  

This preserves literal tabs.

---

## 6. Adding or Updating Data

When modifying canonical data:

1. Edit files under `data/`  
2. Run `make validate`  
3. Run `make pre-commit`  
4. Commit with a clear, governance‑aligned message  

Never edit JSONL files manually without validation.

---

## 7. Documentation Contributions

Documentation lives under `docs/`.  
When adding or updating documentation:

- keep tone consistent with governance philosophy  
- explain both *what* and *why*  
- ensure examples are correct and reproducible  
- avoid editor‑induced formatting drift  

---

## 8. Commit Messages

Commit messages should:

- describe the change clearly  
- reference the ritual or milestone (e.g., T02, T03)  
- reflect governance intent  

Examples:

- `T02: Extract metrics for sprint-04 and update schema docs`  
- `Fix Makefile indentation and add tab sentinel section`  
- `T03: Consolidate metrics time-series and update parquet file`  

---

## 9. Asking for Help

If you encounter:

- validation errors  
- schema mismatches  
- Makefile indentation issues  
- unexpected metrics output  

consult:

- `docs/workflow-rituals.md`  
- this `contributing.md`  
- the tab sentinel  
- the validator output  

These artifacts are designed to guide contributors through common issues.

---

## 10. Final Notes

This ecosystem is designed to be:

- durable  
- auditable  
- contributor‑friendly  
- governance‑aligned  

Your contributions help maintain its clarity and integrity.  
Thank you for participating in a system built for long‑term stewardship.

