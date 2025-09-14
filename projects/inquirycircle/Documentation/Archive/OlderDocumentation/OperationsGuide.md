<!-- InquiryCircle2 – OperationsGuide – Stage2 – 9/4/2025 at 11:30 AM ET -->

# Operations Guide

## Part 1: Development Workflow

### Development Environment Setup

#### Prerequisites
- Windows 10/11 with WSL2 (Ubuntu 22.04)
- Docker Engine and Docker Compose installed in WSL
- Node.js 18+ and npm (for frontend development)
- Python 3.10+ (for backend development)
- Git configured in WSL

#### Local Development Structure
```
/home/scott/inquirycircle/
├── compose/              # Docker compose configurations
├── caddy/               # Reverse proxy configuration
├── frontend/            # Vue 3 + Tailwind + Jitsi application
├── backend/             # Django REST API
└── Documentation/       # Project documentation
```

### Frontend Development (Vue + Tailwind + Jitsi)

#### Local Development Mode
```bash
cd frontend
npm install
npm run dev  # Runs on http://localhost:5173
```

#### Build for Production
```bash
npm run build  # Creates dist/ directory
# Copy dist/ contents to caddy/site/ for serving
cp -r dist/* ../caddy/site/
```

#### Frontend Key Components
- `src/router/` - Protected routes with key-based guards
- `src/stores/` - Pinia stores for auth, circles, messages
- `src/services/jitsi.js` - Jitsi Meet SDK integration
- `src/services/api.js` - Backend API client
- `src/components/video/` - Jitsi video components
- `src/components/auth/` - Key entry forms

#### Frontend Testing Checklist
- [ ] Vue Router navigation works
- [ ] Tailwind styles apply correctly
- [ ] Jitsi Meet SDK loads and connects
- [ ] API calls to backend succeed
- [ ] Key-based authentication flow works
- [ ] Facilitator vs participant roles differentiate

### Backend Development (Django)

#### Local Development Mode
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  # Runs on http://localhost:8000
```

#### Backend Key Endpoints
- `/api/health/` - Backend health check
- `/api/auth/verify-key/` - Key validation
- `/api/circles/` - Circle CRUD operations
- `/api/messages/` - Facilitator messages
- `/api/jitsi/config/` - Jitsi room configuration

#### Database Setup (SQLite)
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db' / 'inquirycircle.db',
    }
}
```
#### Backend Testing Checklist

  **1. Health Check Endpoint**
  - Simple /api/health/ that returns JSON status
  - Tests: Django running, database connected, basic routing
  curl http://localhost:8000/api/health/
  - Expected: {"status": "healthy", "database": "connected"}

  **2. Authentication Flow Test**
  - /api/auth/verify-key/ endpoint
  - Test valid/invalid keys, role detection (facilitator vs participant)
  - Tests the key format and expected responses
  - Valid facilitator key
  curl -X POST -H "Authorization: Key facilitator-key-123" \
       http://localhost:8000/api/auth/verify-key/
  -Expected: {"valid": true, "role": "facilitator"}

  - Valid participant key  
  curl -X POST -H "Authorization: Key participant-key-456" \
       http://localhost:8000/api/auth/verify-key/
  -Expected: {"valid": true, "role": "participant"}

  - Invalid key
  curl -X POST -H "Authorization: Key invalid-key"   
       http://localhost:8000/api/auth/verify-key/
  - Expected: {"valid": false, "error": "Invalid key"}

  **3. Core API Endpoints**
  - /api/circles/ - CRUD operations
  - /api/messages/ - Message management
  - Basic data persistence verification
  -Create circle
  curl -X POST -H "Authorization: Key facilitator-key-123" \
       -H "Content-Type: application/json" \
       -d '{"name": "Test Circle"}' \
       http://localhost:8000/api/circles/
  - Expected: {"id": 1, "name": "Test Circle", "created_at": "..."}

  -Get circles
  curl -H "Authorization: Key facilitator-key-123" \
       http://localhost:8000/api/circles/
  - Expected: [{"id": 1, "name": "Test Circle", ...}]

  - Create message
  curl -X POST -H "Authorization: Key facilitator-key-123" \
       -H "Content-Type: application/json" \
       -d '{"circle_id": 1, "content": "Welcome to the circle", "html": true}' \
       http://localhost:8000/api/messages/
  - Expected: {"id": 1, "content": "Welcome to the circle", ...}

  **4. Database State Test**
  - SQLite file creation and data persistence
  - Migration status verification
  - Sample data insertion/retrieval
  # Check database file exists
  ls -la backend/db/inquirycircle.db

  # Check migration status
  cd backend && python manage.py showmigrations
  # Expected: All migrations marked with [X]

  # Check database tables
  cd backend && python manage.py shell -c "
  from django.db import connection
  cursor = connection.cursor()
  cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")
  print([table[0] for table in cursor.fetchall()])
  "
  # Expected: Django tables + circles, auth_keys, messages, sessions

  # Verify data persistence (restart backend, check data still exists)
  curl -H "Authorization: Key facilitator-key-123" \
       http://localhost:8000/api/circles/
  # Expected: Previously created circles still present


### Integration Testing (Docker Compose)

#### Start Full Stack Locally

cd compose
docker-compose -f docker-compose.dev.yml up -d
```

#### Verify Integration
1. Caddy serves frontend at http://localhost:8080
2. API proxied correctly at http://localhost:8080/api
3. Jitsi rooms create and join successfully
4. Data persists across container restarts

### Testing Procedures

#### Frontend Tests
```bash
cd frontend
npm run test:unit
npm run test:e2e
```

#### Backend Tests

cd backend
python manage.py test
```

#### Integration Tests

# Run full stack locally
docker-compose -f docker-compose.dev.yml up
# Execute integration test suite
npm run test:integration
```

### Debug Commands
```bash
# Check container status
docker ps -a

# View logs
docker-compose logs caddy
docker-compose logs backend
docker-compose logs frontend

# Enter container shell
docker exec -it <container_name> /bin/bash

# Test internal networking
docker exec caddy wget -O- http://backend:8000/api/health/
```

## Part 2: Deployment Procedures

### Phase 1 — Project Structure Setup

#### Actions - WSL
```bash
cd /home/scott
mkdir -p inquirycircle/{backend,frontend,caddy,compose}
cd inquirycircle

# Create directory structure
mkdir -p caddy/{site,logs}
mkdir -p backend/db
mkdir -p compose
```

#### Actions - VPS
```bash
sudo mkdir -p /srv/inquirycircle/{backend,frontend,caddy,compose}
sudo mkdir -p /srv/inquirycircle/caddy/site/dist
sudo mkdir -p /var/lib/inquirycircle/backend/sqlite
sudo mkdir -p /etc/inquirycircle

# Set permissions
sudo chown -R $USER:$USER /srv/inquirycircle
```

#### Milestone M1 — Structure Ready
- [ ] Directories exist in both WSL and VPS
- [ ] Permissions configured correctly

### Phase 2 — Docker Configuration

#### Docker Compose Development (compose/docker-compose.dev.yml)
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

#### Frontend Dockerfile
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

#### Backend Dockerfile
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "ic_core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Phase 3 — Caddy Configuration

#### Caddyfile (WSL Development)
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

  # SPA fallback for client-side routing
  try_files {path} /index.html
  file_server

  # Logging
  log {
    output file /var/log/caddy/access.log
  }
}
```

#### Caddyfile (VPS Production)
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

### Phase 4 — Build and Deploy

#### Build Frontend
```bash
cd frontend
npm run build
# Creates dist/ directory

# Copy to Caddy serving location
cp -r dist/* ../caddy/site/
```

#### Deploy to VPS
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

### Phase 5 — Full Stack Integration

#### Start Services (WSL)
```bash
cd compose
docker-compose -f docker-compose.dev.yml up -d

# Verify services
docker ps
docker logs ic-caddy
docker logs ic-backend
```

#### Start Services (VPS)
```bash
cd /srv/inquirycircle/compose
docker-compose -f docker-compose.prod.yml up -d

# Verify HTTPS
curl https://catbench.com/api/health/
```

#### Integration Tests
1. Navigate to application URL
2. Enter access key
3. Create/join a circle
4. Start Jitsi video session
5. Send facilitator message
6. Verify participant sees message

### Production Deployment Process

#### Local Dry-Run
```bash
# Use production-like compose file
docker-compose -f docker-compose.prod.yml up -d
# Test at http://localhost:8080
```

#### VPS Deployment
```bash
# SSH to VPS
ssh user@catbench.com

# Pull latest code
cd /srv/inquirycircle
git pull

# Build and restart
docker-compose down
docker-compose up -d --build

# Verify at https://catbench.com
```

## Troubleshooting

### Common Issues

| Issue | Check | Fix |
|-------|-------|-----|
| 502 Bad Gateway | Backend container status | `docker-compose restart backend` |
| Jitsi not loading | External service status | Check Jitsi service, API keys |
| Keys not working | Backend logs | Verify key format, database connection |
| No HTTPS | Caddy logs | Check DNS, firewall ports 80/443 |
| Database errors | SQLite permissions | Check volume mounts, file permissions |
| Frontend not updating | Build cache | Clear browser cache, rebuild frontend |
| API timeout | Container networking | Verify Docker network connectivity |

### Health Monitoring
```bash
# API health
curl http://localhost:8080/api/health/

# Container status
docker-compose ps

# View logs
docker-compose logs -f [service-name]

# System resources
docker stats
```

## Rollback Procedures

### Quick Rollback
```bash
# Restore previous compose file
git checkout HEAD~1 docker-compose.yml
docker-compose down
docker-compose up -d

# Restore previous frontend
git checkout HEAD~1 caddy/site/
docker-compose restart caddy
```

### Database Rollback
```bash
# Restore from backup
python manage.py flush
python manage.py loaddata backup_[timestamp].json
```

## Security Checklist
- [ ] No secrets in code repository
- [ ] Environment variables for sensitive config
- [ ] HTTPS enforced in production
- [ ] Backend not directly accessible
- [ ] Key validation on all protected endpoints
- [ ] CORS configured correctly
- [ ] Input validation on all forms
- [ ] SQL injection prevention (ORM usage)

## Performance Considerations
- Frontend: Bundle splitting, lazy loading
- Backend: Database indexing, query optimization
- Caddy: Caching headers, compression
- Jitsi: External service (no self-hosting overhead in Stage 2)

## Database Migration (SQLite → PostgreSQL)

### Phase 1: SQLite (Current)
```yaml
# Backend uses SQLite file
volumes:
  - ./backend/db:/app/db
```

### Phase 2: PostgreSQL Migration (Future)
1. **Backup existing data**
```bash
python manage.py dumpdata > backup.json
```

2. **Add PostgreSQL service to compose**
```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: inquirycircle
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

3. **Update Django settings** for PostgreSQL connection

4. **Migrate and restore**
```bash
python manage.py migrate
python manage.py loaddata backup.json
```

## Milestones Summary

### Development Milestones
1. **Frontend Framework** - Vue + Tailwind + Jitsi working
2. **Backend API** - Django endpoints responding
3. **Container Config** - Docker Compose files ready
4. **Caddy Ready** - Proxy and static serving configured
5. **Integration Working** - Full stack operational

### Production Milestones
6. **Frontend Deployed** - Static files built and served
7. **Production Ready** - Security and monitoring in place
8. **Database Migration** - PostgreSQL ready (Stage 3)
9. **Project Complete** - All documentation and handoff done

---

**Note**: PostgreSQL migration is deferred to Stage 3. Stage 2 uses SQLite for the working prototype.