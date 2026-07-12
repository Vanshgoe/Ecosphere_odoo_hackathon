import { Card, EmptyState } from '../components/common';

type SettingsView = 'departments' | 'categories' | 'configuration' | 'notifications';

const configToggles = [
  { label: 'Enable auto emission calculation', key: 'enable_auto_calc' },
  { label: 'Require evidence for all CSR activities', key: 'evidence_required' },
  { label: 'Auto-award badges on challenge completion', key: 'auto_badges' },
  { label: 'Email alerts for new compliance issues', key: 'email_compliance' },
];

export default function Settings({ view }: { view: SettingsView }) {
  const titles: Record<SettingsView, string> = {
    departments: 'Departments',
    categories: 'Categories',
    configuration: 'ESG Configuration',
    notifications: 'Notification Settings',
  };

  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">SETTINGS</p>
          <h2>{titles[view]}</h2>
          <p className="page-description">
            {view === 'configuration' || view === 'notifications'
              ? 'Configuration settings shown below. Backend persistence for these settings is not exposed by the current API.'
              : `${titles[view]} management is not exposed by the current frontend API.`}
          </p>
        </div>
      </div>

      {(view === 'configuration' || view === 'notifications') ? (
        <Card>
          <div className="settings-toggles">
            {configToggles.map((toggle) => (
              <label key={toggle.key} className="toggle-row">
                <input type="checkbox" disabled />
                <span>{toggle.label}</span>
              </label>
            ))}
          </div>
          <p className="page-description" style={{ marginTop: 16 }}>
            These configuration toggles correspond to{' '}
            <code>ecosphere.esg.configuration</code> in the backend. The
            frontend API does not expose read/write endpoints for this model, so
            toggles are displayed as read-only placeholders.
          </p>
        </Card>
      ) : (
        <Card>
          <EmptyState
            title="Backend capability unavailable"
            detail={`${titles[view]} records are not exposed by the current frontend API. Manage them via the Odoo backend.`}
          />
        </Card>
      )}
    </>
  );
}
