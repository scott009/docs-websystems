<!-- {{PROJECT_NAME}} – OperationsGuide – Stage1 – {{TIMESTAMP}} -->

# Operations Guide

## Purpose
Define *how* to build, test, deploy, and operate {{PROJECT_NAME}}. This document is procedural: it captures development workflows, deployment steps, guardrails, and troubleshooting. Strategic constraints and architecture live in project-specification.md.

---

## AI Assistant Instructions (Deploy-as-Commit Pattern)

### Daily Session Startup Protocol
**Model Hint: Claude Haiku** ✨ *Simple session initialization tasks*

When starting a new session:
1. **Always read this operations-guide.md first** - contains stable procedures
2. **Request latest current-status.md section** - contains current tasks and state  
3. **Execute health checks** - verify system state before proceeding
4. **Capture evidence** - logs, outputs, screenshots at each step

### Deployment Pattern (Incremental & Safe)
**Model Hint: Claude Sonnet 4** 🧠 *Deployment requires risk assessment, decision-making, and rollback readiness*

When deploying changes:
1. **Pre-deployment verification**:
   ```bash
   curl http://localhost:[port]/health/     # Verify local health
   docker-compose ps                        # Check container status  
   git status                               # Verify clean working tree
   ```

2. **Incremental deployment steps**:
   - Apply one change at a time
   - Test each change before proceeding  
   - Capture evidence of success/failure
   - Be ready to rollback at any step

3. **Post-deployment verification**:
   ```bash
   curl https://[your-domain]/health/       # Verify production health
   docker-compose logs --tail=20 [service] # Check for errors
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
The AI should check current-status.md for:
- **Current project version/phase** - determines active procedures
- **Recent changes** - what was last modified or deployed
- **Known issues** - existing problems to be aware of  
- **Test credentials** - current authentication credentials
- **Next tasks** - what needs to be accomplished

---

## Development Guardrails
- Operate only in **bash** for development commands
- All production actions require explicit confirmation
- When creating files, use standard file creation methods
- Keep filesystem locations as documented in infrastructure.md
- Proceed incrementally: verify each step before moving forward
- Be rollback-ready at all times (retain prior configs and builds)
- Capture evidence: logs, health checks, curl outputs, screenshots
- Use test credentials in development; production credentials stored securely

---

## Command Reference (Complete)

### Development Environment Commands
**Model Hint: Claude Haiku** ✨ *Simple navigation and startup commands*

#### Navigation & Setup
```bash
# Navigate to project directory
cd [/path/to/project]

# Check git status
git status
git log --oneline -10

# Environment verification
docker --version
docker-compose --version
node --version  # if using Node.js
python --version  # if using Python
```

#### Local Development Server
```bash
# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# View running containers
docker-compose ps

# View logs
docker-compose logs -f [service-name]

# Stop development environment
docker-compose -f docker-compose.dev.yml down
```

### Health Check Commands
**Model Hint: Claude Haiku** ✨ *Standard verification commands*

```bash
# API health checks
curl -v http://localhost:[port]/health/
curl -v http://localhost:[port]/api/health/

# Service-specific health checks
curl -v http://localhost:[port]/api/status/
curl -v http://localhost:[port]/api/version/

# Container health
docker-compose ps
docker stats --no-stream
```

### Production Commands
**Model Hint: Claude Sonnet 4** 🧠 *Production deployment requires careful decision-making*

```bash
# Production health verification
curl -v https://[your-domain]/health/
curl -v https://[your-domain]/api/health/

# Production container management
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml logs --tail=50

# Production deployment (use with extreme caution)
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

### Emergency Commands
**Model Hint: Claude Sonnet 4** 🧠 *Emergency situations require immediate expert analysis*

```bash
# Emergency rollback (development)
docker-compose down
git checkout [previous-commit]
docker-compose up -d

# Emergency stop (production)
docker-compose -f docker-compose.prod.yml stop

# Emergency logs
docker-compose logs --tail=100 > emergency-logs-$(date +%Y%m%d-%H%M%S).txt
```

---

## Troubleshooting Reference

### Common Error Patterns
**Model Hint: Claude Sonnet 4** 🧠 *Error diagnosis requires pattern recognition and analysis*

#### Network/Connectivity Issues
| Symptom | Likely Cause | Diagnostic Command | Solution |
|---------|--------------|-------------------|----------|
| Connection refused | Service not running | `docker-compose ps` | Start the service |
| 502 Bad Gateway | Backend unreachable | `docker-compose logs backend` | Check backend health |
| Timeout | Network/firewall | `curl -v [url]` | Check networking |

#### Application Issues
| Symptom | Likely Cause | Diagnostic Command | Solution |
|---------|--------------|-------------------|----------|
| 500 Internal Error | Application crash | `docker-compose logs [service]` | Check error logs |
| 404 Not Found | Routing issue | Check reverse proxy config | Update routes |
| Authentication failed | Credential issue | Check auth configuration | Verify credentials |

#### Container/Docker Issues
| Symptom | Likely Cause | Diagnostic Command | Solution |
|---------|--------------|-------------------|----------|
| Container won't start | Configuration error | `docker-compose logs [service]` | Fix configuration |
| Out of memory | Resource limit | `docker stats` | Increase limits |
| Volume mount issue | Path problem | `docker-compose config` | Fix volume paths |

---

## Procedure Checklists

### Frontend Development
**Model Hint: Claude Haiku** ✨ *Standard development procedures*

- [ ] Navigate to frontend directory
- [ ] Install dependencies
- [ ] Start development server
- [ ] Verify http://localhost:[port] loads
- [ ] Check browser console for errors
- [ ] Test API connectivity
- [ ] Build production version
- [ ] Test production build locally

### Backend Development
**Model Hint: Claude Haiku** ✨ *Standard development procedures*

- [ ] Navigate to backend directory
- [ ] Set up virtual environment (if applicable)
- [ ] Install dependencies
- [ ] Run database migrations
- [ ] Start development server
- [ ] Test API endpoints
- [ ] Check application logs
- [ ] Verify database connectivity

### Full Stack Integration
**Model Hint: Claude Sonnet 4** 🧠 *Integration testing requires coordination analysis*

- [ ] Start all services via docker-compose
- [ ] Verify service discovery
- [ ] Test frontend → backend communication
- [ ] Test authentication flow
- [ ] Test data persistence
- [ ] Check cross-origin policies
- [ ] Verify production build integration
- [ ] Test error handling

### Deployment Checklist
**Model Hint: Claude Sonnet 4** 🧠 *Deployment requires risk assessment and rollback planning*

#### Pre-deployment
- [ ] Code review completed
- [ ] All tests passing
- [ ] Security scan passed
- [ ] Backup current production state
- [ ] Rollback plan documented

#### Deployment
- [ ] Deploy to staging first
- [ ] Run smoke tests
- [ ] Deploy to production
- [ ] Verify health endpoints
- [ ] Check application logs
- [ ] Monitor for 15 minutes

#### Post-deployment
- [ ] Verify all features working
- [ ] Check performance metrics
- [ ] Update monitoring alerts
- [ ] Document deployment
- [ ] Clean up old artifacts

---

## Rollback Procedures

### Emergency Rollback (<2 minutes)
**Model Hint: Claude Sonnet 4** 🧠 *Emergency decisions require immediate expert judgment*

```bash
# 1. Stop current services immediately
docker-compose down

# 2. Restore previous working version
git checkout [previous-working-commit]

# 3. Restart services
docker-compose up -d

# 4. Verify health
curl -v http://localhost:[port]/health/
```

### Planned Rollback
**Model Hint: Claude Haiku** ✨ *Standard rollback procedures*

```bash
# 1. Identify target version
git log --oneline -10

# 2. Create rollback branch
git checkout -b rollback-to-[version]

# 3. Reset to target version
git reset --hard [target-commit]

# 4. Test rollback locally
docker-compose up -d
# Run health checks

# 5. Deploy rollback to production
docker-compose -f docker-compose.prod.yml up -d
```

---

## Recovery Verification

### Standard Health Checks
**Model Hint: Claude Haiku** ✨ *Standard verification commands*

```bash
# Service availability
curl -f http://localhost:[port]/health/ || echo "FAILED"

# Database connectivity
curl -f http://localhost:[port]/api/db-health/ || echo "DB FAILED"

# Authentication
curl -f -H "Authorization: Bearer [token]" http://localhost:[port]/api/user/ || echo "AUTH FAILED"

# External dependencies
curl -f [external-service-health-url] || echo "EXTERNAL FAILED"
```

### Performance Verification
```bash
# Response time check
time curl http://localhost:[port]/health/

# Resource usage
docker stats --no-stream

# Error rate check
docker-compose logs --since=5m | grep -i error | wc -l
```

---

**Related Documentation**:  
[current-status](./current-status.md) | [project-specification](./project-specification.md) | [infrastructure](./infrastructure.md)

**Operations Version**: v1.0.0 | **Last Updated**: {{DATE}} | **Next Review**: Monthly