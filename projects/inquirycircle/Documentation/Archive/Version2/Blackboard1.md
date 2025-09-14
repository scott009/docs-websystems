# Blackboard1
<!-- InquiryCircle v2 – Blackboard Note – blackboard1.md -->
# Inquiry Circle Blackboard (v2)

**Document Type**: Project Note  
**Project**: Inquiry Circle  
**Applies To**: System Version 2  
**Filename**: blackboard1.md  

---

## System Architecture Overview
- **Backend**: Django (Python) served by Gunicorn, managed with systemd (inside container).  
- **Frontend**: Vue 3 + Tailwind CSS + Vite (served via container).  
- **Web Server**: Caddy **as a separate container** (handles HTTPS, reverse proxy, static files).  
- **Database**: SQLite (development) / PostgreSQL (production, containerized).  
- **Video**:  
  - **Version 1**: Jitsi Meet embedded via **public server iframe**.  
  - **Version 2 (planned)**: Evaluate adding Jitsi server container(s) into the stack.  

---

## Core Concepts
- **Inquiry Group**: A group of humans using a Circle. Roles: *Facilitators* (have facilitator keys) and *Participants*.  
- **Circle**: A web page with embedded Jitsi + control UI. The core unit of interaction.  
- **Facilitator Key**: Grants special rights in a Circle (e.g., muting, managing session flow). Keys are Circle-specific.  
- **Inquiry Session**: A meeting of an Inquiry Group. Sessions are transient, may add scheduling later.  
- **Circle Server**: The web app that provides Circles. Managed by a Circle Server Admin (global rights: create/destroy Circles, manage keys).  
- **Access Flow**: Users enter keys on landing page → system grants Circle access + displays info based on key.  

---

## Components
1. **Backend (Django)**  
   - Endpoints: `/api/health`, `/api/records`, `/api/circles`.  
   - Auth: key-based (hashed keys planned for v2.x).  

2. **Frontend (Vue 3)**  
   - Healthcheck page.  
   - Circle join UI.  
   - Participant/facilitator dashboards.  

3. **Video (Jitsi)**  
   - v1: Public Jitsi server via iframe.  
   - v2: Evaluate embedding self-hosted Jitsi container(s).  

4. **Reverse Proxy (Caddy)**  
   - Runs as its own container.  
   - Handles HTTPS with automatic Let’s Encrypt certs.  
   - Routes frontend, backend, and Jitsi subdomains.  

---

## Deployment
- **Local Dev (WSL)**: Immutable images, no bind mounts in prod-dry-run.  
- **VPS (catbench.com)**:  
  - `docker-compose.prod.yml` for full stack.  
  - Caddy container handles HTTPS and routing.  
  - Django backend served with Gunicorn + systemd inside container.  

---

## Data Model (initial)
- **Circle**: { id, name, created_at }  
- **FacilitatorKey**: { id, circle_id, key_hash, created_at }  
- **Participant**: { id, circle_id, display_name, joined_at }  
- **Record**: { id, name, value, created_at }  

---

## API Endpoints
- `/api/health` → returns 200 + status.  
- `/api/records` → CRUD for test model.  
- `/api/circles` → Circle CRUD (protected).  

---

## Security
- Keys stored in plain text for v2.0 baseline (to be hashed in v2.1).  
- No expiration or rotation yet.  
- HTTPS enforced via Caddy.  
- No user accounts/passwords (keys only).  

---

## File Structure (planned)
