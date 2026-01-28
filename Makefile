# === Paths and configuration ===
PYTHON := python3

REGISTRY := frameworks/schema_registry.json
VALIDATOR := scripts/jsonl_to_parquet.py

SCRIPTS_DIR := scripts
KANBAN_SCRIPT := $(SCRIPTS_DIR)/generate_kanban.py
UPDATE_SCRIPT := $(SCRIPTS_DIR)/update_status.py

# Sprint ID stored in repo root as .sprint
SPRINT_FILE := .sprint
SPRINT_ID := $(shell cat $(SPRINT_FILE) 2>/dev/null || echo "sprint-04")

# === Phony targets ===
.PHONY: help registry validate kanban standup post-standup sprint

# === Help ===
help:
	@echo ""
	@echo "Available targets:"
	@echo "  help            Show this help message"
	@echo "  registry        Validate the schema registry JSON"
	@echo "  validate        Run JSONL validator (no Parquet write)"
	@echo "  kanban          Generate Kanban (current + snapshot) for $(SPRINT_ID)"
	@echo "  standup         Pre-standup: validate + generate Kanban"
	@echo "  post-standup    Post-standup: validate + regenerate Kanban"
	@echo "  sprint          Set the current sprint (usage: make sprint SPRINT_ID=sprint-05)"
	@echo ""
	@echo "Current sprint: $(SPRINT_ID)"
	@echo ""

# === Existing: validate schema registry ===
registry:
	@echo "Validating schema registry..."
	@$(PYTHON) -c "import json; json.load(open('$(REGISTRY)')); print('Schema registry OK.')"

# === Existing: run JSONL validator ===
validate:
	@echo "Running validator..."
	@$(PYTHON) $(VALIDATOR) --validate-only

# === New: generate Kanban ===
kanban:
	@echo "Generating Kanban for $(SPRINT_ID)..."
	@$(PYTHON) $(KANBAN_SCRIPT)

# === New: pre-standup ritual ===
standup: validate
	@echo "Generating Kanban for $(SPRINT_ID)..."
	@$(PYTHON) $(KANBAN_SCRIPT)
	@echo "Standup board ready at reports/$(SPRINT_ID)/kanban/current.md"

# === New: post-standup ritual ===
post-standup: validate
	@echo "Regenerating Kanban for $(SPRINT_ID)..."
	@$(PYTHON) $(KANBAN_SCRIPT)
	@echo "Post-standup validation and Kanban refresh complete."

# === New: set sprint ID ===
sprint:
	@echo "$(SPRINT_ID)" > $(SPRINT_FILE)
	@echo "Sprint set to $(
