#!/usr/bin/env python3

import json
import re
import sys
import argparse
import mlflow
import pandas as pd
from pathlib import Path
from datetime import datetime

# -------------------------------------------------------------------
# Paths
# -------------------------------------------------------------------

DATA_DIR = Path("data")
REGISTRY_PATH = Path("frameworks/schema_registry.json")

# -------------------------------------------------------------------
# Utility: load JSONL into DataFrame
# -------------------------------------------------------------------

def load_jsonl(path: Path) -> pd.DataFrame:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return pd.DataFrame(rows)

# -------------------------------------------------------------------
# Utility: load schema registry
# -------------------------------------------------------------------

def load_registry() -> dict:
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------------------------------------------------
# Error helper
# -------------------------------------------------------------------

def fail(msg: str):
    print(f"VALIDATION ERROR: {msg}")
    sys.exit(1)

# -------------------------------------------------------------------
# Timestamp parsing
# -------------------------------------------------------------------

def parse_timestamp(value: str) -> datetime:
    cleaned = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(cleaned)
    except Exception as e:
        fail(f"Invalid timestamp '{value}': {e}")

# -------------------------------------------------------------------
# Status validation
# -------------------------------------------------------------------

def validate_status(status: str, allowed: list, label: str):
    if status not in allowed:
        fail(f"{label} invalid status '{status}' (allowed: {allowed})")

# -------------------------------------------------------------------
# Status history validation (corrected for Option A)
# -------------------------------------------------------------------

def validate_status_history(record: dict, transitions: dict, label: str):
    history = record.get("status_history")

    # Option A: history must exist and be non-empty
    if not history:
        fail(f"{label} missing or empty status_history")

    last_time = None

    # Validate transitions between consecutive entries
    for i in range(1, len(history)):
        prev = history[i - 1]
        curr = history[i]

        from_s = prev["status"]
        to_s = curr["status"]

        # Check legal transitions
        allowed_next = transitions.get(from_s, [])
        if to_s not in allowed_next:
            fail(f"{label} illegal transition {from_s} → {to_s}")

        # Check timestamps
        ts_prev = parse_timestamp(prev["timestamp"])
        ts_curr = parse_timestamp(curr["timestamp"])
        if ts_curr <= ts_prev:
            fail(f"{label} status_history timestamps must be strictly increasing")

        last_time = ts_curr

    # Final status must match last entry
    final_status = history[-1]["status"]
    if record.get("status") != final_status:
        fail(
            f"{label} final status '{record.get('status')}' "
            f"does not match last transition '{final_status}'"
        )

# -------------------------------------------------------------------
# Identifier pattern validation
# -------------------------------------------------------------------

def validate_id_pattern(df: pd.DataFrame, pattern: str, field: str, label: str):
    regex = re.compile(pattern)
    for _, row in df.iterrows():
        value = row[field]
        if not regex.match(value):
            fail(f"{label} invalid {field} '{value}' does not match pattern {pattern}")

# -------------------------------------------------------------------
# Required fields validation
# -------------------------------------------------------------------

def validate_required_fields(df: pd.DataFrame, required: list, label: str):
    missing = [f for f in required if f not in df.columns]
    if missing:
        fail(f"{label} missing required fields: {missing}")

# -------------------------------------------------------------------
# Foreign key validation
# -------------------------------------------------------------------

def validate_foreign_keys(df: pd.DataFrame, fk_map: dict, lookup: dict, label: str):
    for fk_field, target in fk_map.items():
        table, field = target.split(".")
        valid_values = lookup[table][field]
        for _, row in df.iterrows():
            if row[fk_field] not in valid_values:
                fail(
                    f"{label} invalid FK: {fk_field}='{row[fk_field]}' "
                    f"not found in {target}"
                )

# -------------------------------------------------------------------
# Dataset-level validation
# -------------------------------------------------------------------

def validate_dataset(df: pd.DataFrame, schema: dict, lookup: dict, label: str, registry: dict):
    validate_required_fields(df, schema["required_fields"], label)

    id_field = schema["required_fields"][0]
    validate_id_pattern(df, schema["id_pattern"], id_field, label)

    allowed_status = schema["status_values"]
    for _, row in df.iterrows():
        validate_status(row["status"], allowed_status, label)

    if "foreign_keys" in schema:
        validate_foreign_keys(df, schema["foreign_keys"], lookup, label)

    transitions = registry["workflow"]["allowed_transitions"]
    for _, row in df.iterrows():
        validate_status_history(row, transitions, label)

# -------------------------------------------------------------------
# Main pipeline
# -------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args()

    registry = load_registry()
    schemas = registry["schemas"]

    df_sprints = load_jsonl(DATA_DIR / "sprints.jsonl")
    df_issues = load_jsonl(DATA_DIR / "issues.jsonl")
    df_tasks = load_jsonl(DATA_DIR / "tasks.jsonl")

    lookup = {
        "sprints": {"id": set(df_sprints["id"])},
        "issues": {"id": set(df_issues["id"])},
        "tasks": {"id": set(df_tasks["id"])}
    }

    mlflow.set_experiment("schema_validation")

    with mlflow.start_run(run_name="sprint04_validation"):

        mlflow.log_param("registry_version", registry["registry_version"])
        mlflow.log_param("sprints_schema_version", schemas["sprints"]["schema_version"])
        mlflow.log_param("issues_schema_version", schemas["issues"]["schema_version"])
        mlflow.log_param("tasks_schema_version", schemas["tasks"]["schema_version"])

        mlflow.log_param("sprint_records", len(df_sprints))
        mlflow.log_param("issue_records", len(df_issues))
        mlflow.log_param("task_records", len(df_tasks))

        mlflow.log_artifact(str(REGISTRY_PATH))

        validate_dataset(df_sprints, schemas["sprints"], lookup, "Sprints", registry)
        validate_dataset(df_issues, schemas["issues"], lookup, "Issues", registry)
        validate_dataset(df_tasks, schemas["tasks"], lookup, "Tasks", registry)

        if args.validate_only:
            print("Validation passed. No Parquet written.")
            return

        df_sprints.to_parquet(DATA_DIR / "sprints.parquet", index=False)
        df_issues.to_parquet(DATA_DIR / "issues.parquet", index=False)
        df_tasks.to_parquet(DATA_DIR / "tasks.parquet", index=False)

        print("Validation passed. Parquet regenerated.")

# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
