
<!-- InquiryCircle2 – ProjectSpec – Stage2 – 9/12/2025 at 8:15 AM ET -->

# Project Specification

## Purpose
Define what InquiryCircle is intended to deliver in Stage 2, the architecture it rests on, and the constraints that shape development. This document sets the *what* and the *rules of the game* — not the step-by-step *how* (that lives in OperationsGuide.md) and not the evolving goals/minor versions (that live in Status.md).

---

## Stage 2 Definition
Deliver a working full-stack InquiryCircle system:  
- **Frontend**: Vue 3 + Tailwind SPA with Jitsi integration.  
- **Backend**: Django + DRF with key-based authentication and SQLite persistence.  
- **Gateway**: Caddy as the single entrypoint, serving static files and proxying `/api` requests.  
- **Containers**: Docker Compose for dev/prod parity (WSL ↔ VPS).  
- **Outcome**: Integrated, tested, and deployed on the VPS with rollback and monitoring in place.  
- **Deferred**: Self-hosted Jitsi, PostgreSQL migration, advanced analytics, and multi-tenant support.~~~~

---

## Stage 2 Scope Test
A feature belongs in Stage 2 if it can be built with the Vue frontend, Django backend, and external Jitsi SDK, persists data in SQLite, and is served through Caddy/Compose **without introducing new infrastructure or authentication models**.

---

## Constraints (Strategic “musts”)
- **Authentication**: All user access via keys (no usernames/passwords).  
- **Roles**: Keys determine facilitator vs participant.  
- **Networking**: Caddy is the only public surface; backend is internal-only.  
- **Video**: External Jitsi service only (self-hosting is later).  
- **Data**: Persistence through volumes/bind mounts; no data stored in containers.  
- **Environments**: WSL path `/home/scott/inquirycircle`, VPS path `/srv/inquirycircle`.  
- **Repositories**: GitHub `scott009/InquiryCircle` (main), `scott009/InquiryCircle-legacy` (history).

---

## Technical Architecture

### Core Components
- **Caddy**: Reverse proxy, TLS termination, static file server.  
- **Frontend (Vue 3 + Tailwind + Jitsi SDK)**: SPA with video, messaging, circle management.  
- **Backend (Django + DRF + Gunicorn)**: REST APIs for circles, messages, authentication, and Jitsi config.  
- **Data Layer**: SQLite file (Stage 2 baseline).

### How Components Interact
Internet → Caddy
├─ serves SPA (Vue + Tailwind + Jitsi build)
└─ proxies /api/* → Backend (Django/Gunicorn)
↳ manages circles, auth, messaging
↳ integrates with external Jitsi
↳ persists data in SQLite


## Documentation Standards

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
<!-- InquiryCircle2 – ProjectSpec – Stage2 – 9/1/2025 at 11:45 AM ET (superseded) -->

## Guiding Principles
- **Container Single-Purpose**: Separate frontend, backend, and gateway.  
- **Configuration as Code**: Compose files and configs are version-controlled.  
- **Environment Parity**: Dev and prod share the same topology.  
- **Security First**: Private networks, TLS everywhere, key-based access.  
- **Operational Simplicity**: Standard Docker patterns, clear logging, easy rollback.