#!/usr/bin/env python3
"""
generate_review.py

Generates a sprint review artifact consisting of:
1. A JSON review file (metrics + time-series snapshot + metadata)
2. A Markdown narrative review using the governance template

Outputs are written to:
reports/<sprint>/review/review-YYYYMMDD-HHMMSS.{json,md}
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_latest_metrics(metrics_dir):
    """Return the most recent metrics JSON file in the sprint metrics directory."""
    files = sorted(metrics_dir.glob("metrics-*.json"))
    if not files:
        raise FileNotFoundError(f"No metrics files found in {metrics_dir}")
    return load_json(files[-1]), files[-1]


def load_latest_timeseries(ts_path):
    """Load the full metrics time-series JSONL file."""
    if not ts_path.exists():
        raise FileNotFoundError(f"Time-series file not found: {ts_path}")

    entries = []
    with open(ts_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries


def generate_markdown_review(sprint, timestamp, metrics, previous_entry, current_entry):
    """Generate the Markdown narrative review using the governance template."""

    date_str = timestamp.strftime("%Y-%m-%d")
    ts_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")

    md = f"""# Sprint Review — {sprint}

**Date:** {date_str}  
**Generated:** {ts_str}  
**Sprint Window:** {current_entry.get('sprint_start', 'N/A')} → {current_entry.get('sprint_end', 'N/A')}

---

## 1. Sprint Summary

A concise overview of the sprint’s intent, focus areas, and major accomplishments.

**Prompts for contributors:**
- What was the primary goal of the sprint?
- What major milestones or rituals were completed?
- What changed in the ecosystem (schemas, workflows, documentation, governance)?
- What new capabilities or stability improvements emerged?

---

## 2. Key Metrics Overview

A high-level summary of the sprint’s metrics.

**Highlights (auto-extracted):**

- Tasks completed: **{metrics.get('tasks_completed', 'N/A')}**
- Tasks added: **{metrics.get('tasks_added', 'N/A')}**
- Tasks removed: **{metrics.get('tasks_removed', 'N/A')}**
- Total tasks: **{metrics.get('total_tasks', 'N/A')}**

Additional metrics are available in the JSON artifact.

---

## 3. Changes Since Last Sprint

A comparison with the previous sprint’s time-series entry.

**Prompts:**
- What increased?
- What decreased?
- What stabilized?
- What patterns are emerging across sprints?
- Any regressions or improvements worth noting?

**Auto-detected:**
- Previous sprint total tasks: **{previous_entry.get('total_tasks', 'N/A')}**
- Current sprint total tasks: **{current_entry.get('total_tasks', 'N/A')}**

---

## 4. Risks, Observations, and Signals

Qualitative reflections on the sprint’s operational health.

**Prompts:**
- Did any workflows show friction?
- Were there schema mismatches or validator issues?
- Did any rituals require repair or refinement?
- Are there early signals of future complexity or drift?
- What governance lessons emerged?

---

## 5. Next Steps and Recommendations

Forward-looking guidance for the next sprint.

**Prompts:**
- What should be prioritized next?
- Are there technical or governance debts to address?
- What rituals or scripts might need refinement?
- What new capabilities or documentation should be added?
- What stability or contributor-experience improvements are recommended?

---

## 6. Artifact Index

Generated for this sprint:

- Metrics JSON
- Time-series updates
- Review narrative (this document)
- Any schema updates
- Any new documentation
- Any new governance artifacts

"""

    return md


def main():
    if len(sys.argv) != 2:
        print("Usage: generate_review.py <sprint-name>")
        sys.exit(1)

    sprint = sys.argv[1]

    # Paths
    sprint_dir = Path(f"reports/{sprint}")
    metrics_dir = sprint_dir / "metrics"
    review_dir = sprint_dir / "review"
    review_dir.mkdir(parents=True, exist_ok=True)

    ts_path = Path("data/metrics_timeseries.jsonl")

    # Load data
    metrics, metrics_file = load_latest_metrics(metrics_dir)
    timeseries = load_latest_timeseries(ts_path)

    if len(timeseries) < 2:
        previous_entry = {}
    else:
        previous_entry = timeseries[-2]

    current_entry = timeseries[-1]

    # Timestamp
    now = datetime.now()
    ts_tag = now.strftime("%Y%m%d-%H%M%S")

    # JSON review artifact
    review_json = {
        "sprint": sprint,
        "generated_at": now.isoformat(),
        "metrics_file": str(metrics_file),
        "metrics": metrics,
        "previous_timeseries_entry": previous_entry,
        "current_timeseries_entry": current_entry,
    }

    json_path = review_dir / f"review-{ts_tag}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(review_json, f, indent=2)

    # Markdown narrative
    md_content = generate_markdown_review(
        sprint=sprint,
        timestamp=now,
        metrics=metrics,
        previous_entry=previous_entry,
        current_entry=current_entry,
    )

    md_path = review_dir / f"review-{ts_tag}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"Review generated:\n- {json_path}\n- {md_path}")


if __name__ == "__main__":
    main()
