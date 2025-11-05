# InquiryCircle Phase 6 Refactoring - Documentation Context

This directory contains all planning and specification documents for the Phase 6 refactoring.

## Directory Structure

```
/mnt/c/Users/scott/Documents/AIProjects/Markdown/docs-websystems/projects/inquirycircle/
│
├── Documentation/                    # Core project documentation
│   ├── ProjectSpec.md               # Project specification (loaded by context-loader.sh)
│   ├── OperationsGuide.md           # Operations guide
│   └── Status.md                    # Project status
│
├── refactor_25P6phase.md            # Phase 6 refactoring plan (THE MASTER PLAN)
│
├── WEB_CLAUDE_TASK_BRIEF.md         # Detailed task assignments for web Claude
├── QUICK_START_WEB_CLAUDE.md        # Quick start guide (start here!)
├── web-claude-context.txt           # Project context (paste into claude.ai)
├── README_WEB_CLAUDE.md             # This file
│
└── web-claude-specs/                # Web Claude deliverables (13 documents)
    ├── BACKEND_CHANGES_REQUIRED.md
    ├── FRONTEND_CHANGES_REQUIRED.md
    ├── PHASE1_DATABASE_IMPLEMENTATION.md
    ├── PHASE2_AUTHENTICATION_IMPLEMENTATION.md
    ├── PHASE3_FACILITATOR_PANEL_APIs_IMPLEMENTATION.md
    ├── PHASE4_FACILITATOR_CONTROL_APIs_IMPLEMENTATION.md
    ├── PHASE5_FACILITATOR_PANEL_COMPONENT.md
    ├── PHASE6_SHARED_COMPONENTS.md
    ├── PHASE7_MEETING_VIEWS.md
    ├── PHASE8_ROUTER_CLEANUP.md
    ├── TESTING_STRATEGY.md
    ├── MIGRATION_STRATEGY.md
    ├── API_SPECIFICATION.md
    └── CODE_REVIEW_FEEDBACK.md       (after implementation)
```

## Implementation Context (Separate!)

Implementation work happens in: `/home/scott/inquirycircle/` (WSL context)
- This is the actual Git repository
- Contains frontend/, backend/, docker-compose.yml, etc.
- Claude Code (CLI) works here for implementation

## Workflow

1. **Planning Phase** (Web Claude with $250 credits)
   - Works in this directory (docs context)
   - Reviews GitHub repo: scott009/InquiryCircle
   - Generates 13 specification documents
   - Saves to `web-claude-specs/`

2. **Implementation Phase** (Claude Code CLI with regular credits)
   - Works in `/home/scott/inquirycircle/` (WSL context)
   - Reads specs from this directory
   - Executes implementation in Git repo
   - Commits and pushes changes

3. **Review Phase** (Web Claude with remaining credits)
   - Reviews GitHub commits
   - Generates CODE_REVIEW_FEEDBACK.md
   - Saves to `web-claude-specs/`

## Getting Started

**Start here:** Read `QUICK_START_WEB_CLAUDE.md`

## Key Insight

**Separation of Concerns:**
- **Docs Context** (this directory) = Planning, specs, documentation, thinking
- **Implementation Context** (WSL) = Code, git, execution, running

This keeps planning materials organized and separate from code clutter!
