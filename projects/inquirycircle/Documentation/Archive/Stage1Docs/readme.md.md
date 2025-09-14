# readme.md
<!-- InquiryCircle – Notes – 8/24/2025 at 9:31 PM ET -->
now suggest an application st

## Overview of the Inquiry Circle Project (Version 1)

The **Inquiry Circle Project** is a web-based platform designed to support structured group inquiry sessions, especially for Buddhist recovery communities. Its purpose is to create a simple, reliable environment where participants can gather online, guided by facilitators, with a focus on meaningful conversation rather than technical complexity.

---

## Core Concepts
- **Inquiry Group**: A group of people who regularly meet for inquiry sessions.  
- **Circle**: The central meeting space — implemented as a web page that embeds a Jitsi video-conference window along with a control UI.  
- **Inquiry Session**: A live, time-bound meeting of an Inquiry Group within a Circle.  
- **Facilitator Keys**: Special access codes that grant facilitators additional rights (e.g., managing aspects of the Circle).  
- **Participants**: Regular group members who join sessions using standard access.  

---

## System Components
- **Frontend**: Vue 3 + Tailwind CSS + Vite.  
- **Backend**: Django with Gunicorn, exposing APIs for managing Circles, users, and session data.  
- **Video Integration**: Jitsi Meet embedded in Circle pages.  
- **Web Server**: Caddy reverse proxy for serving frontend + backend, handling SSL.  
- **Database**: SQLite in early development; PostgreSQL planned for VPS deployments.  
- **Hosting**: Docker Compose orchestration in two environments:  
  - Local WSL (dev + prod-dry-run)  
  - VPS (catbench.com) for live deploy  

---

## Administrative Roles
- **Circle Server Admin**: Global authority who manages Circles and facilitator keys.  
- **Facilitators**: Hold facilitator keys for specific Circles.  
- **Participants**: Join sessions with standard access (no special privileges).  

---

## Access Flow
1. A user enters the landing page of the Circle server.  
2. They provide a facilitator key or participant key.  
3. Based on the key, they are granted access to a Circle page with the correct role (facilitator vs participant).  
