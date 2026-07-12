import { NavLink, Outlet, useLocation } from 'react-router-dom';
import { useState } from 'react';

/* ─── Navigation structure ─── */
interface NavItem {
  label: string;
  path: string;
}

interface NavSection {
  label: string;
  module: string;
  items: NavItem[];
}

export const sections: NavSection[] = [
  {
    label: 'Dashboard',
    module: 'dashboard',
    items: [{ label: 'Executive Overview', path: '/' }],
  },
  {
    label: 'Environmental',
    module: 'environmental',
    items: [
      { label: 'Emission Factors', path: '/environmental/emission-factors' },
      { label: 'Product ESG Profiles', path: '/environmental/product-profiles' },
      { label: 'Carbon Transactions', path: '/environmental/carbon' },
      { label: 'Environmental Goals', path: '/environmental/goals' },
    ],
  },
  {
    label: 'Social',
    module: 'social',
    items: [
      { label: 'CSR Activities', path: '/social/csr' },
      { label: 'Employee Participation', path: '/social/participation' },
      { label: 'Diversity Dashboard', path: '/social/diversity' },
    ],
  },
  {
    label: 'Governance',
    module: 'governance',
    items: [
      { label: 'Policies', path: '/governance/policies' },
      { label: 'Policy Acknowledgements', path: '/governance/acknowledgements' },
      { label: 'Audits', path: '/governance/audits' },
      { label: 'Compliance Issues', path: '/governance/compliance-issues' },
      { label: 'Risk Register', path: '/governance/risks' },
    ],
  },
  {
    label: 'Gamification',
    module: 'gamification',
    items: [
      { label: 'Challenges', path: '/gamification/challenges' },
      { label: 'Challenge Participation', path: '/gamification/participation' },
      { label: 'Badges', path: '/gamification/badges' },
      { label: 'Rewards', path: '/gamification/rewards' },
      { label: 'Leaderboard', path: '/gamification/leaderboard' },
    ],
  },
  {
    label: 'Reports',
    module: 'reports',
    items: [
      { label: 'Environmental Report', path: '/reports/environmental' },
      { label: 'Social Report', path: '/reports/social' },
      { label: 'Governance Report', path: '/reports/governance' },
      { label: 'ESG Summary', path: '/reports/esg-summary' },
      { label: 'Custom Report Builder', path: '/reports/custom' },
    ],
  },
  {
    label: 'Settings',
    module: 'settings',
    items: [
      { label: 'Departments', path: '/settings/departments' },
      { label: 'Categories', path: '/settings/categories' },
      { label: 'ESG Configuration', path: '/settings/configuration' },
      { label: 'Notification Settings', path: '/settings/notifications' },
    ],
  },
];

const tabs = sections.map(({ label, module, items }) => ({
  label,
  module,
  path: items[0].path,
}));

function getPageTitle(path: string): string {
  for (const sec of sections) {
    for (const item of sec.items) {
      if (item.path === path) return item.label;
    }
  }
  return 'EcoSphere';
}

function getActiveModule(path: string): string {
  if (path === '/') return 'dashboard';
  const seg = path.split('/')[1];
  return seg || 'dashboard';
}

export function AppShell() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();
  const activeModule = getActiveModule(location.pathname);

  return (
    <div className="app-shell">
      {/* ─── Sidebar ─── */}
      <aside
        className={`sidebar ${sidebarOpen ? 'sidebar-open' : ''}`}
        aria-label="Primary navigation"
      >
        <div className="brand">
          <span className="brand-mark">◒</span>
          <span>EcoSphere</span>
        </div>
        <nav>
          {sections.map((section) => (
            <section
              className={`nav-group module-${section.module}`}
              key={section.label}
            >
              <h2>{section.label}</h2>
              {section.items.map((item) => (
                <NavLink
                  onClick={() => setSidebarOpen(false)}
                  to={item.path}
                  end={item.path === '/'}
                  key={item.path}
                >
                  {item.label}
                </NavLink>
              ))}
            </section>
          ))}
        </nav>
      </aside>

      {/* ─── Mobile overlay ─── */}
      {sidebarOpen && (
        <button
          className="overlay"
          aria-label="Close navigation"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* ─── Main ─── */}
      <main>
        <header className="header">
          <button
            className="menu-button"
            aria-label="Open navigation"
            onClick={() => setSidebarOpen(true)}
          >
            ☰
          </button>
          <div>
            <span className="eyebrow">ESG MANAGEMENT PLATFORM</span>
            <h1>{getPageTitle(location.pathname)}</h1>
          </div>
          <div className="account" aria-label="Odoo session account">
            Session via Odoo
          </div>
        </header>

        {/* ─── Module tabs ─── */}
        <nav className="module-tabs" aria-label="Modules">
          {tabs.map((tab) => (
            <NavLink
              key={tab.module}
              className={({ isActive }) =>
                `module-${tab.module}${
                  isActive || activeModule === tab.module ? ' active' : ''
                }`
              }
              to={tab.path}
              end={tab.module === 'dashboard'}
            >
              {tab.label}
            </NavLink>
          ))}
        </nav>

        <div className="page">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
