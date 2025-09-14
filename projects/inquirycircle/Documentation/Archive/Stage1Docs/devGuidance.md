# devGuidance

      
# Inquiry Circle Project Instructions

## Project Overview
- **Project Name**:Inquiry Circle
- **Environment**: SharedSystem Context
- **Purpose**: redme.md

## Critical Constraints
1. **DO NOT** modify the functioning of the cdv2 container without explicit permission
2. The cdv2 container must remain running at all times
3. The connection test at http://localhost:8080 must continue to work
4.  Do not attemp to run commands in powershell  
5. Do not change web page content without permission

## Connection Test Verification
Before making any changes, always verify the connection test shows:
Vue ↔ Django Test Load Records Bravo — hello — [timestamp] Alpha — 42 — [timestamp]


## File System Access
- WSL filesystem path: `\\wsl.localhost\Ubuntu\home\scott`
- Be cautious with file system operations to avoid affecting the running cdv2 container

## Workflow
1. Always check connection test before making changes
2. Make changes incrementally
3. Verify connection test after each change
4. Be prepared to rollback if the connection test fails
##Stop here
  
  
##  Milestones  
    Each milestone should include a documentd repeatable test
### Frontend  Milestones
    Once the Frontend milestones are reached merge the frontend branch into master

#### 1 - Routing
    status:{Done,tested,git branch tagged} 
#### 2- Tailwindcss with postcss    
    status:{Done,tested,git branch tagged}   
#### 3 - Pinia    
     status:{Done,tested,git branch tagged}  
####  4 - Axios    
     status:{Done,tested,git branch tagged} 
#### 5 -frontend healthcheck      
     status:{Done,tested,git branch tagged} 

    
