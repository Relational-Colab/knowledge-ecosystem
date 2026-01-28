#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path
import sys

DATA_DIR = Path("data")

SPRINT_ID = Path(".sprint").read_text().strip() if Path(".sprint").exists() else "sprint-04"
REPORTS_DIR = Path("reports") / SPRINT_ID
KANBAN_DIR = REPORTS_DIR / "kanban"
HISTORY_DIR = KANBAN_DIR / "history"
MINUTES_DIR = REPORTS_DIR / "minutes"

STATUS_ORDER = ["todo", "in_progress", "review", "done"]

def load_jsonl(path):
    with open(path, "r") as f:
        return [json.loads(line) for line in f]

def group_by_status(records):
    groups = {}
    for r in records:
        status = r.get("status", "unknown")
        groups.setdefault(status, []).append(r)
    return groups

def load_today_minutes():
    today = datetime.now().strftime("%Y-%m-%d")
    path = MINUTES_DIR / f"{today}.json"
    if not path.exists():
        return None
    with open(path, "r") as f:
        return json.load(f)

def render_markdown(title, issues, tasks, minutes):
    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"Sprint: {SPRINT_ID}")
    lines.append(f"Generated: {datetime.now().isoformat()}")
    lines.append("")

    def section(header, items):
        lines.append(f"## {header}")
        lines.append("")
        if not items:
            lines.append("_None_")
            lines.append("")
            return
        for item in sorted(items, key=lambda x: x["id"]):
            summary = item.get("summary", "").strip()
            lines.append(f"- **{item['id']}** — {summary}")
        lines.append("")

    issue_groups = group_by_status(issues)
    task_groups = group_by_status(tasks)

    all_statuses = [s for s in STATUS_ORDER if s in issue_groups or s in task_groups]
    unexpected = sorted(
        set(issue_groups.keys()) | set(task_groups.keys()) - set(STATUS_ORDER)
    )
    all_statuses.extend(unexpected)

    for status in all_statuses:
        section(f"Issues — {status}", issue_groups.get(status, []))
        section(f"Tasks — {status}", task_groups.get(status, []))

    # Append minutes if present
    if minutes:
        lines.append("---")
        lines.append("")
        today = datetime.now().strftime("%Y-%m-%d")
        lines.append(f"## Standup Minutes ({today})")
        lines.append("")
        for u in minutes.get("updates", []):
            lines.append(
                f"- {u['entity']} {u['id']} → {u['status']} — {u['reason']} (by {u['actor']})"
            )
        lines.append("")

    return "\n".join(lines)

def main():
    issues = load_jsonl(DATA_DIR / "issues.jsonl")
    tasks = load_jsonl(DATA_DIR / "tasks.jsonl")
    minutes = load_today_minutes()

    KANBAN_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    snapshot_path = HISTORY_DIR / f"{today}.md"
    current_path = KANBAN_DIR / "current.md"

    md = render_markdown("Sprint Kanban", issues, tasks, minutes)

    with open(current_path, "w") as f:
        f.write(md)
    with open(snapshot_path, "w") as f:
        f.write(md)

    print(f"Kanban generated:")
    print(f"- Current:   {current_path}")
    print(f"- Snapshot:  {snapshot_path}")

if __name__ == "__main__":
    main()
