
<!-- InquiryCircle2 – ProjectSpec – Stage2 – 10/4/2025 at 10:30 PM ET -->

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

### Stage 2.4.0-foundation (✅ Complete)
- **Workorder System**: YAML-based specifications for AI-assisted development
  - Structured workorders in `/workorders/` directory
  - Template system for creating new workorders
  - Clear specifications for domain models, tests, and infrastructure
  - Enable lower-level AI models (Haiku) to execute well-defined tasks
  - Workorders created: reactions-domain, reactions-tests
- **Interactions App Skeleton**: Foundation for reaction system and future interactions
  - Clean architecture: domain, infrastructure, policies, tests subdirectories
  - Domain-first approach (pure Python, framework-agnostic)
  - Django app structure ready for Phase 1-4 development
  - Comprehensive README documenting architecture and phases
  - UI components already exist (ReactionBar1/2, element-descriptions.json)

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

## Interactions Architecture

### Overview
InquiryCircle uses a **Clean Architecture** approach for user interactions (reactions, polls, Q&A, etc.) that separates business logic from infrastructure concerns.

### Architecture Layers

**Layer 1: Domain (Pure Python)**
- Pure business logic with no framework dependencies
- Testable with fakes/mocks, no database or network required
- Location: `/backend/interactions/domain/`
- Example: `reactions.py` - Reaction types, visibility modes, services

**Layer 2: Infrastructure (Django/Channels Adapters)**
- Concrete implementations of domain interfaces
- Connects to database, cache, WebSocket channels
- Location: `/backend/interactions/infrastructure/`
- Example: `repository.py`, `broadcaster.py`, `cache.py`

**Layer 3: Application (APIs and Endpoints)**
- HTTP REST APIs and WebSocket consumers
- Orchestrates use cases using domain services
- Location: `/backend/interactions/` (views.py, consumers.py)

**Layer 4: Presentation (Vue Components)**
- UI components that call backend APIs
- Location: `/frontend/src/components/reactions/`
- Already implemented: ReactionBar1.vue, ReactionBar2.vue

### Workorder System

**Purpose**: Enable AI assistants (especially lower-level models like Haiku) to build components from structured YAML specifications.

**Location**: `/workorders/`

**Structure**:
- `workorder-[feature]-[component].yml` - Detailed specifications
- `templates/workorder-template.yml` - Template for new workorders
- `README.md` - Documentation and workflow

**Workorder Contents**:
- Metadata: title, assigned AI, stage, priority, dependencies
- Context: business description, reference materials, rules
- Deliverables: output paths, required components
- Specifications: detailed class/function/test specs
- Technical Requirements: dependencies, code style, structure
- Acceptance Criteria: functional and technical requirements
- Validation: commands to verify correctness
- Notes & Hints: guidance for AI execution

**Development Philosophy**:
- Build tested, production-ready code BEFORE integration
- Domain logic stays pure and reusable
- Lower-level AIs execute well-defined tasks efficiently
- Tests verify correctness independent of UI/framework

### Interactions App Structure

```
backend/interactions/
├── domain/              # Pure Python business logic
│   └── reactions.py     # Reaction domain models (Phase 1)
├── infrastructure/      # Django/Channels adapters (Phase 2)
│   ├── repository.py    # Database persistence
│   ├── broadcaster.py   # WebSocket broadcasting
│   └── cache.py         # Participant directory
├── policies/            # Business rules (Phase 2)
│   └── reaction_policy.py
├── tests/               # Unit and integration tests
│   └── test_reactions.py
├── models.py            # Django models (Phase 2)
├── consumers.py         # WebSocket endpoints (Phase 3)
├── views.py             # HTTP endpoints (Phase 3)
└── README.md            # Architecture documentation
```

### Development Phases

**Phase 1: Domain Layer** (Foundation established)
- Build pure Python domain models
- Write comprehensive unit tests with fakes
- No Django dependencies, fully testable in isolation
- Workorders: reactions-domain.yml, reactions-tests.yml

**Phase 2: Infrastructure Layer** (Deferred)
- Implement Django/Channels adapters
- Create database models for persistence
- Connect to Redis for caching
- Implement policy enforcement

**Phase 3: Application Layer** (Deferred)
- Build WebSocket consumers for real-time
- Create HTTP API endpoints as fallback
- Wire up routing and authentication

**Phase 4: Frontend Integration** (Deferred)
- Connect Vue components to backend APIs
- Implement real-time event handling
- UI components already exist, just need connection

### Extensibility

The `interactions` app name was chosen to support future features beyond reactions:
- ✅ Reactions (12 types, 3 visibility modes) - Stubs and workorders created
- ✅ Airtime Allocation System (AAS) - Stubs and workorders created
- 📋 Polls (future)
- 📋 Q&A (future)
- 📋 Hand-raising (future)
- 📋 Annotations (future)

All follow the same clean architecture pattern: domain → infrastructure → application → presentation.

---

## Airtime Allocation System (AAS)

### Overview
The Airtime Allocation System manages speaking time distribution in InquiryCircle meetings through configurable rules and enforcement mechanisms.

### Core Concepts

**Time Tracking (Hourglass System)**
- Monitor dominant speaker via Jitsi API
- Track cumulative speaking time per participant
- Display visual indicators and warnings
- Advisory enforcement (stats and warnings only)

**Allocation Rules**
Six different algorithms for distributing speaking time:
1. **Equal Share**: `duration / num_participants`
2. **Custom Allocation**: Facilitator-defined (e.g., invited speaker gets more)
3. **Progressive Stack**: Less spoken = higher priority
4. **Round-Robin**: Fixed time slots in rotation
5. **Reaction-Based**: Positive reactions add time, negative subtract (depends on reactions)
6. **Advisory Only**: Track and report, no enforcement

**Enforcement Levels**
- **ADVISORY**: Stats only, no control
- **SOFT**: Warnings and prompts
- **HARD**: Auto-mute when time expires

**Time Lending**
- Participants can transfer unused time to others
- Lending cap (default 50% of allocation)
- Validates available time before transfer
- Broadcasts updates to all participants

### Domain Models

**Value Objects:**
- `TimeAllocation` - Participant time budget (allocated, used, borrowed, lent)
- `SpeakingSession` - Single speaking instance (start, end, duration)
- `MeetingContext` - Meeting metadata (scheduled vs. adhoc, duration, participants)
- `TimeWarning` - Warning event (yellow 50%, orange 25%, red 5%)
- `MuteCommand` - Mute/unmute command (hard enforcement)

**Services:**
- `AirtimeTracker` - Real-time speaking time tracking
- `AllocationCalculator` - Calculate time allocations per rule
- `TimeLendingService` - Transfer time between participants

**Interfaces:**
- `AirtimeRepository` - Persistence (sessions, allocations, history)
- `SpeakerTracker` - Jitsi integration (dominant speaker events)
- `AirtimeBroadcaster` - Event distribution (warnings, mute commands, updates)

### Token Economy (Future)

Advanced integration combining reactions with airtime allocation:

**Token Mechanics:**
- Speaking costs tokens (1 token = 30 seconds default)
- Sending reactions costs tokens
- Receiving positive reactions earns tokens
- Receiving negative reactions reduces tokens

**Token Costs/Rewards:**
```
Sending "love": -2 tokens
Receiving "love": +2 tokens
Sending "like": -1 token
Receiving "like": +1 token
Sending "dislike": -1 token (target loses 1 token)
Sending "hate": -2 tokens (target loses 2 tokens)
```

**Dependencies:**
Token economy requires reaction system to be implemented first.

### Facilitator Controls

Facilitators have complete override capabilities:
- Choose allocation rule for meeting
- Set enforcement level (advisory/soft/hard)
- Override rules (bypass, reallocate, pause)
- View real-time usage statistics
- Manually grant time bonuses/penalties

### Integration with Jitsi

**Event Handling:**
- Listen for `dominantSpeakerChanged` events from Jitsi iframe
- Track speaking sessions automatically
- Calculate duration when speaker changes
- Update allocations and check warnings

**Control Commands:**
- Can send mute/unmute commands (hard enforcement)
- Broadcast time warnings to participants
- Update UI displays with current allocations

### Development Phases

**Phase 1: Basic Time Tracking** (Foundation established)
- Implement airtime.py domain models
- Track speaking time (no enforcement)
- Display stats to participants
- Workorders: airtime-domain.yml, airtime-tests.yml

**Phase 2: Allocation Rules** (Deferred)
- Implement rule algorithms
- Add warning system
- Soft enforcement (warnings only)
- UI: Time allocation displays, warning indicators

**Phase 3: Policy Enforcement** (Deferred)
- Implement policy layer
- Add hard enforcement (auto-mute)
- Facilitator override controls
- UI: Enforcement controls

**Phase 4: Token Economy** (Deferred)
- Integrate with reaction system
- Implement token transactions
- Full economic model
- UI: Token balance displays

### File Structure

```
backend/interactions/
├── domain/
│   ├── reactions.py         # Reaction system
│   ├── airtime.py           # AAS core (Phase 1)
│   ├── allocation_rules.py  # Rule implementations (Phase 2)
│   └── token_economy.py     # Token system (Phase 4, depends on reactions)
├── infrastructure/
│   ├── jitsi_tracker.py     # Speaker tracking (Phase 2)
│   └── ...
├── policies/
│   └── airtime_policy.py    # Policy enforcement (Phase 3)
└── tests/
    ├── test_reactions.py
    └── test_airtime.py      # AAS tests (Phase 1)
```

### Current Status

**✅ Foundation Complete:**
- Stub files created (7 files, 1,652 lines)
- Workorders created (domain + tests)
- Architecture documented
- Ready for Haiku execution

**📋 Pending Implementation:**
- Domain models (workorder-airtime-domain.yml)
- Unit tests (workorder-airtime-tests.yml)
- Infrastructure adapters (Phase 2+)

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

**Document Version**: v2.4.0-foundation | **Last Updated**: 10/4/2025 | **Status**: ✅ Current