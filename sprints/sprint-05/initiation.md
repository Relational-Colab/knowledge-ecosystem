# Sprint 05 Initiation Document
**Era:** Substrate Migration  
**Theme:** Establish the event‑sourced substrate and projection engine  
**Sprint Duration:** 2026‑02‑02 → 2026‑02‑15  
**Status:** Active

---

## 1. Sprint Intent
Sprint 05 marks the beginning of the substrate era.  
The goal is to replace the legacy JSONL substrate with a durable, auditable, event‑sourced foundation that supports tri‑modal retrieval (SQL, graph, vector) and future contributor‑ready workflows.

This sprint focuses on establishing the substrate, validating the projection loop, and migrating one or two workflows end‑to‑end. The objective is architectural stability, not full migration.

---

## 2. Objectives

### 2.1 Event Substrate
- Define event schema (event types, metadata, required fields).  
- Implement append‑only event logging with validation.  
- Introduce event‑level governance rules (immutability, auditability, contributor safety).

### 2.2 Projection Engine
- Implement minimal projection engine capable of:
  - reading the event log  
  - applying projection rules  
  - producing derived state  
- Create projection registry for future workflows.  
- Validate projection determinism and reproducibility.

### 2.3 Workflow Migration (Initial)
- Migrate **standup** workflow to event‑sourced form.  
- Migrate **Kanban** workflow to projection‑based state.  
- Confirm projections produce identical or improved outputs compared to legacy JSONL.

### 2.4 Governance & Documentation
- Document:
  - event schema  
  - projection rules  
  - substrate philosophy  
  - migration rationale  
- Update Makefile targets to operate on the new substrate.  
- Ensure all artifacts are contributor‑ready and auditable.

---

## 3. Stretch Goals
- Introduce embeddings for glossary terms.  
- Begin graph modeling of glossary relationships.  
- Prototype hybrid retrieval (SQL + graph + vector).  
- Explore event‑driven glossary updates.

---

## 4. Constraints
- No premature optimization.  
- No multi‑workflow migration until projection engine is stable.  
- All changes must be teachable, auditable, and contributor‑ready.  
- Maintain backward compatibility until projections are validated.

---

## 5. Definition of Done
- Event substrate exists and is operational.  
- Projection engine produces correct state for at least one workflow.  
- Standup and Kanban operate on projections.  
- Documentation is complete and contributor‑ready.  
- Sprint boundary is tagged and clean.  
- Migration rationale is recorded for future contributors.

---

## 6. Risks & Mitigations
| Risk | Mitigation |
|------|------------|
| Projection engine complexity increases | Start minimal; expand only after validation |
| Schema drift during migration | Lock schema early; document changes rigorously |
| Contributor confusion during transition | Provide clear migration rationale and diagrams |
| Makefile breakage | Incremental updates with validation targets |

---

## 7. Architectural Notes
- Substrate must support future tri‑modal retrieval.  
- Event log is the single source of truth; projections are disposable.  
- All workflows will eventually be migrated to event‑sourced form.  
- This sprint establishes the foundation for Sprints 06–12.

---

## 8. Initial Commit Checklist
- [ ] Create `substrate/events/` directory  
- [ ] Add event schema and validator  
- [ ] Implement append‑only event writer  
- [ ] Create projection engine skeleton  
- [ ] Migrate standup workflow  
- [ ] Migrate Kanban workflow  
- [ ] Update Makefile targets  
- [ ] Add contributor documentation  
- [ ] Validate projections against legacy JSONL  
- [ ] Record migration rationale  
