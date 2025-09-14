<!-- InquiryCircle2 – README – Stage2 – 9/2/2025 at 11:20 AM ET -->

# InquiryCircle

A collaborative video conferencing platform designed for inquiry-based learning groups, featuring role-based access control, facilitator messaging, and key-based authentication.

## Overview

InquiryCircle creates virtual spaces where facilitators can guide inquiry-based discussions through integrated video conferencing, real-time messaging, and structured participant management. Built with modern web technologies and containerized architecture for reliable deployment.

### Key Features

- **Video Conferencing**: Integrated Jitsi Meet for high-quality group video sessions
- **Key-Based Authentication**: Secure, simple access without traditional user accounts
- **Role Management**: Distinct facilitator and participant capabilities
- **Virtual Circles**: Customizable spaces for different inquiry groups
- **Facilitator Messaging**: Real-time HTML message system for session guidance
- **Session Control**: Complete circle lifecycle management

## Technology Stack

### Frontend
- **Vue 3** - Progressive JavaScript framework
- **Tailwind CSS** - Utility-first styling with PostCSS
- **Jitsi Web SDK** - Video conferencing integration
- **Pinia** - State management
- **Axios** - HTTP client for API communication
- **Vite** - Build tool and dev server

### Backend
- **Django 4.2** - Python web framework
- **Django REST Framework** - API development
- **Gunicorn** - WSGI HTTP server
- **SQLite/PostgreSQL** - Database (migration path included)

### Infrastructure
- **Docker** - Container platform
- **Docker Compose** - Multi-container orchestration
- **Caddy** - Reverse proxy with automatic HTTPS
- **Ubuntu 22.04** - Host OS (WSL2 and VPS)

## Project Structure

```
inquirycircle/
├── frontend/                 # Vue 3 SPA application
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── services/        # API and Jitsi integration
│   │   ├── stores/          # Pinia state management
│   │   └── router/          # Vue Router configuration
│   └── dist/                # Built static assets
├── backend/                 # Django REST API
│   ├── ic_core/            # Main Django project
│   ├── circles/            # Circle management app
│   ├── authentication/     # Key-based auth app
│   ├── messages/           # Facilitator messaging
│   └── jitsi_integration/  # Jitsi room management
├── caddy/                  # Reverse proxy configuration
│   ├── Caddyfile          # Caddy server config
│   └── site/              # Static file serving
├── compose/               # Docker Compose files
│   ├── docker-compose.dev.yml
│   └── docker-compose.prod.yml
└── docs/                  # Project documentation
```

## Quick Start

### Prerequisites

- Windows 10/11 with WSL2 (Ubuntu 22.04)
- Docker and Docker Compose installed in WSL
- Node.js 18+ and npm
- Python 3.10+
- Git

### Development Setup

1. **Clone the repository**
```bash
cd /home/$USER
git clone [repository-url] inquirycircle
cd inquirycircle
```

2. **Set up the frontend**
```bash
cd frontend
npm install
npm run dev  # Development server at http://localhost:5173
```

3. **Set up the backend**
```bash
cd ../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver  # API at http://localhost:8000
```

4. **Run with Docker Compose**
```bash
cd ../compose
docker-compose -f docker-compose.dev.yml up -d
# Application at http://localhost:8080
```

## Configuration

### Environment Variables

Create a `.env` file:
- **Development**: `compose/.env` 
- **Production**: `/etc/inquirycircle/env` (for security)

Example `.env` contents:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL - Phase 2)
DB_USER=inquirycircle
DB_PASSWORD=secure-password
DB_NAME=inquirycircle

# Jitsi Configuration
JITSI_APP_ID=your-jitsi-app-id
JITSI_API_KEY=your-jitsi-api-key
```

### Caddy Configuration

The Caddyfile handles:
- Static file serving for the Vue SPA
- API reverse proxy to Django backend
- Automatic HTTPS with Let's Encrypt (production)
- SPA routing with fallback to index.html

## Deployment

### Production Deployment (VPS)

1. **Prepare the VPS**
```bash
ssh user@catbench.com
sudo mkdir -p /srv/inquirycircle
cd /srv/inquirycircle
git clone [repository-url] .
```

2. **Configure environment**
```bash
sudo mkdir -p /etc/inquirycircle
sudo cp compose/.env.example /etc/inquirycircle/env
sudo nano /etc/inquirycircle/env  # Add production values
```

3. **Build and deploy**
```bash
cd frontend
npm ci && npm run build
cp -r dist/* ../caddy/site/

cd ../compose
docker-compose -f docker-compose.prod.yml up -d
```

4. **Verify deployment**
```bash
curl https://catbench.com/api/health/
# Visit https://catbench.com in browser
```

## Database Migration

### SQLite to PostgreSQL

1. **Backup existing data**
```bash
python manage.py dumpdata > backup.json
```

2. **Update compose file** to include PostgreSQL service

3. **Update Django settings** for PostgreSQL connection

4. **Migrate and restore**
```bash
python manage.py migrate
python manage.py loaddata backup.json
```

## API Documentation

### Key Endpoints

- `GET /api/health/` - Service health check
- `POST /api/auth/verify-key/` - Validate access key
- `GET/POST /api/circles/` - Circle CRUD operations
- `GET/POST /api/messages/` - Message management
- `POST /api/jitsi/config/` - Get Jitsi room configuration

### Authentication

All API requests require a valid access key:
```javascript
headers: {
  'Authorization': 'Key your-access-key-here'
}
```

## Development Guidelines

### Frontend Development
- Follow Vue 3 Composition API patterns
- Use Tailwind utility classes for styling
- Implement proper error handling for API calls
- Test Jitsi integration across browsers

### Backend Development
- Follow Django REST Framework best practices
- Write comprehensive API tests
- Use Django's ORM for database operations
- Implement proper logging

### Git Workflow
1. Create feature branch from main
2. Make changes and test locally
3. Run linters and tests
4. Create pull request with description
5. Deploy to staging for testing
6. Merge to main and deploy to production

## Testing

### Frontend Tests
```bash
cd frontend
npm run test:unit
npm run test:e2e
```

### Backend Tests
```bash
cd backend
python manage.py test
```

### Integration Tests
```bash
# Run full stack locally
docker-compose -f docker-compose.dev.yml up
# Execute integration test suite
npm run test:integration
```

## Troubleshooting

### Common Issues

**502 Bad Gateway**
- Check if backend container is running: `docker ps`
- Restart backend: `docker-compose restart backend`

**Jitsi Connection Failed**
- Verify external Jitsi service is accessible
- Check API credentials in environment variables

**Database Connection Error**
- Verify database container is running
- Check credentials in `.env` file
- Ensure migrations are applied

**HTTPS Not Working**
- Verify DNS A records point to server IP
- Check Caddy logs: `docker logs ic-caddy`
- Ensure ports 80/443 are open in firewall

## Monitoring

### Health Checks
```bash
# API health
curl http://localhost:8080/api/health/

# Container status
docker-compose ps

# View logs
docker-compose logs -f [service-name]
```

### Performance Monitoring
- Frontend: Browser DevTools Performance tab
- Backend: Django Debug Toolbar (development)
- Infrastructure: `docker stats` for resource usage

## Security

### Best Practices
- All secrets in environment variables
- HTTPS enforced in production
- Backend only accessible through Caddy
- Key validation on all protected endpoints
- CORS properly configured
- Input validation and sanitization
- SQL injection prevention via ORM

### Key Management
- Generate secure random keys
- Distribute keys through secure channels
- Implement key rotation policy
- Log key usage for audit

## Contributing

1. Review the `ProjectBaseline.md` for development constraints
2. Follow the `devGuidance.md` for setup instructions
3. Check `Runbook.md` for deployment procedures
4. Submit issues for bugs or feature requests
5. Create pull requests for contributions

## Documentation

### Stage 2 Documentation
- `ArchitecturalOverview.md` - System design and components
- `ProjectBaseline.md` - Development standards and constraints
- `devGuidance.md` - Developer setup and workflow
- `SharedSystemContext.md` - Infrastructure details
- `Runbook.md` - Deployment and operations procedures
- `LabelingStandard.md` - Documentation conventions

## Roadmap

### Stage 2 (Current)
- ✅ Caddy reverse proxy setup
- ✅ Vue 3 + Jitsi frontend
- ✅ Django REST API backend
- ✅ Key-based authentication
- ✅ External Jitsi integration
- ✅ SQLite persistence (working prototype)

### Stage 3 (Future)
- PostgreSQL migration (production-grade persistence)
- Self-hosted Jitsi infrastructure
- Advanced facilitator tools
- Recording capabilities
- Analytics dashboard
- Multi-tenant support

## Support

For issues, questions, or contributions:
- Review documentation in `/Stage2Docs`
- Check troubleshooting guide above
- Submit issues on GitHub
- Contact project maintainers

## License

[License information to be added]

---

**Project Status**: Stage 2 - Full application implementation with external Jitsi integration

**Last Updated**: September 2, 2025