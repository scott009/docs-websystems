<!-- {{PROJECT_NAME}} – Infrastructure – Stage1 – {{TIMESTAMP}} -->

# Infrastructure

## Purpose
Define the environments and system layout for {{PROJECT_NAME}}. This document captures *where* development and production take place — not constraints (project-specification.md) or procedures (operations-guide.md).

---

## Environments

### Development Environment
- **Platform**: [Windows/Mac/Linux + Container Details]
- **Container Runtime**: Docker + Docker Compose
- **Development Tools**: [IDE, extensions, etc.]
- **Access URLs**:  
  - http://localhost:[port] → Main application entrypoint
  - http://localhost:[port] → Frontend development server
  - http://localhost:[port] → Backend development server

### Local Container Environment
- **Purpose**: Dev/dry-run environment with production topology
- **Code root**: `[/path/to/project]`
- **IDE Integration**: [Your IDE setup]
- **Workflow**: All development occurs in containerized environment

### Production Environment
- **Platform**: [Cloud provider, VPS, or physical server details]
- **Access**: [How to access production environment]
- **Project root**: `[/path/to/production/deployment]`
- **Static assets**: `[/path/to/static/files]`
- **Persistent data**: `[/path/to/persistent/storage]`

---

## DNS & Domain Configuration

- **Primary Domain**: [your-primary-domain.com]
- **Application URL**: [https://app.your-domain.com]
- **IP Address**: [Your production IP]
- **Subdomains**:
  - `api.` → API endpoints
  - `admin.` → Administrative interface
  - `dev.` → Development/staging environment
  - `docs.` → Documentation (if separate)

### Reserved Subdomains
- `www`, `staging`, `test`, `backup`, `monitoring`

---

## Network Topology

### Development Environment
```
Docker network: {{PROJECT_NAME}}_network
├── gateway (exposed: [port]:[internal-port])
│   ├─ routes /api/* → backend:[port]
│   └─ serves static files from frontend build
├── backend (internal: [port])
│   ├─ REST API endpoints
│   └─ connects to database:[port]
└── database (internal: [port])
    └─ persistent storage via volumes
```

### Production Environment
```
Internet (port 80/443) → Gateway/Reverse Proxy
├── TLS termination
├── Static file serving
└── API proxy /api/* → Backend Container
    ├── Application logic
    ├── Database connections
    └── External service integrations
```

---

## Storage & Persistence

### Development Storage
- **Database**: Docker volume `{{PROJECT_NAME}}_db_data`
- **Static files**: Local bind mount `./static:/app/static`
- **Logs**: Docker volume `{{PROJECT_NAME}}_logs`
- **Backups**: Local directory `./backups`

### Production Storage
- **Database**: `/var/lib/{{PROJECT_NAME}}/db`
- **Static assets**: `/srv/{{PROJECT_NAME}}/static`
- **Application logs**: `/var/log/{{PROJECT_NAME}}`
- **Backups**: `/srv/{{PROJECT_NAME}}/backups`
- **SSL certificates**: `/etc/ssl/{{PROJECT_NAME}}`

---

## Security Configuration

### Development Security
- **Network**: Internal Docker network isolation
- **Authentication**: Test credentials only
- **TLS**: Self-signed certificates or HTTP only
- **Firewall**: Host firewall manages access

### Production Security
- **Network**: Private internal networks, public gateway only
- **Authentication**: Production credential management
- **TLS**: Valid SSL certificates with auto-renewal
- **Firewall**: Strict ingress rules (80/443 only)
- **Secrets**: Secure credential storage system

---

## Monitoring & Logging

### Development Monitoring
- **Container logs**: `docker-compose logs`
- **Application logs**: Console output
- **Health checks**: Manual curl commands
- **Performance**: Local resource monitoring

### Production Monitoring
- **System metrics**: [Your monitoring solution]
- **Application logs**: Centralized logging system
- **Health endpoints**: Automated monitoring
- **Alerts**: [Your alerting system]
- **Uptime monitoring**: External service monitoring

---

## Backup & Recovery

### Development Backup
- **Code**: Git repository with remote origin
- **Database**: Local database dumps
- **Configuration**: Version controlled docker-compose files

### Production Backup
- **Database**: Automated daily backups
- **Static files**: Synchronized to backup storage
- **Configuration**: Infrastructure as code repository
- **Recovery time objective**: [Your RTO target]
- **Recovery point objective**: [Your RPO target]

---

## External Dependencies

### Required External Services
- **[Service 1]**: [Purpose, how it's used]
- **[Service 2]**: [Purpose, how it's used]
- **[Service 3]**: [Purpose, how it's used]

### Optional External Services
- **[Service A]**: [Purpose, fallback if unavailable]
- **[Service B]**: [Purpose, fallback if unavailable]

### Service Integration Points
```
{{PROJECT_NAME}}
├── Authentication via [External Auth Service]
├── Email via [Email Service Provider]
├── File storage via [Storage Service]
├── Analytics via [Analytics Service]
└── Monitoring via [Monitoring Service]
```

---

## Development Workflow

### Local Development Setup
1. Clone repository
2. Install Docker and Docker Compose
3. Copy environment configuration
4. Run `docker-compose up -d`
5. Access application at http://localhost:[port]

### Code Deployment Flow
```
Developer Machine
├── Git commit/push
├── CI/CD Pipeline (if configured)
├── Staging deployment
├── Production deployment
└── Health verification
```

---

## Production Deployment Architecture

### Container Orchestration
- **Orchestrator**: [Docker Compose / Kubernetes / etc.]
- **Service discovery**: [How services find each other]
- **Load balancing**: [How traffic is distributed]
- **Health checks**: [How service health is monitored]

### Scaling Strategy
- **Horizontal scaling**: [How to scale out]
- **Vertical scaling**: [How to scale up]
- **Database scaling**: [Database scaling approach]
- **Static asset scaling**: [CDN or file serving strategy]

---

## Environment Variables & Configuration

### Development Configuration
```bash
# Database
DB_HOST=localhost
DB_PORT=[port]
DB_NAME={{PROJECT_NAME}}_dev

# Application
APP_ENV=development
DEBUG=true
LOG_LEVEL=debug

# External Services
API_KEY_SERVICE1=[dev-key]
API_URL_SERVICE2=[dev-url]
```

### Production Configuration
```bash
# Database
DB_HOST=[production-db-host]
DB_PORT=[port]
DB_NAME={{PROJECT_NAME}}_prod

# Application
APP_ENV=production
DEBUG=false
LOG_LEVEL=info

# External Services
API_KEY_SERVICE1=[production-key]
API_URL_SERVICE2=[production-url]
```

---

**Related Documentation**:  
[operations-guide](./operations-guide.md) | [project-specification](./project-specification.md) | [current-status](./current-status.md)

**Infrastructure Version**: v1.0.0 | **Last Updated**: {{DATE}} | **Next Review**: Quarterly