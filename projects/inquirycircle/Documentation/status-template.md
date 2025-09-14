# STATUS Documentation Template

## Purpose
This template provides optimal structure for STATUS.md updates to support the daily AI workflow pattern. Use this as a reference when updating your actual STATUS.md file.

---

## Template Structure

### **AI Session Handoff Section** (Always Include)
```markdown
## AI Session Context - [Date]

### Current Project State
- **Stage/Phase**: Stage 2.X.X - [brief description] 
- **Last Stable Deployment**: [date/commit] - [what's working]
- **System Health**: ✅ All systems operational | 🔄 Issues detected | ❌ System down

### Test Credentials (Current)
- **Facilitator Key**: `facilitator-key-123`
- **Participant Key**: `participant-key-456`
- **Backup Keys**: [if any alternates exist]

### Known Issues/Blockers
- [Issue 1]: [impact] - [workaround if any]
- [Issue 2]: [impact] - [next steps]
- **None** - [if no current issues]

### Environment Status
- **WSL Development**: [working/issues]
- **VPS Production**: [working/issues] 
- **External Services**: Jitsi [operational/issues]
```

### **Current Tasks Section** (Daily Focus)
```markdown
## Today's Tasks - [Date]

### In Progress
- **Task 1**: [description] - [current step/progress]
- **Task 2**: [description] - [blockers/next actions]

### Next Up
- **Priority 1**: [description] - [ready/waiting on X]
- **Priority 2**: [description] - [dependencies]

### Recently Completed
- **[Date]**: [Task] - [outcome/evidence]
- **[Date]**: [Task] - [verification steps taken]
```

### **Evidence & Health Checks** (Verification Focus)
```markdown
## System Verification - [Date/Time]

### Last Health Check Results
```bash
# Development
curl http://localhost:8080/api/health/
# Result: {"status": "healthy", "database": "connected"}

# Production  
curl https://catbench.com/api/health/
# Result: [actual response]
```

### Container Status
```bash
docker-compose ps
# [paste actual output showing service states]
```

### Recent Changes Evidence
- **[Change 1]**: [command executed] → [result/verification]
- **[Change 2]**: [test performed] → [outcome]
```

### **Development Session Notes** (Progress Tracking)
```markdown
## Session Log - [Date]

### What We Accomplished
- [Achievement 1] - [verification method]
- [Achievement 2] - [evidence captured]

### Issues Encountered
- **Issue**: [description]
- **Solution**: [what fixed it] 
- **Prevention**: [how to avoid next time]

### Next Session Prep
- **Immediate Tasks**: [ready to execute]
- **Blockers to Resolve**: [dependencies needed]
- **Questions for AI**: [specific help needed]
```

---

## AI Integration Guidelines

### **Daily Session Startup**
When starting an AI session, provide:
1. **AI Session Context** section (current state)
2. **Today's Tasks** section (current focus)
3. **Last Health Check Results** (system verification)

### **During Development**
Update these sections in real-time:
- Log each significant action in **Session Log**
- Capture evidence of changes in **Evidence & Health Checks**
- Update task progress in **Current Tasks**

### **Session End**  
Always update:
- **Current Project State** (new stable point)
- **Next Session Prep** (handoff for future)
- **Recently Completed** (move finished tasks)

---

## Quick Reference Commands

### Status Check Commands (copy/paste ready)
```bash
# System Health
curl http://localhost:8080/api/health/
curl https://catbench.com/api/health/

# Container Status
docker-compose ps

# Git Status
git status --porcelain

# Recent Activity
git log --oneline -5
```

### Evidence Capture Pattern
```markdown
### [Action Taken] - [Timestamp]
**Command**: `[exact command executed]`
**Result**: 
```
[paste actual output]
```
**Verification**: [how success was confirmed]
**Impact**: [what this changed/enabled]
```

---

## Template Usage Notes

### **For Daily AI Sessions**
- Copy relevant sections from this template
- Fill in current actual data  
- Paste into daily communication with AI
- Keep focused on current session needs

### **For Status Documentation**
- Use this structure in your actual STATUS.md
- Adapt sections based on current project needs
- Archive completed sections regularly
- Maintain current state accuracy

### **For Handoffs**
- **Session-to-session**: Focus on "Next Session Prep"
- **AI-to-AI**: Ensure "AI Session Context" is current
- **Problem escalation**: Include full "Evidence & Health Checks"

---

**Related Documentation**:  
[operations-guide](./operations-guide.md) | [project-spec](./project-spec.md) | [infrastructure](./infrastructure.md)

**Template Version**: v1.0.0 | **Created**: 9/12/2025 | **Purpose**: AI Workflow Optimization