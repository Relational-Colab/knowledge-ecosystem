import yaml
from pathlib import Path

BATCH_FILE = Path("data/batch-aiml.yaml")
OUTPUT_FILE = Path("lookup/aiml-index.yaml")

def load_batch_file():
    with open(BATCH_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def build_index_entry(entry):
    return {
        "id": entry["id"],
        "en_term": entry["en"]["term"],
        "zh_term": entry["zh"]["term"],
        "topic": entry["topic"],
        "tags": entry["tags"],
        "paths": {
            "en": f"i18n/en/aiml/{entry['id']}.yaml",
            "zh": f"i18n/zh/aiml/{entry['id']}.yaml",
        },
    }

def generate_lookup_index():
    entries = load_batch_file()
    index = [build_index_entry(e) for e in entries]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        yaml.dump(
            index,
            f,
            allow_unicode=True,
            sort_keys=False,
            width=1000
        )

    print(f"Lookup index written to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_lookup_index()
