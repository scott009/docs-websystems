<!-- InquiryCircle2 – Runbook – Stage2 – 9/2/2025 at 11:15 AM ET -->

# Runbook: InquiryCircle Full Stack Deployment

**Project**: InquiryCircle  
**Scope**: Deploy complete video conferencing platform with Vue/Jitsi frontend, Django backend, Caddy reverse proxy  
**Stage 2 Coverage**: External Jitsi integration, key-based auth, facilitator messaging, SQLite→PostgreSQL migration  
**Out of Scope**: Self-hosted Jitsi containers (Stage 3)

---

## Definitions
- **Constraints**: Rules that govern our interaction and execution during development
- **Requirements & Assumptions**: Non-negotiable system shape and expectations
- **Milestones**: Checkpoints with explicit acceptance tests

---

## Constraints (development interaction rules)

### Constraint: Minimal Change  
*(See ProjectBaseline §Constraints: Minimal Change for full policy)*

- Only change what the request **explicitly** covers; all else is **frozen**  
- If a broader change is **strictly necessary**, pause and request: `ACK UNFREEZE <area>: <reason>`  
- You may add an **Impact Advisory** (warnings + optional follow-ups), but **do not implement** them  
- **Verify**: show before/after for changed surfaces and confirm **no deltas** outside scope

**PR/Commit checklist:**  
- [ ] Confined to stated scope  
- [ ] Impact Advisory provided (if relevant)  
- [ ] No frozen-surface deltas  
- [ ] (If needed) `ACK UNFREEZE …` recorded

### Operational Constraints
- Operate **only in bash** on WSL and VPS (no PowerShell)  
- Keep filesystem locations **as-documented** (WSL `/home/scott/inquirycircle`, VPS `/srv/inquirycircle`)  
- Keep changes **incremental**; verify after each step before proceeding  
- Be **rollback-ready** at every step (retain prior configs and builds)  
- **No self-hosted Jitsi** in Stage 2; external Jitsi service only  
- **Key-based auth only**; no username/password implementation

---

## Requirements & Assumptions (system/architecture)
- Three **separate runtime containers**: Caddy, Frontend, Backend  
- Backend service reachable by **service name** on Docker network (e.g., `backend:8000`)  
- Frontend built by **Vite** and served from `caddy/site/dist/`  
- **Single docker network** for app services (e.g., `inquirycircle_network`)  
- VPS domain `catbench.com` points to server; Caddy obtains **Let's Encrypt** certs on ports **80/443**  
- SPA routing uses **fallback to `index.html`**  
- Database uses **SQLite** for Stage 2 prototype (PostgreSQL planned for Stage 3)

---

## Phase 1 — Project Structure Setup

**Actions - WSL**
```bash
cd /home/scott
mkdir -p inquirycircle/{backend,frontend,caddy,compose}
cd inquirycircle

# Create directory structure
mkdir -p caddy/{site,logs}
mkdir -p backend/db
mkdir -p compose
```

**Actions - VPS**
```bash
sudo mkdir -p /srv/inquirycircle/{backend,frontend,caddy,compose}
sudo mkdir -p /srv/inquirycircle/caddy/site/dist
sudo mkdir -p /var/lib/inquirycircle/backend/sqlite
sudo mkdir -p /etc/inquirycircle

# Set permissions
sudo chown -R $USER:$USER /srv/inquirycircle
```

**Milestone M1 — Structure Ready**
- [ ] Directories exist in both WSL and VPS
- [ ] Permissions configured correctly

---

## Phase 2 — Frontend Development (Vue + Jitsi)

**Actions**
```bash
cd frontend

# Initialize Vue project with Vite
npm create vite@latest . -- --template vue
npm install

# Add dependencies
npm install vue-router@4 pinia axios
npm install tailwindcss postcss autoprefixer
npm install @jitsi/web-sdk

# Configure Tailwind
npx tailwindcss init -p
```

**Frontend Key Components**
- `src/router/` - Protected routes with key-based guards
- `src/stores/` - Pinia stores for auth, circles, messages
- `src/services/jitsi.js` - Jitsi Meet SDK integration
- `src/services/api.js` - Backend API client
- `src/components/video/` - Jitsi video components
- `src/components/auth/` - Key entry forms

**Verification**
```bash
npm run dev
# Navigate to http://localhost:5173
# Verify Vue app loads with Tailwind styles
```

**Milestone M2 — Frontend Framework**
- [ ] Vue app with routing works
- [ ] Tailwind styles apply
- [ ] Jitsi SDK loads without errors

---

## Phase 3 — Backend Development (Django API)

**Actions**
```bash
cd backend

# Create Django project
python -m venv venv
source venv/bin/activate
pip install django djangorestframework gunicorn
pip install python-dotenv cors-headers

django-admin startproject ic_core .

# Create apps
python manage.py startapp circles
python manage.py startapp authentication
python manage.py startapp messages
python manage.py startapp jitsi_integration
```

**Backend Key Endpoints**
- `/api/health/` - Health check
- `/api/auth/verify-key/` - Key validation
- `/api/circles/` - Circle CRUD
- `/api/messages/` - Facilitator messages
- `/api/jitsi/config/` - Room configuration

**Database Setup (SQLite)**
```bash
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db' / 'inquirycircle.db',
    }
}

python manage.py makemigrations
python manage.py migrate
```

**Verification**
```bash
python manage.py runserver
# Test http://localhost:8000/api/health/
```

**Milestone M3 — Backend API**
- [ ] Django server runs
- [ ] API endpoints respond
- [ ] SQLite database created

---

## Phase 4 — Docker Compose Configuration

**Actions - Create compose/docker-compose.dev.yml**
```yaml
version: '3.8'

services:
  caddy:
    image: caddy:2-alpine
    container_name: ic-caddy
    restart: unless-stopped
    ports:
      - "8080:80"
    volumes:
      - ../caddy/Caddyfile:/etc/caddy/Caddyfile:ro
      - ../caddy/site:/srv/site:ro
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - backend
    networks:
      - inquirycircle_network

  frontend:
    build: ../frontend
    container_name: ic-frontend
    restart: unless-stopped
    environment:
      - NODE_ENV=production
    volumes:
      - ../frontend/dist:/app/dist
    networks:
      - inquirycircle_network

  backend:
    build: ../backend
    container_name: ic-backend
    restart: unless-stopped
    environment:
      - DJANGO_SETTINGS_MODULE=ic_core.settings
      - SECRET_KEY=${SECRET_KEY}
      - DEBUG=False
      - ALLOWED_HOSTS=localhost,127.0.0.1,backend
    volumes:
      - ../backend/db:/app/db
    networks:
      - inquirycircle_network

volumes:
  caddy_data:
  caddy_config:

networks:
  inquirycircle_network:
    driver: bridge
```

**Frontend Dockerfile**
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["npx", "serve", "-s", "dist", "-l", "3000"]
```

**Backend Dockerfile**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "ic_core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**Milestone M4 — Container Config**
- [ ] Docker Compose files created
- [ ] Frontend Dockerfile ready
- [ ] Backend Dockerfile ready
- [ ] Environment variables configured

---

## Phase 5 — Caddy Configuration

**Actions - Create caddy/Caddyfile (WSL)**
```
{
  auto_https off
}

:80 {
  # Serve static files from built frontend
  root * /srv/site/dist

  # Route API calls to backend container (internal port 8000)
  @api path /api/*
  handle @api {
    reverse_proxy backend:8000
  }

  # Route to frontend container for dynamic content (internal port 3000)
  @app {
    not path /api/*
    not file
  }
  handle @app {
    reverse_proxy frontend:3000
  }

  # SPA fallback for client-side routing
  try_files {path} /index.html
  file_server

  # Logging
  log {
    output file /var/log/caddy/access.log
  }
}
```

**Actions - Create caddy/Caddyfile (VPS)**
```
catbench.com, icircle.catbench.com {
  root * /srv/site/dist

  # API proxy
  @api path /api/*
  handle @api {
    reverse_proxy backend:8000
  }

  # SPA fallback  
  try_files {path} /index.html
  file_server

  # Security headers
  header {
    X-Frame-Options "SAMEORIGIN"
    X-Content-Type-Options "nosniff"
    X-XSS-Protection "1; mode=block"
  }

  # Logging
  log {
    output file /var/log/caddy/access.log
  }
}

www.catbench.com {
  redir https://catbench.com{uri}
}
```

**Milestone M5 — Caddy Ready**
- [ ] Caddyfile configured for both environments
- [ ] Proxy rules defined
- [ ] SPA fallback configured

---

## Phase 6 — Build and Deploy Frontend

**Actions - Build Frontend**
```bash
cd frontend
npm run build
# Creates dist/ directory

# Copy to Caddy serving location
cp -r dist/* ../caddy/site/
```

**Actions - Deploy to VPS**
```bash
# From WSL
rsync -avz caddy/site/ user@catbench.com:/srv/inquirycircle/caddy/site/

# Or build on VPS
ssh user@catbench.com
cd /srv/inquirycircle/frontend
npm ci
npm run build
cp -r dist/* ../caddy/site/dist/
```

**Milestone M6 — Frontend Deployed**
- [ ] Frontend built successfully
- [ ] Static files in place
- [ ] Assets accessible via Caddy

---

## Phase 7 — Full Stack Integration

**Actions - Start Services (WSL)**
```bash
cd compose
docker-compose -f docker-compose.dev.yml up -d

# Verify services
docker ps
docker logs ic-caddy
docker logs ic-backend
```

**Actions - Start Services (VPS)**
```bash
cd /srv/inquirycircle/compose
docker-compose -f docker-compose.prod.yml up -d

# Verify HTTPS
curl https://catbench.com/api/health/
```

**Integration Tests**
1. Navigate to application URL
2. Enter access key
3. Create/join a circle
4. Start Jitsi video session
5. Send facilitator message
6. Verify participant sees message

**Milestone M7 — Integration Working**
- [ ] Frontend loads via Caddy
- [ ] API calls succeed
- [ ] Jitsi video works
- [ ] Key authentication works
- [ ] Messages display

---

## Phase 8 — Stage 2 Completion

**Note**: PostgreSQL migration is deferred to Stage 3. Stage 2 uses SQLite for the working prototype.

**Stage 2 Deliverables**
- [ ] Working prototype with SQLite persistence
- [ ] Full video conferencing via external Jitsi
- [ ] Key-based authentication functioning
- [ ] Facilitator messaging system operational
- [ ] Deployed and accessible to test users

**Stage 3 Planning (Future)**
- PostgreSQL migration for production-grade persistence
- Self-hosted Jitsi infrastructure
- Enhanced performance and scaling capabilities

---

## Phase 9 — Production Hardening

**Actions - Security**
```bash
# Update Django settings
ALLOWED_HOSTS = ['catbench.com', 'icircle.catbench.com']
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

# Configure CORS
CORS_ALLOWED_ORIGINS = [
    "https://catbench.com",
    "https://icircle.catbench.com",
]
```

**Actions - Monitoring**
```bash
# Health check endpoint
curl https://catbench.com/api/health/

# Container logs
docker-compose logs -f --tail=100

# System resources
docker stats
```

**Milestone M9 — Production Ready**
- [ ] Security headers configured
- [ ] HTTPS enforced
- [ ] Monitoring in place
- [ ] Backup strategy defined

---

## Phase 10 — Documentation & Handoff

**Actions**
1. Document all configuration files
2. Create user guide for facilitators
3. Create participant guide
4. Document key management process
5. Create troubleshooting guide

**Deliverables**
- Configuration snapshot (git commit hash)
- Deployment timestamp
- Service versions
- Key distribution plan
- Support contact information

**Milestone M10 — Project Complete**
- [ ] All documentation complete
- [ ] System fully operational
- [ ] Handoff materials prepared
- [ ] Stage 2 objectives met

---

## Rollback Procedures

**Quick Rollback**
```bash
# Restore previous compose file
git checkout HEAD~1 docker-compose.yml
docker-compose down
docker-compose up -d

# Restore previous frontend
git checkout HEAD~1 caddy/site/
docker-compose restart caddy
```

**Database Rollback**
```bash
# Restore from backup
python manage.py flush
python manage.py loaddata backup_[timestamp].json
```

---

## Troubleshooting Quick Reference

| Issue | Check | Fix |
|-------|-------|-----|
| 502 Bad Gateway | Backend container status | `docker-compose restart backend` |
| Jitsi not loading | External service status | Check Jitsi service, API keys |
| Keys not working | Backend logs | Verify key format, database connection |
| No HTTPS | Caddy logs | Check DNS, firewall ports 80/443 |
| Database errors | PostgreSQL logs | Check credentials, migrations |

---

*End of Runbook - InquiryCircle Stage 2 Implementation*