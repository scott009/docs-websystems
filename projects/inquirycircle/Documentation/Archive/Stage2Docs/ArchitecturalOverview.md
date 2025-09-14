<!-- InquiryCircle2 – ArchitecturalOverview – Stage2 – 9/2/2025 at 6:45 AM ET -->  
<!-- accepted – 9/2/2025 at 7:00  AM ET -->  

# Architectural Overview — Full Project Implementation

## Purpose
Deliver a complete **InquiryCircle** web application for collaborative video conferencing with role-based access control, facilitator messaging, and key-based authentication. Built with containerized architecture ensuring dev/prod parity and single public entrypoint.

## Core Application Features
- **Video Conferencing**: Jitsi Meet integration for inquiry group sessions
- **Role-Based Access**: Facilitators vs. participants with different capabilities  
- **Key-Based Authentication**: No traditional user accounts; access via keys
- **Customizable Circles**: Virtual meeting spaces for different groups
- **Facilitator Messaging**: HTML message system for session guidance
- **Session Management**: Circle creation, participant management, session control

## Technical Architecture

### Core Components
- **Caddy (reverse proxy / static / TLS)** — the only public-facing service; routes traffic, serves built assets, handles HTTPS/TLS
- **Frontend (Vue 3 + Tailwind CSS + Jitsi SDK)** — single-page app with video integration, compiled to static files
- **Backend (Django + Gunicorn)** — REST/API for circles, authentication, messaging, and Jitsi room management
- **Data layer** — **SQLite** file (v1) with path to **PostgreSQL** later

### How Components Interact
```
Internet → Caddy → ├─ serves SPA (built Vue+Tailwind+Jitsi static assets)
                   └─ proxies /api → Backend (Django/Gunicorn)
                                     ↳ manages circles, auth, messages
                                     ↳ integrates with Jitsi Meet rooms
                                     ↳ reads/writes DB (SQLite → Postgres)
```

## Frontend Implementation (Vue 3 + Tailwind + Jitsi)
- **Build Process**: Vite build → static assets served by Caddy
- **Video Integration**: Jitsi Meet SDK for embedded conferencing (external Jitsi service integration)
- **UI Components**: 
  - Video conference interface with Jitsi embedding
  - Circle management dashboard (facilitator view)
  - Participant interface with message display
  - Key-based login/access forms
- **Routing**: SPA routing with Caddy fallback to `index.html`
- **Styling**: Tailwind CSS (processed via PostCSS) for consistent, utility-first UI

## Backend Implementation (Django)
- **Authentication API**: Key-based access control, role determination
- **Circles API**: Create/manage inquiry circles, participant lists  
- **Messages API**: Facilitator HTML message management and delivery
- **Jitsi Integration**: External Jitsi service integration - room creation, configuration, participant management
- **Session Management**: Circle state, active sessions, participant tracking
- **Private Network**: Only accessible via Caddy proxy on internal Docker network

## Data Architecture
- **Stage 2**: SQLite file persisted on volume/bind mount (working prototype)
- **Stage 3**: PostgreSQL as dedicated container (production-ready persistence)
- **Data Models**: Circles, Keys/Auth, Messages, Sessions, Participant relationships

## Container Architecture
- **Single-purpose containers**: Frontend runtime, Backend API service, Caddy as gateway
- **Network Isolation**: All services on private Docker network; only Caddy exposed
- **Persistence**: Named volumes for Caddy TLS state, bind mounts for SQLite, static assets
- **Development Parity**: Same container setup WSL ↔ VPS, different ports only

## Environment Strategy
- **WSL Development**: Full topology match with localhost ports (8080, etc.)
- **VPS Production (catbench.com)**: Identical container setup, Caddy handles HTTPS/certificates
- **Configuration**: Environment-specific compose files, shared Caddyfile patterns

---

## Directory Structure — WSL (Development)
```
/home/<user>/inquirycircle/
├─ compose/
│  ├─ docker-compose.dev.yml      # WSL development setup
│  └─ .env                        # local development environment
├─ caddy/
│  ├─ Caddyfile                   # reverse proxy + static serving config
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

## Directory Structure — VPS Production (catbench.com)
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
└─ README.md

/etc/inquirycircle/               # system config (restricted access)
├─ env                            # production environment secrets
└─ caddy/                         # operational overrides (if needed)

# Note: Static files served from /srv/inquirycircle/caddy/site/dist/

/var/lib/inquirycircle/           # persistent runtime data
├─ backend/
│  └─ sqlite/                     # SQLite database location
└─ caddy/                         # TLS cert storage (or use named volumes)
```

## Development Workflow
1. **Local Development**: Edit code → build frontend → test on localhost:8080
2. **Integration Testing**: Full stack with Jitsi, circles, messaging locally  
3. **Production Deploy**: Same containers, same configs → catbench.com deployment
4. **No Surprises**: Dev/prod parity ensures predictable deployments

## Security Model
- **Single Public Entrypoint**: Only Caddy exposed; all services behind reverse proxy
- **Key-Based Access**: No username/password; access controlled via secure keys
- **Role Enforcement**: Backend validates facilitator vs. participant permissions
- **TLS Termination**: Caddy handles all HTTPS/certificate management
- **Network Isolation**: Backend and data layer on private container network

## Scalability Path
- **Phase 1**: SQLite + single backend container
- **Phase 2**: PostgreSQL container + potential backend scaling
- **Phase 3**: Horizontal scaling with load balancing (if needed)
- **Jitsi**: External service integration only (self-hosted Jitsi planned for Stage 3, not covered here)

---

## Guiding Principles
- **Container Single-Purpose**: Frontend build artifacts, Backend API service, Caddy gateway — separate concerns
- **Configuration as Code**: All setup in version-controlled compose files and configs
- **Environment Parity**: Identical development and production container topology
- **Security First**: Private networks, minimal exposure, TLS everywhere
- **Operational Simplicity**: Standard Docker patterns, clear logging, easy rollback