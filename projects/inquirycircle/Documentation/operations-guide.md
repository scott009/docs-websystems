
<!-- InquiryCircle2 – OperationsGuide – Stage2 – 9/12/2025 at 8:45 AM ET -->

# Operations Guide

## Purpose
Define *how* to build, test, deploy, and operate InquiryCircle in Stage 2.  
This document is procedural: it captures development workflows, deployment steps, guardrails, and troubleshooting. Strategic constraints and architecture live in ProjectSpec.md.

---

## AI Assistant Instructions (Deploy-as-Commit Pattern)

### AI Context Loading Protocol
**Model Hint: Claude Haiku** ✨ *Simple session initialization for new AI models*

When starting a new AI session (especially when switching models):
```bash
# Run the context loader to bring AI up to speed
/home/scott/inquirycircle/context-loader.sh
```

This script loads all canonical documentation from DOCS-ENV:
- **project-spec.md** - Architecture and constraints
- **STATUS.md** - Current progress and priorities
- **operations-guide.md** - Procedures and commands
- **infrastructure.md** - Environment setup
- **CHANGELOG.md** - Documentation evolution

### Daily Session Startup Protocol
**Model Hint: Claude Haiku** ✨ *Simple session initialization tasks*

When continuing work in an existing session:
1. **Check current STATUS.md** - review latest progress and tasks
2. **Execute health checks** - verify system state before proceeding
3. **Capture evidence** - logs, outputs, screenshots at each step

For new sessions, use the AI Context Loading Protocol above first.

### Deployment Pattern (Incremental & Safe)
**Model Hint: Claude Sonnet 4** 🧠 *Deployment requires risk assessment, decision-making, and rollback readiness*

When deploying changes:
1. **Pre-deployment verification**:
   ```bash
   curl https://localhost/api/health/ -k      # Verify local health
   docker-compose ps                          # Check container status  
   git status                                 # Verify clean working tree
   ```

2. **Incremental deployment steps**:
   - Apply one change at a time
   - Test each change before proceeding  
   - Capture evidence of success/failure
   - Be ready to rollback at any step

3. **Post-deployment verification**:
   ```bash
   curl https://catbench.com/api/health/      # Verify production health
   docker-compose logs --tail=20 caddy       # Check for errors
   docker-compose logs --tail=20 backend     # Check application logs
   ```

4. **Rollback triggers** (execute immediately if detected):
   - Health check returns non-200 status
   - Critical error in application logs
   - Any 5xx errors in production
   - Container restart loops

### AI Evidence Requirements
**Model Hint: Claude Haiku** ✨ *Documentation and evidence capture*

Always provide evidence for:
- Command outputs (especially curl responses)
- Container status (`docker-compose ps` output)  
- Log snippets when troubleshooting
- Before/after comparisons for changes
- Health check results at each deployment step

### AI Error Response Protocol  
**Model Hint: Claude Sonnet 4** 🧠 *Error analysis and recovery decisions require advanced reasoning*

When encountering errors:
1. **Stop immediately** - don't proceed with additional changes
2. **Capture full error details** - logs, error messages, stack traces
3. **Reference troubleshooting tables** - find matching error pattern
4. **Execute diagnostic commands** - gather more information
5. **Propose rollback if uncertain** - safety first approach

### STATUS.md Integration Points
The AI should check STATUS.md for:
- **Current project version/phase** - determines active procedures
- **Recent changes** - what was last modified or deployed
- **Known issues** - existing problems to be aware of
- **Test keys** - current authentication credentials
- **Next tasks** - what needs to be accomplished

### AI Frontend Change Deployment Protocol
**Model Hint: Claude Sonnet 4** 🧠 *Frontend changes require containerized build workflow*

**Critical Understanding**: The frontend is containerized and served through Docker/nginx. Vue component changes do NOT appear in the browser until the Docker container is rebuilt.

**Required Steps for ANY Frontend Change**:
1. **Build the Vue frontend locally**:
   ```bash
   cd /home/scott/inquirycircle/frontend && npm run build
   ```

2. **Rebuild the frontend Docker container**:
   ```bash
   cd /home/scott/inquirycircle/compose
   docker-compose -f docker-compose.dev.yml up -d --build frontend
   ```

3. **Verify deployment**:
   ```bash
   # Check new build files exist
   docker exec ic-frontend ls -la /usr/share/nginx/html/assets/

   # Verify component is in bundle (replace ComponentName)
   docker exec ic-frontend grep -o "ComponentName" /usr/share/nginx/html/assets/[bundle-name].js
   ```

**When to Use This Protocol**:
- Creating new Vue components
- Editing existing Vue components
- Changing styles in Vue files
- Modifying Vue templates
- Any change to `/home/scott/inquirycircle/frontend/src/`

**User Instruction**: After deployment, user must hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R) to bypass cache.

**Common Mistake**: Running only `npm run build` without rebuilding the container. The container serves files from its internal `/usr/share/nginx/html/` directory, not from the local `dist/` folder.

### AI Documentation Commit Protocol (docs-env)
  **Model Hint: Claude Haiku** ✨ *Simple documentation maintenance tasks*
  When working in the docs-env environment to commit documentation changes:

#### Environment Verification
We are now working in the DOCS-ENV environment  
The Remote repo when working in the DOCS-ENV environment is     https://github.com/scott009/docs-websystems

  1. Navigate to docs-env directory:
  cd /mnt/c/Users/scott/Documents/AIProjects/Markdown/docs-websystems/projects/inquirycircle
  2. Check git status:    git status
  3. Add documentation files:   # For STATUS.md updates
  git add Documentation/STATUS.md

  # For other documentation files:
  git add Documentation/[filename].md
  4. Commit with standard format:
  git commit -m "$(cat <<'EOF'
  [Brief description of changes]
  EOF
  )"

  5. Push to repository:
  git push origin main

  Common Documentation Files

  - Documentation/STATUS.md - Project status and progress
  - Documentation/project-spec.md - Architecture and constraints
  - Documentation/operations-guide.md - Procedures and workflows
  - Documentation/infrastructure.md - Environment setup
  - Documentation/CHANGELOG.md - Documentation evolution

  Sample Commit Messages
  - "Update STATUS.md for Stage X.X.X: [brief feature description]"
  - "Add new documentation for [feature/component name]"
  - "Revise project specifications for [specific change]"
  - "Update operations guide with [new procedure/protocol]"
  Error Handling
  - If git commands fail, verify location with pwd
  - Use ls Documentation/ to confirm files exist
  - Check git repository status if push fails


---

## Development Guardrails
- Operate only in **bash** on WSL and VPS (no PowerShell).  
- All VPS actions are done by the operator over SSH. AI may suggest commands, but must not assume execution access
- When creating files, use `echo "..." > filename` for the first line and  
  `echo "..." >> filename` for subsequent lines (instead of heredocs). 
- Keep filesystem locations as documented in Infrastructure.md.  
- Proceed incrementally: verify each step before moving forward.  
- Be rollback-ready at all times (retain prior configs and builds).  
- Capture evidence: logs, health checks, curl outputs, screenshots.  
- Use test keys in development; production keys stored securely in `/etc/inquirycircle/env`.

---

## Command Reference (Complete)

### Development Environment Commands
**Model Hint: Claude Haiku** ✨ *Simple navigation and startup commands*

```bash
# Project Navigation
cd /home/scott/inquirycircle                 # Project root (WSL)
cd frontend && npm run dev                   # Frontend dev server (localhost:5173)
cd backend && source venv/bin/activate      # Activate Python environment
cd backend && python manage.py runserver    # Backend dev server (localhost:8000)

# Frontend Operations
npm install                                  # Install dependencies
npm run build                               # Build for production
npm run test:unit                           # Run unit tests
npm run test:e2e                            # Run end-to-end tests
cp -r dist/* ../caddy/site/                 # Deploy built assets

# Backend Operations
pip install -r requirements.txt             # Install Python dependencies
python manage.py migrate                    # Run database migrations
python manage.py makemigrations            # Create new migrations
python manage.py test                      # Run Django tests
python manage.py shell                     # Django shell
python manage.py collectstatic --noinput   # Collect static files

# Docker Operations (Development)
cd compose                                  # Navigate to compose directory
docker-compose -f docker-compose.dev.yml up -d     # Start all services (detached)
docker-compose -f docker-compose.dev.yml down      # Stop all services
docker-compose -f docker-compose.dev.yml restart [service]  # Restart specific service
docker-compose logs -f [service]           # Follow logs for service
docker-compose ps                          # Show service status
docker stats                               # Show resource usage

# Container Management
docker exec -it [container_name] /bin/bash # Enter container shell
docker system prune -f                     # Clean up unused resources
docker images                              # List images
docker volume ls                           # List volumes
```

### Frontend Development Workflow
**Required for ALL Frontend Changes**

The frontend is containerized and served through Docker/nginx. Changes to Vue components require a complete build-and-deploy cycle to appear in the browser.

**Standard Workflow**:
```bash
# 1. Build the Vue frontend
cd /home/scott/inquirycircle/frontend
npm run build

# 2. Rebuild and restart the frontend container
cd /home/scott/inquirycircle/compose
docker-compose -f docker-compose.dev.yml up -d --build frontend

# 3. Verify deployment
docker exec ic-frontend ls -la /usr/share/nginx/html/assets/  # Check timestamps
docker-compose -f docker-compose.dev.yml ps                   # Verify container running

# 4. Clear browser cache and hard refresh
# Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
```

**When to Use This Workflow**:
- Creating new Vue components
- Editing existing Vue components
- Changing styles in `.vue` files
- Modifying Vue templates
- Any change to `/home/scott/inquirycircle/frontend/src/`

**Verification Tips**:
```bash
# Check if specific component is in bundle
docker exec ic-frontend grep -o "ComponentName" /usr/share/nginx/html/assets/VideoTestDemo-*.js

# View frontend container logs
docker-compose -f docker-compose.dev.yml logs --tail=20 frontend
```

**Common Pitfalls**:
- ❌ Running only `npm run build` → changes won't appear (container not updated)
- ❌ Skipping browser cache clear → old version still visible
- ❌ Checking too quickly → container may still be starting (wait 5-10 seconds)

### Production Environment Commands  
**Model Hint: Claude Sonnet 4** 🧠 *Production deployment requires careful evaluation and rollback readiness*

```bash
# VPS Access & Navigation
ssh user@catbench.com                      # SSH to production server
cd /srv/inquirycircle                      # Production project root

# Deployment Operations
git pull                                   # Update code from GitHub
docker-compose down                        # Stop current services
docker-compose up -d --build             # Build and start services
docker-compose -f docker-compose.prod.yml up -d --build  # Production specific

# Production Monitoring
curl https://catbench.com/api/health/     # Health check (should return JSON)
curl -I https://catbench.com              # Check HTTPS headers
curl -f https://icircle.catbench.com      # Test specific subdomain
docker-compose logs --tail=50 [service]   # View recent logs
```

### Health Check Commands
**Model Hint: Claude Haiku** ✨ *Simple verification commands with predictable outputs*

```bash
# Quick Health Verification (Single Command)
curl https://localhost/api/health/ -k && echo " ✅ Local OK" || echo " ❌ Local Failed"
curl https://catbench.com/api/health/ && echo " ✅ Prod OK" || echo " ❌ Prod Failed"

# Local Development Health Checks
curl https://localhost/api/health/ -k      # Full stack through Caddy (HTTPS)
curl http://localhost/api/health/          # Full stack through Caddy (HTTP)
docker-compose ps | grep -v Exit           # Check all services running

# Production Health Checks
curl https://catbench.com/api/health/      # Production API health
curl https://icircle.catbench.com/api/health/  # Subdomain health
curl -f -s -o /dev/null https://catbench.com && echo "HTTPS OK" || echo "HTTPS FAIL"

# Database Health Checks
cd backend && python manage.py shell -c "from django.db import connection; cursor = connection.cursor(); cursor.execute('SELECT 1'); print('DB OK')"
```

### Emergency/Troubleshooting Commands
**Model Hint: Claude Sonnet 4** 🧠 *Emergency situations require careful analysis and decision-making*

```bash
# Service Recovery
docker-compose restart caddy              # Restart reverse proxy
docker-compose restart backend            # Restart API server
systemctl status docker                   # Check Docker daemon

# Log Investigation
docker-compose logs --tail=100 caddy      # Caddy access/error logs
docker-compose logs --tail=100 backend    # Django application logs
journalctl -u docker -f                   # Docker system logs

# Quick Rollback
git checkout HEAD~1                        # Rollback code to previous commit
docker-compose down && docker-compose up -d  # Redeploy previous version

# Resource Cleanup
docker system prune -a -f                 # Clean all unused Docker resources
docker volume prune -f                    # Clean unused volumes
```

---

## Development Workflow

### Environment Setup
- **Frontend prerequisites**: Node.js 18+, npm.  
- **Backend prerequisites**: Python 3.10+, Django, virtualenv.  
- **Containers**: Docker + Docker Compose installed in WSL.  
- **Git**: Configured for repo `scott009/InquiryCircle`.

### Local Development Structure
/home/scott/inquirycircle/
├── compose/ # Docker compose configurations
├── caddy/ # Reverse proxy configs and static site
├── frontend/ # Vue 3 + Tailwind + Jitsi
├── backend/ # Django REST API
└── Documentation/

yaml
Copy code

---

## Complete Procedure Checklists

### Frontend Development Checklist
**Model Hint: Claude Haiku** ✨ *Routine setup and verification tasks*

**Initial Setup**
- [ ] Node.js 18+ installed
- [ ] Navigate to `cd frontend`
- [ ] Run `npm install` (verify no errors)
- [ ] Verify `package.json` includes Vue 3, Tailwind, Jitsi SDK

**Development Mode**
- [ ] Run `npm run dev` → should show "Local: http://localhost:5173"
- [ ] Open browser to http://localhost:5173
- [ ] Verify hot-reload works (make a change, see it update)
- [ ] Check browser console for errors (should be clean)

**Build and Deploy Process**
- [ ] Run `npm run build` (should complete without errors)  
- [ ] Verify `dist/` directory created with files
- [ ] Copy assets: `cp -r dist/* ../caddy/site/`
- [ ] Verify files copied to caddy/site/ directory
- [ ] Test production build at http://localhost:8080 (through Caddy)

**Frontend Testing Checklist**  
**Model Hint: Claude Sonnet 4** 🧠 *Complex integration testing requiring analysis of multiple systems*

- [ ] Vue Router navigation works (test all routes)
- [ ] Tailwind styles apply correctly (check responsive design)
- [ ] Jitsi SDK loads without errors (check browser console)
- [ ] API calls to backend succeed (test in Network tab)
- [ ] Key-based authentication flow works (test valid/invalid keys)
- [ ] Facilitator vs participant roles display correctly
- [ ] Video conferencing interface loads
- [ ] Facilitator messaging interface functions

### Backend Development Checklist
**Model Hint: Claude Haiku** ✨ *Standard Django setup procedures*

**Initial Setup**
- [ ] Python 3.10+ installed
- [ ] Navigate to `cd backend`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate environment: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify no dependency conflicts

**Development Mode**
- [ ] Run migrations: `python manage.py migrate`
- [ ] Check database file created: `ls -la db/inquirycircle.db`
- [ ] Start server: `python manage.py runserver`
- [ ] Verify server starts on http://localhost:8000
- [ ] Check Django admin interface loads

**API Testing Checklist**  
**Model Hint: Claude Sonnet 4** 🧠 *API testing requires response analysis and error interpretation*

- [ ] Health endpoint: `curl http://localhost:8000/api/health/` → JSON response
- [ ] Auth endpoint with valid facilitator key → `{"valid": true, "role": "facilitator"}`
- [ ] Auth endpoint with valid participant key → `{"valid": true, "role": "participant"}`  
- [ ] Auth endpoint with invalid key → `{"valid": false, "error": "Invalid key"}`
- [ ] Circle creation: POST to `/api/circles/` → creates circle
- [ ] Circle retrieval: GET `/api/circles/` → returns circles list
- [ ] Message creation: POST to `/api/messages/` → saves message
- [ ] Message retrieval: GET `/api/messages/` → returns messages

**Database Verification**
- [ ] SQLite file exists: `ls -la backend/db/inquirycircle.db`
- [ ] Migrations applied: `python manage.py showmigrations` (all [X])
- [ ] Tables created: Check via Django shell
- [ ] Test data persists across server restarts
- [ ] Database connections work: Test via shell command

### Docker Integration Checklist
**Model Hint: Claude Sonnet 4** 🧠 *Multi-container integration requires system-level thinking*

**Development Stack**
- [ ] Navigate to `cd compose`
- [ ] Environment file exists: check `.env` or `.env.example`
- [ ] Run: `docker-compose -f docker-compose.dev.yml up -d`
- [ ] Verify all containers start: `docker-compose ps` (all "Up")
- [ ] Check container logs: `docker-compose logs` (no errors)
- [ ] Test Caddy routing: http://localhost:8080 → frontend
- [ ] Test API proxying: http://localhost:8080/api/health/ → backend JSON

**Integration Verification**
- [ ] Frontend loads through Caddy reverse proxy
- [ ] API calls from frontend reach backend successfully  
- [ ] Jitsi integration works through frontend
- [ ] Authentication flow works end-to-end
- [ ] Data persists across container restarts
- [ ] All services communicate on Docker network
- [ ] Volume mounts work correctly (database, static files)

Integration via Docker Compose
Start Full Stack (dev)


cd compose
docker-compose -f docker-compose.dev.yml up -d
Verify

Caddy serves frontend at http://localhost:8080

API proxied at http://localhost:8080/api

Jitsi sessions load (external service)

Data persists across restarts

Testing Procedures
Frontend


cd frontend
npm run test:unit
npm run test:e2e
Backend


cd backend
python manage.py test
Integration


docker-compose -f docker-compose.dev.yml up
npm run test:integration
Deployment Procedures
WSL Dry-Run


docker-compose -f docker-compose.prod.yml up -d
VPS Deployment


ssh user@catbench.com
cd /srv/inquirycircle
git pull
docker-compose down
docker-compose up -d --build
Verify


curl https://catbench.com/api/health/
## Troubleshooting Reference (Complete)

**Model Hint: Claude Sonnet 4** 🧠 *All troubleshooting requires analysis, pattern recognition, and decision-making*

### Network & Connectivity Issues
| Error Pattern | Symptoms | Root Cause | Quick Fix | Deep Fix |
|--------------|----------|------------|-----------|----------|
| 502 Bad Gateway | Browser shows 502, Caddy can't reach backend | Backend container down/not responding | `docker-compose restart backend` | Check resource limits, backend logs |
| 504 Gateway Timeout | Request hangs, then 504 error | Backend slow response or deadlock | `docker-compose restart backend` | Investigate database locks, optimize queries |
| Connection Refused | `curl: (7) Failed to connect` | Service not running on expected port | `docker-compose ps` → `docker-compose up -d [service]` | Check port bindings in compose file |
| No HTTPS | HTTPS fails, HTTP works | Caddy TLS issue, DNS problem | `docker-compose logs caddy` | Check DNS A records, firewall ports 80/443 |
| DNS Resolution Fails | `nslookup` fails for domain | DNS configuration issue | Check A records at registrar | Wait for DNS propagation (up to 48h) |

### Application-Level Issues  
| Error Pattern | Symptoms | Root Cause | Quick Fix | Deep Fix |
|--------------|----------|------------|-----------|----------|
| Auth keys not working | 401/403 errors on API calls | Invalid key format or DB corruption | Check key format in STATUS.md | Verify database schema, reload test keys |
| Jitsi not loading | Video interface blank/error | External Jitsi API issue or config | Check Jitsi service status | Verify API keys, check external dependencies |
| API returns HTML not JSON | API endpoints return Django error pages | Django misconfiguration or crash | `docker-compose logs backend` | Check Django settings, database connection |
| Frontend stale content | Changes not reflected in browser | Browser cache or build cache issue | Hard refresh (Ctrl+F5), rebuild frontend | `npm run build && cp -r dist/* ../caddy/site/` |
| Database errors | 500 errors, "database locked" | SQLite file corruption or permissions | `docker-compose restart backend` | Check volume mounts, file permissions |

### Container & Infrastructure Issues
| Error Pattern | Symptoms | Root Cause | Quick Fix | Deep Fix |
|--------------|----------|------------|-----------|----------|
| Container won't start | `docker-compose ps` shows Exit status | Image build failure or resource limits | `docker-compose logs [service]` | Check Dockerfile, available memory/disk |
| Volume mount issues | Database doesn't persist across restarts | Incorrect volume configuration | Check `docker-compose.yml` volume syntax | Verify host paths exist, check permissions |
| Out of disk space | Containers fail to start, builds fail | Docker images/volumes consuming disk | `docker system prune -a -f` | Monitor disk usage, implement cleanup policies |
| Memory issues | Containers randomly restart, slow performance | Insufficient memory allocation | `docker stats` to check usage | Increase WSL2 memory limit, optimize containers |
| Port conflicts | "Port already in use" error | Another service using same port | `netstat -tulpn \| grep [port]` | Change port in compose file or stop conflicting service |

### Development-Specific Issues
| Error Pattern | Symptoms | Root Cause | Quick Fix | Deep Fix |
|--------------|----------|------------|-----------|----------|
| npm commands fail | Package install/build errors | Node version or dependency issues | `rm -rf node_modules && npm install` | Check Node version, update package.json |
| Python/Django errors | Import errors, migration failures | Virtual environment or dependency issues | `source venv/bin/activate && pip install -r requirements.txt` | Recreate virtual environment |
| Git sync issues | Merge conflicts, push failures | Repository state mismatch | `git status && git stash && git pull` | Resolve conflicts manually, force push if needed |
| Build failures | Frontend/backend won't build | Missing dependencies or config errors | Check build logs for specific errors | Update dependencies, fix configuration files |

### Production-Specific Issues  
| Error Pattern | Symptoms | Root Cause | Quick Fix | Deep Fix |
|--------------|----------|------------|-----------|----------|
| TLS certificate issues | HTTPS warnings, expired cert errors | Caddy certificate renewal failed | `docker-compose restart caddy` | Check DNS, firewall, Caddy logs |
| Resource exhaustion | Site slow/unresponsive, high load | VPS overloaded | `docker stats` → restart heavy containers | Scale VPS resources, optimize containers |
| Security alerts | Failed auth attempts, unusual traffic | Brute force or bot attacks | Check access logs, block IPs | Implement rate limiting, security headers |

### Diagnostic Commands by Issue Type
**Model Hint: Claude Haiku** ✨ *Simple diagnostic commands with predictable outputs*

```bash
# Network Issues
curl -v https://catbench.com/api/health/     # Full connection test
nslookup catbench.com                        # DNS resolution test
telnet catbench.com 443                      # Port connectivity test

# Application Issues  
docker-compose logs --tail=100 backend      # Backend application logs
docker-compose logs --tail=100 caddy        # Reverse proxy logs
curl -H "Authorization: Key facilitator-key-123" localhost:8080/api/auth/verify-key/

# Container Issues
docker system df                             # Disk usage by containers
docker stats --no-stream                    # Memory/CPU usage snapshot
docker-compose config                        # Validate compose file syntax

# Database Issues
cd backend && python manage.py shell -c "from django.db import connection; connection.ensure_connection()"
ls -la backend/db/                           # Check database file permissions
```

## Rollback and Recovery Procedures (Complete)

### Emergency Rollback (< 2 minutes)
**Model Hint: Claude Sonnet 4** 🧠 *Critical production decisions require careful evaluation and speed*

When production is down or critically broken:

```bash
# 1. Immediate service restoration (run on VPS)
ssh user@catbench.com
cd /srv/inquirycircle
docker-compose down                          # Stop broken services
git checkout HEAD~1                          # Rollback code to previous commit  
docker-compose up -d                         # Start with previous version

# 2. Verify rollback success  
curl https://catbench.com/api/health/        # Should return {"status": "healthy"}
docker-compose ps                            # All services should show "Up"
```

### Targeted Rollback Procedures

#### Code Rollback (Git-based)
**Model Hint: Claude Haiku** ✨ *Standard git operations with clear outcomes*

```bash
# Check recent commits
git log --oneline -5                         # Show last 5 commits

# Rollback to specific commit
git checkout [commit-hash]                   # Rollback to specific commit
# OR
git reset --hard HEAD~1                     # Rollback 1 commit (permanent)
# OR  
git revert HEAD                              # Create new commit that undoes last change

# Redeploy after rollback
docker-compose down && docker-compose up -d --build
```

#### Frontend Rollback
```bash
# If frontend build is broken
cd frontend
git checkout HEAD~1 -- package.json         # Rollback package.json only
git checkout HEAD~1 -- src/                 # Rollback source code only
npm install && npm run build                # Rebuild
cp -r dist/* ../caddy/site/                 # Redeploy
```

#### Backend Rollback  
```bash
# Database migration rollback
cd backend && source venv/bin/activate
python manage.py migrate [app_name] [migration_number]  # Rollback to specific migration
# OR
python manage.py migrate [app_name] zero    # Rollback all migrations for app

# Code rollback
git checkout HEAD~1 -- backend/             # Rollback backend code only
docker-compose restart backend              # Restart with previous code
```

#### Configuration Rollback
```bash
# Docker Compose rollback
git checkout HEAD~1 -- compose/docker-compose.*.yml
docker-compose down && docker-compose up -d

# Environment variables rollback  
git checkout HEAD~1 -- compose/.env
docker-compose restart [affected-services]
```

### Database Recovery Procedures

#### SQLite Database Recovery
**Model Hint: Claude Sonnet 4** 🧠 *Database recovery requires careful data handling and verification*
```bash
# Create backup before any changes (always do this first)
cd backend && cp db/inquirycircle.db db/inquirycircle.db.backup.$(date +%Y%m%d_%H%M%S)

# Restore from backup
cp db/inquirycircle.db.backup.[timestamp] db/inquirycircle.db
docker-compose restart backend

# Export/import data for recovery
python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json   # Create export
python manage.py flush                                            # Clear database  
python manage.py migrate                                          # Recreate tables
python manage.py loaddata backup_[timestamp].json               # Restore data
```

#### Database Corruption Recovery
```bash
# Check database integrity
cd backend && python manage.py shell -c "
from django.db import connection
cursor = connection.cursor()  
cursor.execute('PRAGMA integrity_check;')
print(cursor.fetchall())
"

# If corruption detected:
mv db/inquirycircle.db db/corrupted_$(date +%Y%m%d_%H%M%S).db    # Preserve corrupted file
python manage.py migrate                                          # Create fresh database
# Restore from latest backup or rebuild from scratch
```

### Container Recovery Procedures

#### Individual Container Recovery
**Model Hint: Claude Haiku** ✨ *Standard container operations*
```bash
# Restart single container
docker-compose restart [service-name]       # Soft restart
docker-compose stop [service-name] && docker-compose up -d [service-name]  # Hard restart

# Rebuild single container
docker-compose stop [service-name]
docker-compose rm [service-name]            # Remove container
docker-compose up -d --build [service-name] # Rebuild and start

# Reset container to clean state
docker-compose down [service-name]
docker rmi inquirycircle_[service-name]     # Remove image
docker-compose up -d --build [service-name] # Force rebuild
```

#### Full Stack Recovery
```bash
# Nuclear option: rebuild everything
docker-compose down -v                      # Stop and remove volumes
docker system prune -a -f                   # Remove all unused containers/images
docker-compose up -d --build               # Rebuild entire stack from scratch
```

### Recovery Verification Checklist
**Model Hint: Claude Haiku** ✨ *Standard verification commands*

After any rollback/recovery:
- [ ] Health check returns 200: `curl https://catbench.com/api/health/`
- [ ] All containers running: `docker-compose ps` (all "Up")  
- [ ] No error logs: `docker-compose logs --tail=20`
- [ ] Authentication works: Test with valid key
- [ ] Frontend loads correctly: Visit https://catbench.com
- [ ] Database accessible: Test API endpoints
- [ ] SSL/TLS working: Check HTTPS certificate

### Recovery Time Objectives (RTO)
- **Emergency rollback**: < 2 minutes (service restoration)
- **Targeted rollback**: < 5 minutes (specific component)  
- **Database recovery**: < 10 minutes (from backup)
- **Full rebuild**: < 15 minutes (nuclear option)
Monitoring
Health


curl http://localhost:8080/api/health/
docker-compose ps
docker-compose logs -f [service]
docker stats
Security

Watch for failed auth attempts

Monitor cert expiry warnings

Check container restart frequency

Performance Tips
Frontend: bundle splitting, lazy loading

Backend: query optimization, DB indexing

Caddy: caching headers, compression

Jitsi: external service (no hosting overhead)

---

## STATUS.md Integration Reference

This operations guide provides **stable procedures**. For **current project state**, always check STATUS.md for:

### Current Status Indicators
- **Project phase/version** → Determines which procedures are active
- **Last successful deployment** → Baseline for rollback decisions  
- **Known issues** → Current problems affecting operations
- **Test credentials** → Authentication keys for testing
- **Recent changes** → What was modified since last stable state

### Daily Workflow Integration
**AI Session Start**: Read this guide + latest STATUS.md section  
**During Work**: Update STATUS.md with progress, issues, solutions
**Session End**: Update STATUS.md with current state, next steps

### STATUS.md Checkpoint Pattern
When making significant changes:
1. **Before**: Document current stable state in STATUS.md
2. **During**: Log each step and its outcome  
3. **After**: Update STATUS.md with new stable state or rollback

---

**Related Documentation**:  
[project-spec](./project-spec.md) | [infrastructure](./infrastructure.md) | [STATUS](./STATUS.md) | [status-template](./status-template.md)

**Document Version**: v2.1.0 | **Last Updated**: 9/12/2025 | **Status**: ✅ Production Ready