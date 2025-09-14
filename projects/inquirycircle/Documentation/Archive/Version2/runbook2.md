<!-- InquiryCircle: Runbook (not yet accepted) – 2025-08-25 11:45 AM ET -->
# InquiryCircle v1 – Runbook (Caddy First Implementation)

**Constraint:** Minimal Change  
*(Do not propagate edits from this runbook into other documents until explicitly accepted.)*

---

## Phase 1: Prepare VPS

1. **SSH into VPS**  
   ```bash
   ssh root@catbench.com
Update and upgrade packages

bash
Copy code
apt update && apt upgrade -y
Install Docker & Docker Compose plugin

bash
Copy code
apt install -y docker.io docker-compose-plugin
systemctl enable docker
systemctl start docker
Phase 2: Folder structure
On VPS, place under /srv instead of ~ so collaborators don’t rely on root’s home:

bash
Copy code
/srv/inquirycircle/
  docker-compose.prod.yml
  backend/
  frontend/
  caddy/
    Caddyfile
    data/   (TLS certs, auto-managed by Caddy)
    logs/   (log output if mounted)
  db/
  docs/
Phase 3: Caddy setup
Minimal Caddyfile (/srv/inquirycircle/caddy/Caddyfile):

caddyfile
Copy code
{
    email admin@catbench.com
}

catbench.com {
    reverse_proxy backend:8000
    handle_path /api/* {
        reverse_proxy backend:8000
    }
    handle_path /* {
        reverse_proxy frontend:5173
    }
    log {
        output file /srv/logs/caddy_access.log
    }
}
docker-compose.prod.yml snippet:

yaml
Copy code
version: "3.9"
services:
  caddy:
    image: caddy:2
    container_name: ic-caddy
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./caddy/Caddyfile:/etc/caddy/Caddyfile
      - ./caddy/data:/data
      - ./caddy/logs:/srv/logs
    networks:
      - icnet

  backend:
    build: ./backend
    restart: unless-stopped
    expose:
      - "8000"
    networks:
      - icnet

  frontend:
    build: ./frontend
    restart: unless-stopped
    expose:
      - "5173"
    networks:
      - icnet

networks:
  icnet:
Phase 4: Sanity checks
Ports, DNS, and certificates

Ports 80/443 open on VPS (UFW / security group).

No other server (Apache/Nginx) binding 80/443.

A (and AAAA, if present) records for catbench.com point to VPS.

System clock synced (timedatectl status) so Let’s Encrypt works smoothly.

Django headers
In backend settings.py (prod config):

python
Copy code
ALLOWED_HOSTS = ["catbench.com"]
CSRF_TRUSTED_ORIGINS = ["https://catbench.com"]
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
Phase 5: Deployment
Bring up stack

bash
Copy code
cd /srv/inquirycircle
docker compose -f docker-compose.prod.yml up -d
Verify Caddy logs

bash
Copy code
docker compose -f docker-compose.prod.yml logs --tail=50 caddy
Check endpoints

https://catbench.com → frontend loads

https://catbench.com/api/health → backend health check

Open Items (block acceptance)
Sync VPS system clock (systemd-timesyncd or chrony).

Fix Caddy logs path (./caddy/logs -> /srv/logs mount or update Caddyfile).

Verify Django prod headers above.