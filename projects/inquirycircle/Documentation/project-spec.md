
<!-- InquiryCircle2 – ProjectSpec – Stage2 – 10/4/2025 at 3:30 PM ET -->

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

### Stage 2.2 (✅ Complete)
- **PDF Viewer Component**: Scrolling document panel alongside video interface
- **Multi-User PDF Display**: Same document visible to facilitator and participants
- **Independent Navigation**: Each user can scroll through PDF independently
- **Panel Integration**: Non-overlay layout preserving video functionality
- **Micro-versions**:
  - 2.2.1: Multiple PDF files with facilitator selection
  - 2.2.2: HTML Window Components architecture

### Stage 2.3 (✅ Complete)
- **Route Restructure**: New route organization for meeting and administration
  - `/meeting`: Standard participant meeting interface
  - `/facmeet`: Facilitator meeting interface with enhanced controls
  - `/administration`: Circle and facilitator management
  - `/tests`: System health checks and component testing
  - `/facpanel`: Facilitator control panel
- **TopBar Component**: Global navigation with NavMenu1 and StatusBar1
- **Simplified Jitsi**: Direct public Jitsi embed (development configuration)
- **Reaction Bars**: Interactive reaction system for participants and facilitators

### Stage 2.3.4 (✅ Complete)
- **DescBar1 Component**: Element description display system
  - Positioned below reaction bars, always visible
  - Displays element label, ID, and functional description
  - Interactive: Updates on click of included UI elements
  - Covers 30 interactive elements (reactions, options, labels)
  - Visual styling: Light buff background, black border
  - Height matches reaction bar, approximately 1/3 screen width
  - JSON-based element descriptions in `/frontend/public/data/element-descriptions.json`
  - Development/exploration tool for system examination

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

**Architecture Verified from /meeting Route Analysis**:

The InquiryCircle meeting interface demonstrates a hierarchical composition where visual elements map directly to both frontend components and backend domain logic. The `/meeting` route provides the canonical example of display element integration.

**Element Mapping Table**:
| Label | ID | Parent | Class | File |
|-------|----|---------|---------|----|
| topbar | topbar1 | NA | NA | NA |
| reactionbar | reaction1 | NA | NA | NA |
| reactionbar2 | reaction2 | NA | NA | NA |
| DescriptionBar | descbar1 | NA | DescBar1.vue | DescBar1.vue |
| Navigation Menu | navmenu1 | topbar1 | NA | NA |
| StatusBar | statbar1 | topbar1 | NA | NA |
| User Name | username | statbar1 | NA | NA |
| User Role | userrole | statbar1 | NA | NA |
| CircleName | circname | statbar1 | NA | NA |
| Logout/login | logout1 | navmenu1 | NA | NA |
| participant 2 | part2 | jitsiwin1 | NA | NA |
| participant's perspective | partpersp | jitsiwin1 | NA | NA |
| Speaker | speaker1 | jitsiwin1 | NA | NA |
| participant1 | part1 | jitsiwin1 | NA | NA |
| participant 3 | part3 | jitsiwin1 | NA | NA |
| Facilitator | facil1 | jitsiwin1 | NA | NA |
| jitsiwin1 | jitsi1 | mainarea | NA | NA |
| ContentPanel1 | content1 | mainarea | NA | NA |
| Like | like1 | reaction1 | LikeReaction | reactions.py |
| Love | love1 | reaction1 | LoveReaction | reactions.py |
| Dislike | dislike1 | reaction1 | DislikeReaction | reactions.py |
| Hate | hate1 | reaction1 | HateReaction | reactions.py |
| Agree | agree1 | reaction1 | AgreeReaction | reactions.py |
| Disagree | disagree1 | reaction1 | DisagreeReaction | reactions.py |
| Hurry Up | hurryup1 | reaction1 | HurryUpReaction | reactions.py |
| Go on | goon1 | reaction1 | GoOnReaction | reactions.py |
| Interesting | interest1 | reaction1 | InterestingReaction | reactions.py |
| Boring | boring1 | reaction1 | BoringReaction | reactions.py |
| Sympathy | sympathy1 | reaction1 | SympathyReaction | reactions.py |
| Laugh | laugh1 | reaction1 | LaughReaction | reactions.py |
| Like | like_l1 | reaction2 | NA | NA |
| Love | love_l1 | reaction2 | NA | NA |
| Dislike | dislike_l1 | reaction2 | NA | NA |
| Hate | hate_l1 | reaction2 | NA | NA |
| Agree | agreel1 | reaction2 | NA | NA |
| Disagree | disagree_l1 | reaction2 | NA | NA |
| Hurry Up | hurryup_l1 | reaction2 | NA | NA |
| Go on | goon_l1 | reaction2 | NA | NA |
| Interesting | interest_l1 | reaction2 | NA | NA |
| Boring | boring_l1 | reaction2 | NA | NA |
| Sympathy | sympathy_l1 | reaction2 | NA | NA |
| Laugh | laugh_l1 | reaction2 | NA | NA |
| roptionPublic | ropt1 | reaction1 | NF | NF |
| roptionAnon | ropt2 | reaction1 | NF | NF |
| roptionSecret | ropt3 | reaction1 | NF | NF |
| rchoicePublic | rch1 | reaction2 | NF | NF |
| rchoiceAnon | rch2 | reaction2 | NF | NF |
| rchoiceSecret | rch3 | reaction2 | NF | NF |

**Core Display Areas**:
- **topbar**: Navigation and user identity elements
- **mainarea**: Primary content (video conference + content panel)
- **jitsiwin1**: Video conference interface with participant tiles
- **reaction1**: Reaction button interface mapped to domain classes
- **descbar1**: Element description panel for UI exploration and documentation
- **bottombar**: Status and reaction aggregation displays

**Frontend-Backend Integration**:
- **UI Elements** (navmenu1, username, etc.): Vue components for interface
- **Reaction Elements** (like1, love1, etc.): Direct mapping to Python domain classes
- **Container Elements** (topbar, mainarea, etc.): Layout composition structures
- **Content Elements** (content1, reactionbx1): Dynamic content areas

**Reaction System Architecture**:
The reaction elements demonstrate clean separation between presentation and domain logic:
- Each reaction button maps to a concrete class in `reactions.py`
- WebSocket communication handled by `consumers.py`
- Policy validation through `policy_impl.py`
- Real-time broadcasting via `broadcast_channels.py`
- Participant context from `directory_cache.py`

**DescBar1 Architecture**:
The element description system provides interactive documentation for UI elements:
- **Interactive Elements** (30 total):
  - Reaction buttons (24): like1, love1, dislike1, hate1, agree1, disagree1, hurryup1, goon1, interest1, boring1, sympathy1, laugh1 (reaction1) + label equivalents (reaction2)
  - Reaction options (6): ropt1, ropt2, ropt3, rch1, rch2, rch3
- **Excluded Elements**: TopBar components, non-clickable containers
- **Data Source**: JSON file at `/frontend/public/data/element-descriptions.json`
- **Display Format**: Element header (label + ID) + functional description
- **Update Trigger**: Click event on any included element
- **Visibility**: Currently visible to all users (future: per-circle admin control)
- **Use Cases**: Developer exploration, system documentation, user training, facilitator reference

### Display Element Capabilities (Optional)
Each display element may support different capabilities as needed:

**Content Sources** (verified in screenshot):
- Static HTML files served through Caddy (ContentPanel1, ContentPanel2)
- Vue template rendering with dynamic data (TopMenu1, TitleBlock, StatusWin1)
- API-driven content from Django backend (StatusWin1, Widget1, Widget2)
- External service integration (JitsiWin1)
- System notifications and status messages (Bar1)

**Navigation Methods** (evident from content panels):
- Independent scroll state per user (ContentPanel1, ContentPanel2)
- Table of contents navigation (ContentPanel1)
- Document text display with formatting (ContentPanel2)
- Widget-based controls (Widget1, Widget2)

**Layout Behaviors** (confirmed from visual layout):
- Fixed positioning within display component (all elements)
- Grid-based responsive layout (3-row, 9-element composition)
- Hierarchical sizing (JitsiWin1 dominant, others supporting)
- Symmetric balance (Widget1 ↔ Widget2, ContentPanel1 ↔ ContentPanel2)
- Status persistence (StatusWin1, Bar1)

**User Permissions** (inferred from interface elements):
- Navigation menu access (TopMenu1)
- Status monitoring (StatusWin1)
- Content interaction (ContentPanel1, ContentPanel2)
- Widget control access (Widget1, Widget2)
- Video conference participation (JitsiWin1)
- System message visibility (Bar1)

### Composition Patterns
**Current Implementations**:
- **test-video-integration route**:
  - **Layout**: 3-row composition with 9 total elements
  - **Top Row**: TopMenu1 (full width) + TitleBlock (center) + StatusWin1 (right)
  - **Middle Row**: JitsiWin1 (dominant center video interface)
  - **Bottom Row**: Bar1 (full width notification) + Widget1/ContentPanel1 (left) + Widget2/ContentPanel2 (right)
- **Future routes**: May use different combinations of available elements

**Layout Architecture**:
- **Grid-based composition**: Elements arranged in responsive grid patterns
- **Hierarchical sizing**: JitsiWin1 dominates center, supporting elements surround
- **Mirrored widgets**: Widget1 and Widget2 provide balanced control placement
- **Content symmetry**: ContentPanel1 and ContentPanel2 offer dual-pane content display

**Composition Rules**:
- Display elements maintain independent state unless explicitly synchronized
- Each route defines which elements are included and how they're arranged
- Elements can be reused across different route/display combinations
- New routes can be created by composing existing elements in new ways
- Widget pairing maintains visual balance (Widget1 ↔ Widget2)
- Content panels provide flexible document display (ContentPanel1 ↔ ContentPanel2)

### Implementation Strategy
**Stage 2.2.2 Focus**:
- Replace `pdfviewer` with enhanced ContentPanel1/ContentPanel2 implementation
- Add local stylesheet support to content display elements
- Maintain existing 9-element composition while improving individual element capabilities
- Preserve Widget1/Widget2 mirrored control architecture

**Verified Architecture Benefits**:
- **Visual Balance**: Widget1/Widget2 pairing creates symmetric interface
- **Content Flexibility**: ContentPanel1/ContentPanel2 support diverse content types
- **Video Prominence**: JitsiWin1 central placement prioritizes video interaction
- **Status Integration**: StatusWin1 provides persistent state information
- **Navigation Consistency**: TopMenu1 and TitleBlock establish clear hierarchy

**Future Enhancement Path**:
- Add new display elements without changing existing routes
- Create new route experiences by composing elements differently
- Enhance individual element capabilities (static → dynamic content)
- Maintain backward compatibility through capability-based design
- Expand Widget1/Widget2 control capabilities while preserving balance

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

**Document Version**: v2.3.4 | **Last Updated**: 10/4/2025 | **Status**: ✅ Current