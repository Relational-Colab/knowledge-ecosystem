# Schema Registry — Governance‑Grade Specification

The `schema_registry.json` file defines the authoritative, machine‑readable contract for all canonical datasets in the Knowledge Ecosystem. It is the foundation of the schema‑driven validation pipeline and ensures that all telemetry remains coherent, auditable, and reconstructable.

Where `schema_standard.md` describes the schemas conceptually, the registry encodes them operationally.

---

## 1. Purpose of the Schema Registry

The schema registry provides:

- a single source of truth for dataset definitions  
- strict identifier formats  
- required fields for each dataset  
- allowed workflow states  
- foreign‑key relationships  
- schema versioning  
- evolution history  
- references to machine‑readable schema files  

It enables the validator to enforce governance rules dynamically, without hard‑coded logic.

---

## 2. Registry Structure

The registry contains three major sections:

### **(a) `registry_version`**  
Tracks the version of the registry itself.

### **(b) `schemas`**  
Defines the rules for each dataset:

- `id_pattern` — regex for WBS‑style identifiers  
- `required_fields` — fields that must appear in canonical JSONL  
- `status_values` — allowed workflow states (`todo`, `in_progress`, `review`, `done`)  
- `foreign_keys` — lineage constraints  
- `schema_version` — version of the dataset schema  
- `schema_file` — path to the machine‑readable JSON schema  

These definitions are consumed by the validator and by future governance automation.

### **(c) `evolution`**  
Documents schema changes over time, including:

- field additions  
- workflow changes  
- identifier updates  
- schema file introductions  
- migration notes  

This structure ensures long‑term stability and contributor clarity.

---

## 3. How the Validator Uses the Registry

The validator (`scripts/jsonl_validator.py`, invoked via `jsonl_to_parquet.py`) loads the registry dynamically and enforces:

- required fields  
- identifier formats  
- allowed status values  
- legal workflow transitions  
- timestamp validity  
- foreign‑key integrity  
- sprint/issue/task lineage  
- presence of `mlflow_run_id`, `depends_on`, and `status_history`  
- strict mode (`--strict`) requiring `schema_version` fields  

Validation must pass before Parquet files are generated.

This makes the pipeline:

- schema‑driven  
- evolvable  
- contributor‑ready  
- governance‑grade  
- reconstructable from first principles  

---

## 4. Governance Principles Embedded in the Registry

### **Sovereignty**  
Rules are stored locally in open, human‑readable formats.

### **Reconstructability**  
Any contributor can rebuild the telemetry layer from canonical JSONL + the registry + the validator.

### **Traceability**  
Identifier formats, lineage rules, and workflow transitions are explicit and enforced.

### **Auditability**  
Schema changes are recorded in the `evolution` section and versioned in Git.

### **Separation of Concerns**  
- The registry defines rules.  
- The validator enforces them.  
- Canonical JSONL expresses data.  
- Parquet is derived.  
- MLflow logs lineage and experiment metadata.  

This separation ensures clarity, safety, and long‑term maintainability.

---

## 5. Sprint‑04 Schema Evolution

Sprint 04 introduced the first major schema unification:

- replaced `backlog` with `todo` as the canonical first workflow state  
- unified field names (`id`, `sprint`, `status`, `depends_on`, `mlflow_run_id`)  
- added machine‑readable schema files under `frameworks/schema/`  
- introduced `schema_file` references in the registry  
- standardized `status_history` across issues and tasks  
- aligned identifier patterns with WBS conventions  
- updated the validator to enforce the new workflow and field structure  

These changes are recorded in `schema_registry.json` under `evolution.version = 3`.

---

## 6. Future Evolution

The registry will expand to support:

- schema migrations  
- compatibility checks  
- dataset‑specific governance policies  
- extended lineage definitions  
- version‑to‑version transformation rules  
- MLflow‑logged schema versions  
- automated schema diffing  

A `schema_migrations/` directory will be introduced when the first transformation rules are required.
