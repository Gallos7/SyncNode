# SyncNode ⚡️

> A modern, enterprise-grade issue tracking and team collaboration platform.

**SyncNode** is a full-stack, multi-tenant issue tracking system built for performance, security, and scalability. It combines a robust **FastAPI (Python)** backend with a highly responsive **React + Tailwind** frontend, featuring advanced Role-Based Access Control (RBAC) and real-time audit logging.

---

## 🎬 Demo Preview

<video src="https://github.com/user-attachments/assets/5a648d90-3de6-4a0d-be01-125c24adf2f6" controls="controls" muted="muted" style="max-height: 600px; width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);"></video>

---

## ✨ Key Features

- **🏢 Multi-Tenant Architecture**  
  Complete data isolation between company workspaces.

- **🔐 Enterprise-Grade Security**  
  JWT-based authentication with strict token handling, HttpOnly-ready architecture, and seamless multi-tab session synchronization.

- **🛡️ Advanced RBAC System**  
  A 6-tier permission model *(Superadmin, Owner, Admin, IT, Manager, Developer)* controlling access, actions, and visibility.

- **📋 Immutable Audit Logs**  
  Every issue mutation is tracked with full actor attribution and chronological history.

- **🛠️ IT Administration Tools**  
  Built-in capabilities for password resets, account recovery, and user management.

- **🐳 Fully Containerized**  
  Orchestrated via Docker Compose for seamless, reproducible environments across all machines.

---

## 🏗️ Tech Stack

### Backend
- **Framework:** FastAPI (Python)  
- **Database:** MySQL (SQLAlchemy ORM)  
- **Migrations:** Alembic  
- **Security:** Raw Bcrypt, Python-JOSE (JWT)  
- **Email Service:** Resend API  

### Frontend
- **Framework:** React 19 + Vite  
- **Styling:** Tailwind CSS v4  
- **Routing:** React Router v7  
- **HTTP Client:** Axios 

### DevOps
- **Containerization:** Docker & Docker Compose

---

## 📂 Project Structure

This project follows a **monorepo architecture**, fully orchestrated by Docker:

```text
SyncNode/
|
├── docker-compose.yml    # Master orchestration file
├── backend/              # FastAPI backend
│   ├── Dockerfile        # Backend container blueprint
│   ├── requirements.txt  # Python dependencies
|   ├── .env.example      # Environment variables template
│   ├── seed.py           # Database seeder script
|   ├── nuke.py           # Database reset utility
│   ├── alembic/          # Database migrations
│   └── app/              # Core API logic
│       ├── core/             # Configuration & settings
│       ├── db/               # Database engine & session handling
│       ├── models/           # SQLAlchemy models
│       ├── routers/          # API routes (endpoints)
│       ├── schemas/          # Pydantic schemas
│       └── services/         # Business logic layer
|
├── frontend/             # React (Vite) frontend
|   ├── Dockerfile        # Frontend container blueprint
|   ├── package.json      # Node dependencies
│   ├── src/              # React components and views
│   │   ├── components/   # Reusable UI components
│   │   ├── context/      # Global state (AuthContext)
│   │   ├── hooks/        # Custom hooks
│   │   ├── layouts/      # Layout components
│   │   ├── pages/        # Route-level pages
│   │   └── services/     # API communication (Axios)
```

---

## 🚀 Getting Started

SyncNode is fully containerized. You do not need to install Python, Node.js, or MySQL on your local machine to run this application.

---

### Prerequisites

- [Docker Desktop]`(https://www.docker.com/products/docker-desktop/)` installed and running.

---

### 1️⃣ Environment Setup

Clone the repository and set up your backend environment variables:

```bash
git clone "https://github.com/Gallos7/SyncNode.git"
cd SyncNode/backend
cp .env.example .env
```


*Note: Ensure you add your `RESEND_API_KEY` and update the `DATABASE_URL` in the `.env` file to point to the Docker database service (e.g., `mysql+pymysql://root:"Your_Password"@db:3306/syncnode`)*


---

### 2️⃣ Launch the Fleet

Return to the root project folder and start the entire stack:

```bash
cd ..
docker compose up --build
```

*Note: This single command will spin up the MySQL Database, the FastAPI Backend, and the React Frontend on an isolated network.*

- **Frontend UI**: `http://localhost:5173`
- **Backend Swagger API**: `http://localhost:8000/docs`
- **Database Port *(For DB Viewers)***: `localhost:3307`

---

## 🛠️ Developer Tools

To interact with the database inside the Docker container, open a new terminal in the root directory while the containers are running.

### 🌱 Apply Migrations & Seed the Database

Automatically populates the database with realistic sample data to facilitate local testing:
- **4 Isolated Companies** *(SyncNode System, TechFlow Inc, SoftSolutions, Innovate Ltd)*
- **7 Users** spanning the full RBAC hierarchy (Superadmin, Owner, Admin, IT, Developer)
- **3 Dummy Issues** and historical Activity Feed logs

```bash
# 1. Build the database tables
docker compose exec api alembic upgrade head

# 2. Seed the data
docker compose exec api python seed.py
```

**Test credentials (Password is `password123` for all):**
- **System Superadmin:** `superadmin@syncnode.com` (Global access)
- **Standard Admin:** `alex@techflow.com` (TechFlow workspace)
- **IT Administrator:** `david@techflow.com` (TechFlow IT roles & permissions)

---

### 🧨 Nuke the Database

⚠️ **Danger zone** — completely resets the database.

```bash
docker compose exec api python nuke.py
```

---
---

<div align="center">
  <p><i>Developed by Parissis Dimitris</i></p>
</div>
