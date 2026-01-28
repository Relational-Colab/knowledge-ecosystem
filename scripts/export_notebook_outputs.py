#!/usr/bin/env python3
import nbformat
import base64
import json
from pathlib import Path

def export_notebook_outputs(notebook_path, output_dir):
    nb = nbformat.read(notebook_path, as_version=4)

    output_dir = Path(output_dir)
    fig_dir = output_dir / "figures"
    table_dir = output_dir / "tables"
    text_dir = output_dir / "text"

    fig_dir.mkdir(parents=True, exist_ok=True)
    table_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)

    index_entries = []

    fig_count = 1
    table_count = 1
    text_count = 1

    for cell in nb.cells:
        if "outputs" not in cell:
            continue

        for output in cell["outputs"]:
            # PNG figures
            if output.get("data", {}).get("image/png"):
                png_data = base64.b64decode(output["data"]["image/png"])
                fname = f"fig-{fig_count:02d}.png"
                fpath = fig_dir / fname
                fpath.write_bytes(png_data)
                index_entries.append(f"- **Figure {fig_count}** → `figures/{fname}`")
                fig_count += 1

            # JSON tables
            if output.get("data", {}).get("application/json"):
                json_data = output["data"]["application/json"]
                fname = f"table-{table_count:02d}.json"
                fpath = table_dir / fname
                with fpath.open("w") as f:
                    json.dump(json_data, f, indent=2)
                index_entries.append(f"- **Table {table_count}** → `tables/{fname}`")
                table_count += 1

            # Text outputs
            if output.get("text"):
                text_data = output["text"]
                fname = f"text-{text_count:02d}.txt"
                fpath = text_dir / fname
                fpath.write_text(text_data)
                index_entries.append(f"- **Text {text_count}** → `text/{fname}`")
                text_count += 1

    # Write index file
    index_path = output_dir / "sprint-03-index.md"
    with index_path.open("w") as f:
        f.write("# Sprint 03 — Exported Notebook Artifacts\n\n")
        f.write("\n".join(index_entries))

    print(f"Export complete. Artifacts written to {output_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Export notebook cell outputs.")
    parser.add_argument("notebook", help="Path to the notebook file")
    parser.add_argument("output_dir", help="Directory to write exported artifacts")

    args = parser.parse_args()
    export_notebook_outputs(args.notebook, args.output_dir)
