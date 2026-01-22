# Schema Standard — Sprints, Issues, Tasks

This document defines the formal schema standard for the Knowledge Ecosystem.  
It establishes the structure, identifiers, and relationships for the three core governance objects:

- **Sprints**  
- **Issues**  
- **Tasks**

These schemas form the backbone of the local‑first governance architecture and provide the substrate for MLflow telemetry, sprint analytics, and long‑term auditability.

---

## 1. Identifier Standard (WBS‑Aligned)

All schema objects use the hybrid, zero‑padded identifier format.

### Sprint ID
```text
S03
```

### Issue ID
```text
S03.I02
```

### Task ID
```text
S03.I02.T05
```

### Identifier Rules

- Identifiers must be zero‑padded to two digits.  
- Identifiers must be stable once created.  
- Identifiers must be globally unique within their schema.  
- Identifiers must be hierarchically consistent (task → issue → sprint).  

This ensures perfect lexical sorting, perfect lineage, and clean MLflow integration.

---

## 2. Sprints Schema (`sprints.parquet`)

The Sprints schema defines the timeboxes that structure the project.

### Fields

<table>
  <thead>
    <tr>
      <th>Field</th>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>sprint_id</code></td>
      <td>string</td>
      <td>WBS identifier, e.g., <code>"S03"</code></td>
    </tr>
    <tr>
      <td><code>name</code></td>
      <td>string</td>
      <td>Optional human-readable name</td>
    </tr>
    <tr>
      <td><code>start_date</code></td>
      <td>datetime</td>
      <td>Sprint start</td>
    </tr>
    <tr>
      <td><code>end_date</code></td>
      <td>datetime</td>
      <td>Sprint end</td>
    </tr>
    <tr>
      <td><code>status</code></td>
      <td>string</td>
      <td><code>planned</code> / <code>active</code> / <code>closed</code></td>
    </tr>
    <tr>
      <td><code>notes</code></td>
      <td>string</td>
      <td>Optional narrative or metadata</td>
    </tr>
  </tbody>
</table>

### Constraints

- `sprint_id` is the primary key.  
- `start_date` ≤ `end_date`.  
- `status` must be one of: `planned`, `active`, `closed`.

---

## 3. Issues Schema (`issues.parquet`)

Issues represent work packages within a sprint.

### Fields

<table>
  <thead>
    <tr>
      <th>Field</th>
      <th>Type</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>issue_id</code></td>
      <td>string</td>
      <td>WBS identifier, e.g., <code>"S03.I02"</code></td>
    </tr>
    <tr>
      <td><code>sprint_id</code></td>
      <td>string</td>
      <td>Foreign key to Sprints</td>
    </tr>
    <tr>
      <td><code>title</code></td>
      <td>string</td>
      <td>Issue title</td>
    </tr>
    <tr>
      <td><code>description</code></td>
      <td>string</td>
      <td>Optional narrative</td>
    </tr>
    <tr>
      <td><code>status</code></td>
      <td>string</td>
      <td><code>backlog</code> / <code>in_progress</code> / <code>done</code></td>
    </tr>
    <tr>
      <td><code>created_at</code></td>
      <td>datetime</td>
      <td>Creation timestamp</td>
    </tr>
    <tr>
      <td><code>updated_at</code></td>
      <td>datetime</td>
      <td>Last update</td>
    </tr>
    <tr>
      <td><code>tags</code></td>
      <td>list/string</td>
      <td>Optional labels</td>
    </tr>
  </tbody>
</table>

### Constraints

- `issue_id` is the primary key.  
- `sprint_id` must reference an existing Sprint.  
- `status` must be one of: `backlog`, `in_progress`, `done`.

---

