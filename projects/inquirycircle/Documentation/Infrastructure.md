# Infrastructure
<!-- InquiryCircle2 – Infrastructure – Stage2 – 9/12/2025 at 9:15 AM ET -->

# Infrastructure

## Purpose
Define the environments and system layout for InquiryCircle. This document captures *where* development and production take place — not constraints (ProjectSpec) or procedures (OperationsGuide).

---

## Environments

### DEV-PC (Windows 10/11 + WSL Ubuntu 22.04)
- Local development machine.  
- Run Linux commands (bash, docker, git) inside WSL.  
- Access URLs:  
  - http://localhost:8080 → Caddy entrypoint  
  - http://localhost:5173 → Frontend dev server  
  - http://localhost:8000 → Backend dev server  

### WSL Ubuntu (inside DEV-PC)
- Dev/dry-run environment (Docker Engine + Compose).  
- Code root: `/home/scott/inquirycircle`.  
- IDE: VSCode with Remote WSL extension.  
- Workflow: All development occurs inside Linux environment.

### VPS (catbench.com, Ubuntu 22.04)
- Production deployment target.  
- Access: `ssh user@catbench.com`.  
- Project root: `/srv/inquirycircle`.  
- Static assets: `/srv/inquirycircle/caddy/site/dist`.  
- Persistent data: `/var/lib/inquirycircle`.

### DOCS-ENV (Documentation Management Environment)
- **Platform**: Windows 10/11 native filesystem  
- **Access Path**: `/mnt/c/Users/scott/Documents/AIProjects/Markdown/docs-websystems/projects/inquirycircle/`
- **Purpose**: Cross-project documentation templates and AI context management
- **Tools**: Windows file explorer, VNote, text editors, git for Windows
- **Integration**: Accessible from WSL via mount, serves AI model context loading
- **Repository**: Version controlled via GitHub at docs-websystems
- **Workflow**: Edit docs in VNote, commit changes, AI loads context for model switching

---

## DNS
- `@` and `*` → 72.60.26.118  
- Active domains:  
  - https://catbench.com → Caddy reverse proxy  
  - https://icircle.catbench.com → InquiryCircle application (Stage 2 target)  
- Reserved subdomains: `dev.icircle`, `icgeneric`, `jitsi.icircle` (future), `ssh`, `www`.

---

## Network Topology

**Development (WSL)**
Docker network: inquirycircle_network
├── caddy (exposed: 8080:80)
│ ├─ routes /api/* → backend:8000
│ └─ routes /* → frontend:3000 or static
├── frontend (internal: 3000)
├── backend (internal: 8000)
└── [future: postgres (internal: 5432)]

markdown
Copy code

**Production (VPS)**
Docker network: inquirycircle_network
├── caddy (exposed: 80, 443)
│ ├─ routes /api/* → backend:8000
│ └─ routes /* → frontend:3000 or static
├── frontend (internal: 3000)
├── backend (internal: 8000)
└── [future: postgres (internal: 5432)]

yaml
Copy code

---

## Directory Layout

### WSL Development
/home/scott/inquirycircle/
├─ compose/ # Compose configs, .env files
├─ caddy/ # Static site (dist/)
├─ frontend/ # Vue 3 + Jitsi source
├─ backend/ # Django REST API
└─ Documentation/ # Markdown docs (Windows path)



### VPS Production
/srv/inquirycircle/ # Git repo
├─ compose/ # docker-compose.prod.yml
├─ caddy/ # Caddyfile + static assets
├─ frontend/ # Vue source (if built on server)
├─ backend/ # Django source
└─ Documentation/

/etc/inquirycircle/ # Production env secrets
/var/lib/inquirycircle/ # Persistent runtime data


---

## Version Control
- GitHub repos:  
  - `scott009/InquiryCircle` → active Stage 2 repo.  
 
- Branch strategy:  
  - `main` → production-ready.  
  - `develop` → integration branch.  
  - `feature/*`, `hotfix/*` → scoped branches.  

---

## Security Boundaries
- **Development**: services local-only, test keys used.  
- **Production**: only Caddy exposed (80/443), TLS via Caddy, backend internal, secrets in `/etc/inquirycircle/env`.

---

## Monitoring Points
- Container CPU/memory usage.  
- Disk usage for volumes.  
- API response times.  
- Cert expiry warnings.  
- Failed authentication attempts.

---

**Related Documentation**:  
[operations-guide](./operations-guide.md) | [project-spec](./project-spec.md) | [README](./README.md) | [CHANGELOG](./CHANGELOG.md)

**Document Version**: v2.1.0 | **Last Updated**: 9/12/2025 | **Status**: ✅ Current

