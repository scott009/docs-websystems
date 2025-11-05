# InquiryCircle Phase 6 Refactoring
## Architecture Redesign: Circle Types and Route Structure

**Date:** 2025-11-04
**Status:** Design Complete, Implementation Pending
**Scope:** Complete refactoring of circle type architecture and route structure

---

## Problem Statement

The initial Phase 6 implementation created special routes for each circle type:
- `/translation-circle/:circleId` for translation circles
- Would require `/discussion-circle/:circleId` for discussion circles
- Each new circle type requires new routes = not scalable

**Core Issue:** Circle type was treated as routing logic instead of data.

---

## Architectural Solution

### Principle: Circle Type as Data, Not Routes

Circle type is a **property of the circle data**, not a routing concern. All circles use the same standard routes, and views dynamically load appropriate components based on `circle.circle_type`.

### Standard Route Structure

**Circle-type agnostic routes:**
- `/facpanel` - Facilitator control panel (configuration, start meeting)
- `/facmeet/:circleId` - Facilitator meeting view
- `/meeting/:circleId` - Participant meeting view
- `/administration` - Admin functions (existing)
- `/tests` - System tests (existing)

**Route behavior:**
- `/facmeet/:circleId` and `/meeting/:circleId` load circle data
- Based on `circle.circle_type`, render appropriate components dynamically
- Translation circles → TranslationContent components
- Discussion circles → DiscussionContent components (future)

---

## Key Concepts

### Circle = Group of People (not a meeting)

A circle is a **permanent group** that can have multiple meetings over time.

**Example:**
- Circle #6 = "Thai Translation Team" (the people)
- Meeting 1: Recovery Dharma → Thai (last week, ended)
- Meeting 2: Heart Sutra → Thai (today, active)
- Meeting 3: Another Book → Thai (next week, future)

### Key-to-Circle Mapping

**Simplified model for Phase 6:**
- 1 key = 1 circle
- Facilitator key grants access to ONE circle only
- Participant key grants access to ONE circle only
- Multiple circles = multiple keys (deferred: master keys with multiple circles)

### Session Lifecycle

**Session creation:**
- Session does NOT start when facilitator logs in
- Session starts when facilitator clicks [Start Meeting] in `/facpanel`
- Only one active session per circle at a time

**Session states:**
- `active` - Meeting in progress
- `completed` - Meeting ended normally
- `aborted` - Meeting ended abnormally

---

## Database Schema

### TranslationDocument (System-Wide Library)

**Concept:** JSON files (books) are system-wide resources, not tied to specific circles.

**Schema:**
```python
class TranslationDocument(models.Model):
    """System-wide library of translation JSON files (books)"""

    # File identification
    file_path = models.CharField(max_length=512)
        # "rdg_en_v3.json", "heart_sutra.json"

    title = models.CharField(max_length=255)
        # "Recovery Dharma", "Heart Sutra"

    edition = models.CharField(max_length=50, blank=True)
    json_version = models.CharField(max_length=50, blank=True)

    # Available languages in this JSON file
    available_languages = models.JSONField(default=list)
        # ["thai", "vietnamese", "korean", "japanese"]

    # Tracking
    created_at = models.DateTimeField(default=timezone.now)
    last_modified_at = models.DateTimeField(auto_now=True)
```

**Changes from current model:**
- **REMOVE:** `circle` ForeignKey (was circle-specific, now system-wide)
- **REMOVE:** `language` CharField (one file has ALL languages)
- **REMOVE:** `created_by` ForeignKey (system library, not user-owned)
- **REMOVE:** `last_loaded_at`, `last_saved_at` (not needed)
- **REMOVE:** `status` field (not needed for library)
- **ADD:** `available_languages` JSONField

**Rationale:**
- One JSON file = one database record
- Multiple circles can use same JSON file
- Each circle chooses which language from that file

### TranslationSession (Per-Meeting)

**Concept:** Each meeting creates a session with document + language selection.

**Schema:**
```python
class TranslationSession(models.Model):
    """Active translation editing session (one per meeting)"""

    # What circle and what content
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
    document = models.ForeignKey(TranslationDocument, on_delete=models.CASCADE)
    target_language = models.CharField(max_length=50)  # NEW FIELD

    # Session state
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
        # 'active', 'completed', 'aborted'

    # Lifecycle tracking
    started_by = models.ForeignKey(AccessKey, on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    ended_by = models.ForeignKey(AccessKey, on_delete=models.SET_NULL, null=True)

    # Statistics
    total_paragraphs = models.IntegerField(default=0)
    paragraphs_modified = models.IntegerField(default=0)
```

**Changes from current model:**
- **ADD:** `target_language` CharField (which language this session is working on)

### Circle (No Changes)

**Existing model is sufficient:**
```python
class Circle(models.Model):
    circle_type = models.CharField(...)  # 'translation', 'discussion', 'study'
    name = models.CharField(...)
    status = models.CharField(...)  # 'inactive', 'active', 'ended'
    facilitator_key = models.ForeignKey(AccessKey, ...)
    # ... rest of fields unchanged
```

**Circle status interpretation:**
- `inactive` - No active session
- `active` - Has active session (meeting in progress)
- `ended` - Circle permanently closed

**Determining circle status:**
```python
# Check if circle has active session
active_session = TranslationSession.objects.filter(
    circle=circle,
    status='active'
).first()

circle_status = 'active' if active_session else 'inactive'
```

### No TranslationCircleConfig Table

**Decision:** No persistent configuration table needed.

**Configuration strategy:** Smart defaults from last session
- When facilitator goes to `/facpanel`, query last completed session
- Pre-fill document + language dropdowns with last-used values
- Facilitator can change or keep defaults
- No configuration saved until [Start Meeting] clicked

**Rationale:**
- Simpler architecture (one less table)
- Configuration is ephemeral (only matters when starting meeting)
- Last session provides good default
- No "staging area" complexity

---

## User Flows

### Facilitator Login and Meeting Start

```
1. Facilitator enters key at /
   ↓
2. Backend validates:
   - circleId: 6
   - role: "facilitator"
   - circleType: "translation"
   ↓
3. Redirect to: /facpanel
   ↓
4. /facpanel loads:
   - Circle #6 details (name, type, status)
   - Query last session: document="Recovery Dharma", language="Thai"
   - Pre-fill dropdowns with last values
   - [Start Meeting] button (disabled until valid selection)
   ↓
5. Facilitator reviews configuration:
   - Can keep defaults OR
   - Change document to "Heart Sutra" OR
   - Change language to "Vietnamese"
   ↓
6. Click [Start Meeting]:
   - API call: POST /api/circles/6/start-translation-session
   - Creates TranslationSession record (document + language)
   - Loads paragraphs from JSON into ParagraphCorrection table
   - Returns session_id
   ↓
7. Redirect to: /facmeet/6
   ↓
8. /facmeet/6 loads:
   - Circle data (sees circle_type="translation")
   - Active session data (document, language, paragraphs)
   - Dynamically renders TranslationContent component
   - Shows small facilitator control bar
```

### Participant Login

```
1. Participant enters key at /
   ↓
2. Backend validates:
   - circleId: 6
   - role: "participant"
   - circleType: "translation"
   ↓
3. Redirect to: /meeting/6 (direct to meeting)
   ↓
4. /meeting/6 loads:
   - Circle data (sees circle_type="translation")
   - Active session data (document, language, paragraphs)
   - Dynamically renders TranslationContent component
   - No facilitator controls
```

### First-Time Circle (No Previous Session)

```
1. Facilitator → /facpanel
   ↓
2. No previous session found
   ↓
3. Dropdowns show:
   - Document: [Select document ▼]
   - Language: [Select language ▼]
   - [Start Meeting] button DISABLED
   ↓
4. Facilitator MUST select both before proceeding
   ↓
5. [Start Meeting] button enables when both selected
```

---

## Frontend Architecture

### View Components

**New/Modified Views:**

1. **FacilitatorPanel.vue** (NEW)
   - Path: `/facpanel`
   - Purpose: Pre-meeting configuration and session start
   - Features:
     - Display circle details
     - Document selection dropdown (from TranslationDocument library)
     - Language selection dropdown (from selected document's available_languages)
     - Validation: both required before [Start Meeting] enabled
     - Smart defaults: pre-fill from last session
     - [Start Meeting] button → creates session, redirects to /facmeet

2. **FacilitatorMeeting.vue** (RENAMED from TranslationCircle.vue)
   - Path: `/facmeet/:circleId`
   - Purpose: Facilitator meeting interface
   - Features:
     - Loads circle data dynamically
     - Based on circle_type, renders appropriate content component
     - Small facilitator control bar (navigate all, lock editing, end meeting)
     - Shares most UI with ParticipantMeeting.vue

3. **ParticipantMeeting.vue** (NEW)
   - Path: `/meeting/:circleId`
   - Purpose: Participant meeting interface
   - Features:
     - Loads circle data dynamically
     - Based on circle_type, renders appropriate content component
     - No facilitator controls
     - Shares TranslationContent component with FacilitatorMeeting

### Shared Components

**TranslationContent.vue** (extracted from existing code)
- Composition of 4 translation-specific elements:
  - DocumentNavigator
  - EnglishTextDisplay
  - AITranslationDisplay
  - CorrectedTextEditor
- VideoConference (Jitsi integration)
- Used by both FacilitatorMeeting and ParticipantMeeting

**SmallFacilitatorControls.vue** (NEW)
- Compact control bar for facilitator actions during meeting
- Buttons (small, easily extensible):
  - Navigate All: [Paragraph dropdown ▼] - syncs all participants to paragraph
  - Lock Editing: [Lock toggle] - prevent participant edits
  - End Meeting: [End] - end session, save corrections to JSON
- Design: Single row, minimal height, icon-focused

### Component Layout

**FacilitatorPanel.vue Layout:**
```
╔═══════════════════════════════════════╗
║ Facilitator Panel - Circle #6        ║
║ Thai Translation Team                 ║
╠═══════════════════════════════════════╣
║ Type: Translation                     ║
║ Status: Inactive (No active session)  ║
╠═══════════════════════════════════════╣
║ Next Meeting Configuration:           ║
║                                       ║
║ Document: [Recovery Dharma      ▼]   ║
║ Language: [Thai                 ▼]   ║
║                                       ║
║           [Start Meeting]             ║
╚═══════════════════════════════════════╝
```

**FacilitatorMeeting.vue Layout:**
```
╔════════════════════════════════════════════════╗
║ TopBar (navigation, user info, status)        ║
╠════════════════════════════════════════════════╣
║ FacilitatorControls: [Nav▼][Lock][End] ...    ║
╠════════════════════════════════════════════════╣
║                                                ║
║         Video Conference (Jitsi)               ║
║                                                ║
╠════════════════════════════════════════════════╣
║ Navigator │ English │ AI Trans │ Corrected    ║
║           │         │          │               ║
╚════════════════════════════════════════════════╝
```

**ParticipantMeeting.vue Layout:**
```
╔════════════════════════════════════════════════╗
║ TopBar (navigation, user info, status)        ║
╠════════════════════════════════════════════════╣
║                                                ║
║         Video Conference (Jitsi)               ║
║                                                ║
╠════════════════════════════════════════════════╣
║ Navigator │ English │ AI Trans │ Corrected    ║
║           │         │          │               ║
╚════════════════════════════════════════════════╝
```

### Router Configuration

**New routes:**
```javascript
{
  path: '/facpanel',
  name: 'FacilitatorPanel',
  component: FacilitatorPanel,
  meta: { requiresAuth: true, requiresFacilitator: true }
},
{
  path: '/facmeet/:circleId',
  name: 'FacilitatorMeeting',
  component: FacilitatorMeeting,
  meta: { requiresAuth: true, requiresFacilitator: true }
},
{
  path: '/meeting/:circleId',
  name: 'ParticipantMeeting',
  component: ParticipantMeeting,
  meta: { requiresAuth: true }
}
```

**Remove route:**
```javascript
// DELETE THIS:
{
  path: '/translation-circle/:circleId',
  name: 'TranslationCircle',
  component: TranslationCircle
}
```

### File Structure

```
frontend/src/
├── views/
│   ├── FacilitatorPanel.vue          (NEW)
│   ├── FacilitatorMeeting.vue        (RENAME from TranslationCircle.vue)
│   ├── ParticipantMeeting.vue        (NEW)
│   ├── Welcome.vue                   (existing)
│   └── ...
├── components/
│   ├── circles/
│   │   ├── translation/
│   │   │   ├── TranslationContent.vue        (EXTRACT from existing)
│   │   │   ├── SmallFacilitatorControls.vue  (NEW)
│   │   │   ├── DocumentNavigator.vue         (existing)
│   │   │   ├── EnglishTextDisplay.vue        (existing)
│   │   │   ├── AITranslationDisplay.vue      (existing)
│   │   │   └── CorrectedTextEditor.vue       (existing)
│   │   └── discussion/                       (future)
│   ├── layout/
│   │   ├── TopBar.vue                        (existing)
│   │   └── ...
│   └── VideoConference.vue                   (existing)
└── router/
    └── index.js                              (UPDATE)
```

---

## Backend API Requirements

### FacilitatorPanel APIs

**1. GET /api/circles/:id/panel-info**
- Returns circle details + last session defaults
- Response:
```json
{
  "circle": {
    "id": 6,
    "name": "Thai Translation Team",
    "circle_type": "translation",
    "status": "inactive"
  },
  "last_session": {
    "document_id": 1,
    "document_title": "Recovery Dharma",
    "target_language": "thai",
    "ended_at": "2025-10-28T14:30:00Z"
  },
  "active_session": null
}
```

**2. GET /api/translation-documents/**
- Returns list of available documents
- Response:
```json
[
  {
    "id": 1,
    "title": "Recovery Dharma",
    "edition": "v3",
    "available_languages": ["thai", "vietnamese", "korean", "japanese"]
  },
  {
    "id": 2,
    "title": "Heart Sutra",
    "edition": "2024",
    "available_languages": ["thai", "tibetan", "chinese"]
  }
]
```

**3. POST /api/circles/:id/start-translation-session**
- Creates new TranslationSession
- Loads paragraphs from JSON into ParagraphCorrection
- Request body:
```json
{
  "document_id": 1,
  "target_language": "thai"
}
```
- Response:
```json
{
  "session_id": 42,
  "circle_id": 6,
  "document_id": 1,
  "target_language": "thai",
  "total_paragraphs": 245,
  "started_at": "2025-11-04T10:00:00Z"
}
```

### Facilitator Control APIs

**1. POST /api/translation-sessions/:id/navigate-all**
- Broadcasts paragraph navigation to all participants
- Request body:
```json
{
  "paragraph_id": "p9-15"
}
```

**2. POST /api/translation-sessions/:id/lock-editing**
- Toggles editing lock for participants
- Request body:
```json
{
  "locked": true
}
```

**3. POST /api/translation-sessions/:id/end-meeting**
- Ends session
- Writes corrections back to JSON
- Updates session status to 'completed'
- Response:
```json
{
  "session_id": 42,
  "status": "completed",
  "ended_at": "2025-11-04T11:30:00Z",
  "paragraphs_modified": 23,
  "corrections_saved": true
}
```

### Login Redirect Logic Update

**Current behavior:**
- All users redirect to `/welcome` after login

**New behavior:**
```python
# In authentication/views.py LoginView

if user_role == 'facilitator':
    redirect_url = '/facpanel'
elif user_role == 'participant':
    # Get circle_id from access key
    circle_id = access_key.circle.id
    redirect_url = f'/meeting/{circle_id}'
```

---

## Implementation Plan

### Phase 1: Database (Backend)
1. Modify `backend/circles/translation/models.py`:
   - Update TranslationDocument model (remove circle FK, add available_languages)
   - Update TranslationSession model (add target_language field)
2. Create Django migration
3. Run migration on dev database

### Phase 2: Authentication (Backend)
4. Update login redirect logic in `authentication/views.py`
5. Test: facilitator → /facpanel, participant → /meeting/:id

### Phase 3: FacilitatorPanel APIs (Backend)
6. Create `/api/circles/:id/panel-info` endpoint
7. Create `/api/translation-documents/` list endpoint
8. Create `/api/circles/:id/start-translation-session` endpoint
9. Test API endpoints with curl/Postman

### Phase 4: Facilitator Control APIs (Backend)
10. Create `/api/translation-sessions/:id/navigate-all` endpoint
11. Create `/api/translation-sessions/:id/lock-editing` endpoint
12. Create `/api/translation-sessions/:id/end-meeting` endpoint

### Phase 5: FacilitatorPanel View (Frontend)
13. Create `FacilitatorPanel.vue` component
14. Implement document/language selection UI
15. Implement smart defaults from last session
16. Wire up [Start Meeting] to API
17. Test full flow: login → facpanel → configure → start

### Phase 6: Shared Components (Frontend)
18. Extract `TranslationContent.vue` from existing TranslationCircle.vue
19. Create `SmallFacilitatorControls.vue` component
20. Test components in isolation

### Phase 7: Meeting Views (Frontend)
21. Rename `TranslationCircle.vue` → `FacilitatorMeeting.vue`
22. Refactor to use TranslationContent component
23. Add SmallFacilitatorControls
24. Create `ParticipantMeeting.vue` (similar to FacilitatorMeeting, minus controls)
25. Test both views

### Phase 8: Router & Cleanup (Frontend)
26. Update `router/index.js`:
    - Add /facpanel route
    - Add /facmeet/:id route
    - Add /meeting/:id route
    - Remove /translation-circle/:id route
27. Remove old FacilitatorControls component (document/language selection)
28. Update any links/references to old routes

### Phase 9: Integration Testing
29. Test facilitator flow: login → facpanel → configure → start → facmeet → controls → end
30. Test participant flow: login → meeting → view/edit
31. Test multiple sessions: same circle, different documents
32. Test edge cases: no previous session, invalid selections

---

## Migration Considerations

### Breaking Changes

This refactoring introduces **breaking changes** to existing data:

**TranslationDocument model changes:**
- Removing `circle` ForeignKey
- Removing `language` CharField
- Adding `available_languages` JSONField

**If existing data:**
- Need data migration to extract languages from existing records
- Need to deduplicate TranslationDocument records (same file_path)
- Need to update TranslationSession references

**If clean slate:**
- Can simply drop and recreate tables
- Simpler migration path

### API Compatibility

**Old endpoints that will break:**
- Any endpoint that assumes TranslationDocument has `circle` or `language` fields
- Any endpoint that creates TranslationSession without `target_language`

**New endpoints required:**
- All FacilitatorPanel endpoints (listed above)
- All FacilitatorControl endpoints (listed above)

### Frontend Route Changes

**Old routes removed:**
- `/translation-circle/:circleId`

**Any bookmarks or hardcoded links will break.**

---

## Benefits of New Architecture

### Scalability
- Adding new circle types = new components, not new routes
- DiscussionCircle, StudyCircle, etc. use same route structure
- Configuration logic is reusable across circle types

### Consistency
- All circles use same route patterns
- Users have predictable navigation
- Easier to maintain and document

### Separation of Concerns
- Configuration (/facpanel) separate from meeting (/facmeet)
- Pre-meeting setup vs. during-meeting actions clearly separated
- Cleaner user experience

### Data Model
- TranslationDocument as system library = cleaner, more reusable
- One JSON file = one database record (no duplication)
- Sessions properly scoped to meetings (not circles)

### Flexibility
- Circles can work on different documents over time
- Same document can be used by multiple circles
- Easy to add more languages to existing documents

---

## Future Enhancements

### Multi-Circle Keys
- Currently deferred: 1 key = 1 circle
- Future: Master facilitator key with multiple circles
- Would require circle selection UI in /facpanel

### Pre-Scheduled Meetings
- Currently: Ad-hoc meeting creation
- Future: Schedule meetings in advance with document/language pre-configured
- Would require meeting scheduling table

### Discussion Circle Type
- Implement DiscussionContent component
- Reuse same route structure (/facmeet, /meeting)
- Different display elements (reading panel, discussion prompts, etc.)

### Advanced Facilitator Controls
- Participant muting (beyond Jitsi controls)
- Breakout rooms
- Timer/agenda management
- All fit in SmallFacilitatorControls extensible design

---

## Questions & Decisions Log

**Q: Should TranslationDocument be circle-specific or system-wide?**
A: System-wide library. One JSON file = one record, reusable across circles.

**Q: Where to store document/language selection before meeting starts?**
A: No persistent config. Smart defaults from last session, ephemeral until [Start Meeting].

**Q: When does session start?**
A: When facilitator clicks [Start Meeting] in /facpanel, not at login.

**Q: Circle = meeting or group?**
A: Circle = group of people. Can have multiple sessions (meetings) over time.

**Q: Multi-circle keys now or later?**
A: Later. Phase 6 uses 1 key = 1 circle for simplicity.

**Q: Should Circle.status have 'configured' state?**
A: No. Just 'active' (has session) or 'inactive' (no session). Configuration is ephemeral.

---

## Status

**Design:** ✅ Complete
**Implementation:** ⏳ Pending
**Testing:** ⏳ Pending
**Documentation:** ✅ This document

**Next Step:** Begin Phase 1 (Database modifications)
