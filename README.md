# EcoSphere — ESG Management Platform

EcoSphere is a full-stack ESG (Environmental, Social, Governance) management platform built on **Odoo 18** with a modern **React + TypeScript** frontend.

## Architecture

```
├── backend/          Odoo 18 custom addons + Docker Compose
│   ├── custom_addons/
│   │   ├── ecosphere_core/
│   │   ├── ecosphere_environment/
│   │   ├── ecosphere_social/
│   │   ├── ecosphere_governance/
│   │   ├── ecosphere_gamification/
│   │   ├── ecosphere_dashboard/
│   │   └── ecosphere_reports/
│   └── docker-compose.yml
└── frontend/         React SPA (Vite + TypeScript)
```

## Quick Start

### Backend

```bash
cd backend
cp .env.example .env
docker compose up --build
```

Open `http://localhost:8069`, create a database, install modules in order:
`ecosphere_core` → `ecosphere_environment` → `ecosphere_social` → `ecosphere_governance` → `ecosphere_gamification` → `ecosphere_dashboard` → `ecosphere_reports`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Log in via Odoo first (`http://localhost:8069/web`).

### Production Build

```bash
cd frontend
npm run build
```

## Features

- **Executive Dashboard** — Live ESG scores, KPIs, ECharts visualizations
- **Environmental** — Carbon transaction ledger, environmental goals with progress tracking
- **Social** — CSR activity management with approval lifecycle
- **Governance** — Policy management, audits, compliance issues, risk register
- **Gamification** — Challenges, rewards, XP leaderboard
- **Reports** — ESG summary with radar charts, report catalog
- **Settings** — Department/category management, ESG configuration

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Odoo 18, Python, PostgreSQL |
| Frontend | React 18, TypeScript 5, Vite 5 |
| State | TanStack Query v5 |
| Charts | Apache ECharts |
| API | JSON-RPC over Axios |
| Infrastructure | Docker, Docker Compose |

## Team

Built for the Odoo Hackathon.