# EcoSphere Odoo 18 Backend

EcoSphere is a native Odoo ESG MVP: configurable E/S/G metrics and scoring, carbon ledger, CSR and governance records, employee gamification, JSON dashboard endpoints, and QWeb reporting.

## Start

Copy `.env.example` to `.env`, place the OCA `report_xlsx` addon in `third_party_addons/`, then run `docker compose up --build`. Open `http://localhost:8069`, create a database, and install in order: `ecosphere_core`, `ecosphere_environment`, `ecosphere_social`, `ecosphere_governance`, `ecosphere_gamification`, `ecosphere_dashboard`, `ecosphere_reports`.

Dashboard JSON endpoints: `/ecosphere/dashboard/summary` and `/ecosphere/dashboard/emissions` (authenticated JSON-RPC). Both return ECharts-compatible `labels`, `series`, and `metadata`.

Carbon is calculated as activity data × a configured, company-specific emission factor. Seed factors must be validated for the deployment region; no factors in this repository are scientifically authoritative. Missing scoring metrics are intended to be excluded from a category calculation.

All business records carry a company where applicable. Access groups are defined in Core; production deployment should add company record rules tailored to the organisation's manager hierarchy.
