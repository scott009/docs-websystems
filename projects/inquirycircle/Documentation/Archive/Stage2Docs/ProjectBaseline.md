<!-- InquiryCircle2 – ProjectBaseline – Stage2 – 9/2/2025 at 11:00 AM ET -->

# Project Baseline Instructions

## Project Overview
**InquiryCircle**: A collaborative video conferencing platform for inquiry-based learning groups with role-based access control, facilitator messaging, and key-based authentication.

## Shared System Context 

### DEV-PC (Windows 10 + WSL Ubuntu 22.04)  
- Purpose: Local development machine
- Usage: Run Linux commands (bash, docker, git) inside WSL
- Access URLs: http://localhost:8080 (Caddy), http://localhost:8000 (Django dev) for testing

### WSL Ubuntu (inside DEV-PC)
- Purpose: Dev / prod-dry-run environment (Docker Engine + Docker Compose)
- Code location: /home/scott/inquirycircle (WSL filesystem)
- Notes: Images built here for local testing are separate from the VPS

### VPS (catbench.com, Ubuntu 22.04)
- Purpose: Production deployment target
- Access: SSH to user@catbench.com is operational
- URL: https://catbench.com (production InquiryCircle application)

## Instruction Document Labeling Standards
### Project & Runbook Nomenclature

This system defines simple, human-friendly labels for projects, subprojects, and their documentation lifecycle.  
It is designed to be durable across sessions and avoids the complexity of version control systems like Git.  

### Project / Subproject Naming
- **Project:** InquiryCircle (base project name)
- **Subprojects:** Add suffix to indicate scope:
  - `InquiryCircle:frontend` - Vue/Jitsi UI development
  - `InquiryCircle:backend` - Django API development  
  - `InquiryCircle:deploy` - Production deployment
  - `InquiryCircle:postgres-migration` - Database migration

### Definitions 
- **Constraints**: Rules that govern our interaction and execution during development
- **Requirements & Assumptions**: Non-negotiable system shape and expectations
- **Milestones**: Checkpoints with explicit acceptance tests

### Document Stage Labels
1. **Notes (N)** → Freeform ideas and early discussion  
2. **Draft (D)** → Structured outline, still changing  
3. **Accepted (A)** → Agreed version to follow
4. **Completed (C)** → Final state after task success  
5. **Archived (AR)** → Past work, preserved for reference but no longer active

### Timestamp Rule
- Every document label must include a **timestamp (date + hour:minute, no seconds)**  
- The **latest timestamp is always authoritative** over earlier versions, regardless of stage label  
- This rule applies consistently across all stages: Notes, Draft, Accepted, Completed  
- A **timezone marker** should be included once at the top of the document for clarity (e.g., `ET`, `PT`, or `UTC`)    

### Additional Conventions  
#### Superseded Mark 
If you keep older versions of the same file, mark them explicitly:
```
<!-- InquiryCircle:backend – Accepted – 9/1/2025 at 11:45 AM ET (superseded) -->
```

### Example Usage
```
# Implement Jitsi integration for inquiry circles
<!-- InquiryCircle:frontend – Accepted – 9/2/2025 at 11:45 AM ET -->
```
When finished:
```
<!-- InquiryCircle:frontend – Completed – 9/2/2025 at 3:15 PM ET -->
```
In this case, the 3:15 PM entry is authoritative over the 11:45 AM entry because it is the later timestamp.

## Constraint: Scope Integrity (Principle of Minimal Change)  
Canonical Name: Minimal Change

**Intent**  
Avoid making changes that are not logically implied by the request itself. A request to change *X* does not authorize changes to *Y/Z* unless they are strictly necessary to achieve the stated outcome for *X*.

**Rule**  
- Treat the request's **explicit scope** as the only mutable surface  
- Everything else is **frozen by default** (content, look/feel, APIs, schemas, configs, performance characteristics, schedules, etc.)
- "Strictly necessary" test: *Could the requested outcome be achieved without altering area Y?*  
  - **Yes →** Y remains frozen  
  - **No →** propose an unfreeze (see below) before changing Y

**Advisory (allowed without changing anything)**  
- Provide an **Impact Advisory** listing potential side effects or related areas that might merit changes  
- Offer **optional follow-up tasks** (clearly labeled "OPTIONAL") but **do not** implement them

**Unfreeze Protocol (explicit approval required)**  
- To modify anything outside the stated scope, obtain an explicit line of approval:  
  - `ACK UNFREEZE <area>: <narrow scope / reason>`  
- Without this line, frozen areas must remain unchanged

**Verification**  
- Capture **before/after** evidence for the changed area(s)  
- Confirm **no deltas** for frozen surfaces (e.g., outputs, content, UI structure, API payloads, configs) beyond the authorized scope

**Commit/PR Hygiene**  
- Title: `chore(scope): <what changed> (no unrelated changes)`  
- Include a checklist:  
  - [ ] Changes confined to stated scope  
  - [ ] Impact Advisory provided  
  - [ ] No frozen-surface deltas  
  - [ ] (If applicable) `ACK UNFREEZE …` present

**Escalation**  
- If a compliance/security issue *forces* broader changes, **block and escalate** with a note:  
  - `ESCALATE: scope conflict — <summary>`

## Project-Specific Constraints

### Authentication Constraint
- All user access must be through key-based authentication
- No traditional username/password authentication to be implemented
- Keys determine both access rights and role (facilitator vs participant)

### External Service Constraint (Stage 2)
- Jitsi Meet integration uses external Jitsi service only
- Self-hosted Jitsi is Stage 3 scope (not covered in current implementation)
- Backend manages room creation/configuration via Jitsi API

### Data Persistence Constraint
- Stage 2 Phase 1: SQLite file-based persistence
- Stage 2 Phase 2: PostgreSQL container migration
- All data must be persisted on volumes/bind mounts (never in containers)