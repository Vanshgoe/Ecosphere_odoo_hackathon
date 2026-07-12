import { ResourceScreen, type ResourceScreenConfig } from '../components/resource';
import { ProgressBar } from '../components/common';
import type { ApiRecord } from '../types/api';

/* ─── Helpers ─── */
const states = (items: Array<[string, string]>) =>
  items.map(([value, label]) => ({ value, label }));

const m2oId = (label: string, required = false) => ({
  key: label
    .toLowerCase()
    .replace(/ /g, '_')
    .replace(/id$/, 'id'),
  label,
  kind: 'number' as const,
  required,
  helper: 'Odoo record ID.',
});

/* ─── Configurations per resource ─── */
const configs: Record<string, ResourceScreenConfig> = {
  goals: {
    title: 'Environmental Goals',
    module: 'Environmental',
    resource: 'goals',
    description:
      'Set, monitor, and update company ESG targets with progress tracking.',
    statusField: 'status',
    fields: [
      { key: 'name', label: 'Goal name', kind: 'text', required: true },
      m2oId('category_id', true),
      m2oId('metric_id', true),
      { key: 'baseline_value', label: 'Baseline', kind: 'number' },
      { key: 'target_value', label: 'Target', kind: 'number' },
      { key: 'current_value', label: 'Current', kind: 'number' },
      { key: 'start_date', label: 'Start date', kind: 'date' },
      { key: 'target_date', label: 'Deadline', kind: 'date', required: true },
      {
        key: 'progress_percentage',
        label: 'Progress',
        kind: 'number',
        readOnly: true,
      },
      {
        key: 'status',
        label: 'Status',
        kind: 'select',
        options: states([
          ['draft', 'Draft'],
          ['active', 'Active'],
          ['achieved', 'Achieved'],
          ['failed', 'Failed'],
          ['cancelled', 'Cancelled'],
        ]),
      },
      m2oId('responsible_user_id'),
    ],
    render: (row: ApiRecord, field) => {
      if (field.key === 'progress_percentage') {
        return <ProgressBar value={Number(row.progress_percentage ?? 0)} />;
      }
      return undefined;
    },
  },

  carbon: {
    title: 'Carbon Transactions',
    module: 'Environmental',
    resource: 'carbon',
    description:
      'Operational emissions records calculated from company-specific emission factors.',
    statusField: 'state',
    fields: [
      { key: 'name', label: 'Name', kind: 'text', required: true },
      { key: 'source_type', label: 'Source type', kind: 'text', required: true },
      {
        key: 'activity_value',
        label: 'Activity value',
        kind: 'number',
        required: true,
      },
      {
        key: 'activity_unit',
        label: 'Activity unit',
        kind: 'text',
        required: true,
      },
      m2oId('emission_factor_id', true),
      { key: 'transaction_date', label: 'Date', kind: 'date' },
      {
        key: 'emissions_kg_co2e',
        label: 'kg CO₂e',
        kind: 'number',
        readOnly: true,
      },
      {
        key: 'scope',
        label: 'Scope',
        kind: 'text',
        readOnly: true,
      },
      {
        key: 'state',
        label: 'State',
        kind: 'select',
        options: states([
          ['draft', 'Draft'],
          ['calculated', 'Calculated'],
          ['cancelled', 'Cancelled'],
        ]),
      },
    ],
  },

  csr: {
    title: 'CSR Activities',
    module: 'Social',
    resource: 'csr',
    description:
      'Corporate social responsibility activities and their approval lifecycle.',
    statusField: 'state',
    fields: [
      { key: 'name', label: 'Activity name', kind: 'text', required: true },
      { key: 'description', label: 'Description', kind: 'textarea' },
      { key: 'start_date', label: 'Start date', kind: 'date' },
      { key: 'end_date', label: 'End date', kind: 'date' },
      {
        key: 'target_participants',
        label: 'Target participants',
        kind: 'number',
      },
      {
        key: 'state',
        label: 'State',
        kind: 'select',
        options: states([
          ['draft', 'Draft'],
          ['submitted', 'Submitted'],
          ['approved', 'Approved'],
          ['completed', 'Completed'],
          ['cancelled', 'Cancelled'],
        ]),
      },
      m2oId('organizer_id'),
    ],
  },

  policies: {
    title: 'Policies',
    module: 'Governance',
    resource: 'policies',
    description:
      'Governance policy lifecycle, ownership, and review schedule.',
    statusField: 'state',
    fields: [
      { key: 'name', label: 'Policy name', kind: 'text', required: true },
      { key: 'code', label: 'Policy code', kind: 'text', required: true },
      { key: 'description', label: 'Description', kind: 'textarea' },
      m2oId('owner_id'),
      { key: 'version', label: 'Version', kind: 'text' },
      { key: 'effective_date', label: 'Effective date', kind: 'date' },
      { key: 'review_date', label: 'Review date', kind: 'date' },
      {
        key: 'state',
        label: 'State',
        kind: 'select',
        options: states([
          ['draft', 'Draft'],
          ['published', 'Published'],
          ['archived', 'Archived'],
        ]),
      },
    ],
  },

  audits: {
    title: 'Audits',
    module: 'Governance',
    resource: 'audits',
    description: 'ESG audit records with findings, scores, and status.',
    statusField: 'state',
    fields: [
      { key: 'name', label: 'Audit title', kind: 'text', required: true },
      { key: 'audit_type', label: 'Audit type', kind: 'text' },
      { key: 'auditor', label: 'Auditor', kind: 'text' },
      { key: 'start_date', label: 'Start date', kind: 'date' },
      { key: 'end_date', label: 'End date', kind: 'date' },
      { key: 'findings', label: 'Findings', kind: 'textarea' },
      { key: 'score', label: 'Score', kind: 'number' },
      {
        key: 'state',
        label: 'Status',
        kind: 'select',
        options: states([
          ['draft', 'Draft'],
          ['in_progress', 'In Progress'],
          ['completed', 'Completed'],
        ]),
      },
    ],
  },

  issues: {
    title: 'Compliance Issues',
    module: 'Governance',
    resource: 'compliance-issues',
    description:
      'Severity-tagged compliance issues with owners, due dates, and resolution tracking.',
    statusField: 'state',
    fields: [
      { key: 'name', label: 'Issue', kind: 'text', required: true },
      {
        key: 'severity',
        label: 'Severity',
        kind: 'select',
        options: states([
          ['low', 'Low'],
          ['medium', 'Medium'],
          ['high', 'High'],
          ['critical', 'Critical'],
        ]),
      },
      m2oId('responsible_user_id'),
      { key: 'due_date', label: 'Due date', kind: 'date' },
      { key: 'description', label: 'Description', kind: 'textarea' },
      {
        key: 'state',
        label: 'Status',
        kind: 'select',
        options: states([
          ['open', 'Open'],
          ['in_progress', 'In Progress'],
          ['resolved', 'Resolved'],
          ['overdue', 'Overdue'],
          ['cancelled', 'Cancelled'],
        ]),
      },
    ],
  },

  risks: {
    title: 'Risk Register',
    module: 'Governance',
    resource: 'risks',
    description:
      'Governance risks with likelihood, impact, ownership, and mitigation plans.',
    statusField: 'state',
    fields: [
      { key: 'name', label: 'Risk name', kind: 'text', required: true },
      { key: 'category', label: 'Category', kind: 'text' },
      { key: 'probability', label: 'Probability', kind: 'number' },
      { key: 'impact', label: 'Impact', kind: 'number' },
      {
        key: 'risk_score',
        label: 'Risk score',
        kind: 'number',
        readOnly: true,
      },
      { key: 'mitigation_plan', label: 'Mitigation plan', kind: 'textarea' },
      m2oId('owner_id'),
      {
        key: 'state',
        label: 'Status',
        kind: 'select',
        options: states([
          ['open', 'Open'],
          ['mitigated', 'Mitigated'],
          ['closed', 'Closed'],
        ]),
      },
    ],
  },

  challenges: {
    title: 'Challenges',
    module: 'Gamification',
    resource: 'challenges',
    description:
      'Gamification challenges with XP rewards, deadlines, and lifecycle.',
    statusField: 'state',
    fields: [
      { key: 'name', label: 'Challenge name', kind: 'text', required: true },
      { key: 'description', label: 'Description', kind: 'textarea' },
      { key: 'xp_reward', label: 'XP reward', kind: 'number' },
      { key: 'start_date', label: 'Start date', kind: 'date' },
      { key: 'end_date', label: 'End date', kind: 'date' },
      {
        key: 'state',
        label: 'Status',
        kind: 'select',
        options: states([
          ['draft', 'Draft'],
          ['active', 'Active'],
          ['closed', 'Closed'],
        ]),
      },
    ],
  },

  rewards: {
    title: 'Rewards',
    module: 'Gamification',
    resource: 'rewards',
    description: 'Rewards available for XP redemption.',
    fields: [
      { key: 'name', label: 'Reward name', kind: 'text', required: true },
      { key: 'xp_cost', label: 'XP cost', kind: 'number', required: true },
      { key: 'active', label: 'Active', kind: 'boolean' },
    ],
  },
};

/* ─── Component ─── */
export default function Resources({
  screen,
}: {
  screen: keyof typeof configs;
}) {
  const config = configs[screen];
  if (!config) {
    return (
      <div className="state state-error" role="alert">
        <strong>Unknown screen: {screen}</strong>
      </div>
    );
  }
  return <ResourceScreen config={config} />;
}
