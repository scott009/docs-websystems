# LabelingStandard
###  Project & Runbook Nomenclature

This system defines simple, human-friendly labels for projects, subprojects, and their documentation lifecycle.  
It is designed to be durable across sessions and avoids the complexity of version control systems like Git.  


### Project / Subproject Naming
- **Project:** Use a short base name (e.g., `VotingApp`, `InquiryCircle`, `DockerIC`).  
- **Subproject:** Add a suffix to indicate scope (e.g., `VotingApp:catbench-deploy`, `DockerIC:learn-docker`).  



### Document Stage Labels
    1. **Notes** → Freeform ideas and early discussion.  
    2. **Draft** → Structured outline, still changing.  
    3. **Runbook** → Step-by-step instructions for execution.  
    4. **Accepted Runbook** → Agreed “one true version” to follow.  
    5. **Completed** → Final state after project/subproject success.  
    6. **Archived** → Past work, preserved for reference but no longer active.


### Timestamp Rule
    - Every document label must include a **timestamp (date + hour:minute, no seconds)**.  
    - The **latest timestamp is always authoritative** over earlier versions, regardless of stage label.  
    - This rule applies consistently across all stages: Notes, Draft, Runbook, Accepted Runbook, Completed.  
    - A **timezone marker** should be included once at the top of the document   
      for clarity in collaborations (e.g., `ET`, `PT`, or `UTC`).    
      
### Additional Conventions  
#### Superseded Mark 
    If you keep older versions of the same file, mark them explicitly:
        <!-- VotingApp:catbench-deploy – Accepted Runbook – 8/22/2025 at 11:45 AM ET (superseded) -->  

### Accepted Abreviations
    N = Notes
    D = Draft
    R = Runbook
    AR = Accepted Runbook
    C = Completed

### Example Usage
    # make a minor change to the voting app and redeploy
    <!-- VotingApp:catbench-deploy – Accepted Runbook – 8/22/2025 at 11:45 AM ET -->
When finished:
        <!-- VotingApp:catbench-deploy – Completed – 8/22/2025 at 3:15 PM ET -->
        In this case, the 3:15 PM entry is authoritative over the 11:45 AM entry because it is the later timestamp.

