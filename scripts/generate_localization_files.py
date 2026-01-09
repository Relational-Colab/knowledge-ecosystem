import yaml
from pathlib import Path

# Paths
BATCH_FILE = Path("data/batch-aiml.yaml")
EN_DIR = Path("i18n/en/aiml")
ZH_DIR = Path("i18n/zh/aiml")

def load_batch_file():
    """Load the batch YAML file containing all AIML terms."""
    with open(BATCH_FILE, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def write_yaml(path, content):
    """Write a YAML file with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(
            content,
            f,
            allow_unicode=True,
            sort_keys=False,
            width=1000
        )

def build_localization_content(entry, lang):
    """Construct the canonical localization file structure."""
    return {
        "term": entry[lang]["term"],
        "definition": entry[lang]["definition"],
        "pronunciation": entry[lang]["pronunciation"],
        "topic": entry["topic"],
        "tags": entry["tags"],
    }

def validate_entry(entry):
    """Ensure the batch entry contains all required fields."""
    required_fields = ["id", "en", "zh", "topic", "tags"]
    for field in required_fields:
        if field not in entry:
            raise ValueError(f"Missing required field: {field}")

    for lang in ["en", "zh"]:
        for subfield in ["term", "definition", "pronunciation"]:
            if subfield not in entry[lang]:
                raise ValueError(
                    f"Missing {lang}.{subfield} in id={entry['id']}"
                )

def generate_localization_files():
    """Generate EN + ZH localization files for each AIML term."""
    entries = load_batch_file()

    for entry in entries:
        validate_entry(entry)

        id_value = entry["id"]

        # English file
        en_content = build_localization_content(entry, "en")
        en_path = EN_DIR / f"{id_value}.yaml"
        write_yaml(en_path, en_content)

        # Chinese file
        zh_content = build_localization_content(entry, "zh")
        zh_path = ZH_DIR / f"{id_value}.yaml"
        write_yaml(zh_path, zh_content)

        print(f"Generated: {en_path} and {zh_path}")

if __name__ == "__main__":
    generate_localization_files()
    print("\nAll localization files generated successfully.")
