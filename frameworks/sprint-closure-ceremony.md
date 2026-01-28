# Sprint Closure Ceremony  
**Canonical Governance Document**

This document defines the official, governance‑aligned procedure for closing a sprint in the Knowledge Ecosystem. It ensures that every sprint ends with a clean boundary, complete artifacts, validated data truth, and a fresh cognitive context for the next sprint.

---

# 1. Purpose

The Sprint Closure Ceremony:

- preserves the integrity of canonical data  
- ensures analytics and derived artifacts are archived  
- creates a clear historical boundary  
- supports contributor‑ready governance  
- provides a cognitive reset for the next sprint  

This ceremony is mandatory for all sprint closures.

---

# 2. Timing Model

To protect the sprint boundary and ensure a calm, deliberate closure, the following timing model is enforced:

### T − 2:00 — Begin Retrospective Work
- Draft and refine `retrospective.md`  
- Reflect on lessons learned, governance insights, and systemic observations  
- Ensure the retrospective is thoughtful and unrushed  

### T − 1:00 — Begin the Sprint Closure Ceremony
- Execute all technical and governance steps  
- Allow buffer time for unexpected issues  
- Ensure all artifacts are complete before the boundary  

### T 0 — Sprint Boundary
- All closure steps are complete  
- The sprint is formally sealed  
- A new sprint may begin  

This timing model ensures both reflection and execution receive the cognitive space they require.

---

# 3. Ceremony Steps

The Sprint Closure Ceremony consists of nine steps.  
All steps must be completed before the sprint boundary.

---

## Step 1 — Complete All In‑Scope Work

Before closure:

- All issues and tasks intended for the sprint must be in **Done** or explicitly **rolled over**  
- No items may remain in **In‑Progress** or **Review**  
- All governance checkpoints must be satisfied  

This ensures the sprint reflects actual delivery.

---

## Step 2 — Validate Canonical JSONL

Run the validator to confirm data truth:

```bash
python scripts/jsonl_to_parquet.py --validate-only
```

Requirements:

- A clean “Validation passed” is mandatory  
- If validation fails, correct the data and re‑run  
- Commit corrections before proceeding  

This step ensures canonical truth is sealed before analytics.

---

## Step 3 — Execute the Analytics Notebook

Run the sprint analytics notebook one final time:

- refresh metrics  
- regenerate charts  
- update narrative cells  
- confirm outputs reflect the final sprint state  

The notebook becomes the analytical record of the sprint.

---

## Step 4 — Export Notebook Outputs (Derived Artifacts)

Use the export script to archive all notebook outputs:

```bash
python scripts/export_notebook_outputs.py notebooks/sprint_history.ipynb reports/sprint-XX
```

This produces:

- `figures/`  
- `tables/`  
- `text/`  
- `sprint-XX-index.md`  

These artifacts form the sprint’s reporting layer.

---

## Step 5 — Write the Sprint Summary

Create a Markdown summary containing:

- completed work  
- rolled‑over work  
- key metrics  
- governance notes  
- risks and mitigations  
- narrative insights  

This is the human‑readable story of the sprint.

---

## Step 6 — Commit All Sprint Artifacts

Commit:

- canonical JSONL  
- analytics notebook  
- exported artifacts  
- sprint summary  
- schema or validator updates (if any)  

This ensures the sprint is fully expressed in the repository.

---

## Step 7 — Tag the Sprint Boundary

Create a durable historical boundary:

```bash
git tag sprint-XX-close
git push --tags
```

This tag marks the sprint as sealed and immutable.

---

## Step 8 — Cognitive Reset

Acknowledge completion:

- clear mental state  
- release sprint context  
- prepare for the next sprint  

This reinforces the psychological boundary that mirrors the technical one.

---

## Step 9 — Close the Sprint Conversation

To maintain cognitive and narrative separation:

- end the current sprint’s chat thread  
- shut down and restart the development laptop  
- begin the next sprint in a **fresh conversation**  

This ensures the next sprint starts with a clean cognitive slate.

---

# 4. Ceremony Completion Criteria

A sprint is considered closed when:

- all nine steps are complete  
- all artifacts are committed  
- the sprint boundary tag is pushed  
- the conversation is closed  
- the next sprint begins in a new thread  

Only then is the sprint formally sealed.

---

# 5. Governance Notes

- The ceremony is intentionally structured to be calm, deliberate, and buffer‑protected  
- The export step ensures derived artifacts are preserved outside notebooks  
- The conversation‑closure ritual reinforces cognitive hygiene  
- The timing model prevents rushed or incomplete closures  
- This ceremony scales to multi‑contributor environments  
