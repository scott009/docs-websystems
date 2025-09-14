
# Project Baseline Instructions

  
## Shared System Context 
  
### DEV-PC (Windows 10 + WSL Ubuntu 22.04)  
- Purpose: Local development machine.
- Usage: Run Linux commands (bash, docker, git) inside WSL.
- Access URLs (local runs): http://localhost:portnum on web brwoser for testing local 

### WSL Ubuntu (inside DEV-PC)
- Purpose: Dev / prod-dry-run environment (Docker Engine + Docker Compose).
- Code location: /home/<you>/ProjectLocation  (WSL filesystem)
- Notes: Images built here for local testing are separate from the VPS.

### VPS (catbench.com, Ubuntu 22.04)
- Purpose: Remote deploy target.
- Access: SSH to user@catbench.com is up and runninng



## Instruction Document Labeling Standards
###  Project & Runbook Nomenclature

This system defines simple, human-friendly labels for projects, subprojects, and their documentation lifecycle.  
It is designed to be durable across sessions and avoids the complexity of version control systems like Git.  


### Project / Subproject Naming
- **Project:** Use a short base name (e.g., `VotingApp`, `InquiryCircle`, `DockerIC`).  
- **Subproject:** Add a suffix to indicate scope (e.g., `VotingApp:catbench-deploy`, `DockerIC:learn-docker`).  

### Definitions 
- **Constraints**: Rules that govern our interaction and execution during development.
- **Requirements & Assumptions**: Non-negotiable system shape and expectations.
- **Milestones**: Checkpoints with explicit acceptance tests.

### Document Stage Labels
    1. **Notes** → Freeform ideas and early discussion.  
    2. **Draft** → Structured outline, still changing.  
    3. **Runbook** → Step-by-step instructions for execution.  
    4. **Accepted Runbook** → Agreed “one true version” to follow.  
    5. **Completed** → Final state after project/subproject success.  
    6. **Archived** → Past work, preserved for reference but no longer active.


### Timestamp Rule
    - Every document label must include a **timestamp (date + hour:minute, no seconds)**.  
    - The **latest timestamp is always authoritative** over earlier versions, regardless of stage label.  
    - This rule applies consistently across all stages: Notes, Draft, Runbook, Accepted Runbook, Completed.  
    - A **timezone marker** should be included once at the top of the document   
      for clarity in collaborations (e.g., `ET`, `PT`, or `UTC`).    
      
### Additional Conventions  
#### Superseded Mark 
    If you keep older versions of the same file, mark them explicitly:
        <!-- VotingApp:catbench-deploy – Accepted Runbook – 8/22/2025 at 11:45 AM ET (superseded) -->  

### Accepted Abreviations
    N = Notes
    D = Draft
    R = Runbook
    AR = Accepted Runbook
    C = Completed

### Example Usage
    # make a minor change to the voting app and redeploy
    <!-- VotingApp:catbench-deploy – Accepted Runbook – 8/22/2025 at 11:45 AM ET -->
When finished:
        <!-- VotingApp:catbench-deploy – Completed – 8/22/2025 at 3:15 PM ET -->
        In this case, the 3:15 PM entry is authoritative over the 11:45 AM entry because it is the later timestamp.


## Constraint: Scope Integrity (Principle of Minimal Change)  
  Canonical Name: Minimal Change

**Intent**  
Avoid making changes that are not logically implied by the request itself. A request to change *X* does not authorize changes to *Y/Z* unless they are strictly necessary to achieve the stated outcome for *X*.

**Rule**  
- Treat the request’s **explicit scope** as the only mutable surface.  
- Everything else is **frozen by default** (content, look/feel, APIs, schemas, configs, performance characteristics, schedules, etc.).
- “Strictly necessary” test: *Could the requested outcome be achieved without altering area Y?*  
  - **Yes →** Y remains frozen.  
  - **No →** propose an unfreeze (see below) before changing Y.

**Advisory (allowed without changing anything)**  
- Provide an **Impact Advisory** listing potential side effects or related areas that might merit changes.  
- Offer **optional follow-up tasks** (clearly labeled “OPTIONAL”) but **do not** implement them.

**Unfreeze Protocol (explicit approval required)**  
- To modify anything outside the stated scope, obtain an explicit line of approval:  
  - `ACK UNFREEZE <area>: <narrow scope / reason>`  
- Without this line, frozen areas must remain unchanged.

**Verification**  
- Capture **before/after** evidence for the changed area(s).  
- Confirm **no deltas** for frozen surfaces (e.g., outputs, content, UI structure, API payloads, configs) beyond the authorized scope.

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


