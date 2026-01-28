#!/usr/bin/env python3
import argparse
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import sys
import shutil
import mlflow

DATA_DIR = Path("data")
REGISTRY_PATH = Path("frameworks/schema_registry.json")

# Sprint is passed in by Makefile via env or defaults here
SPRINT_ID = Path(sys.argv[0]).parent.parent.joinpath(".sprint").read_text().strip() \
    if Path(".sprint").exists() else "sprint-04"

REPORTS_DIR = Path("reports") / SPRINT_ID
MINUTES_DIR = REPORTS_DIR / "minutes"
TRANSACTIONS_DIR = REPORTS_DIR / "transactions"
MINUTES_DIR.mkdir(parents=True, exist_ok=True)
TRANSACTIONS_DIR.mkdir(parents=True, exist_ok=True)

def load_jsonl(path):
    with open(path, "r") as f:
        return [json.loads(line) for line in f]

def save_jsonl(path, records):
    with open(path, "w") as f:
        for r in records:
            f.write(json.dumps(r, separators=(",", ":")) + "\n")

def load_registry():
    with open(REGISTRY_PATH, "r") as f:
        return json.load(f)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def next_timestamp(last_ts):
    now = datetime.now(timezone.utc)
    if last_ts is None:
        return now.isoformat()
    last = datetime.fromisoformat(last_ts)
    if now <= last:
        return (last.replace(microsecond=last.microsecond + 1)).isoformat()
    return now.isoformat()

def update_status(record, new_status, actor, reason):
    old_status = record["status"]
    last_ts = record["status_history"][-1]["timestamp"] if record.get("status_history") else None
    ts = next_timestamp(last_ts)
    record["status"] = new_status
    record.setdefault("status_history", []).append({
        "status": new_status,
        "timestamp": ts,
        "actor": actor,
        "reason": reason
    })
    return old_status, ts

def parse_line(line):
    parts = line.strip().split(maxsplit=4)
    if len(parts) < 5:
        raise ValueError(f"Invalid line (need 5 fields): {line}")
    entity, rid, status, actor, reason = parts
    if reason.startswith('"') and reason.endswith('"'):
        reason = reason[1:-1]
    return {
        "entity": entity,
        "id": rid,
        "status": status,
        "actor": actor,
        "reason": reason,
    }

def read_batch_from_stdin():
    print("Enter updates (one per line). Format:")
    print("<entity> <id> <status> <actor> \"<reason>\"")
    print("Blank line to finish.\n")
    updates = []
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break
        if not line:
            break
        updates.append(parse_line(line))
    return updates

def read_batch_from_file(path):
    updates = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            updates.append(parse_line(line))
    return updates

def archive_batch_file(path):
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = TRANSACTIONS_DIR / f"{ts}-updates.txt"
    shutil.copy(path, dest)
    return dest

def save_minutes_pending(updates):
    ts = datetime.now(timezone.utc).isoformat()
    pending_path = MINUTES_DIR / "pending.json"
    payload = {
        "captured_at": ts,
        "sprint": SPRINT_ID,
        "updates": updates,
    }
    with open(pending_path, "w") as f:
        json.dump(payload, f, indent=2)
    return pending_path

def finalize_minutes(pending_path):
    if not pending_path.exists():
        return None
    today = datetime.now().strftime("%Y-%m-%d")
    final_path = MINUTES_DIR / f"{today}.json"
    pending_path.replace(final_path)
    return final_path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", action="store_true",
                        help="Force interactive batch mode.")
    parser.add_argument("--file", type=str,
                        help="Path to a batch file containing updates.")
    parser.add_argument("entity", nargs="?", choices=["issue", "task"])
    parser.add_argument("id", nargs="?")
    parser.add_argument("status", nargs="?")
    parser.add_argument("actor", nargs="?")
    parser.add_argument("reason", nargs="?")
    args = parser.parse_args()

    registry = load_registry()
    transitions = registry["workflow"]["allowed_transitions"]

    # Decide mode
    if args.file:
        batch_path = Path(args.file)
        if not batch_path.exists():
            raise SystemExit(f"ERROR: Batch file not found: {args.file}")
        updates = read_batch_from_file(batch_path)
        archived = archive_batch_file(batch_path)
        print(f"Batch file archived to {archived}")

    elif args.entity is None or args.batch:
        updates = read_batch_from_stdin()

    else:
        if args.reason is None:
            raise SystemExit("Need: entity id status actor reason")
        updates = [{
            "entity": args.entity,
            "id": args.id,
            "status": args.status,
            "actor": args.actor,
            "reason": args.reason,
        }]

    if not updates:
        print("No updates provided.")
        return

    pending_path = save_minutes_pending(updates)
    print(f"Standup decisions captured in {pending_path}")

    issues = load_jsonl(DATA_DIR / "issues.jsonl")
    tasks = load_jsonl(DATA_DIR / "tasks.jsonl")
    issue_map = {r["id"]: r for r in issues}
    task_map = {r["id"]: r for r in tasks}

    mlflow.set_experiment("status_updates")
    with mlflow.start_run(run_name=f"{SPRINT_ID}_standup"):
        mlflow.log_param("sprint", SPRINT_ID)
        mlflow.log_param("num_updates", len(updates))

        mlflow.log_param("issues_sha256_before", sha256_file(DATA_DIR / "issues.jsonl"))
        mlflow.log_param("tasks_sha256_before", sha256_file(DATA_DIR / "tasks.jsonl"))

        # Validate all transitions first
        for u in updates:
            rec = issue_map.get(u["id"]) if u["entity"] == "issue" else task_map.get(u["id"])
            if rec is None:
                raise SystemExit(f"ERROR: {u['entity']} '{u['id']}' not found")
            old_status = rec["status"]
            if u["status"] not in transitions.get(old_status, []):
                raise SystemExit(f"ERROR: Illegal transition {old_status} → {u['status']} for {u['id']}")

        # Apply updates
        for u in updates:
            rec = issue_map[u["id"]] if u["entity"] == "issue" else task_map[u["id"]]
            old, ts = update_status(rec, u["status"], u["actor"], u["reason"])
            key = f"{u['entity']}:{u['id']}"
            mlflow.log_param(f"{key}_old_status", old)
            mlflow.log_param(f"{key}_new_status", u["status"])
            mlflow.log_param(f"{key}_timestamp", ts)
            print(f"{key}: {old} → {u['status']} at {ts}")

        save_jsonl(DATA_DIR / "issues.jsonl", list(issue_map.values()))
        save_jsonl(DATA_DIR / "tasks.jsonl", list(task_map.values()))

        mlflow.log_param("issues_sha256_after", sha256_file(DATA_DIR / "issues.jsonl"))
        mlflow.log_param("tasks_sha256_after", sha256_file(DATA_DIR / "tasks.jsonl"))

    final_minutes = finalize_minutes(pending_path)
    if final_minutes:
        print(f"Standup minutes finalized at {final_minutes}")

if __name__ == "__main__":
    main()
