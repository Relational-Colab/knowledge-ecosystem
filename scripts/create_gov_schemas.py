import pandas as pd
from datetime import datetime

# -------------------------------------------------------------------
# 1. SPRINTS
# -------------------------------------------------------------------

sprints = [
    {
        "sprint_id": "S03",
        "name": "Sprint 03",
        "start_date": "2025-01-20",
        "end_date": "2025-02-02",
        "status": "active",
        "notes": "Mid-sprint pivot to local-first telemetry"
    }
]

df_sprints = pd.DataFrame(sprints)
df_sprints.to_parquet("sprints.parquet", index=False)


# -------------------------------------------------------------------
# 2. ISSUES
# -------------------------------------------------------------------

now = datetime.now().isoformat()

issues = [
    {
        "issue_id": "S03.I01",
        "sprint_id": "S03",
        "title": "Establish local-first telemetry substrate",
        "description": "",
        "status": "in_progress",
        "created_at": now,
        "updated_at": now,
        "tags": []
    },
    {
        "issue_id": "S03.I02",
        "sprint_id": "S03",
        "title": "MLflow heartbeat + governance metrics",
        "description": "",
        "status": "in_progress",
        "created_at": now,
        "updated_at": now,
        "tags": []
    },
    {
        "issue_id": "S03.I03",
        "sprint_id": "S03",
        "title": "Sprint 03 analytics + notebooks",
        "description": "",
        "status": "backlog",
        "created_at": now,
        "updated_at": now,
        "tags": []
    },
    {
        "issue_id": "S03.I04",
        "sprint_id": "S03",
        "title": "Mid-sprint review + governance alignment",
        "description": "",
        "status": "done",
        "created_at": now,
        "updated_at": now,
        "tags": []
    }
]

df_issues = pd.DataFrame(issues)
df_issues.to_parquet("issues.parquet", index=False)


# -------------------------------------------------------------------
# 3. TASKS
# -------------------------------------------------------------------

tasks = [
    {
        "task_id": "S03.I01.T01",
        "issue_id": "S03.I01",
        "sprint_id": "S03",
        "title": "Create forensic extraction script",
        "description": "",
        "status": "done",
        "created_at": now,
        "updated_at": now,
        "mlflow_run_id": "",
        "tags": []
    },
    {
        "task_id": "S03.I01.T02",
        "issue_id": "S03.I01",
        "sprint_id": "S03",
        "title": "Generate forensic datasets",
        "description": "",
        "status": "done",
        "created_at": now,
        "updated_at": now,
        "mlflow_run_id": "",
        "tags": []
    },
    {
        "task_id": "S03.I02.T01",
        "issue_id": "S03.I02",
        "sprint_id": "S03",
        "title": "Implement MLflow heartbeat run",
        "description": "",
        "status": "in_progress",
        "created_at": now,
        "updated_at": now,
        "mlflow_run_id": "",
        "tags": []
    },
    {
        "task_id": "S03.I02.T02",
        "issue_id": "S03.I02",
        "sprint_id": "S03",
        "title": "Add governance metrics extractor",
        "description": "",
        "status": "done",
        "created_at": now,
        "updated_at": now,
        "mlflow_run_id": "",
        "tags": []
    },
    {
        "task_id": "S03.I03.T01",
        "issue_id": "S03.I03",
        "sprint_id": "S03",
        "title": "Build sprint history notebook",
        "description": "",
        "status": "in_progress",
        "created_at": now,
        "updated_at": now,
        "mlflow_run_id": "",
        "tags": []
    },
    {
        "task_id": "S03.I04.T01",
        "issue_id": "S03.I04",
        "sprint_id": "S03",
        "title": "Draft mid-sprint review",
        "description": "",
        "status": "done",
        "created_at": now,
        "updated_at": now,
        "mlflow_run_id": "",
        "tags": []
    }
]

df_tasks = pd.DataFrame(tasks)
df_tasks.to_parquet("tasks.parquet", index=False)

print("Parquet files created: sprints.parquet, issues.parquet, tasks.parquet")
