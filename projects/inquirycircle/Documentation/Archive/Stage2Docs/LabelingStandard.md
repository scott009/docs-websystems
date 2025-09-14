<!-- InquiryCircle2 – LabelingStandard – Stage2 – 9/2/2025 at 7:10 AM ET -->  
<!-- accepted – 9/2/2025 at 7:25AM ET -->
# Labeling Standard
### Project & Document Nomenclature

This system defines simple, human-friendly labels for projects, subprojects, and their documentation lifecycle.  
It is designed to be durable across sessions and avoids the complexity of version control systems like Git.  

## Project / Subproject Naming
- **Project:** Use a short base name (e.g., `VotingApp`, `InquiryCircle`, `DockerIC`).  
- **Subproject:** Add a suffix to indicate scope (e.g., `VotingApp:catbench-deploy`, `DockerIC:learn-docker`).  

## Document Stage Labels
1. **Notes** → Freeform ideas and early discussion.  
2. **Draft** → Structured outline, still changing.  
3. **Accepted** → Agreed "one true version" to follow.  
4. **Completed** → Final state after project/subproject success.  
5. **Archived** → Past work, preserved for reference but no longer active.

## Timestamp Rule
- Every document label must include a **timestamp (date + hour:minute, no seconds)**.  
- The **latest timestamp is always authoritative** over earlier versions, regardless of stage label.  
- This rule applies consistently across all stages: Notes, Draft, Accepted, Completed, Archived.  
- A **timezone marker** should be included once at the top of the document   
  for clarity in collaborations (e.g., `ET`, `PT`, or `UTC`).    
      
## Additional Conventions  
### Superseded Mark 
If you keep older versions of the same file, mark them explicitly:
    <!-- VotingApp:catbench-deploy – Accepted – 8/22/2025 at 11:45 AM ET (superseded) -->  

## Accepted Abbreviations
- N = Notes
- D = Draft
- A = Accepted
- C = Completed
- AR = Archived

## Example Usage
```
# make a minor change to the voting app and redeploy
<!-- VotingApp:catbench-deploy – Accepted – 8/22/2025 at 11:45 AM ET -->
```
When finished:
```
<!-- VotingApp:catbench-deploy – Completed – 8/22/2025 at 3:15 PM ET -->
```
In this case, the 3:15 PM entry is authoritative over the 11:45 AM entry because it is the later timestamp.

## Document Types
The following document types are used in this project (all markdown files):

- **ArchitecturalOverview.md** - High-level system architecture, component relationships, and technical implementation strategy
- **ProjectBaseline.md** - Foundational project constraints, requirements, shared system context, and development principles  
- **devGuidance.md** - Development workflow instructions, coding standards, and project-specific developer guidelines
- **LabelingStandard.md** - Documentation nomenclature, stage labels, timestamp rules, and file organization conventions
- **Runbook.md** - Step-by-step operational procedures for deployment, maintenance, or specific technical tasks. Specialized runbooks might exist for specific procedures
- **Bookmark.md** - Session progress tracker, current status, and next task planning
- **SharedSystemContext.md** - Common environment definitions, system contexts, and cross-project infrastructure details  
- **readme.md** - Project overview, setup instructions, and getting started guide

*Note: Document types are explicitly marked with .md extension. Future projects may include other file types (.py, .yml, .txt, etc.).*