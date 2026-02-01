# Metrics Schema (T02)
This document defines the structure, meaning, and rationale of all metrics produced by `scripts/extract_metrics.py`. It is written for contributors with varying levels of experience in software engineering, data analytics, and AI/ML.

The goal is to ensure:
- clarity  
- reproducibility  
- governance alignment  
- future extensibility (T03–T04)  
- ML‑readiness  

Each metric is described with:
- **Name**
- **Type**
- **Example**
- **Definition**
- **How it is computed**
- **Why it matters** (governance + analytics + ML)

---

# 1. Top‑Level Structure

The metrics file is a JSON document with this high‑level shape:

```json
{
  "timestamp": "...",
  "num_sprints": ...,
  "num_issues": ...,
  "num_tasks": ...,
  "tasks_per_issue": { ... },
  "issues_per_sprint": { ... },
  "issue_status_distribution": { ... },
  "task_status_distribution": { ... },
  "dependency_edges": ...,
  "issues_with_dependencies": ...,
  "avg_dependencies_per_issue": ...,
  "sprint_completion_ratio": ...,
  "tasks_per_issue_status": { ... },
  "sprint_workload_summary": { ... },
  "issue_load_score": { ... },
  "flow_health": { ... },
  "validation": { ... }
}
```

Each section below explains these fields in detail.

---

# 2. Metadata

## **timestamp**
- **Type:** string (ISO‑8601)
- **Example:** `"2026-01-28T16:49:42.123456"`
- **Definition:** The exact time the metrics were generated.
- **Why it matters:**  
  - Enables time‑series analysis  
  - Supports MLflow lineage  
  - Allows reproducibility and auditability  

---

# 3. Basic Counts

## **num_sprints**
- **Type:** integer  
- **Definition:** Number of sprint records in `sprints.jsonl`.

## **num_issues**
- **Type:** integer  
- **Definition:** Number of issue records in `issues.jsonl`.

## **num_tasks**
- **Type:** integer  
- **Definition:** Number of task records in `tasks.jsonl`.

**Why these matter:**  
These are baseline indicators of dataset size and sprint complexity. They also serve as sanity checks for data completeness.

---

# 4. Issue–Task Relationships

## **tasks_per_issue**
- **Type:** object mapping issue_id → integer  
- **Example:**
  ```json
  { "ISSUE-001": 4, "ISSUE-002": 2 }
  ```
- **Definition:** Number of tasks associated with each issue.
- **How computed:** `tasks.groupby("issue_id").size()`
- **Why it matters:**  
  - Identifies overloaded issues  
  - Supports workload balancing  
  - Useful for ML models predicting issue duration or risk  

---

## **issues_per_sprint**
- **Type:** object mapping sprint_id → integer  
- **Definition:** Number of issues assigned to each sprint.
- **Why it matters:**  
  - Shows sprint scope  
  - Helps detect over‑ or under‑loaded sprints  
  - Useful for forecasting sprint capacity  

---

# 5. Status Distributions

## **issue_status_distribution**
- **Type:** object mapping status → count  
- **Example:** `{ "todo": 3, "in_progress": 5, "done": 7 }`
- **Definition:** Count of issues in each workflow state.

## **task_status_distribution**
- **Type:** object mapping status → count  
- **Definition:** Count of tasks in each workflow state.

**Why these matter:**  
These distributions are the backbone of Kanban analytics. They reveal bottlenecks, flow health, and sprint progress.

---

# 6. Dependency Metrics

## **dependency_edges**
- **Type:** integer  
- **Definition:** Total number of dependency links across all issues.

## **issues_with_dependencies**
- **Type:** integer  
- **Definition:** Number of issues that depend on at least one other issue.

## **avg_dependencies_per_issue**
- **Type:** float  
- **Definition:** Mean number of dependencies per issue.

**Why these matter:**  
Dependencies are a major source of risk.  
These metrics help identify:

- blocked work  
- critical path issues  
- structural complexity  
- potential delays  

They also support ML models predicting issue slippage.

---

# 7. Sprint Completion

## **sprint_completion_ratio**
- **Type:** float (0–1)
- **Definition:**  
  ```
  completed_issues / total_issues
  ```
- **Why it matters:**  
  - High‑level sprint health indicator  
  - Useful for burndown/burnup analytics  
  - Supports forecasting  

---

# 8. Mini‑Kanban Snapshot

## **tasks_per_issue_status**
- **Type:** object mapping issue_id → {status → count}
- **Example:**
  ```json
  {
    "ISSUE-001": { "todo": 1, "in_progress": 2, "review": 0, "done": 1 }
  }
  ```
- **Definition:** Per‑issue breakdown of tasks by status.
- **Why it matters:**  
  - Reveals bottlenecks at the issue level  
  - Supports flow analysis  
  - Enables ML models to detect stalled issues  

This is a compact, structured Kanban board.

---

# 9. Sprint Workload Summary

## **sprint_workload_summary**
- **Type:** object  
- **Fields:**
  - `total_tasks`
  - `tasks_todo`
  - `tasks_in_progress`
  - `tasks_in_review`
  - `tasks_done`
- **Why it matters:**  
  - High‑level sprint workload snapshot  
  - Useful for standup summaries  
  - Supports WIP (work‑in‑progress) analysis  

---

# 10. Issue Load Score

## **issue_load_score**
- **Type:** object mapping issue_id → integer  
- **Definition:** Weighted sum of tasks by status:
  ```
  todo = 1
  in_progress = 2
  review = 3
  done = 0
  ```
- **Why it matters:**  
  - Quantifies issue complexity  
  - Helps identify overloaded issues  
  - Useful for ML models predicting issue duration or risk  

---

# 11. Flow Health Indicator

## **flow_health**
- **Type:** object  
- **Fields:**
  - `review_overload`: issues with ≥2 tasks in review  
  - `in_progress_overload`: issues with ≥3 tasks in progress  
  - `blocked_issues`: issues with dependencies  
- **Why it matters:**  
  - Detects bottlenecks  
  - Surfaces systemic flow problems  
  - Supports governance decisions  
  - Useful for anomaly detection models  

---

# 12. Validation Metrics

## **validation**
- **Type:** object  
- **Fields:**
  - `orphan_tasks`: tasks referencing nonexistent issues  
  - `issues_without_tasks`: issues with no tasks  
  - `num_orphan_tasks`: integer  
  - `num_issues_without_tasks`: integer  
- **Why it matters:**  
  - Ensures data integrity  
  - Detects schema drift  
  - Supports governance and debugging  
  - Prevents ML models from training on corrupted data  

---

# 13. Summary

This metrics schema provides:

- a complete analytical view of sprint health  
- a foundation for MLflow logging (T04)  
- a basis for dashboards and time‑series analytics (T03)  
- a governance‑grade structure for contributors  

Every metric is:

- deterministic  
- reproducible  
- explainable  
- aligned with your workflow schema  
- ready for downstream ML tasks  

