
<!-- InquiryCircle2 – ProjectSpec – Stage2 – 9/19/2025 at 2:15 PM ET -->

# Project Specification

## Purpose
Define what InquiryCircle is intended to deliver in Stage 2, the architecture it rests on, and the constraints that shape development. This document sets the *what* and the *rules of the game* — not the step-by-step *how* (that lives in OperationsGuide.md) and not the evolving goals/minor versions (that live in Status.md).

---

## Stage 2 Definition
Deliver a working full-stack InquiryCircle system with progressive feature enhancements:

### Stage 2.1 (✅ Complete)
- **Frontend**: Vue 3 + Tailwind SPA with Jitsi integration
- **Backend**: Django + DRF with key-based authentication and SQLite persistence
- **Gateway**: Caddy as the single entrypoint, serving static files and proxying `/api` requests
- **Containers**: Docker Compose for dev/prod parity (WSL ↔ VPS)
- **Outcome**: Minimal viable system deployed and operational on VPS

### Stage 2.2 (🔄 Planning)
- **PDF Viewer Component**: Scrolling document panel alongside video interface
- **Multi-User PDF Display**: Same document visible to facilitator and participants
- **Independent Navigation**: Each user can scroll through PDF independently
- **Panel Integration**: Non-overlay layout preserving video functionality
- **Micro-versions**:
  - 2.2.1: Multiple PDF files with facilitator selection
  - 2.2.x: Additional document enhancements

### Stage 2.x Deferred
- Self-hosted Jitsi, PostgreSQL migration, advanced analytics, multi-tenant support

---

## Stage 2 Scope Test
A feature belongs in Stage 2 if it can be built with the Vue frontend, Django backend, and external Jitsi SDK, persists data in SQLite, and is served through Caddy/Compose **without introducing new infrastructure or authentication models**.

### Stage 2.2 Scope Validation
The PDF viewer feature meets Stage 2 criteria:
- ✅ **Frontend**: Vue component for PDF display using existing libraries
- ✅ **Backend**: Django static file serving or simple PDF API endpoints
- ✅ **No new infrastructure**: Uses existing Caddy/Docker setup
- ✅ **No new authentication**: Leverages existing key-based access
- ✅ **Progressive enhancement**: Builds on Stage 2.1 foundation

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

---

## Display Component Architecture

### Architectural Model
InquiryCircle uses a **hierarchical component composition** where routes present user experiences through composable display elements.

**Three-Layer Structure**:
- **Route Level**: URL paths that define user experiences (`/test-jitsi`, `/facilitator-dashboard`)
- **Display Component Level**: Vue components that orchestrate multiple display elements
- **Display Element Level**: Individual content panels that can be reused across displays

### Display Elements (Composable)
**Core Elements**:
- **htmlwin1**: Primary HTML document panel
- **htmlwin2**: Secondary HTML document panel
- **pdfviewer**: PDF document panel (legacy, being phased out in Stage 2.2.2)
- **jitsi-video**: Video conferencing interface
- **facilitator-controls**: Administrative interface elements
- **participant-chat**: Messaging and communication panels

### Display Element Capabilities (Optional)
Each display element may support different capabilities as needed:

**Content Sources**:
- Static HTML files served through Caddy
- Vue template rendering with dynamic data
- API-driven content from Django backend
- External service integration

**Navigation Methods**:
- Independent scroll state per user
- Synchronized navigation across participants
- Section jumping and bookmarks
- Facilitator-controlled content selection

**Layout Behaviors**:
- Fixed positioning within display component
- Resizable panels with saved preferences
- Show/hide state management
- Responsive breakpoint handling

**User Permissions**:
- Facilitator-only controls (content selection, navigation sync)
- Participant access levels (view-only, limited interaction)
- Role-based feature availability

### Composition Patterns
**Current Implementations**:
- **test-jitsi route**: Composes `jitsi-video` + `htmlwin1` + `htmlwin2`
- **Future routes**: May use different combinations of available elements

**Composition Rules**:
- Display elements maintain independent state unless explicitly synchronized
- Each route defines which elements are included and how they're arranged
- Elements can be reused across different route/display combinations
- New routes can be created by composing existing elements in new ways

### Implementation Strategy
**Stage 2.2.2 Focus**:
- Replace `pdfviewer` with enhanced `htmlwin1`/`htmlwin2` implementation
- Add local stylesheet support to HTML display elements
- Maintain existing composition patterns while improving individual element capabilities

**Future Enhancement Path**:
- Add new display elements without changing existing routes
- Create new route experiences by composing elements differently
- Enhance individual element capabilities (static → dynamic content)
- Maintain backward compatibility through capability-based design

---

## Documentation Standards

### Version Strategy
- **Major versions** (2.1, 2.2, 2.3): Significant feature additions or architectural changes
- **Micro versions** (2.2.1, 2.2.2): Incremental enhancements within same feature set
- **Git workflow**: Micro versions committed frequently on WSL, major versions tagged for deployment
- **Deployment cadence**: Multiple WSL commits per deployment stage, optional tagging for micro versions

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

---

**Related Documentation**:  
[operations-guide](./operations-guide.md) | [infrastructure](./infrastructure.md) | [README](./README.md) | [CHANGELOG](./CHANGELOG.md)

**Document Version**: v2.2.0 | **Last Updated**: 9/19/2025 | **Status**: ✅ Current