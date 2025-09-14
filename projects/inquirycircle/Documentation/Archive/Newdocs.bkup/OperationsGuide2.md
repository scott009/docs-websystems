
<!-- InquiryCircle2 – OperationsGuide – Stage2 – 9/12/2025 at 8:45 AM ET -->

# Operations Guide

## Purpose
Define *how* to build, test, deploy, and operate InquiryCircle in Stage 2.  
This document is procedural: it captures development workflows, deployment steps, guardrails, and troubleshooting. Strategic constraints and architecture live in ProjectSpec.md.

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

## Frontend Procedures

**Dev Mode**
cd frontend
npm install
npm run dev  # http://localhost:5173
Build for Production


npm run build
cp -r dist/* ../caddy/site/
Checklist

Vue Router works

Tailwind styles applied

Jitsi SDK loads

API calls succeed

Key-based auth flow works

Facilitator/participant roles enforced

Backend Procedures
Dev Mode


cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  # http://localhost:8000
Key Endpoints

/api/health/

/api/auth/verify-key/

/api/circles/

/api/messages/

/api/jitsi/config/

Checklist

Health check returns JSON

Auth keys validated (facilitator vs participant)

Circle CRUD operations work

Messages persist

SQLite file created in backend/db/

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
Troubleshooting
Issue	Check	Fix
502 Bad Gateway	Backend container status	docker-compose restart backend
Jitsi not loading	External service availability	Verify Jitsi API keys
Keys not working	Backend logs	Confirm key format, DB connection
No HTTPS	Caddy logs, DNS, ports	Open ports 80/443, check firewall
DB errors	SQLite permissions	Check mounts, file permissions
Frontend stale	Browser cache, build cache	Clear cache, rebuild frontend

Rollback Procedures
Quick Rollback


git checkout HEAD~1 docker-compose.yml
docker-compose down
docker-compose up -d
Database Rollback


python manage.py flush
python manage.py loaddata backup_[timestamp].json
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