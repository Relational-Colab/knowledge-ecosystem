# Time‑Series Metrics and the Evolution of Sprint Analytics (T03)

This document explains how metrics evolve over time and how the project will build a time‑series analytics layer (T03). It complements:

- `metrics-schema.md` — what each metric means  
- `metrics-interpretation.md` — how to interpret metrics in a single sprint  

This guide focuses on **how metrics behave across multiple sprints**, how to store them as a **time‑series dataset**, and how this enables **governance, forecasting, and ML‑driven insights**.

---

# 1. Why Time‑Series Matter

A single metrics file tells you what happened *today*.  
A time‑series of metrics tells you:

- how your workflow evolves  
- whether your governance discipline is improving  
- where bottlenecks form and dissolve  
- how predictable your sprints are  
- how stable your velocity is  
- how complexity accumulates or resolves  
- how dependencies affect flow over time  

Time‑series data transforms your ecosystem from a static snapshot into a **living analytical instrument**.

---

# 2. What Becomes a Time‑Series

Every metric in T02 becomes a time‑series when collected across sprints. Examples:

### **2.1 Sprint Completion Ratio Over Time**
Shows whether the team consistently finishes sprints.

### **2.2 Issue and Task Status Distributions Over Time**
Reveals whether:
- review bottlenecks are chronic  
- WIP overload is systemic  
- planning accuracy is improving  

### **2.3 Dependency Metrics Over Time**
Tracks structural complexity:
- Are dependency chains growing  
- Are issues becoming more interdependent  
- Are blocked issues increasing  

### **2.4 Issue Load Scores Over Time**
Shows whether issues are:
- becoming more complex  
- being decomposed effectively  
- accumulating technical debt  

### **2.5 Flow Health Indicators Over Time**
Reveals patterns such as:
- recurring review overload  
- persistent WIP spikes  
- dependency‑driven stalls  

These patterns are essential for governance and ML.

---

# 3. How Time‑Series Data Will Be Stored (T03)

T03 introduces a **canonical time‑series metrics store**.

## 3.1 Storage Format
We will store metrics in:

- **JSON** (human‑readable, canonical)  
- **Parquet** (columnar, analytics‑friendly)  

Each metrics extraction produces:

```
reports/<sprint>/metrics/metrics-<timestamp>.json
```

T03 will consolidate these into:

```
analytics/metrics_timeseries.parquet
analytics/metrics_timeseries.jsonl
```

Each row represents one metrics extraction event.

---

# 4. Time‑Series Schema

A time‑series row contains:

- timestamp  
- sprint_id  
- all scalar metrics  
- flattened versions of structured metrics  

Example (simplified):

```json
{
  "timestamp": "2026-01-28T16:49:42",
  "sprint_id": "sprint-04",
  "sprint_completion_ratio": 0.42,
  "tasks_todo": 12,
  "tasks_in_progress": 7,
  "tasks_in_review": 4,
  "tasks_done": 9,
  "dependency_edges": 6,
  "review_overload": 1,
  "in_progress_overload": 0,
  "blocked_issues": 2
}
```

Structured metrics (like `tasks_per_issue_status`) will be flattened or stored as nested JSON depending on downstream needs.

---

# 5. How Time‑Series Metrics Evolve

## 5.1 Sprint Completion Ratio
- **Upward trend** → improving predictability  
- **Downward trend** → planning issues or scope creep  
- **Volatility** → unstable workflow  

## 5.2 Status Distributions
- **Growing “review” column** → chronic review bottleneck  
- **Growing “in_progress”** → WIP overload  
- **Shrinking “todo” early in sprint** → good planning  

## 5.3 Dependency Metrics
- **Increasing dependency_edges** → rising structural complexity  
- **Increasing blocked_issues** → risk of systemic delays  

## 5.4 Issue Load Score
- **Rising average load score** → issues becoming heavier  
- **Falling load score** → better decomposition  

## 5.5 Flow Health Indicators
- **Recurring review_overload spikes** → governance action needed  
- **Recurring in_progress_overload** → WIP limit violations  
- **Persistent blocked_issues** → dependency mismanagement  

---

# 6. What T03 Enables

## 6.1 Governance Insights
Time‑series analytics allow you to answer:

- Are we improving sprint over sprint  
- Are bottlenecks recurring  
- Are issues becoming more complex  
- Are dependencies growing  
- Is our workflow stable  

This is the foundation of governance‑grade decision‑making.

---

## 6.2 Predictive Analytics (T04+)
Time‑series metrics are ideal for ML tasks:

- **forecasting sprint completion**  
- **predicting issue slippage**  
- **detecting anomalies in flow health**  
- **estimating issue complexity**  
- **predicting review bottlenecks**  

Because the metrics are structured and consistent, they are ML‑ready.

---

## 6.3 Dashboards and Visualizations
T03 enables dashboards such as:

- sprint completion over time  
- WIP trends  
- review bottleneck frequency  
- dependency complexity curves  
- issue load score evolution  

These dashboards help contributors understand the system at a glance.

---

# 7. Implementation Plan for T03

### **Step 1: Create analytics/ directory**
```
analytics/
    metrics_timeseries.jsonl
    metrics_timeseries.parquet
```

### **Step 2: Write a consolidation script**
This script will:

- scan all metrics files  
- extract scalar metrics  
- flatten structured metrics  
- append to the time‑series dataset  

### **Step 3: Add Makefile target**
```
make timeseries
```

### **Step 4: Add documentation**
Explain how to run and interpret the time‑series layer.

### **Step 5: Prepare for MLflow (T04)**
Once time‑series data exists, MLflow logging becomes trivial.

---

# 8. Summary

This document explains how metrics evolve over time and how T03 will build a time‑series analytics layer that supports:

- governance  
- sprint management  
- forecasting  
- anomaly detection  
- ML‑driven insights  

T02 gave you a rich snapshot.  
T03 turns those snapshots into a **living history**.  
T04 will turn that history into **intelligence**.

