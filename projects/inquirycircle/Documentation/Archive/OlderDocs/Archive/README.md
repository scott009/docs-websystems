# InquiryCircle

A web-based video conferencing platform for inquiry groups with role-based access control.

## Overview

InquiryCircle provides **Circles** - web pages with embedded Jitsi video conferencing and lightweight control interfaces. Users can join as either **Facilitators** (with special privileges) or **Participants** using key-based authentication.

## Architecture

- **Frontend**: Vue.js v3 + Tailwind CSS
- **Backend**: Django (Python)
- **Video**: Jitsi Meet (iframe embed)
- **Web Server**: Caddy
- **Process Manager**: Gunicorn + systemd
- **Hosting**: VPS (Ubuntu 22.04)
- **Authentication**: Key-based (no user accounts)

## Project Structure

```
InquiryCircle/
├── backend/          # Django application
├── frontend/         # Vue.js application
├── config/           # Caddy, Gunicorn configs
├── deployment/       # Deployment scripts and docs
└── docs/            # Additional documentation
```

## Quick Start

### Development Setup

1. **Backend Setup**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   python manage.py runserver
   ```

2. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Production Deployment

See `deployment/README.md` for VPS deployment instructions.

## Core Features

- **Circle Management**: Create and manage video conference rooms
- **Role-Based Access**: Facilitator keys with elevated privileges
- **Embedded Video**: Seamless Jitsi Meet integration
- **Admin Interface**: Global Circle and key management
- **Simple Access Flow**: Homepage → Key Entry → Circle Routing

## Version 1 Scope

- JSON file persistence for data storage
- Environment configuration support
- Basic Circle functionality
- Jitsi iframe embedding
- Simple role differentiation
- Admin controls for Circle/key management

## Demo Keys

- `admin-master-key` (Admin access)
- `facilitator-demo` (Facilitator for demo-circle)
- `participant-demo` (Participant for demo-circle)
