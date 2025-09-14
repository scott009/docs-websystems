<!-- InquiryCircle – Notes – 8/24/2025 at 10:12 PM ET -->
# Architectural overview (high level) — updated with directory structures

## Purpose
Deliver a simple, reliable **v1** web app for Inquiry Circles with a clear separation of concerns and a single public entrypoint.

## Core pieces
- **Caddy (reverse proxy / static / TLS)** — the only public-facing service; routes traffic and serves built assets.
- **Frontend (Vue 3 + Tailwind CSS)** — a single-page app compiled to static files.
- **Backend (Django + Gunicorn)** — REST/API and server logic, private behind Caddy.
- **Data layer** — **SQLite** file (v1) with a path to **PostgreSQL** later.

## How they fit together
Internet → Caddy → ├─ serves SPA (built Vue+Tailwind static assets)
└─ proxies /api → Backend (Django/Gunicorn)
↳ reads/writes DB (SQLite now; Postgres later)

markdown
Copy
Edit

## Frontend (Vue 3 + TailwindCSS with PostCSS) in v1
- Built once (Vite build) → **static assets**.  
- Tailwind (processed via PostCSS) provides utility-first styling for fast, consistent UI.  
- SPA routing supported by Caddy fallback to `index.html`.  

## Backend (Django) in v1
- Minimal endpoints (auth/keys, circle/session basics).
- Private service on internal network; only Caddy can reach it.

## Data approach
- **Start: SQLite file persisted on a volume/bind mount** (no separate DB container).
- **Later: swap to Postgres** as a dedicated container; update app config and run migrations.

## Environments
- **WSL dev & prod-dry-run**: same topology as prod; local ports only.
- **VPS (catbench.com)**: identical shape; Caddy handles HTTPS and routing.

---

## Directory structure — WSL (dev + prod-dry-run)
/home/<you>/inquiry-circle/
├─ compose/ # docker-compose files (dev/dry-run)
│ ├─ compose.yml
│ └─ .env # local-only environment (never commit real secrets)
├─ caddy/
│ ├─ Caddyfile # source-of-truth (bind-mounted)
│ └─ site/ # placeholder or built SPA (dist/)
├─ frontend/ # Vue 3 + Tailwind source
│ └─ dist/ # Vite build output (served by Caddy in dry-run)
├─ backend/ # Django source
│ ├─ ic_core/ …
│ ├─ manage.py
│ └─ db/ # SQLite file here (bind-mount for persistence)
├─ ops/
│ └─ notes/ # runbooks/labels
└─ README.md

yaml
Copy
Edit

**Notes (WSL):**
- Keep everything under your home for easy iteration.
- Dry-run mirrors prod: Caddy serves `/` and proxies `/api` to backend.

---

## Directory structure — VPS (catbench.com) (collaborator-friendly; no `~`)
/opt/inquiry-circle/ # app "code & infra" workspace (git repo can live here)
├─ compose/
│ ├─ compose.yml # production compose
│ └─ .env.example # template; real secrets live in /etc/ic/env
├─ caddy/
│ ├─ Caddyfile # tracked config (bind-mounted)
│ └─ site/ # built SPA or placeholder index.html
├─ frontend/ # optional (if building on-server); else CI copies dist to /srv/ic/spa
│ └─ dist/
├─ backend/ # Django app (if building on-server)
│ └─ ic_core/ …
└─ docs/ # project docs, runbooks

Copy
Edit
/etc/ic/ # system config (restricted)
├─ env # real environment file(s) used by compose
└─ caddy/ # optional: ops-only snippets/overrides

Copy
Edit
/srv/ic/ # public/static artifacts served by Caddy
└─ spa/ # final built frontend assets (dist/)

Copy
Edit
/var/lib/ic/ # persistent runtime data (not in repo)
├─ backend/
│ └─ sqlite/ # SQLite file location for v1 (bind-mount into backend)
└─ caddy/
├─ data/ # if ever bind-mounting; otherwise use named volumes
└─ config/

Copy
Edit
/var/log/ic/ # optional host-side logs (if you tee/rotate outside Docker)
└─ caddy/

markdown
Copy
Edit

**Notes (VPS):**
- **/opt/inquiry-circle**: developer workspace; grant group access to collaborators.
- **/etc/ic**: admin-only secrets and operational config.
- **/srv/ic**: what Caddy serves (e.g., SPA build, future static assets).
- **/var/lib/ic**: persistent data (e.g., SQLite v1). For Caddy’s `/data` and `/config` prefer **named volumes**; map paths here only if you later decide to bind-mount or back them up externally.

**Group setup hint:**
sudo groupadd icdev
sudo chgrp -R icdev /opt/inquiry-circle /srv/ic
sudo chmod -R g+rwX /opt/inquiry-circle /srv/ic
sudo find /opt/inquiry-circle /srv/ic -type d -exec chmod g+s {} ;

markdown
Copy
Edit

---

## Guiding principles (v1)
- Keep containers **single-purpose**; **frontend and backend in separate containers**.
- **One entrypoint (Caddy)** for security, simplicity, and easy multi-app hosting.
- Use **named volumes** for Caddy’s `/data` and `/config` so TLS state persists across redeploys.