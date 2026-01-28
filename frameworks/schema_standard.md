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
      <td><code>id</code></td>
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

- `id` is the primary key.  
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
      <td><code>id</code></td>
      <td>string</td>
      <td>WBS identifier, e.g., <code>"S03.I02"</code></td>
    </tr>
    <tr>
      <td><code>sprint</code></td>
      <td>string</td>
      <td>Foreign key to Sprints</td>
    </tr>
    <tr>
      <td><code>title</code></td>
      <td>string</td>
      <td>Issue title</td>
    </tr>
    <tr>
      <td><code>status</code></td>
      <td>string</td>
      <td><code>todo</code> / <code>in_progress</code> / <code>review</code> / <code>done</code></td>
    </tr>
    <tr>
      <td><code>created_at</code></td>
      <td>datetime</td>
      <td>Creation timestamp</td>
    </tr>
    <tr>
      <td><code>updated_at</code></td>
      <td>datetime</td>
      <td>Last update timestamp</td>
    </tr>
    <tr>
      <td><code>depends_on</code></td>
      <td>list[string]</td>
      <td>Identifiers of issues this issue depends on</td>
    </tr>
    <tr>
      <td><code>mlflow_run_id</code></td>
      <td>string</td>
      <td>Optional MLflow lineage reference</td>
    </tr>
    <tr>
      <td><code>status_history</code></td>
      <td>list[object]</td>
      <td>Ordered list of workflow transitions with timestamps</td>
    </tr>
  </tbody>
</table>

### Constraints

- `id` is the primary key.  
- `sprint` must reference an existing Sprint.  
- `status` must be one of: `todo`, `in_progress`, `review`, `done`.  
- `status_history` must follow legal transitions:  
  - `todo → in_progress`  
  - `in_progress → review`  
  - `review → done`  

---

## 4. Tasks Schema (`tasks.parquet`)

Tasks represent the atomic units of work within an issue.

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
      <td><code>id</code></td>
      <td>string</td>
      <td>WBS identifier, e.g., <code>"S03.I02.T05"</code></td>
    </tr>
    <tr>
      <td><code>issue_id</code></td>
      <td>string</td>
      <td>Foreign key to Issues</td>
    </tr>
    <tr>
      <td><code>sprint</code></td>
      <td>string</td>
      <td>Foreign key to Sprints</td>
    </tr>
    <tr>
      <td><code>title</code></td>
      <td>string</td>
      <td>Task title</td>
    </tr>
    <tr>
      <td><code>status</code></td>
      <td>string</td>
      <td><code>todo</code> / <code>in_progress</code> / <code>review</code> / <code>done</code></td>
    </tr>
    <tr>
      <td><code>created_at</code></td>
      <td>datetime</td>
      <td>Creation timestamp</td>
    </tr>
    <tr>
      <td><code>updated_at</code></td>
      <td>datetime</td>
      <td>Last update timestamp</td>
    </tr>
    <tr>
      <td><code>depends_on</code></td>
      <td>list[string]</td>
      <td>Identifiers of tasks this task depends on</td>
    </tr>
    <tr>
      <td><code>mlflow_run_id</code></td>
      <td>string</td>
      <td>Optional MLflow lineage reference</td>
    </tr>
    <tr>
      <td><code>status_history</code></td>
      <td>list[object]</td>
      <td>Ordered list of workflow transitions with timestamps</td>
    </tr>
  </tbody>
</table>

### Constraints

- `id` is the primary key.  
- `issue_id` must reference an existing Issue.  
- `sprint` must match the sprint of the referenced Issue.  
- `status` must be one of: `todo`, `in_progress`, `review`, `done`.  
- `status_history` must follow legal transitions:  
  - `todo → in_progress`  
  - `in_progress → review`  
  - `review → done`  

---

## 5. Workflow Semantics

The canonical sprint workflow is:

```
todo → in_progress → review → done
```

This workflow is enforced by:

- the schema registry  
- the validator  
- the canonical JSONL  
- MLflow lineage logging  

This ensures consistent flow‑metrics across all sprints.

---

## 6. Alignment With Schema Registry

This document defines the **conceptual schema**.  
The machine‑readable schema lives under:

```
frameworks/schema/
    issues.schema.json
    tasks.schema.json
    workflow.schema.json
```

The registry (`schema_registry.json`) references these files and records schema evolution.

---

## 7. Sprint‑04 Schema Unification

Sprint 04 introduced:

- unified field names (`id`, `sprint`, `status`, `depends_on`, `mlflow_run_id`)  
- canonical workflow (`todo → in_progress → review → done`)  
- standardized `status_history`  
- removal of legacy fields (`description`, `tags`, `sprint_id`, `issue_id`, `task_id`)  
- machine‑readable schema files  
- validator integration  

This schema now governs all future sprints.

