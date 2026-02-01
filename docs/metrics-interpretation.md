# Interpreting Metrics in Real Sprint Scenarios
This document explains **how to interpret the metrics** produced by `extract_metrics.py` in the context of sprint execution, governance, and AI/ML reasoning. While `metrics-schema.md` defines *what* each metric is, this guide explains *how to use them* to understand sprint health, detect bottlenecks, and support decision‑making.

The goal is to help contributors — regardless of background — read the metrics artifact as a meaningful analytical report.

---

# 1. Understanding Sprint Health at a Glance

The following top‑level metrics give you an immediate sense of sprint scale and complexity:

- **num_sprints**  
- **num_issues**  
- **num_tasks**

### How to interpret:
- A high number of issues with a low number of tasks may indicate under‑specified work.
- A high number of tasks per issue may indicate complexity or poor decomposition.
- A sudden jump in tasks or issues between sprints may indicate scope creep.

These metrics are the “vital signs” of the sprint.

---

# 2. Interpreting Issue–Task Relationships

## 2.1 Tasks Per Issue
This metric shows how work is distributed across issues.

### How to interpret:
- **Even distribution** → healthy workload balance.  
- **One issue with 10+ tasks** → likely overloaded; may need decomposition.  
- **Issues with 0 tasks** → under‑defined or incorrectly scoped.

### Governance implications:
- Overloaded issues should be flagged early.  
- Issues without tasks may violate workflow discipline.  
- This metric supports planning and prioritization.

---

## 2.2 Issues Per Sprint
This shows how much work is assigned to each sprint.

### How to interpret:
- **Too many issues in a sprint** → risk of overcommitment.  
- **Too few issues** → underutilization or incomplete planning.  
- **Uneven distribution across sprints** → planning inconsistency.

### Governance implications:
- Helps maintain consistent sprint capacity.  
- Supports retrospective analysis of planning accuracy.

---

# 3. Reading Status Distributions

## 3.1 Issue Status Distribution  
## 3.2 Task Status Distribution

These distributions reveal the overall flow of work.

### How to interpret:
- **High “todo” count mid‑sprint** → planning or prioritization issues.  
- **High “in_progress” count** → possible WIP overload.  
- **High “review” count** → review bottleneck.  
- **High “done” count early** → front‑loaded sprint or small tasks.

### Governance implications:
- Supports WIP limits.  
- Helps identify systemic delays.  
- Useful for standup discussions.

---

# 4. Understanding Dependencies

## 4.1 dependency_edges  
## 4.2 issues_with_dependencies  
## 4.3 avg_dependencies_per_issue

Dependencies are a major source of risk.

### How to interpret:
- **High dependency_edges** → complex sprint; risk of cascading delays.  
- **Many issues_with_dependencies** → sprint may be fragile.  
- **High avg_dependencies_per_issue** → structural complexity.

### Governance implications:
- Issues with dependencies should be prioritized early.  
- Dependency chains should be visualized or tracked explicitly.  
- Helps identify critical path items.

---

# 5. Sprint Completion Ratio

This is the simplest high‑level indicator of sprint progress.

### How to interpret:
- **0.0–0.3** early in sprint → normal.  
- **0.0–0.3 late in sprint** → risk of sprint failure.  
- **0.7–1.0** near end → healthy sprint.

### Governance implications:
- Supports burndown/burnup analysis.  
- Helps detect unrealistic sprint commitments.

---

# 6. Mini‑Kanban Snapshot (Tasks Per Issue Per Status)

This is one of the most powerful metrics in the system.

### How to interpret:
For each issue, you see:

```
todo / in_progress / review / done
```

This reveals:

- **Stalled issues** (many tasks in review or in_progress)  
- **Underdeveloped issues** (all tasks in todo)  
- **Healthy flow** (tasks moving left → right)  

### Governance implications:
- Enables issue‑level flow analysis.  
- Helps identify bottlenecks early.  
- Supports standup discussions with concrete evidence.

---

# 7. Sprint Workload Summary

This is the sprint‑level Kanban.

### How to interpret:
- **High tasks_in_progress** → WIP overload.  
- **High tasks_in_review** → review bottleneck.  
- **High tasks_todo late in sprint** → planning failure.  
- **High tasks_done early** → front‑loaded sprint or small tasks.

### Governance implications:
- Helps enforce WIP limits.  
- Supports capacity planning.  
- Useful for sprint retrospectives.

---

# 8. Issue Load Score

This metric quantifies issue complexity using weighted task statuses.

### How to interpret:
- **High score** → complex or overloaded issue.  
- **Low score** → simple or nearly complete issue.  
- **Sudden score increase** → scope creep.

### Governance implications:
- Helps prioritize work.  
- Supports risk assessment.  
- Useful for ML models predicting issue duration.

---

# 9. Flow Health Indicator

This is a governance‑grade signal of sprint flow.

### Fields:
- **review_overload**  
- **in_progress_overload**  
- **blocked_issues**

### How to interpret:
- **review_overload > 0** → review bottleneck; reviewers overloaded.  
- **in_progress_overload > 0** → too much WIP; context switching risk.  
- **blocked_issues > 0** → dependencies preventing progress.

### Governance implications:
- Helps enforce WIP limits.  
- Supports early detection of systemic issues.  
- Useful for standup and mid‑sprint corrections.

---

# 10. Validation Metrics

These ensure data integrity.

### How to interpret:
- **orphan_tasks** → tasks referencing nonexistent issues; data corruption.  
- **issues_without_tasks** → incomplete issue definitions.  
- **num_orphan_tasks > 0** → must be fixed immediately.  
- **num_issues_without_tasks > 0** → governance violation.

### Governance implications:
- Protects the canonical dataset.  
- Prevents ML models from training on corrupted data.  
- Ensures contributor discipline.

---

# 11. Putting It All Together: A Real Scenario

Imagine a sprint where:

- many tasks are in review  
- several issues have high load scores  
- sprint_completion_ratio is low  
- flow_health.review_overload is high  
- dependency_edges is high

### Interpretation:
This sprint is bottlenecked at review, with complex issues and dependency‑driven delays. The team should:

- prioritize clearing review  
- reduce WIP  
- break down overloaded issues  
- address dependency chains early  

This is how metrics become governance.

---

# 12. Why This Matters for AI/ML

These metrics form the foundation for:

- predictive models (issue duration, sprint success)  
- anomaly detection (flow breakdowns)  
- time‑series forecasting (velocity, throughput)  
- risk scoring (dependency‑driven delays)  

Because the metrics are structured, consistent, and schema‑aligned, they are ideal for MLflow logging and downstream analytics.

---

# 13. Summary

This document teaches contributors how to read the metrics artifact as a meaningful analytical report. It connects:

- sprint execution  
- project management methodology  
- governance discipline  
- AI/ML reasoning  

Together with `metrics-schema.md`, it forms a complete guide to understanding and using the metrics layer of the knowledge ecosystem.
