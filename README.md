# MedConnect

> A full-stack medical prescription management platform connecting patients, doctors, chemists, and administrators.

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Backend: Flask](https://img.shields.io/badge/Backend-Flask-lightgrey?logo=flask)
![Frontend: Vue 3](https://img.shields.io/badge/Frontend-Vue%203-42b883?logo=vue.js)
![Database: SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)

---

## Overview

MedConnect is a web application that digitises the prescription workflow between healthcare participants:

- **Doctors** create digital prescriptions with detailed medicine instructions.
- **Patients** view their prescriptions and place medicine orders with a chemist.
- **Chemists** receive and fulfil orders, updating status as they progress.
- **Administrators** review and approve doctor and chemist registrations before they can use the platform.

The application supports four UI languages: **Azerbaijani (AZ)**, **English (EN)**, **Russian (RU)**, and **Turkish (TR)**.

---

## Table of Contents

1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Prerequisites](#prerequisites)
4. [Getting Started](#getting-started)
   - [Docker (Recommended)](#docker-recommended)
   - [Manual Setup](#manual-setup)
5. [Creating an Admin Account](#creating-an-admin-account)
6. [API Overview](#api-overview)
7. [Order Status Workflow](#order-status-workflow)
8. [Project Structure](#project-structure)
9. [User Roles](#user-roles)
10. [Security Notes](#security-notes)
11. [License](#license)

---

## Features

- **Role-based dashboards** — separate interfaces for patients, doctors, chemists, and admins
- **Digital prescriptions** — create prescriptions with multiple medicines, dosage, frequency, and duration
- **Medicine orders** — patients order from an approved chemist; chemists track and fulfil orders
- **Admin approval flow** — doctors and chemists must be approved before they can log in
- **JWT authentication** — stateless token-based auth with a 24-hour expiry
- **Profile management** — all users can update their profile details
- **Multi-language support** — AZ / EN / RU / TR via a built-in i18n module
- **Docker support** — single `docker-compose up` spins up the full stack

---

## Tech Stack

### Backend
| Package | Purpose |
|---|---|
| Flask | Web framework |
| Flask-SQLAlchemy | ORM |
| Flask-Migrate (Alembic) | Database migrations |
| Flask-JWT-Extended | JWT authentication |
| Flask-Bcrypt | Password hashing |
| Flask-CORS | Cross-Origin Resource Sharing |
| python-dotenv | Environment variable loading |
| SQLite | Default database |

### Frontend
| Package | Purpose |
|---|---|
| Vue 3 | UI framework |
| Vue Router 4 | Client-side routing |
| Pinia | State management |
| Axios | HTTP client |
| Vite | Build tool / dev server |

---

## Prerequisites

- **Python** 3.9+
- **Node.js** 18+ and **npm** 9+
- **Docker** & **Docker Compose** *(only needed for the Docker setup)*

---

## Getting Started

### Docker (Recommended)

The fastest way to run the full stack locally or in production.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/medconnect.git
   cd medconnect
   ```

2. **Create a root `.env` file** and set a strong secret key:
   ```bash
   echo "JWT_SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')" > .env
   ```

3. **Build and start the containers:**
   ```bash
   docker-compose up --build
   ```
   Run in detached mode (background):
   ```bash
   docker-compose up -d --build
   ```

4. **Access the application:**
   | Service | URL |
   |---|---|
   | Frontend | http://localhost |
   | Backend API | http://localhost:5000 |

5. **Stop the containers:**
   ```bash
   docker-compose down
   ```

---

### Manual Setup

#### Backend

1. Navigate to the backend directory and create a virtual environment:
   ```bash
   cd backend
   python -m venv venv
   ```

2. Activate the virtual environment:
   - **Windows:** `venv\Scripts\activate`
   - **Linux / macOS:** `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file and set your secret key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and replace `JWT_SECRET_KEY` with a strong random value.

5. Apply database migrations:
   ```bash
   flask db upgrade
   ```

6. Start the development server:
   ```bash
   python app.py
   ```
   The API will be available at **http://localhost:5000**.

#### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   The default `VITE_API_BASE_URL=http://localhost:5000` works for local development.

4. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at **http://localhost:5173**.

---

## Creating an Admin Account

There is no public registration endpoint for admins. Use the Flask CLI command after the backend is running:

```bash
cd backend
ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD='Y0urStr0ngP@ssw0rd!' ADMIN_NAME="Site Admin" flask create_admin
```

The admin can then log in at `/admin/login` in the frontend.

---

## API Overview

All endpoints are prefixed with `/api/`. Protected routes require a `Bearer` token in the `Authorization` header.

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/register/<role>` | — | Register a patient, doctor, or chemist |
| POST | `/api/login/<role>` | — | Log in (role: patient, doctor, chemist, admin) |
| GET | `/api/me` | ✅ | Get current user profile |
| PUT | `/api/profile` | ✅ | Update current user profile |
| GET | `/api/doctors` | — | List all approved doctors |
| GET | `/api/chemists` | — | List all approved chemists |
| GET | `/api/patients/search?q=` | ✅ Doctor | Search patients by name, email, or phone |
| POST | `/api/prescriptions` | ✅ Doctor | Create a prescription |
| GET | `/api/prescriptions` | ✅ | List prescriptions for current user |
| GET | `/api/prescriptions/<id>` | ✅ | Get a specific prescription |
| PUT | `/api/prescriptions/<id>` | ✅ Doctor | Update a prescription |
| POST | `/api/orders` | ✅ Patient | Place a medicine order |
| GET | `/api/orders` | ✅ | List orders for current user |
| GET | `/api/orders/<id>` | ✅ | Get a specific order |
| POST | `/api/orders/<id>/accept` | ✅ Chemist | Accept a pending order |
| PUT | `/api/orders/<id>/status` | ✅ Chemist | Update order status |
| GET | `/api/admin/overview` | ✅ Admin | Platform-wide statistics and recent activity |
| GET | `/api/admin/pending` | ✅ Admin | List pending doctor/chemist registrations |
| POST | `/api/admin/approve` | ✅ Admin | Approve a doctor or chemist |
| POST | `/api/admin/refuse` | ✅ Admin | Refuse (delete) a doctor or chemist |
| GET | `/api/health` | — | Health check |

---

## Order Status Workflow

```
pending → accepted → preparing → ready → completed
                                        ↘ cancelled
```

| Status | Meaning |
|---|---|
| `pending` | Order placed by patient, awaiting a chemist |
| `accepted` | A chemist has claimed the order |
| `preparing` | Chemist is preparing the medicines |
| `ready` | Order is ready for pickup / delivery |
| `completed` | Order fulfilled |
| `cancelled` | Order was cancelled |

---

## Project Structure

```
medconnect/
├── backend/
│   ├── app.py              # Flask application & all API routes
│   ├── models.py           # SQLAlchemy models (Doctor, Patient, Chemist, Prescription, Medicine, Order, Admin)
│   ├── requirements.txt    # Python dependencies
│   ├── Dockerfile          # Backend container definition
│   ├── .env.example        # Example environment variables
│   └── migrations/         # Alembic database migrations
├── frontend/
│   ├── src/
│   │   ├── views/          # Page-level Vue components
│   │   │   ├── admin/      # Admin dashboard & login
│   │   │   ├── doctor/     # Doctor dashboard & prescription views
│   │   │   ├── patient/    # Patient dashboard & order views
│   │   │   └── chemist/    # Chemist dashboard & order views
│   │   ├── components/     # Reusable Vue components
│   │   ├── stores/         # Pinia state stores
│   │   ├── router/         # Vue Router configuration
│   │   ├── services/       # Axios API service layer
│   │   └── i18n/           # Translations (AZ, EN, RU, TR)
│   ├── Dockerfile          # Frontend container (Nginx)
│   ├── nginx.conf          # Nginx configuration for production
│   ├── .env.example        # Example environment variables
│   └── package.json        # Node dependencies
├── docker-compose.yml      # Multi-container Docker configuration
└── .gitignore
```

---

## User Roles

| Role | Capabilities |
|---|---|
| **Patient** | Register, view prescriptions, place and track medicine orders |
| **Doctor** | Create and update prescriptions, search patients |
| **Chemist** | Accept orders, update order status, manage fulfilment |
| **Admin** | Approve / refuse doctor and chemist registrations, view platform statistics |

> **Note:** Doctor and Chemist accounts require admin approval before the first login.

---

## Security Notes

- **Never** commit `.env` files — they are excluded in `.gitignore`
- Set a strong, randomly generated `JWT_SECRET_KEY` before deploying
- The SQLite database file (`database.db`) contains sensitive user data and is excluded from version control
- Use HTTPS in production (configure your reverse proxy / load balancer accordingly)
- Tokens expire after **24 hours**; refresh your session by logging in again

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
