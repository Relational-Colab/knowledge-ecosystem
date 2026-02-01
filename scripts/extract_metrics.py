#!/usr/bin/env python3
"""
extract_metrics.py — Sprint-04 Metrics Extraction

This script loads canonical JSONL data (sprints, issues, tasks),
computes analytical metrics, and writes them to a timestamped JSON file.

T02 includes:
- Basic counts
- Tasks per issue
- Issues per sprint
- Status distributions
- Dependency metrics
- Sprint completion ratio
- Mini-Kanban snapshot (tasks per issue per status)
- Sprint workload summary
- Flow health indicator
- Issue load score
- Data validation metrics

Future tasks (T03–T04) will extend this with Parquet output and MLflow logging.
"""

import json
from pathlib import Path
from datetime import datetime

import pandas as pd


# === Paths ===
DATA_DIR = Path("data")
SPRINT_FILE = Path(".sprint")
CURRENT_SPRINT = SPRINT_FILE.read_text().strip() if SPRINT_FILE.exists() else "sprint-04"

OUTPUT_DIR = Path("reports") / CURRENT_SPRINT / "metrics"


# === Canonical Loader ===
def load_jsonl(path: Path) -> pd.DataFrame:
    """Load a JSONL file into a pandas DataFrame."""
    records = []
    with open(path, "r") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return pd.DataFrame(records)


def load_canonical():
    """Load all canonical governance datasets."""
    sprints = load_jsonl(DATA_DIR / "sprints.jsonl")
    issues = load_jsonl(DATA_DIR / "issues.jsonl")
    tasks = load_jsonl(DATA_DIR / "tasks.jsonl")
    return sprints, issues, tasks


# === Metrics Computation (T02) ===
def compute_metrics(sprints: pd.DataFrame, issues: pd.DataFrame, tasks: pd.DataFrame) -> dict:
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "num_sprints": len(sprints),
        "num_issues": len(issues),
        "num_tasks": len(tasks),
    }

    # Tasks per issue
    metrics["tasks_per_issue"] = (
        tasks.groupby("issue_id").size().rename("tasks_per_issue").to_dict()
    )

    # Issues per sprint
    issues_per_sprint = {}
    if "issues" in sprints.columns:
        for _, row in sprints.iterrows():
            sprint_id = row["id"]
            issue_list = row.get("issues", [])
            issues_per_sprint[sprint_id] = len(issue_list)
    metrics["issues_per_sprint"] = issues_per_sprint

    # Status distributions
    metrics["issue_status_distribution"] = issues["status"].value_counts().to_dict()
    metrics["task_status_distribution"] = tasks["status"].value_counts().to_dict()

    # Dependency metrics
    issues_with_deps = issues["depends_on"].apply(
        lambda x: len(x) if isinstance(x, list) else 0
    )
    metrics["dependency_edges"] = int(issues_with_deps.sum())
    metrics["issues_with_dependencies"] = int((issues_with_deps > 0).sum())
    metrics["avg_dependencies_per_issue"] = float(issues_with_deps.mean())

    # Sprint completion ratio
    completed_issues = (issues["status"] == "done").sum()
    total_issues = len(issues)
    metrics["sprint_completion_ratio"] = (
        completed_issues / total_issues if total_issues > 0 else 0
    )

    # Mini-Kanban snapshot: tasks per issue per status
    tasks_per_issue_status = (
        tasks.groupby(["issue_id", "status"])
             .size()
             .unstack(fill_value=0)
             .to_dict(orient="index")
    )
    metrics["tasks_per_issue_status"] = tasks_per_issue_status

    # Sprint workload summary
    metrics["sprint_workload_summary"] = {
        "total_tasks": len(tasks),
        "tasks_todo": int((tasks["status"] == "todo").sum()),
        "tasks_in_progress": int((tasks["status"] == "in_progress").sum()),
        "tasks_in_review": int((tasks["status"] == "review").sum()),
        "tasks_done": int((tasks["status"] == "done").sum()),
    }

    # Issue load score (weighted)
    weights = {"todo": 1, "in_progress": 2, "review": 3, "done": 0}
    issue_load_scores = {}
    for issue_id, row in tasks_per_issue_status.items():
        score = sum(row.get(status, 0) * weight for status, weight in weights.items())
        issue_load_scores[issue_id] = score
    metrics["issue_load_score"] = issue_load_scores

    # Flow health indicator
    review_overload = sum(
        1 for row in tasks_per_issue_status.values() if row.get("review", 0) >= 2
    )
    in_progress_overload = sum(
        1 for row in tasks_per_issue_status.values() if row.get("in_progress", 0) >= 3
    )
    blocked_issues = int((issues_with_deps > 0).sum())

    metrics["flow_health"] = {
        "review_overload": review_overload,
        "in_progress_overload": in_progress_overload,
        "blocked_issues": blocked_issues,
    }

    # Validation metrics
    orphan_tasks = tasks[~tasks["issue_id"].isin(issues["id"])]
    issues_without_tasks = issues[~issues["id"].isin(tasks["issue_id"])]

    metrics["validation"] = {
        "orphan_tasks": orphan_tasks["id"].tolist(),
        "issues_without_tasks": issues_without_tasks["id"].tolist(),
        "num_orphan_tasks": len(orphan_tasks),
        "num_issues_without_tasks": len(issues_without_tasks),
    }

    return metrics


# === Output Writers ===
def write_json(metrics: dict, output_path: Path):
    """Write metrics to a JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)


# === MLflow Logging Stub (T04) ===
def log_to_mlflow(metrics: dict):
    """Placeholder for MLflow integration."""
    pass


# === Main Orchestration ===
def main():
    sprints, issues, tasks = load_canonical()
    metrics = compute_metrics(sprints, issues, tasks)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = OUTPUT_DIR / f"metrics-{timestamp}.json"

    write_json(metrics, output_path)
    log_to_mlflow(metrics)

    print(f"Metrics written to {output_path}")


if __name__ == "__main__":
    main()
