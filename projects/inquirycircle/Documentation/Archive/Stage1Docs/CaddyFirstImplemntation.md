
# Caddy-first Implementation (high level)
<!-- InquiryCircle – Notes – 8/24/2025 at 10:00 PM ET -->


## Phase 1 — Local baseline (WSL)
**Goal:** Prove the entrypoint pattern with a simple, reproducible container.

- Create a tiny **Caddyfile** that:  
  - Serves a placeholder SPA page at `/` (e.g., “InquiryCircle v1 — gateway OK”).  
  - (Optional) Adds a stub reverse proxy route like `/api` → a temporary upstream (e.g., `whoami`) just to validate routing.  
- Run Caddy as a **single container** (or minimal compose) with:  
  - Bind mount for Caddyfile  
  - Bind mount for a `site/` folder (your placeholder `index.html`)  
- **Validate locally**: `http://localhost:PORT/` shows the placeholder; `/api` hits the stub.  

✅ **Exit criteria:** You can start/stop Caddy cleanly; placeholder is served; proxy stub works.  

---

## Phase 2 — Prod-dry-run (still WSL)
**Goal:** Match the shape you’ll use in prod.

- Switch to a **compose file** you plan to reuse on the VPS (service name `caddy`, named volumes for `/data` and `/config`).  
- Keep the same Caddyfile and placeholder site.  
- Confirm restart policy, simple logs, and that the container recovers after restart.  

✅ **Exit criteria:** Same commands you’ll use on the VPS work locally without edits.  

---

## Phase 3 — Early deployment on VPS (catbench.com)
**Goal:** Put Caddy in front of the world, even before the app is ready.

- Prepare the directory layout on the VPS (e.g., `/opt/caddy/`).  
- Copy over the Caddyfile and placeholder site.  
- Start the Caddy container using the same compose from Phase 2.  
- Point your DNS **A record** to the VPS.  
- Add your **ACME email**; let Caddy obtain certs.  
- Open ports **80/443** (firewall).  

✅ **Exit criteria:** `https://catbench.com/` serves the placeholder over TLS.  

---

## Phase 4 — Make Caddy the stable ingress
**Goal:** Freeze the gateway so app teams can iterate behind it.

- Keep `/` serving static content (later: your built Vue+Tailwind SPA).  
- Keep `/api` reverse-proxying to an **internal** upstream (later: Django/Gunicorn).  
- Reserve additional routes/hostnames for future apps (e.g., `ic.catbench.com`, `/admin`, `/other-app`).  

✅ **Exit criteria:** Caddy config doesn’t need to change much as services come online.  
