<!-- InquiryCircle2 – README – Stage2 – 9/4/2025 at 11:20 AM ET -->

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
└── Documentation/         # Project documentation
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

## Documentation

- [Project Specification](./ProjectSpec.md) - Architecture, constraints, and standards
- [Operations Guide](./OperationsGuide.md) - Development workflow and deployment procedures
- [Infrastructure](./Infrastructure.md) - System environments and network architecture

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
- Review documentation in `/Documentation`
- Check Operations Guide troubleshooting section
- Submit issues on GitHub
- Contact project maintainers

## License

[License information to be added]

---

**Project Status**: Stage 2 - Full application implementation with external Jitsi integration

**Last Updated**: September 4, 2025