# Web Claude Task Brief - InquiryCircle Phase 6 Refactoring

**Purpose:** Maximize $250 promotional credits (expires Nov 18) for high-value planning and design work

**Your Role:** Deep analysis, detailed planning, specification generation
**Claude Code's Role:** Actual implementation execution

---

## Step 1: Get Context (Session 1 - ~15 min)

### Load Project Documentation
```
I need you to review the InquiryCircle project. Here's how to get started:

1. Access the GitHub repository: scott009/InquiryCircle
2. Read these key files via GitHub:
   - /home/scott/inquirycircle/context-loader.sh (shows doc structure)
   - Look for documentation in the repo or ask me to paste it

3. I will paste the output from running: /home/scott/inquirycircle/context-loader.sh
   (This loads ProjectSpec.md, OperationsGuide.md, Status.md, etc.)

4. I will also paste the refactoring plan: refactor_25P6phase.md

After you have context, confirm you understand:
- Current architecture (Stage 2.5.0 Phase 6 complete)
- The refactoring problem (circle types as routes vs. data)
- The proposed solution (standard routes, dynamic components)
```

---

## Step 2: Codebase Analysis (Session 1-2 - ~30 min)

### Review Current Implementation via GitHub

**Task:** Analyze these files and identify what needs to change:

**Backend Analysis:**
```
Please review via GitHub integration:

1. backend/circles/models.py
   - Current Circle model
   - Document circle_type field and status field

2. backend/circles/translation/models.py
   - Current TranslationDocument model (note the circle FK and language field)
   - Current TranslationSession model (note missing target_language)
   - Current ParagraphCorrection model

3. backend/authentication/views.py
   - Current login redirect logic
   - Identify where to add facilitator vs participant routing

4. backend/circles/translation/views.py
   - Current API endpoints
   - Identify what needs to be modified/added

Create a markdown document: BACKEND_CHANGES_REQUIRED.md
- List every file that needs modification
- List every new file needed
- Identify breaking changes
- Note any potential migration issues
```

**Frontend Analysis:**
```
Please review via GitHub integration:

1. frontend/src/router/index.js
   - Current route structure
   - Identify routes to add/remove

2. frontend/src/views/TranslationCircle.vue
   - Current implementation
   - Identify what to extract into TranslationContent.vue
   - Identify what to keep for FacilitatorMeeting.vue

3. frontend/src/components/circles/translation/
   - Review existing components
   - Identify reusability

Create a markdown document: FRONTEND_CHANGES_REQUIRED.md
- List every file that needs modification
- List every new component needed
- Map component extraction strategy
- Identify shared vs. role-specific code
```

---

## Step 3: Phase 1 Deep Dive - Database Migration (Session 2 - ~45 min)

### Create Detailed Implementation Guide

**Task:** Generate complete Phase 1 implementation specification

**Output Document:** `PHASE1_DATABASE_IMPLEMENTATION.md`

**Required Contents:**

1. **Migration Strategy**
   - Check current database state (is there production data?)
   - If yes: Data migration script to transform existing TranslationDocument records
   - If no: Clean slate migration approach
   - Decision tree for choosing approach

2. **Django Migration Code**
   - Complete migration file with all operations
   - Handle foreign key removal carefully
   - Handle adding available_languages JSONField with defaults
   - Handle adding target_language to TranslationSession

3. **Data Transformation Logic**
   - If existing data: Python script to deduplicate TranslationDocument by file_path
   - Script to extract languages from multiple records into single record's available_languages
   - Script to update TranslationSession references

4. **Validation Scripts**
   - SQL queries to verify migration success
   - Python management command to check data integrity
   - Test cases for migration

5. **Rollback Plan**
   - How to reverse if migration fails
   - Backup strategy

**Specific Questions to Answer:**
- What happens to existing TranslationSession records that reference TranslationDocument?
- Should we use migrations.RunPython for data transformation or separate management command?
- What default value for available_languages on existing records?
- How to handle orphaned records?

---

## Step 4: Phase 2-4 Deep Dive - Backend APIs (Session 3 - ~60 min)

### Create Detailed Implementation Guides

**Task:** Generate complete specifications for backend API development

**Output Documents:**
- `PHASE2_AUTHENTICATION_IMPLEMENTATION.md`
- `PHASE3_FACILITATOR_PANEL_APIs_IMPLEMENTATION.md`
- `PHASE4_FACILITATOR_CONTROL_APIs_IMPLEMENTATION.md`

**For Each API Endpoint, Specify:**

1. **Exact Function Signature**
   ```python
   # Example level of detail needed:
   @api_view(['GET'])
   @permission_classes([IsAuthenticated, IsFacilitator])
   def get_panel_info(request, circle_id):
       """
       Returns circle details and last session info for FacilitatorPanel.

       Args:
           request: DRF request object with authenticated user
           circle_id: int - Circle primary key

       Returns:
           Response with circle data and last_session defaults

       Raises:
           404: Circle not found or user lacks access
           403: User is not facilitator for this circle
       """
       # Implementation guidance here
   ```

2. **Django ORM Queries**
   - Exact queries needed
   - Optimization considerations (select_related, prefetch_related)
   - Handle edge cases (no last session, multiple active sessions)

3. **Request/Response Schemas**
   - Complete JSON examples
   - Validation rules
   - Error responses with status codes

4. **Serializer Specifications**
   - Which serializers to create/modify
   - Field definitions
   - Nested serialization strategy

5. **URL Routing**
   - Exact URL patterns to add to urls.py
   - Parameter names and types
   - Naming conventions

6. **Permission Logic**
   - Custom permission classes needed
   - Access control rules
   - Edge case handling

7. **WebSocket Integration** (for navigate-all, lock-editing)
   - Channel layer message format
   - Consumer handling
   - Broadcasting logic

8. **Test Specifications**
   - Test class structure
   - Fixtures needed
   - Test cases for success and failure paths
   - Mock/patch strategy for external dependencies

---

## Step 5: Phase 5-8 Deep Dive - Frontend Components (Session 4 - ~60 min)

### Create Detailed Implementation Guides

**Task:** Generate complete specifications for frontend development

**Output Documents:**
- `PHASE5_FACILITATOR_PANEL_COMPONENT.md`
- `PHASE6_SHARED_COMPONENTS.md`
- `PHASE7_MEETING_VIEWS.md`
- `PHASE8_ROUTER_CLEANUP.md`

**For Each Component, Specify:**

1. **Component Template Structure**
   ```vue
   <!-- Example level of detail needed: -->
   <template>
     <div class="facilitator-panel">
       <!-- Exact HTML structure -->
       <!-- Tailwind classes specified -->
       <!-- v-bind, v-on, v-model directives -->
     </div>
   </template>
   ```

2. **Component Script Structure**
   ```javascript
   // Exact imports
   // Data properties with types
   // Computed properties
   // Methods with signatures
   // Lifecycle hooks
   // API calls with error handling
   ```

3. **Styling Guidelines**
   - Tailwind utility classes
   - Custom CSS if needed
   - Responsive breakpoints
   - Color scheme consistency

4. **Props and Events**
   - Parent-child communication
   - Event naming conventions
   - Prop validation

5. **State Management**
   - Component-local state
   - Props from parent
   - Vuex usage (if needed)
   - API data caching strategy

6. **API Integration**
   - Which endpoints to call
   - When to call them (mounted, on user action)
   - Loading states
   - Error handling and user feedback

7. **Composition Strategy**
   - How components nest
   - Code reuse patterns
   - Extraction from existing components

8. **Test Specifications**
   - Unit test structure
   - Component testing with Vue Test Utils
   - Mock API responses
   - User interaction tests

---

## Step 6: Test Scenarios & Acceptance Criteria (Session 5 - ~30 min)

### Create Comprehensive Test Documentation

**Task:** Define complete testing strategy for refactoring

**Output Document:** `TESTING_STRATEGY.md`

**Required Contents:**

1. **Unit Test Scenarios**
   - Backend: Model methods, serializers, utilities
   - Frontend: Component logic, utilities, composables

2. **Integration Test Scenarios**
   - API endpoint tests (request → database → response)
   - Component integration tests (parent-child communication)

3. **End-to-End Test Scenarios**
   - Full user flows with expected outcomes:
     - Facilitator login → facpanel → configure → start → facmeet → controls → end
     - Participant login → meeting → view/edit → leave
     - Multiple sessions same circle
     - Different documents different sessions
     - Edge cases (no previous session, invalid selections, concurrent users)

4. **Acceptance Criteria**
   - What "done" means for each phase
   - Quality gates (all tests pass, no console errors, etc.)
   - Performance benchmarks

5. **Regression Test Checklist**
   - Existing features that must still work
   - Routes that must still function
   - Data that must not be corrupted

---

## Step 7: Migration Strategy Document (Session 6 - ~30 min)

### Create Risk Management Plan

**Task:** Detailed migration strategy for production deployment

**Output Document:** `MIGRATION_STRATEGY.md`

**Required Contents:**

1. **Pre-Migration Checklist**
   - Backup strategy
   - Downtime window planning
   - Stakeholder communication
   - Rollback readiness

2. **Migration Execution Plan**
   - Step-by-step commands
   - Verification at each step
   - Time estimates
   - Go/no-go decision points

3. **Breaking Changes Communication**
   - What will break
   - User impact
   - Mitigation strategies
   - User communication templates

4. **Data Migration Specifics**
   - Existing data transformation
   - Data validation post-migration
   - Handling edge cases

5. **Rollback Procedure**
   - Database rollback
   - Code rollback
   - Restore from backup
   - Recovery time estimate

---

## Step 8: API Specification Document (Session 7 - ~30 min)

### Create Complete API Reference

**Task:** Generate OpenAPI-style documentation for all endpoints

**Output Document:** `API_SPECIFICATION.md`

**Format:** For each endpoint:

```markdown
### GET /api/circles/:id/panel-info

**Purpose:** Load facilitator panel with circle details and last session defaults

**Authentication:** Required (Facilitator role)

**URL Parameters:**
- `id` (integer, required): Circle primary key

**Request Headers:**
```
Authorization: Bearer <token>
```

**Success Response (200 OK):**
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

**Error Responses:**
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: User is not facilitator for this circle
- `404 Not Found`: Circle does not exist

**Implementation Notes:**
- Check user's access_key.circle.id matches circle_id
- Query TranslationSession.objects.filter(circle=circle).order_by('-ended_at').first()
- Handle case where last_session is None (new circle)
```

**Repeat for all endpoints in Phases 3-4**

---

## Step 9: Code Review Session (After Implementation - ~30 min)

### Post-Implementation Review

**Task:** Review completed implementation via GitHub

**When:** After Claude Code (CLI) completes implementation

**What to Review:**
1. Pull requests or commits for Phases 1-9
2. Code quality and consistency
3. Test coverage
4. Documentation completeness
5. Security considerations
6. Performance implications

**Output Document:** `CODE_REVIEW_FEEDBACK.md`
- What was done well
- Issues to address
- Optimization opportunities
- Security concerns
- Next steps

---

## Deliverables Summary

**Documents to Generate (bring back to Claude Code for implementation):**
1. ✅ BACKEND_CHANGES_REQUIRED.md
2. ✅ FRONTEND_CHANGES_REQUIRED.md
3. ✅ PHASE1_DATABASE_IMPLEMENTATION.md
4. ✅ PHASE2_AUTHENTICATION_IMPLEMENTATION.md
5. ✅ PHASE3_FACILITATOR_PANEL_APIs_IMPLEMENTATION.md
6. ✅ PHASE4_FACILITATOR_CONTROL_APIs_IMPLEMENTATION.md
7. ✅ PHASE5_FACILITATOR_PANEL_COMPONENT.md
8. ✅ PHASE6_SHARED_COMPONENTS.md
9. ✅ PHASE7_MEETING_VIEWS.md
10. ✅ PHASE8_ROUTER_CLEANUP.md
11. ✅ TESTING_STRATEGY.md
12. ✅ MIGRATION_STRATEGY.md
13. ✅ API_SPECIFICATION.md
14. ✅ CODE_REVIEW_FEEDBACK.md (post-implementation)

**Estimated Credit Usage:**
- ~7 sessions × ~30-60 min each
- Deep analysis, code generation, specification writing
- High-value strategic work

**Success Criteria:**
- Claude Code (CLI) can implement Phases 1-9 by following your detailed specs
- No ambiguity in implementation instructions
- All edge cases documented
- Complete test coverage specified

---

## Tips for Working with Web Claude

1. **Use GitHub Integration:** Point it at scott009/InquiryCircle repo
2. **Request Complete Specs:** Ask for copy-pasteable code, not just descriptions
3. **Iterate on Docs:** Have it refine specs if something is unclear
4. **Save Everything:** Download all markdown files it generates
5. **Be Specific:** "Generate complete Django migration code" not "plan migration"
6. **Ask for Examples:** Request code examples, sample data, test fixtures
7. **Get SQL Too:** Ask for raw SQL queries for complex database operations

---

## Handing Off to Claude Code

After generating all specs:
1. Save all markdown files to `/mnt/c/Users/scott/Documents/AIProjects/Markdown/docs-websystems/projects/inquirycircle/web-claude-specs/`
2. Run context-loader.sh in Claude Code session
3. Point me to the specs directory
4. I'll execute implementation following the detailed guides
5. After implementation, bring web Claude back for code review

---

**Ready to start? Begin with Step 1: Load context into web Claude**
