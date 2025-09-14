# SharedSystem Context
<!-- Shared System Context – Notes – 9/1/2025 at 4:30 PM ET -->


## DEV-PC (Windows 10 + WSL Ubuntu 22.04)
- **Purpose**: Local development machine.  
- **Usage**: Run Linux commands (`bash`, `docker`, `git`) inside WSL.  
- **Access URLs**: `http://localhost:<port>` in browser for local testing.  

---

## WSL Ubuntu (inside DEV-PC)
- **Purpose**: Development / prod dry-run environment (Docker Engine + Docker Compose).  
- **Code Location**: `/home/<user>/ProjectLocation` (inside WSL filesystem).  
- **Notes**: Docker images built here for local testing are **separate** from those on the VPS.  

---

## VPS (catbench.com, Ubuntu 22.04)
- **Purpose**: Remote deployment target.  
- **Access**: SSH available via `user@catbench.com`.  
VPS (catbench.com, Ubuntu 22.04)
Purpose: Remote deployment target.
Access: SSH available via user@catbench.com.
IP address: 72.60.26.118
The project root directory is /srv/inquirycircle
Catbench.com DNS
A Record * 72.60.26.118
A Record @ 72.60.26.118
CNAME Record container1 host.catbench.com.
CNAME Record container2 host.catbench.com.
CNAME Record dev.icircle host.catbench.com.
CNAME Record icgeneric host.catbench.com.
CNAME Record icircle host.catbench.com.
CNAME Record jitsi.icircle host.catbench.com.
CNAME Record ssh host.catbench.com.
CNAME Record www host.catbench.com.
