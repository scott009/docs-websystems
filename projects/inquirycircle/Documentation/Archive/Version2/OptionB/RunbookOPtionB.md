# RunbookOPtionB
<!-- InquiryCircle: Caddy Option B – Runbook (Concise) – 2025-08-29 11:00 AM ET -->
# Caddy as Custom Docker Image (Option B) — Runbook

**Principle:** No bind mounts. Bake config into the image. Persist only `/data` and `/config` via named volumes.

---

## 0) Prereqs
- Docker Engine + Compose on WSL and VPS.
- A container registry you can push to (Docker Hub or GHCR).
- DNS A/AAAA for `catbench.com` → VPS IP.
- VPS firewall allows 80/443.
- VPS clock synced (ACME requires correct time).

---

## 1) Repo layout (high level)
- Keep a `caddy/` folder in the repo (config + optional static assets).
- Include a tiny Dockerfile that copies config/assets into the image.
- Do **not** use host bind mounts in Compose for Caddy.

---

## 2) Build locally (WSL)
- Choose a **pinned tag** (example): `ic-caddy:2.8.4-1`.
- Build the image in the `caddy/` folder.
- Sanity test locally with Compose:
  - Publish `:8080` (dev) instead of `:80/443`.
  - Define **named volumes** for `/data` and `/config`.
  - Bring up, verify:
    - `http://localhost:8080/` (SPA or placeholder)
    - `http://localhost:8080/api/health` (backend proxied)
- Logs:
  - `docker compose logs --tail=80 caddy`
- Health check:
  - Confirm Caddy started and routing works.

---

## 3) Push to registry
- Tag image for your registry namespace.
- Push the exact tag. Record the **image digest**.

---

## 4) VPS deployment
- Pull the same pinned image tag on VPS.
- Compose file references your **pinned tag**.
- Expose ports 80/443 on the VPS service.
- Ensure **ACME email** is set in config; first start obtains certs.
- Verify:
  - `https://catbench.com/` (loads over TLS)
  - `https://catbench.com/api/health` (200 OK)

---

## 5) Operational checks
- TLS: Certs stored in named volume `/data` (persist across restarts).
- Headers: `X-Forwarded-Proto` honored by backend; Django settings correct.
- Observability: stdout logs captured by Docker; optional file logging if needed.
- Restarts: `restart: unless-stopped`; confirm auto-recovery on reboot.

---

## 6) Change management
- Any Caddy change = PR → approved → **new image tag** → deploy.
- No live edits or bind mounts; configuration drift is eliminated.

---

## 7) Rollback (fast path)
- Re-deploy the **previous known-good tag**.
- Validate endpoints; leave a short incident note (tag, time, reason).

---

## 8) Common pitfalls to avoid
- Unpinned `latest` tags.
- Missing DNS/ports or unsynced VPS clock (ACME fail).
- Editing config without bumping image tag.
- Mixing bind mounts back in (reintroduces flakiness).

---

**Status:** Adopted direction for IC; use this for WSL and VPS.  
**Constraint:** Minimal Change to other docs until explicitly accepted.
