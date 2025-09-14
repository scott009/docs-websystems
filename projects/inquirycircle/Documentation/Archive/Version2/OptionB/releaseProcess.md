# releaseProcess
<!-- InquiryCircle: Caddy Option B – Release Process (Mini) – 2025-08-29 11:00 AM ET -->
# Caddy (Option B) — Release & Rollback Process

**Goal:** Reproducible, auditable releases with quick promotion and rollback.

---

## 1) Versioning & tags
- **Base:** upstream Caddy version (e.g., `2.8.4`).
- **IC tag:** `ic-caddy:<base>-<inc>` → e.g., `ic-caddy:2.8.4-1`, `-2`.
- Optional date tag for ops notes: `ic-caddy:2.8.4-2025.08.29-a`.
- Never deploy `latest`. Always pin.

---

## 2) Branch & PR flow
- Changes to Caddy config live under `caddy/`.
- Open a PR with:
  - Summary of ingress changes (paths, hosts, headers).
  - Impact assessment (backend expectations, security headers).
  - Test notes (local curl checks).
- Reviewer confirms:
  - No bind mounts.
  - `/data` and `/config` volumes present.
  - SPA fallback and `/api` contract unchanged (unless explicitly intended).

---

## 3) Build & publish
- Build image from `caddy/`.
- Tag with the **next** release tag.
- Push to registry; capture the **digest** in the PR.
- Attach short **release notes** (what changed, why, risk level).

---

## 4) Promote
- **Dev (WSL):** deploy tag, verify `/` and `/api/health`.
- **Staging (optional):** same tag; hit endpoints and TLS.
- **Prod (VPS):** pull same tag; `up -d`; verify:
  - `https://catbench.com/` (TLS OK)
  - `https://catbench.com/api/health` (200)
  - Caddy logs clean (no 502/404 storms).

---

## 5) Post-deploy checklist (prod)
- ✅ ACME cert renewed/valid; no rate-limit warnings.
- ✅ Backend sees `X-Forwarded-Proto=https`.
- ✅ Security headers present (HSTS if enabled).
- ✅ Error budget unaffected; no spike in 5xx.
- ✅ Record: tag, digest, deploy time, operator.

---

## 6) Rollback
- Trigger when:
  - Regressions at the edge (wrong routes/headers).
  - Backend incompatibility.
- Action:
  - Re-deploy previous tag.
  - Verify endpoints again.
  - Annotate incident with: failing tag, fix tag, duration, user impact.

---

## 7) CI outline (nice-to-have)
- On PR merge to `main` under `caddy/`:
  - Lint config (syntax).
  - Build image; run minimal container test (starts, listens).
  - Push to registry with the computed tag.
  - Post digest + tag back to PR.
- Manual “Promote to Prod” job pulls the tag on VPS and restarts service.

---

## 8) Guardrails
- Pin both **Caddy base** and **IC tag**.
- Keep VPS clock in sync.
- Treat Caddy edits as **infra changes** with PR + tag bump.
- Avoid ad-hoc hotfixes; if unavoidable, follow up with a formal tagged release.

---

**Outcome:** Stable, reversible ingress with clear provenance of every change.
