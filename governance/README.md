# Frameworks

The `frameworks/` directory contains the core governance structures that define how the Knowledge Ecosystem operates. These documents establish the conventions, schemas, and lineage rules that guide navigation, cadence, and architectural decision‑making across the project.

Each framework in this directory serves as a durable reference point for contributors, ensuring that the ecosystem remains coherent, auditable, and aligned with its local‑first design principles.

---

## Included Governance Standards

### 1. Commit Standard (`commit_standard.md`)
Defines the governance‑grade commit annotation system used across the repository.  
It establishes:

- semantic commit types  
- WBS‑aligned scopes (Sxx, Sxx.Iyy, Sxx.Iyy.Tzz)  
- short and long description rules  
- cross‑ecosystem lineage conventions (Markdown, scripts, notebooks, MLflow)  

This standard ensures that every commit is traceable, auditable, and aligned with the sprint → issue → task hierarchy.

---

### 2. Schema Standard (`schema_standard.md`)
Documents the formal structure of the three core governance schemas:

- **Sprints**  
- **Issues**  
- **Tasks**

It defines:

- identifier formats  
- field definitions  
- constraints  
- cross‑schema relationships  
- MLflow lineage requirements  

This standard forms the backbone of the local‑first telemetry and analytics architecture.

---

## Purpose of the Frameworks Directory

This directory acts as the **governance substrate** for the entire project.  
It provides:

- a shared vocabulary  
- consistent metadata conventions  
- stable architectural boundaries  
- reproducible lineage across all artifacts  
- a foundation for future sprints and contributors  

As the ecosystem evolves, additional governance frameworks may be added here to support new capabilities, workflows, or architectural patterns.
