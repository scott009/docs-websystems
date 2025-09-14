<!-- InquiryCircle v1 – Runbook – Caddy First Implementation – DRAFT – 2025-08-25 ET -->
<!-- Baseline Ref: ProjectBaseline §Constraints: Minimal Change -->

# Runbook: Caddy-First Implementation (v1)

**Project**: Inquiry Circle  
**Scope**: Stand up Caddy (as its own container) to serve the built Vue SPA and reverse-proxy the Django backend.  
**Out of Scope (v1)**: Any self-hosted Jitsi, Prosody/JWT/Jibri, key hashing, analytics.

---

## Definitions
- **Constraints**: Rules that govern our interaction and execution during development.
- **Requirements & Assumptions**: Non-negotiable system shape and expectations.
- **Milestones**: Checkpoints with explicit acceptance tests.

---

## Constraints (development interaction rules)

### Constraint: Minimal Change  
*(See ProjectBaseline §Constraints: Minimal Change for full policy)*

- Only change what the request **explicitly** covers; all else is **frozen**.  
- If a broader change is **strictly necessary**, pause and request: `ACK UNFREEZE <area>: <reason>`  
- You may add an **Impact Advisory** (warnings + optional follow-ups), but **do not implement** them.  
- **Verify**: show before/after for changed surfaces and confirm **no deltas** outside scope.

**PR/Commit checklist:**  
[ ] Confined to stated scope  
[ ] Impact Advisory provided (if relevant)  
[ ] No frozen-surface deltas  
[ ] (If needed) `ACK UNFREEZE …` recorded

---

- Operate **only in bash** on WSL and VPS (no PowerShell).  
- **No code edits** (Django/Vue) in this runbook. We only configure/launch Caddy and point it at an existing build.  
- **No database changes** (engine, schema, volumes).  
- **No Jitsi containers** in v1; Jitsi remains a **public iframe**.  
- Keep filesystem locations **as-documented** (WSL `~/inquirycircle`, VPS `/srv/inquirycircle`); do **not** install under `~` on VPS.  
- Keep changes **incremental**; after each step run the specified verification before proceeding.  
- Be **rollback-ready** at every step (retain prior Caddyfile and prior `dist/`).  
- Do not deviate from this runbook without an explicit note and rationale in the doc.  

---

## Requirements & Assumptions (system/architecture)
- Caddy runs as a **separate container**.  
- Backend service is reachable by **service name** on Docker network (e.g., `ic-backend:8000`).  
- The SPA is built by **Vite** and lives under `caddy/site/dist/` for Caddy to serve.  
- **Single docker network** for app services (e.g., `icnet`).  
- VPS domain `catbench.com` points to the server; Caddy will obtain **Let’s Encrypt** certs on ports **80/443**.  
- SPA routing uses **fallback to `index.html`**.  

---

## Phase 1 — Layout & Env Parity

**Actions**
1) Create/confirm directories on WSL and VPS:

```
inquirycircle/
  backend/
  frontend/
  caddy/
    Caddyfile
    site/
    logs/
  docker-compose.prod.yml
  docker-compose.dev.yml
  .env.example (WSL) / .env (VPS)
```

**Milestone M1 — Layout**
- Folders exist in **both** WSL and VPS.  
- `.env` present on VPS (secrets **not** committed to git).  

---

## Phase 2 — Compose: add Caddy service

**Actions** (excerpt)
```yaml
services:
  caddy:
    image: caddy:2
    container_name: ic-caddy
    restart: unless-stopped
    ports:
      - "80:80"      # VPS
      - "443:443"    # VPS
    volumes:
      - ./caddy/Caddyfile:/etc/caddy/Caddyfile:ro
      - ./caddy/site:/srv/site:ro
      - caddy_data:/data
      - caddy_config:/config
    depends_on:
      - backend
    networks: [icnet]

  backend:
    container_name: ic-backend
    # (existing config)
    networks: [icnet]

volumes:
  caddy_data:
  caddy_config:

networks:
  icnet:
    driver: bridge
```
**Milestone M2 — Service up**
- `docker compose up -d caddy` works cleanly (on WSL you may map to `:8080` instead of 80/443).  

---

## Phase 3 — WSL Caddyfile (HTTP, SPA + /api proxy)

**Actions**  
Create `caddy/Caddyfile` for **WSL** (local HTTP):

```
{
  auto_https off
}

:8080 {
  root * /srv/site/dist

  @api path /api/*
  handle @api {
    reverse_proxy ic-backend:8000
  }

  try_files {path} /index.html
  file_server

  log {
    output file /srv/site/../logs/access.log
  }
}
```

**Verification**
- Navigate to `http://localhost:8080` → SPA loads.  
- `http://localhost:8080/api/health` → 200 via proxy.  

**Milestone M3 — Local proxy OK**
- Both checks pass.  

---

## Phase 4 — Build SPA & stage artifacts

**Actions (WSL)**
```bash
cd frontend
npm ci
npm run build          # outputs to frontend/dist
mkdir -p ../caddy/site
rsync -a ./dist/ ../caddy/site/dist/
```

**Actions (VPS)**
- Ensure `/srv/inquirycircle/caddy/site/dist/` has the same build (rsync/scp if you built on WSL).

**Milestone M4 — Artifacts ready**
- `dist/` present under `caddy/site/dist/` on VPS.

---

## Phase 5 — VPS Caddyfile (HTTPS with Let’s Encrypt)

**Actions**  
`/srv/inquirycircle/caddy/Caddyfile`:

```
catbench.com {
  root * /srv/site/dist

  @api path /api/*
  handle @api {
    reverse_proxy ic-backend:8000
  }

  try_files {path} /index.html
  file_server

  log {
    output file /srv/logs/access.log
  }
}

www.catbench.com {
  redir https://catbench.com{uri}
}
```

**Verification**
- DNS A record points to VPS IP.  
- `docker compose up -d caddy` on VPS acquires certs.  

**Milestone M5 — HTTPS live**
- `https://catbench.com` serves SPA.  
- `https://catbench.com/api/health` → 200.  

---

## Phase 6 — Ops checks & rollback

**Quick checks**
- `docker logs ic-caddy --since=10m`  
- `tail -f caddy/logs/access.log`  

**Rollback**
- Restore prior `Caddyfile` and/or prior `site/dist/`.  
- `docker compose up -d caddy`.  

**Milestone M6 — Verified**
- Ops checks pass; site functional.  

---

## Phase 7 — Documentation & recordkeeping

**Actions**
- Capture:
  - Caddyfile SHA256
  - Frontend commit SHA used for build
  - Backend image tag
  - Compose file version/tag
- Update the **blackboard1-v1 note** with “Caddy separate container + SPA fallback confirmed.”

**Milestone M7 — Docs complete**
- Runbook marked **Accepted** (after review), artifacts recorded.

---

*Minimal Change: touch only what’s requested; anything else requires `ACK UNFREEZE`.*
