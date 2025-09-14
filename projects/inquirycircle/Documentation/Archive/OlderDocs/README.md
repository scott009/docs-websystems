<!-- Document Version: 1.1.0 -->
<!-- Last Updated: 2025-08-02 -->

# InquiryCircle v1.1.0 - Human Readable Documentation

*Document: `README.md`*

## What's New in v1.1.0

### CircleMessage1 Feature
- **Purpose**: Allow circle facilitators to set an HTML message displayed to all visitors of a circle
- **Key Features**:
  - Facilitators can enter and approve messages via the control panel
  - Messages are displayed to all circle visitors in a clean, readable house style
  - Uses VueJS and Tailwind CSS for consistent UI
  - Messages are persisted in storage and displayed outside the debug window

### UI Improvements
- Jitsi video frame resized to 75% of original height
- Participant message box moved below Jitsi window for better layout
- Removed "Message from Circle Facilitator" header for cleaner display

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
  - Facilitator message system (new in v1.1.0)

### 2. Role System
- **Facilitators**:
  - Elevated privileges
  - Meeting controls
  - Participant management
  - Message management (new in v1.1.0)
- **Participants**:
  - Standard access
  - Basic meeting functions
  - View facilitator messages (new in v1.1.0)

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
  SECRET_KEY=your-secret-key
  DEBUG=True
  ALLOWED_HOSTS=localhost,127.0.0.1
  JITSI_DOMAIN=meet.jit.si
  ```

### Circle Message Feature (New in v1.1.0)
- Messages are stored in `backend/data/circles.json`
- Facilitators can update messages via the control panel
- Messages are sanitized for security before display

## Deployment Notes

### Version 1.1.0 Changes
- Updated `circle.html` template with new UI layout
- Added message persistence logic in `storage.py`
- Enhanced facilitator API in `views.py`
- Server restart required after template changes

## Changelog

### v1.1.0 (2025-08-02)
- **NEW**: CircleMessage1 feature allowing facilitators to set messages for participants
- **IMPROVED**: UI layout with resized Jitsi frame and repositioned message display
- **IMPROVED**: Cleaner message display without header text
- **FIXED**: Message persistence issues in backend storage

### v1.0 (2025-08-01)
- Initial release
- Basic circle management with role-based access
- Jitsi Meet integration
- Key-based authentication system

## Version Information
- **Version**: 1.1.0
- **Last Updated**: 2025-08-02
- **Compatibility**: Python 3.8+, Node.js 14+

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
├── docfig/                          # Docfig documentation
│   ├── InquiryCircle1.0.Blackboard.md  # v1.0 Blackboard
│   ├── InquiryCircle1.1.Blackboard.md  # v1.1 Blackboard
│   └── readme1.1.md                 # v1.1 Human-readable docs
├── .gitignore                       # Git ignore rules
├── README.md                        # Main project documentation (this document)
└── readme1.1.md                     # Human-readable documentation
