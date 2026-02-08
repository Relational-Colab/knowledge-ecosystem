# Sprint Initiation Ceremony  
**Canonical Governance Document**

This document defines the official, governance‑aligned procedure for initiating a new sprint in the Knowledge Ecosystem. It ensures that each sprint begins with a clean environment, a clear boundary, initialized telemetry, and a fresh cognitive context.

---

# 1. Purpose

The Sprint Initiation Ceremony:

- establishes a clean operational and cognitive baseline  
- initializes telemetry and measurement systems  
- prepares the development environment  
- creates a clear historical boundary for the new sprint  
- ensures contributor‑ready governance from the first minute  

This ceremony is mandatory for all sprint initiations.

---

# 2. Timing Model

The Sprint Initiation Ceremony begins immediately after the Sprint Closure Ceremony and the cognitive reset.

### T + 0:00 — Begin Sprint Initiation
- The previous sprint is fully sealed  
- The development machine has been rebooted  
- A fresh cognitive context is established  

### T + 0:05 — Initialize the new sprint environment
- Open WSL  
- Navigate to the repo root  
- Launch VSCode  
- Initialize telemetry and measurement systems  

### T + 0:10 — Establish sprint boundary markers
- Create the sprint directory  
- Compose or update `initiation.md`  
- Tag the sprint start in Git  
- Begin the new sprint conversation  

This timing model ensures the sprint begins cleanly and consistently.

---

# 3. Ceremony Steps

The Sprint Initiation Ceremony consists of eight steps.  
All steps must be completed before work begins on the new sprint.

---

## Step 1 — Start with a Clean Machine

To ensure a fresh operational and cognitive environment:

- shut down and restart the development laptop  
- allow all processes and state to reset  
- begin the sprint with a clean mental slate  

This mirrors the cognitive reset at sprint closure.

---

## Step 2 — Open Debian WSL and Navigate to the Repo Root

Open a fresh terminal and anchor yourself in the canonical workspace:

```bash
cd ~/dev/knowledge-ecosystem
```

This ensures all subsequent actions occur in the correct context.

---

## Step 3 — Launch VSCode from the Repo Root

Open the development environment:

```bash
code .
```

This guarantees:

- correct working directory  
- correct relative paths  
- immediate visibility of sprint artifacts  

---

## Step 4 — Initialize Telemetry and Measurement Systems

Prepare all systems that will track sprint activity:

- start MLflow tracking (if used)  
- initialize metrics directories  
- prepare time‑series logs  
- verify experiment tracking is ready  
- ensure measurement begins at the sprint boundary  

This step ensures the sprint begins with measurement readiness.

---

## Step 5 — Create the Sprint Directory

Create the directory for the new sprint:

```bash
mkdir -p sprints/sprint-nn
```

This directory will contain:

- `initiation.md`  
- `retrospective.md`  
- any sprint‑specific artifacts  

This ensures each sprint has a self‑contained governance space.

---

## Step 6 — Compose or Update `initiation.md`

Inside `sprints/sprint-nn/`, create or update:

```
sprints/sprint-nn/initiation.md
```

This document should include:

- sprint number  
- sprint start timestamp  
- sprint goals and scope  
- key risks and assumptions  
- telemetry initialization notes  
- any governance considerations  

This becomes the narrative anchor for the sprint.

---

## Step 7 — Tag the Sprint Start in Git

Create a durable historical boundary:

```bash
git tag sprint-nn-start
git push --tags
```

This tag marks the beginning of the sprint and pairs with the eventual `sprint-nn-close` tag.

---

## Step 8 — Begin the New Sprint Conversation

To maintain cognitive and narrative separation:

- open a new chat thread for the sprint  
- establish the sprint’s narrative arc  
- avoid bleed‑through from the previous sprint  

This ensures the sprint begins with a clean conversational context.

---

# 4. Ceremony Completion Criteria

A sprint is considered initiated when:

- the machine has been rebooted  
- the repo root is open in WSL and VSCode  
- telemetry and measurement systems are initialized  
- the sprint directory exists  
- `initiation.md` is composed or updated  
- the sprint start tag is pushed  
- a new sprint conversation is opened  

Only then is the sprint formally initiated.

---

# 5. Governance Notes

- Initiation mirrors closure: one seals the past, the other prepares the future  
- Telemetry must begin at the sprint boundary to ensure accurate analytics  
- The sprint directory ensures contributor‑ready organization  
- The conversational reset reinforces cognitive hygiene  
- This ceremony scales cleanly to multi‑contributor environments  
