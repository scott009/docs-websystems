<!-- {{PROJECT_NAME}} – ProjectSpec – Stage1 – {{TIMESTAMP}} -->

# Project Specification

## Purpose
Define what {{PROJECT_NAME}} is intended to deliver, the architecture it rests on, and the constraints that shape development. This document sets the *what* and the *rules of the game* — not the step-by-step *how* (that lives in operations-guide.md) and not the evolving goals/minor versions (that live in current-status.md).

---

## Project Definition
[Describe your project's core purpose and deliverables]

### Stage 1 (Planning)
- **Frontend**: [Define your frontend framework choice]
- **Backend**: [Define your backend framework choice]
- **Gateway**: [Define your reverse proxy/gateway solution]
- **Containers**: [Define your containerization approach]
- **Outcome**: [Define your minimal viable system goals]

### Stage 2 (Future Enhancement)
- [Define your next major feature additions]
- **Micro-versions**:
  - 2.1: [First enhancement]
  - 2.x: [Additional enhancements]

### Stage X (Deferred)
- [List features deferred to later stages]

---

## Scope Test
A feature belongs in the current stage if it can be built with your chosen technology stack and deployment approach **without introducing new infrastructure or authentication models**.

---

## Constraints (Strategic "musts")
- **Authentication**: [Define your authentication approach]
- **Roles**: [Define your user role system]
- **Networking**: [Define your networking constraints]
- **External Services**: [Define external service dependencies]
- **Data**: [Define data persistence requirements]
- **Environments**: [Define your development and production paths]
- **Repositories**: [Define your git repository structure]

---

## Technical Architecture

### Core Components
- **Gateway**: [Your reverse proxy solution]
- **Frontend**: [Your frontend stack]
- **Backend**: [Your backend stack]
- **Data Layer**: [Your database solution]

### How Components Interact
```
Internet → Gateway
├─ serves Frontend (SPA build)
└─ proxies /api/* → Backend
   ↳ manages [core functions]
   ↳ integrates with [external services]
   ↳ persists data in [database]
```

## Documentation Standards

### Version Strategy
- **Major versions** (1.1, 1.2, 1.3): Significant feature additions or architectural changes
- **Micro versions** (1.2.1, 1.2.2): Incremental enhancements within same feature set
- **Git workflow**: Micro versions committed frequently on development, major versions tagged for deployment
- **Deployment cadence**: Multiple development commits per deployment stage, optional tagging for micro versions

### Document Stage Labels
1. **Notes (N)** – Freeform ideas and early discussion  
2. **Draft (D)** – Structured outline, still changing  
3. **Accepted (A)** – Agreed version to follow  
4. **Completed (C)** – Final state after task success  
5. **Archived (AR)** – Preserved for reference, no longer active  

### Timestamp Rule
Every doc includes a **timestamp (date + hour:minute, TZ)** at the top.  
The **latest timestamp is always authoritative**, regardless of stage label.  

### Superseded Mark
Older versions must be marked explicitly, e.g.:  
<!-- {{PROJECT_NAME}} – ProjectSpec – Stage1 – 9/1/2025 at 11:45 AM ET (superseded) -->

## Guiding Principles
- **Container Single-Purpose**: Separate frontend, backend, and gateway.  
- **Configuration as Code**: Compose files and configs are version-controlled.  
- **Environment Parity**: Dev and prod share the same topology.  
- **Security First**: Private networks, TLS everywhere, secure access.  
- **Operational Simplicity**: Standard patterns, clear logging, easy rollback.

---

**Related Documentation**:  
[operations-guide](./operations-guide.md) | [infrastructure](./infrastructure.md) | [README](./README.md) | [changelog](./changelog.md)

**Document Version**: v1.0.0 | **Last Updated**: {{DATE}} | **Status**: ✅ Template