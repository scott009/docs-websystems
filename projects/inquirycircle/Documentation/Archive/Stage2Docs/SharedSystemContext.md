<!-- InquiryCircle2 – SharedSystemContext – Stage2 – 9/2/2025 at 11:00 AM ET -->

# Shared System Context

## DEV-PC (Windows 10 + WSL Ubuntu 22.04)
- **Purpose**: Local development machine  
- **Usage**: Run Linux commands (`bash`, `docker`, `git`) inside WSL  
- **Access URLs**: 
  - `http://localhost:8080` - Caddy (main entrypoint)
  - `http://localhost:5173` - Frontend dev server (Vite)
  - `http://localhost:8000` - Backend dev server (Django)

---

## WSL Ubuntu (inside DEV-PC)
- **Purpose**: Development / prod dry-run environment (Docker Engine + Docker Compose)  
- **Code Location**: `/home/scott/inquirycircle` (inside WSL filesystem)  
- **Development Environment**:
  - IDE: VSCode with WSL2 Remote Extension
  - AI Assistant: Claude Code integrated in VSCode
  - Terminal: WSL2 Ubuntu bash (accessed through VSCode)
  - Workflow: VSCode connects to WSL2, all development happens in Linux environment
- **Notes**: Docker images built here for local testing are **separate** from those on the VPS  

---

## VPS (catbench.com, Ubuntu 22.04)
- **Purpose**: Production deployment target  
- **Access**: SSH available via `user@catbench.com`  
- **IP Address**: 72.60.26.118
- **Project Root**: `/srv/inquirycircle` (application code and configs)
- **Static Assets**: `/srv/inquirycircle/caddy/site/dist` (served by Caddy)
- **Data Storage**: `/var/lib/inquirycircle` (persistent data)

### DNS Configuration (catbench.com)
- **A Records**:
  - `*` → 72.60.26.118
  - `@` → 72.60.26.118

- **CNAME Records** (all pointing to host.catbench.com):
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

---

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

---

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

---

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

---

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