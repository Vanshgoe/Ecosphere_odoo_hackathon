# EcoSphere — ESG Management Platform Frontend

React + TypeScript single-page application for the Odoo 18 EcoSphere backend.

## Stack

- **Runtime**: React 18, React Router 6, Axios, TanStack Query v5
- **Charts**: Apache ECharts (via `echarts-for-react`)
- **Build**: Vite 5, TypeScript 5
- **Styling**: Vanilla CSS with custom design tokens (dark enterprise theme)

## Setup

```bash
cd frontend
npm install
cp .env.example .env   # optional — defaults work with Vite proxy
```

### Environment

| Variable | Default | Purpose |
|---|---|---|
| `VITE_ODOO_URL` | `http://localhost:8069` | Odoo backend origin. In dev, Vite proxies `/odoo/*` to this origin. |

## Run

### Backend (Odoo 18 + PostgreSQL via Docker)

```bash
cd backend
cp .env.example .env
# Place the OCA report_xlsx addon in third_party_addons/
docker compose up --build
```

Open `http://localhost:8069`, create a database, and install the EcoSphere modules in order:
`ecosphere_core` → `ecosphere_environment` → `ecosphere_social` → `ecosphere_governance` → `ecosphere_gamification` → `ecosphere_dashboard` → `ecosphere_reports`.

### Frontend (Development)

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173`. Vite proxies API calls to the Odoo backend.

### Frontend (Production Build)

```bash
cd frontend
npm run build
npm run preview   # optional — serves the built files locally
```

## Authentication

The backend exposes authenticated JSON-RPC API routes. Log in through Odoo (`/web/session/authenticate`) first; the frontend sends `withCredentials: true` and does not store credentials or tokens. There is no dedicated frontend login screen — the Odoo web login is required.

## Implemented Modules

| Module | Routes | Backend Integration |
|---|---|---|
| **Dashboard** | `/` | Live ESG scores, KPIs, emissions chart, goal/issue charts |
| **Environmental** | Carbon Transactions, Environmental Goals | Full CRUD via API |
| **Environmental** | Emission Factors, Product ESG Profiles | Capability-unavailable (backend-only) |
| **Social** | CSR Activities | Full CRUD via API |
| **Social** | Employee Participation, Diversity Dashboard | Capability-unavailable (backend-only) |
| **Governance** | Policies, Audits, Compliance Issues, Risk Register | Full CRUD via API |
| **Governance** | Policy Acknowledgements | Capability-unavailable (backend-only) |
| **Gamification** | Challenges, Rewards | Full CRUD via API |
| **Gamification** | Leaderboard | Read-only via API |
| **Gamification** | Challenge Participation, Badges | Capability-unavailable (backend-only) |
| **Reports** | Environmental, Social, Governance, ESG Summary, Custom Builder | Dashboard data + visual reference (report generation not exposed by API) |
| **Settings** | Departments, Categories, ESG Configuration, Notification Settings | Visual reference (settings not exposed by API) |

## Backend Capabilities Not Exposed via Frontend API

- Emissions-over-time time series
- Department ESG ranking
- Recent activity feed
- Report generation and export (PDF, Excel, CSV)
- ESG configuration persistence
- Department / Category CRUD
- Notification settings persistence
- Policy acknowledgement workflow
- Employee participation / challenge join workflow
- Badge management and awards
- Diversity metrics
- Login / logout UI
- CORS configuration

## Project Structure

```
src/
  api/          JSON-RPC Axios client and typed endpoint calls
  hooks/        TanStack Query hooks
  components/   App shell, layout, reusable state/card/table primitives
  pages/        Route-level views
  types/        TypeScript interfaces matching backend API shapes
  styles/       Global CSS with design tokens and responsive styling
```

## Known Limitations

- No frontend login screen — requires Odoo web session
- Report generation buttons are disabled (backend does not expose report endpoints)
- Settings toggles are read-only placeholders
- The `VITE_ODOO_URL` environment variable must be set correctly for production deployments behind a reverse proxy
