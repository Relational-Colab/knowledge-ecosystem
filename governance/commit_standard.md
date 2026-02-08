# Commit Standard — Governance‑Grade Annotation for the Knowledge Ecosystem

This document defines the formal commit annotation standard for the Knowledge Ecosystem.  
It ensures that every commit is traceable, auditable, and aligned with the sprint → issue → task hierarchy that structures the entire project.

The standard applies to:

- Git commit messages  
- MLflow tags  
- Notebook annotations  
- Script comments  
- Markdown metadata  

This creates a unified lineage system across the ecosystem.

---

## 1. Commit Message Structure

Every commit message follows this pattern:

```text
<type>(<scope>): <short description>

<long description / rationale>
```

### 1.1 Allowed Commit Types

<table>
  <thead>
    <tr>
      <th>Type</th>
      <th>Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>feat</code></td>
      <td>New capability, feature, or artifact</td>
    </tr>
    <tr>
      <td><code>refactor</code></td>
      <td>Structural improvement without changing behavior</td>
    </tr>
    <tr>
      <td><code>fix</code></td>
      <td>Correcting errors or inconsistencies</td>
    </tr>
    <tr>
      <td><code>docs</code></td>
      <td>Documentation, markdown, notebooks</td>
    </tr>
    <tr>
      <td><code>data</code></td>
      <td>Adding or updating datasets</td>
    </tr>
    <tr>
      <td><code>telemetry</code></td>
      <td>MLflow, metrics, extraction scripts</td>
    </tr>
    <tr>
      <td><code>chore</code></td>
      <td>Repo maintenance, renames, moves</td>
    </tr>
    <tr>
      <td><code>governance</code></td>
      <td>Sprint reviews, retros, checkpoints</td>
    </tr>
    <tr>
      <td><code>init</code></td>
      <td>First commit for a new sprint, issue, or schema</td>
    </tr>
  </tbody>
</table>

---

## 2. Scope Format (WBS‑Aligned)

The scope uses the hybrid, zero‑padded identifier format.

### Sprint Scope
```text
S03
```

### Issue Scope
```text
S03.I02
```

### Task Scope
```text
S03.I02.T05
```

### Scope Rules

- If the commit affects a **task**, use the full task ID.  
- If it affects an **issue**, use the issue ID.  
- If it affects the **sprint**, use the sprint ID.  
- If it affects the **repository globally**, use `repo`.

### Examples

```text
feat(S03.I02.T03): add MLflow heartbeat run
docs(S03.I04): add mid-sprint-review.md
refactor(S03): restructure sprint directory
chore(repo): remove deprecated GitHub artifacts
```

---

## 3. Short Description Rules

- Use imperative mood (“add”, “refactor”, “introduce”).  
- Keep under ~70 characters.  
- Describe *what* changed, not *why*.  

### Examples

```text
feat(S03.I01.T02): create issues schema
telemetry(S03.I02.T03): log first MLflow run
docs(S03.I04): add mid-sprint review
```

---

## 4. Long Description Rules (Governance‑Grade)

The long description is optional but recommended for:

- architectural changes  
- governance artifacts  
- telemetry changes  
- schema evolution  

It should include:

- rationale  
- context  
- implications  
- alignment with sprint goals  

### Example

```text
refactor(S03.I01): establish local-first telemetry architecture

This commit introduces the forensic datasets, extraction scripts, and
notebook required to generate governance-grade metrics directly from
git history. It establishes the substrate for MLflow integration and
the refactored scope of Sprint 03.
```

---

## 5. Cross‑Ecosystem Lineage Conventions

The same identifiers appear consistently in:

### 5.1 Markdown
```text
(S03.I04.T15) Drafting Sprint 03 closure note
```

### 5.2 Python / Scripts
```python
# (S03.I02.T03) MLflow heartbeat run
```

### 5.3 Notebooks
```text
(S03.I03.T11) Load governance metrics dataset
```

###