<!-- InquiryCircle2 – devGuidance – Stage2 – 9/2/2025 at 11:00 AM ET -->

# Development Guidance

## Project Overview
- **Project Name**: InquiryCircle
- **Environment**: SharedSystem Context (WSL Ubuntu + VPS)
- **Purpose**: Collaborative video conferencing platform for inquiry-based learning

## Development Environment Setup

### Prerequisites
- Windows 10/11 with WSL2 (Ubuntu 22.04)
- Docker Engine and Docker Compose installed in WSL
- Node.js 18+ and npm (for frontend development)
- Python 3.10+ (for backend development)
- Git configured in WSL

### Local Development Structure
```
/home/scott/inquirycircle/
├── compose/              # Docker compose configurations
├── caddy/               # Reverse proxy configuration
├── frontend/            # Vue 3 + Tailwind + Jitsi application
├── backend/             # Django REST API
└── README.md
```

## Critical Constraints

### Container Management
1. **Caddy must remain accessible** - The reverse proxy is the single public entrypoint
2. **Container isolation** - Frontend, backend, and Caddy run in separate containers
3. **Network security** - Only Caddy exposed publicly; backend on private network
4. **Data persistence** - Never store data in containers; use volumes/bind mounts

### Development Rules
1. **No PowerShell** - All commands must be run in WSL Ubuntu bash
2. **No direct production changes** - Test locally first, then deploy
3. **Key-based auth only** - No username/password authentication
4. **External Jitsi only (Stage 2)** - Self-hosted Jitsi is Stage 3 scope

## Development Workflow

### 1. Frontend Development (Vue + Tailwind + Jitsi)

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
```

#### Frontend Testing Checklist
- [ ] Vue Router navigation works
- [ ] Tailwind styles apply correctly
- [ ] Jitsi Meet SDK loads and connects
- [ ] API calls to backend succeed
- [ ] Key-based authentication flow works
- [ ] Facilitator vs participant roles differentiate

### 2. Backend Development (Django)

#### Local Development Mode
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  # Runs on http://localhost:8000
```

#### API Endpoints to Test
- `/api/health/` - Backend health check
- `/api/auth/verify-key/` - Key validation
- `/api/circles/` - Circle CRUD operations
- `/api/messages/` - Facilitator messages
- `/api/jitsi/room/` - Jitsi room configuration

### 3. Integration Testing (Docker Compose)

#### Start Full Stack Locally
```bash
cd compose
docker-compose -f docker-compose.dev.yml up -d
```

#### Verify Integration
1. Caddy serves frontend at http://localhost:8080
2. API proxied correctly at http://localhost:8080/api
3. Jitsi rooms create and join successfully
4. Data persists across container restarts

### 4. Database Migration (SQLite → PostgreSQL)

#### Phase 1: SQLite (Current)
```yaml
# Backend uses SQLite file
volumes:
  - ./backend/db:/app/db
```

#### Phase 2: PostgreSQL Migration
```yaml
# Add PostgreSQL service
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: inquirycircle
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## Milestones & Testing

### Frontend Milestones
1. **Routing Setup** - Vue Router with protected routes
   - Test: Navigate between pages, auth redirects work
   
2. **Tailwind + PostCSS** - Utility-first styling
   - Test: Styles apply, responsive design works
   
3. **Pinia State Management** - Global state for auth/circles
   - Test: State persists across components
   
4. **Jitsi Integration** - Video conferencing embedded
   - Test: Create room, join with multiple participants
   
5. **API Integration** - Axios for backend communication
   - Test: All CRUD operations succeed

### Backend Milestones
1. **Django Setup** - Project structure and settings
   - Test: Server starts, admin accessible
   
2. **Key Authentication** - Custom auth backend
   - Test: Keys validate, roles determined correctly
   
3. **Circle Management** - CRUD for inquiry circles
   - Test: Create, update, delete circles
   
4. **Message System** - HTML messages for facilitators
   - Test: Send, update, display messages
   
5. **Jitsi Integration** - Room management API
   - Test: Generate room configs, JWT tokens

### Integration Milestones
1. **Caddy Routing** - Static files and API proxy
   - Test: Frontend loads, API calls route correctly
   
2. **Full Auth Flow** - Key entry to role assignment
   - Test: End-to-end authentication works
   
3. **Video Sessions** - Complete circle session flow
   - Test: Create circle, join video, see messages
   
4. **Data Persistence** - SQLite/PostgreSQL storage
   - Test: Data survives container restarts

## Deployment Process

### Local Dry-Run
```bash
# Use production-like compose file
docker-compose -f docker-compose.prod.yml up -d
# Test at http://localhost:8080
```

### VPS Deployment
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
1. **Caddy not accessible**: Check firewall rules (ports 80/443)
2. **API 502 errors**: Verify backend container is running
3. **Jitsi not connecting**: Check external Jitsi service status
4. **Database errors**: Verify volume mounts and permissions

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