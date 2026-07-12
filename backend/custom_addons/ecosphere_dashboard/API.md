# EcoSphere frontend API (v1)

All API calls are authenticated Odoo JSON requests. Base path: `/api/ecosphere/v1`.
Every response has either `{ "success": true, "data": ... }` or `{ "success": false, "error": { "code": "...", "message": "..." } }`. List responses also contain `{ "pagination": { "limit", "offset", "total" } }`.

## Authentication and browser requests

Log in through Odoo first (normally `POST /web/session/authenticate`), then make requests with the returned `session_id` cookie. In a browser, the frontend must use `credentials: 'include'`; a cross-origin frontend additionally needs a reverse proxy/Odoo CORS configuration which allows its origin and credentials. The routes intentionally use `auth='user'`, so no bearer token is accepted and no endpoint bypasses Odoo ACLs, record rules, or allowed companies.

```js
const call = (path, params = {}) => fetch(`/api/ecosphere/v1/${path}`, {
  method: 'POST', credentials: 'include', headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({jsonrpc: '2.0', method: 'call', params, id: Date.now()}),
}).then(r => r.json()).then(r => r.result);
const goals = await call('goals/list', {limit: 20, offset: 0, status: 'active'});
const created = await call('goals/create', {values: {name: 'Reduce emissions', category_id: 1, metric_id: 2, target_date: '2027-12-31'}});
```

Odoo `type='json'` routes use JSON-RPC, so parameters go inside `params` as above. `me` is the GET-equivalent current-user endpoint: call `POST /me` with `{}`.

## Endpoints

| Endpoint | Body / parameters |
| --- | --- |
| `POST /me` | none; user, active company and allowed companies returned |
| `POST /goals/{list,get,create,update,delete}` | Goal fields: `name, company_id, category_id, metric_id, baseline_value, target_value, current_value, start_date, target_date, status, responsible_user_id` |
| `POST /carbon/{list,get,create,update,delete}` | Carbon fields: `name, company_id, source_model, source_record_id, source_reference, source_type, activity_value, activity_unit, emission_factor_id, transaction_date, state` |
| `POST /carbon/summary` | filters; totals and emissions by scope |
| `POST /csr/{list,get,create,update,delete}` | CSR fields: `name, description, company_id, organizer_id, start_date, end_date, target_participants, state` |
| `POST /csr/summary` | filters; total and counts by state |
| `POST /policies/{list,get,create,update,delete}` | `name, code, description, company_id, owner_id, version, effective_date, review_date, state` |
| `POST /compliance-issues/{list,get,create,update,delete}` | `name, company_id, severity, responsible_user_id, due_date, state, description` |
| `POST /risks/{list,get,create,update,delete}` | `name, company_id, category, probability, impact, mitigation_plan, owner_id, state` |
| `POST /audits/{list,get,create,update,delete}` | `name, company_id, audit_type, auditor, start_date, end_date, findings, score, state` |
| `POST /challenges/{list,get,create,update,delete}` | `name, company_id, description, xp_reward, start_date, end_date, state` |
| `POST /rewards/{list,get,create,update,delete}` | `name, xp_cost, active, company_id` |
| `POST /gamification/leaderboard` | `company_id`, optional `limit`; ordered XP entries |
| `POST /dashboard` | `company_id`, `date_from`, `date_to`; existing dashboard overview data |

For every `create`, send `{ "values": { ... } }`; `update` sends `{ "id": 12, "values": { ... } }`; `get`/`delete` send `{ "id": 12 }`. Lists accept `limit` (default 20, maximum 200), `offset`, `company_id`, `status`, `date_from`, and `date_to` where the resource has an applicable date field. IDs must be integers. Dates use `YYYY-MM-DD`; returned many2one values are consistently `{ "id": 1, "name": "..." }` and returned dates/datetimes are strings.
