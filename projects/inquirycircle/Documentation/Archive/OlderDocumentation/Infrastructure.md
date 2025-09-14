<!-- InquiryCircle2 – Infrastructure – Stage2 – 9/4/2025 at 11:35 AM ET -->

# Infrastructure

## System Environments

### DEV-PC (Windows 10 + WSL Ubuntu 22.04)
- **Purpose**: Local development machine  
- **Usage**: Run Linux commands (`bash`, `docker`, `git`) inside WSL  
- **Access URLs**: 
  - `http://localhost:8080` - Caddy (main entrypoint)
  - `http://localhost:5173` - Frontend dev server (Vite)
  - `http://localhost:8000` - Backend dev server (Django)

### WSL Ubuntu (inside DEV-PC)
- **Purpose**: Development / prod dry-run environment (Docker Engine + Docker Compose)  
- **Code Location**: `/home/scott/inquirycircle` (inside WSL filesystem)  
- **Development Environment**:
  - IDE: VSCode with WSL2 Remote Extension
  - AI Assistant: Claude Code integrated in VSCode
  - Terminal: WSL2 Ubuntu bash (accessed through VSCode)
  - Workflow: VSCode connects to WSL2, all development happens in Linux environment
- **Notes**: Docker images built here for local testing are **separate** from those on the VPS  

### VPS (catbench.com, Ubuntu 22.04)
- **Purpose**: Production deployment target  
- **Access**: SSH available via `user@catbench.com`  
- **IP Address**: 72.60.26.118
- **Project Root**: `/srv/inquirycircle` (application code and configs)
- **Static Assets**: `/srv/inquirycircle/caddy/site/dist` (served by Caddy)
- **Data Storage**: `/var/lib/inquirycircle` (persistent data)

## DNS Configuration (catbench.com)

### A Records
- `*` → 72.60.26.118
- `@` → 72.60.26.118

### CNAME Records (all pointing to host.catbench.com)
- `container1` - Reserved for container services
- `container2` - Reserved for container services  
- `dev.icircle` - Development/staging environment
- `icgeneric` - Generic InquiryCircle instance
- `icircle` - Primary InquiryCircle application
- `jitsi.icircle` - Reserved for future self-hosted Jitsi (Stage 3)
- `ssh` - SSH access endpoint
- `www` - Main website

### Active Services
- **https://catbench.com** - Caddy reverse proxy (active)
- **https://icircle.catbench.com** - InquiryCircle application (Stage 2 deployment target)

## Network Architecture

### Local Development (WSL)
```
Docker Network: inquirycircle_network (bridge)
├── caddy (exposed: 8080:80)  # Only Caddy exposed to host
│   ├── Routes /api/* → backend:8000
│   └── Routes /* → frontend:3000 or static files
├── frontend (internal: 3000)  # Not exposed, accessed via Caddy
├── backend (internal: 8000)   # Not exposed, accessed via Caddy
└── [Stage 3: postgres (internal: 5432)]
```

### Production (VPS)
```
Docker Network: inquirycircle_network (bridge)
├── caddy (exposed: 80:80, 443:443)  # Only Caddy exposed to internet
│   ├── Routes /api/* → backend:8000
│   └── Routes /* → frontend:3000 or static files
├── frontend (internal: 3000)  # Not exposed, accessed via Caddy
├── backend (internal: 8000)   # Not exposed, accessed via Caddy
└── [Stage 3: postgres (internal: 5432)]
```

## Directory Structure

### WSL Development - Current State (Stage 2 Starting Point)
```
/home/scott/inquirycircle/        # Git repository (initialized, main branch)
├─ .git/                          # Git repository
├─ .gitignore                     # Comprehensive ignore patterns
├─ compose/
│  └─ .env.example                # Environment template (moved from root)
├─ caddy/
│  ├─ logs/                       # Log directory (git-ignored, empty)
│  └─ site/
│     └─ dist/                    # Future Vue build output (git-ignored, empty)
├─ frontend/                      # Empty, ready for Vue 3 + Tailwind + Jitsi
├─ backend/                       # Empty, ready for Django REST API
└─ Documentation/                 # Not in repo, lives at Windows path below
```

**Documentation Location**: `/mnt/c/Users/scott/Documents/AIProjects/Markdown/InquiryCircle2/Documentation/`

**Important Notes**:
- Caddy configuration files are **NOT** stored in the repository
- Caddy was configured in Stage 1 and configs live directly on VPS
- Stage 2 focuses on application development (Vue frontend, Django backend)
- All directories are currently empty, ready for Stage 2 implementation

### WSL Development - Target Structure (After Implementation)
```
/home/scott/inquirycircle/
├─ compose/
│  ├─ docker-compose.dev.yml      # WSL development setup
│  └─ .env                        # local development environment
├─ caddy/
│  └─ site/                       # static assets + built SPA
│     └─ dist/                    # Vue+Jitsi build output
├─ frontend/                      # Vue 3 + Tailwind + Jitsi source
│  ├─ src/
│  │  ├─ components/
│  │  │  ├─ video/                # Jitsi integration components  
│  │  │  ├─ circles/              # Circle management UI
│  │  │  ├─ auth/                 # Key-based login components
│  │  │  └─ messages/             # Facilitator messaging UI
│  │  ├─ services/
│  │  │  ├─ jitsi.js              # Jitsi Meet SDK integration
│  │  │  ├─ api.js                # Backend API client
│  │  │  └─ auth.js               # Key-based authentication
│  │  ├─ stores/                  # Pinia state management
│  │  └─ router/                  # Vue router configuration
│  ├─ dist/                       # Vite build output
│  ├─ package.json                # includes Jitsi Meet dependencies
│  └─ vite.config.js
├─ backend/                       # Django REST API
│  ├─ ic_core/
│  │  ├─ circles/                 # Circle models & endpoints
│  │  ├─ auth/                    # Key-based authentication
│  │  ├─ messages/                # Facilitator messaging API
│  │  ├─ jitsi/                   # Jitsi room management
│  │  └─ sessions/                # Session state management
│  ├─ db/                         # SQLite persistence location
│  ├─ requirements.txt
│  └─ manage.py
└─ README.md                      # project setup & deployment guide
```

### VPS Production
```
/srv/inquirycircle/               # git repo workspace
├─ compose/
│  ├─ docker-compose.prod.yml     # production setup
│  └─ .env.example                # template; real secrets in /etc/inquirycircle/
├─ caddy/
│  ├─ Caddyfile                   # production config (HTTPS, catbench.com)
│  └─ site/                       # production static assets
├─ frontend/                      # source (if building on server)
├─ backend/                       # Django source
└─ Documentation/

/etc/inquirycircle/               # system config (restricted access)
├─ env                            # production environment secrets
└─ caddy/                         # operational overrides (if needed)

/var/lib/inquirycircle/           # persistent runtime data
├─ backend/
│  └─ sqlite/                     # SQLite database location
└─ caddy/                         # TLS cert storage (or use named volumes)
```

## Version Control

### Git Configuration
- **GitHub Account**: scott009
- **Git Username**: Scott Tobias
- **Git Email**: scott@farclass.com

### GitHub Repositories
- **InquiryCircle**: https://github.com/scott009/InquiryCircle
  - Main repository for the InquiryCircle platform (Stage 2 implementation)
  - Fresh repository for full stack implementation (Vue frontend, Django backend, Docker configs)
  - Created: September 2025
  
- **InquiryCircle-legacy**: https://github.com/scott009/InquiryCircle-legacy
  - Original InquiryCircle repository (renamed from InquiryCircle)
  - Contains earlier work and experiments
  - Preserved for reference and history
  
- **DockerIC**: https://github.com/scott009/DockerIC
  - Docker-focused repository for containerization experiments
  - Related infrastructure and deployment configurations

### Branch Strategy
- `main`: Production-ready code
- `develop`: Integration branch for feature merging
- `feature/*`: Individual feature development branches
- `hotfix/*`: Emergency production fixes

### Repository Setup
```bash
# Clone the main repository
git clone https://github.com/scott009/InquiryCircle.git
cd InquiryCircle

# Set up git configuration
git config user.name "Scott Tobias"
git config user.email "scott@farclass.com"

# Add remote for deployment
git remote add production user@catbench.com:/srv/inquirycircle
```

## File System Access

### WSL Access from Windows
- WSL filesystem path: `\\wsl.localhost\Ubuntu\home\scott\inquirycircle`
- Windows path from WSL: `/mnt/c/Users/scott/`

### VPS Directory Structure
- Application code: `/srv/inquirycircle/`
- Configuration: `/etc/inquirycircle/`
- Static files: `/srv/inquirycircle/caddy/site/dist`
- Data persistence: `/var/lib/inquirycircle/`
- Logs: `/var/log/ic/`

## Security Boundaries

### Development
- All services accessible on localhost only
- No external traffic routing
- Test keys for authentication

### Production
- Only Caddy exposed to internet (ports 80/443)
- Backend on private Docker network
- TLS certificates managed by Caddy
- Production keys stored in `/etc/inquirycircle/env`

## Resource Allocation

### WSL Resources
- Memory: As configured in `.wslconfig`
- Disk: Shared with Windows host
- CPU: Shared with Windows host

### VPS Resources  
- Memory: As provisioned by hosting provider
- Disk: Dedicated VPS storage
- CPU: Dedicated VPS cores
- Bandwidth: Per hosting plan limits

## Container Resource Limits (Optional)

### Development
```yaml
# No limits in development for flexibility
```

### Production
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  frontend:
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 256M
        reservations:
          cpus: '0.10'
          memory: 128M

  caddy:
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 256M
        reservations:
          cpus: '0.10'
          memory: 128M
```

## Backup Strategy

### Development
- Code: Git repository
- Data: SQLite file copies
- Config: Version controlled

### Production
- Code: Git repository + deployment snapshots
- Data: Daily SQLite backups to `/var/backups/inquirycircle/`
- Config: Backed up to secure location
- TLS Certificates: Caddy manages automatically

## Monitoring Points

### System Health
- CPU usage per container
- Memory usage per container
- Disk usage for data volumes
- Network traffic through Caddy

### Application Health
- API response times
- Jitsi connection success rate
- Active session count
- Error log frequency

### Security Monitoring
- Failed authentication attempts
- Unusual traffic patterns
- Certificate expiry warnings
- Container restart frequency