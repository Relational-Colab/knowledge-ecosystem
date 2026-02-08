# === Tab Sentinel ===
sentinel:
	@echo "Tab indentation is working."

# === Paths and configuration ===
PYTHON := python3

REGISTRY := frameworks/schema_registry.json
VALIDATOR := scripts/jsonl_to_parquet.py

SCRIPTS_DIR := scripts
KANBAN_SCRIPT := $(SCRIPTS_DIR)/generate_kanban.py
UPDATE_SCRIPT := $(SCRIPTS_DIR)/update_status.py
TIMESERIES_SCRIPT := $(SCRIPTS_DIR)/build_timeseries.py

# Sprint ID stored in repo root as .sprint
SPRINT_FILE := .sprint
SPRINT_ID := $(shell cat $(SPRINT_FILE) 2>/dev/null || echo "sprint-04")



# === Phony targets ===
.PHONY: help registry validate kanban standup post-standup sprint metrics timeseries review

# === Help ===
help:
	@echo ""
	@echo "Available targets:"
	@echo "  help			Show this help message"
	@echo "  registry		Validate the schema registry JSON"
	@echo "  validate		Run JSONL validator (no Parquet write)"
	@echo "  kanban			Generate Kanban (current + snapshot) for $(SPRINT_ID)"
	@echo "  standup		Pre-standup: validate + generate Kanban"
	@echo "  post-standup	Post-standup: validate + regenerate Kanban"
	@echo "  sprint			Set the current sprint (usage: make sprint SPRINT_ID=sprint-05)"
	@echo "  metrics		Extract metrics for the current sprint"
	@echo "  timeseries		Build consolidated metrics time-series dataset"
	@echo "  review			Full sprint-review ritual (metrics + timeseries)"
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

# === Batch update ritual ===
update:
	@echo "Opening batch update file..."
	@sh -c "vim ./updates.txt"
	@echo "Applying batch transitions..."
	$(PYTHON) $(UPDATE_SCRIPT) --file updates.txt
	@echo "Regenerating Kanban..."
	$(MAKE) kanban
	@echo "Batch update complete."

# === Generate Kanban ===
kanban:
	@echo "Generating Kanban for $(SPRINT_ID)..."
	@$(PYTHON) $(KANBAN_SCRIPT)

# === Pre-standup ritual ===
standup: validate
	@echo "Generating Kanban for $(SPRINT_ID)..."
	@$(PYTHON) $(KANBAN_SCRIPT)
	@echo "Standup board ready at reports/$(SPRINT_ID)/kanban/current.md"

# === Post-standup ritual ===
post-standup: validate
	@echo "Regenerating Kanban for $(SPRINT_ID)..."
	@$(PYTHON) $(KANBAN_SCRIPT)
	@echo "Post-standup validation and Kanban refresh complete."

# === Set sprint ID ===
sprint:
	@echo "$(SPRINT_ID)" > $(SPRINT_FILE)
	@echo "Sprint set to $(SPRINT_ID)"

# === Metrics extraction (T02) ===
metrics:
	@echo "Extracting metrics for $(SPRINT_ID)..."
	@$(PYTHON) scripts/extract_metrics.py
	@echo "Metrics extraction complete."

# === Time-series consolidation (T03) ===
timeseries:
	@echo "Building consolidated metrics time-series..."
	@$(PYTHON) $(TIMESERIES_SCRIPT)
	@echo "Time-series build complete."

# === Sprint review ritual (T04) ===
review:
	@echo "=== Sprint Review Ceremony Starting ==="
	$(MAKE) metrics sprint=$(SPRINT_ID)
	$(MAKE) timeseries sprint=$(SPRINT_ID)
	@echo "Generating sprint review artifact..."
	$(PYTHON) scripts/generate-review.py $(SPRINT_ID)
	@echo "=== Sprint Review Ceremony Complete ==="

# === Pre-commit ritual (governance checkpoint) ===
.PHONY: pre-commit
pre-commit:
	@echo "=== Pre-Commit Governance Checkpoint ==="
	@echo "1. Validating canonical data..."
	@$(PYTHON) $(VALIDATOR) --validate-only
	@echo "2. Regenerating Kanban for $(SPRINT_ID)..."
	@$(PYTHON) $(KANBAN_SCRIPT)
	@echo "3. Extracting metrics for $(SPRINT_ID)..."
	@$(PYTHON) scripts/extract_metrics.py
	@echo "4. Building consolidated metrics time-series..."
	@$(PYTHON) $(TIMESERIES_SCRIPT)
	@echo "=== Pre-Commit Checkpoint Complete ==="
