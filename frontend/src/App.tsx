import { Route, Routes } from 'react-router-dom';
import { AppShell } from './components/layout';
import Dashboard from './pages/Dashboard';
import Resources from './pages/Resources';
import Unavailable from './pages/Unavailable';
import Leaderboard from './pages/Leaderboard';
import Reports from './pages/Reports';
import Settings from './pages/Settings';

export default function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        {/* ─── Dashboard ─── */}
        <Route path="/" element={<Dashboard />} />

        {/* ─── Environmental ─── */}
        <Route
          path="/environmental/emission-factors"
          element={
            <Unavailable
              module="Environmental"
              title="Emission Factors"
              detail="Emission factor records are managed in the Odoo backend. The frontend API does not expose a CRUD route for this model."
            />
          }
        />
        <Route
          path="/environmental/product-profiles"
          element={
            <Unavailable
              module="Environmental"
              title="Product ESG Profiles"
              detail="Product ESG profile records are managed in the Odoo backend. The frontend API does not expose a CRUD route for this model."
            />
          }
        />
        <Route
          path="/environmental/carbon"
          element={<Resources screen="carbon" />}
        />
        <Route
          path="/environmental/goals"
          element={<Resources screen="goals" />}
        />

        {/* ─── Social ─── */}
        <Route path="/social/csr" element={<Resources screen="csr" />} />
        <Route
          path="/social/participation"
          element={
            <Unavailable
              module="Social"
              title="Employee Participation"
              detail="Participation records and approval actions are not exposed by the frontend API. Manage via the Odoo backend."
            />
          }
        />
        <Route
          path="/social/diversity"
          element={
            <Unavailable
              module="Social"
              title="Diversity Dashboard"
              detail="No diversity metrics or summary endpoint is exposed by the frontend API."
            />
          }
        />

        {/* ─── Governance ─── */}
        <Route
          path="/governance/policies"
          element={<Resources screen="policies" />}
        />
        <Route
          path="/governance/acknowledgements"
          element={
            <Unavailable
              module="Governance"
              title="Policy Acknowledgements"
              detail="Acknowledgement records and actions are not exposed by the frontend API. Manage via the Odoo backend."
            />
          }
        />
        <Route
          path="/governance/audits"
          element={<Resources screen="audits" />}
        />
        <Route
          path="/governance/compliance-issues"
          element={<Resources screen="issues" />}
        />
        <Route
          path="/governance/risks"
          element={<Resources screen="risks" />}
        />

        {/* ─── Gamification ─── */}
        <Route
          path="/gamification/challenges"
          element={<Resources screen="challenges" />}
        />
        <Route
          path="/gamification/participation"
          element={
            <Unavailable
              module="Gamification"
              title="Challenge Participation"
              detail="Participation records and join/completion actions are not exposed by the frontend API."
            />
          }
        />
        <Route
          path="/gamification/badges"
          element={
            <Unavailable
              module="Gamification"
              title="Badges"
              detail="Badge records and award data are not exposed by the frontend API. Manage via the Odoo backend."
            />
          }
        />
        <Route
          path="/gamification/rewards"
          element={<Resources screen="rewards" />}
        />
        <Route
          path="/gamification/leaderboard"
          element={<Leaderboard />}
        />

        {/* ─── Reports ─── */}
        <Route
          path="/reports/environmental"
          element={<Reports view="catalog" />}
        />
        <Route
          path="/reports/social"
          element={<Reports view="catalog" />}
        />
        <Route
          path="/reports/governance"
          element={<Reports view="catalog" />}
        />
        <Route
          path="/reports/esg-summary"
          element={<Reports view="summary" />}
        />
        <Route
          path="/reports/custom"
          element={<Reports view="custom" />}
        />

        {/* ─── Settings ─── */}
        <Route
          path="/settings/departments"
          element={<Settings view="departments" />}
        />
        <Route
          path="/settings/categories"
          element={<Settings view="categories" />}
        />
        <Route
          path="/settings/configuration"
          element={<Settings view="configuration" />}
        />
        <Route
          path="/settings/notifications"
          element={<Settings view="notifications" />}
        />

        {/* ─── 404 ─── */}
        <Route
          path="*"
          element={
            <Unavailable
              module="EcoSphere"
              title="Page not found"
              detail="Choose a module from the navigation."
            />
          }
        />
      </Route>
    </Routes>
  );
}
