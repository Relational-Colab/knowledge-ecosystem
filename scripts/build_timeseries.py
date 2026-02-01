#!/usr/bin/env python3
"""
build_timeseries.py — Consolidate Metrics into a Time-Series Dataset (T03)

This script scans all sprint metrics directories, loads each metrics JSON file,
extracts scalar and semi-structured fields, flattens them into a tabular format,
and writes a consolidated time-series dataset in both JSONL and Parquet formats.

Outputs (canonical):
    data/metrics_timeseries.jsonl
    data/metrics_timeseries.parquet

This dataset supports:
    - sprint reviews
    - governance analytics
    - dashboards
    - MLflow logging (T04)
    - forecasting and anomaly detection
"""

import json
from pathlib import Path
from datetime import datetime

import pandas as pd


# === Paths ===
REPORTS_DIR = Path("reports")
DATA_DIR = Path("data")

JSONL_OUT = DATA_DIR / "metrics_timeseries.jsonl"
PARQUET_OUT = DATA_DIR / "metrics_timeseries.parquet"


# === Helper Functions ===

def load_metrics_file(path: Path) -> dict:
    """Load a single metrics JSON file."""
    with open(path, "r") as f:
        return json.load(f)


def flatten_metrics(metrics: dict, sprint_id: str) -> dict:
    """
    Flatten a metrics dictionary into a single-level dict suitable for
    time-series storage.

    Structured metrics (dicts) are flattened using key prefixes.
    Lists (e.g., orphan_tasks) are converted to counts.
    """
    flat = {
        "timestamp": metrics.get("timestamp"),
        "sprint_id": sprint_id,
    }

    for key, value in metrics.items():
        if key in ("timestamp",):
            continue

        # Scalar values pass through unchanged
        if isinstance(value, (int, float, str)):
            flat[key] = value

        # Dicts are flattened with prefixes
        elif isinstance(value, dict):
            for subkey, subval in value.items():
                flat[f"{key}__{subkey}"] = subval

        # Lists become counts
        elif isinstance(value, list):
            flat[f"{key}_count"] = len(value)

        # Fallback: store as string
        else:
            flat[key] = str(value)

    return flat


def collect_all_metrics() -> pd.DataFrame:
    """
    Walk through reports/<sprint>/metrics directories and collect all metrics files.
    Returns a pandas DataFrame representing the consolidated time-series.
    """
    rows = []

    for sprint_dir in REPORTS_DIR.iterdir():
        if not sprint_dir.is_dir():
            continue

        sprint_id = sprint_dir.name
        metrics_dir = sprint_dir / "metrics"

        if not metrics_dir.exists():
            continue

        for metrics_file in metrics_dir.glob("metrics-*.json"):
            metrics = load_metrics_file(metrics_file)
            flat = flatten_metrics(metrics, sprint_id)
            rows.append(flat)

    if not rows:
        raise RuntimeError("No metrics files found in reports/*/metrics/")

    return pd.DataFrame(rows)


# === Main Orchestration ===

def main():
    df = collect_all_metrics()

    # Sort chronologically
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    # Ensure data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Write JSONL
    df.to_json(JSONL_OUT, orient="records", lines=True)

    # Write Parquet
    df.to_parquet(PARQUET_OUT, index=False)

    print(f"Time-series written to:\n  {JSONL_OUT}\n  {PARQUET_OUT}")


if __name__ == "__main__":
    main()
