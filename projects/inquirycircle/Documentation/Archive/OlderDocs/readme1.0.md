<!-- Document Version: 1.0 -->
<!-- Last Updated: 2025-08-01 -->

# InquiryCircle v1.0 - Human Readable Documentation

*Document: `readme1.0.md`*

## System Overview
- **Type**: Web-based video conferencing platform
- **Purpose**: Facilitate inquiry groups with role-based access control
- **Core Concept**: "Circles" as dedicated web pages with embedded Jitsi video conferencing

## Technical Stack
- **Frontend**: Vue.js v3 + Tailwind CSS
- **Backend**: Django (Python)
- **Video Solution**: Jitsi Meet (iframe embed)
- **Web Server**: Caddy
- **Process Manager**: Gunicorn + systemd
- **Hosting**: VPS (Ubuntu 22.04)
- **Authentication**: Key-based (no traditional user accounts)

## Core Components

### 1. Circle Management
- **Purpose**: Create and manage video conference rooms
- **Key Features**:
  - Role-based access control (Facilitator/Participant)
  - Jitsi Meet integration
  - Key-based authentication

### 2. Role System
- **Facilitators**:
  - Elevated privileges
  - Meeting controls
  - Participant management
- **Participants**:
  - Standard access
  - Basic meeting functions

### 3. Technical Architecture
```
InquiryCircle/
├── backend/          # Django application
│   ├── inquirycircle/  # Main project settings
│   └── circles/       # Circles app (models, views, storage)
├── frontend/         # Vue.js application
│   ├── src/          # Source files
│   └── public/       # Static assets
├── config/           # Server configurations
│   ├── caddy/        # Caddy web server configs
│   └── gunicorn/     # Gunicorn service files
├── deployment/       # Deployment scripts
└── docs/            # Documentation
```

## Key Configuration Files

### Backend Configuration
- `backend/.env` - Environment variables (copy from `.env.example`)
  ```
  DEBUG=True
  SECRET_KEY=your-secret-key
  JITSI_APP_ID=your-jitsi-app-id
  ```

### Frontend Configuration
- `frontend/.env` - Frontend environment variables
  ```
  VUE_APP_API_URL=http://localhost:8000
  VUE_APP_JITSI_DOMAIN=meet.jit.si
  ```

## Setup Instructions

### Backend (Django)
1. Environment setup:
   ```bash
   cd backend
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Unix/Mac: source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

2. Run development server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend (Vue.js)
```bash
cd frontend
npm install
npm run dev
```

## Data Model

### Circle
- `id`: Unique identifier
- `name`: Display name
- `jitsi_room`: Jitsi room name
- `facilitator_key`: Secret key for facilitators
- `participant_key`: Secret key for participants

### Session
- `circle`: ForeignKey to Circle
- `start_time`: Session start timestamp
- `end_time`: Session end timestamp
- `active`: Boolean status

## API Endpoints

### Circle Management
- `GET /api/circles/`: List all circles
- `POST /api/circles/`: Create new circle
- `GET /api/circles/<id>/`: Get circle details
- `POST /api/circles/<id>/join/`: Join a circle

## Security Considerations
- All keys should be securely hashed
- Use HTTPS in production
- Regular security audits recommended

## Demo Credentials
- Admin: `admin-master-key`
- Facilitator: `facilitator-demo` (for demo-circle)
- Participant: `participant-demo` (for demo-circle)

## File Structure
```
InquiryCircle/
│
├── backend/                          # Django backend
│   ├── inquirycircle/                # Main project package
│   │   ├── __init__.py
│   │   ├── settings.py              # Main settings file
│   │   ├── urls.py                  # Root URL configuration
│   │   └── wsgi.py                  # WSGI config
│   │
│   ├── circles/                      # Circles app
│   │   ├── __init__.py
│   │   ├── admin.py                 # Admin interface config
│   │   ├── apps.py                  # App config
│   │   ├── models.py                # Data models
│   │   ├── storage.py               # Data storage implementation
│   │   ├── urls.py                  # App URL routing
│   │   └── views.py                 # Request handlers
│   │
│   ├── manage.py                    # Django management script
│   ├── requirements.txt             # Python dependencies
│   └── .env                         # Environment variables (gitignored)
│
├── frontend/                        # Vue.js frontend
│   ├── public/                      # Static files
│   │   ├── index.html               # Main HTML file
│   │   └── favicon.ico
│   │
│   ├── src/                         # Source files
│   │   ├── assets/                  # Static assets
│   │   ├── components/              # Vue components
│   │   ├── router/                  # Vue Router config
│   │   ├── views/                   # Page components
│   │   ├── App.vue                  # Root Vue component
│   │   └── main.js                  # Entry point
│   │
│   ├── package.json                 # NPM dependencies
│   └── vue.config.js                # Vue CLI config
│
├── config/                          # Server configurations
│   ├── caddy/                       # Caddy web server configs
│   └── gunicorn/                    # Gunicorn service files
│
├── deployment/                      # Deployment scripts
├── docs/                            # Documentation files
├── .gitignore                       # Git ignore rules
├── README.md                        # Main project documentation
└── readme1.0.md                     # Human-readable documentation
```

## Version Information
- **Version**: 1.0
- **Last Updated**: 2025-07-31
- **Compatibility**: Python 3.8+, Node.js 14+
