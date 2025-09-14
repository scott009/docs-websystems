<!-- InquiryCircle2 – ProjectSpec – Stage2 – 9/4/2025 at 11:25 AM ET -->

# Project Specification

## Part 1: Constraints & Governance

### Project Overview
**InquiryCircle**: A collaborative video conferencing platform for inquiry-based learning groups with role-based access control, facilitator messaging, and key-based authentication.

### Core Constraints

#### Constraint: Scope Integrity (Principle of Minimal Change)
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

### Project-Specific Constraints

#### Authentication Constraint
- All user access must be through key-based authentication
- No traditional username/password authentication to be implemented
- Keys determine both access rights and role (facilitator vs participant)

#### External Service Constraint (Stage 2)
- Jitsi Meet integration uses external Jitsi service only
- Self-hosted Jitsi is Stage 3 scope (not covered in current implementation)
- Backend manages room creation/configuration via Jitsi API

#### Data Persistence Constraint
- Stage 2 Phase 1: SQLite file-based persistence
- Stage 2 Phase 2: PostgreSQL container migration
- All data must be persisted on volumes/bind mounts (never in containers)

#### Operational Constraints
- Operate **only in bash** on WSL and VPS (no PowerShell)  
- Keep filesystem locations **as-documented** (WSL `/home/scott/inquirycircle`, VPS `/srv/inquirycircle`)  
- Keep changes **incremental**; verify after each step before proceeding  
- Be **rollback-ready** at every step (retain prior configs and builds)  

## Part 2: Technical Architecture

### Purpose
Deliver a complete **InquiryCircle** web application for collaborative video conferencing with role-based access control, facilitator messaging, and key-based authentication. Built with containerized architecture ensuring dev/prod parity and single public entrypoint.

### Core Application Features
- **Video Conferencing**: Jitsi Meet integration for inquiry group sessions
- **Role-Based Access**: Facilitators vs. participants with different capabilities  
- **Key-Based Authentication**: No traditional user accounts; access via keys
- **Customizable Circles**: Virtual meeting spaces for different groups
- **Facilitator Messaging**: HTML message system for session guidance
- **Session Management**: Circle creation, participant management, session control

### Technical Architecture

#### Core Components
- **Caddy (reverse proxy / static / TLS)** — the only public-facing service; routes traffic, serves built assets, handles HTTPS/TLS
- **Frontend (Vue 3 + Tailwind CSS + Jitsi SDK)** — single-page app with video integration, compiled to static files
- **Backend (Django + Gunicorn)** — REST/API for circles, authentication, messaging, and Jitsi room management
- **Data layer** — **SQLite** file (v1) with path to **PostgreSQL** later

#### How Components Interact
```
Internet → Caddy → ├─ serves SPA (built Vue+Tailwind+Jitsi static assets)
                   └─ proxies /api → Backend (Django/Gunicorn)
                                     ↳ manages circles, auth, messages
                                     ↳ integrates with Jitsi Meet rooms
                                     ↳ reads/writes DB (SQLite → Postgres)
```

### Frontend Implementation (Vue 3 + Tailwind + Jitsi)
- **Build Process**: Vite build → static assets served by Caddy
- **Video Integration**: Jitsi Meet SDK for embedded conferencing (external Jitsi service integration)
- **UI Components**: 
  - Video conference interface with Jitsi embedding
  - Circle management dashboard (facilitator view)
  - Participant interface with message display
  - Key-based login/access forms
- **Routing**: SPA routing with Caddy fallback to `index.html`
- **Styling**: Tailwind CSS (processed via PostCSS) for consistent, utility-first UI

### Backend Implementation (Django)
- **Authentication API**: Key-based access control, role determination
- **Circles API**: Create/manage inquiry circles, participant lists  
- **Messages API**: Facilitator HTML message management and delivery
- **Jitsi Integration**: External Jitsi service integration - room creation, configuration, participant management
- **Session Management**: Circle state, active sessions, participant tracking
- **Private Network**: Only accessible via Caddy proxy on internal Docker network

### Data Architecture
- **Stage 2**: SQLite file persisted on volume/bind mount (working prototype)
- **Stage 3**: PostgreSQL as dedicated container (production-ready persistence)
- **Data Models**: Circles, Keys/Auth, Messages, Sessions, Participant relationships

### Container Architecture
- **Single-purpose containers**: Frontend runtime, Backend API service, Caddy as gateway
- **Network Isolation**: All services on private Docker network; only Caddy exposed
- **Persistence**: Named volumes for Caddy TLS state, bind mounts for SQLite, static assets
- **Development Parity**: Same container setup WSL ↔ VPS, different ports only

### Environment Strategy
- **WSL Development**: Full topology match with localhost ports (8080, etc.)
- **VPS Production (catbench.com)**: Identical container setup, Caddy handles HTTPS/certificates
- **Configuration**: Environment-specific compose files, shared Caddyfile patterns

### Security Model
- **Single Public Entrypoint**: Only Caddy exposed; all services behind reverse proxy
- **Key-Based Access**: No username/password; access controlled via secure keys
- **Role Enforcement**: Backend validates facilitator vs. participant permissions
- **TLS Termination**: Caddy handles all HTTPS/certificate management
- **Network Isolation**: Backend and data layer on private container network

### Scalability Path
- **Phase 1**: SQLite + single backend container
- **Phase 2**: PostgreSQL container + potential backend scaling
- **Phase 3**: Horizontal scaling with load balancing (if needed)
- **Jitsi**: External service integration only (self-hosted Jitsi planned for Stage 3, not covered here)

## Part 3: Documentation Standards

### Project & Document Nomenclature

This system defines simple, human-friendly labels for projects, subprojects, and their documentation lifecycle. It is designed to be durable across sessions and avoids the complexity of version control systems like Git.

### Project / Subproject Naming
- **Project:** InquiryCircle (base project name)
- **Subprojects:** Add suffix to indicate scope:
  - `InquiryCircle:frontend` - Vue/Jitsi UI development
  - `InquiryCircle:backend` - Django API development  
  - `InquiryCircle:deploy` - Production deployment
  - `InquiryCircle:postgres-migration` - Database migration

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

### Document Types
The following document types are used in this project (all markdown files):

- **README.md** - Project overview, setup instructions, and getting started guide
- **ProjectSpec.md** - Architecture, constraints, governance rules, and documentation standards
- **OperationsGuide.md** - Development workflow, deployment procedures, and troubleshooting
- **Infrastructure.md** - System environments, network architecture, and resource allocation
- **STATUS.md** (optional) - Current progress tracker and next tasks

---

## Guiding Principles
- **Container Single-Purpose**: Frontend build artifacts, Backend API service, Caddy gateway — separate concerns
- **Configuration as Code**: All setup in version-controlled compose files and configs
- **Environment Parity**: Identical development and production container topology
- **Security First**: Private networks, minimal exposure, TLS everywhere
- **Operational Simplicity**: Standard Docker patterns, clear logging, easy rollback