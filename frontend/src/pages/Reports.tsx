import ReactECharts from 'echarts-for-react';
import { useDashboard } from '../hooks/useDashboard';
import { Card, EmptyState, ErrorState, LoadingState } from '../components/common';

type ReportView = 'summary' | 'catalog' | 'custom';

const reportCards = [
  {
    title: 'Environmental Report',
    icon: '🌱',
    color: 'var(--environmental)',
    description: 'Emissions, goals, vendor & product breakdown.',
  },
  {
    title: 'Social Report',
    icon: '💙',
    color: 'var(--social)',
    description: 'Diversity, CSR participation, training completion.',
  },
  {
    title: 'Governance Report',
    icon: '🏛',
    color: 'var(--governance)',
    description: 'Policies, audits, compliance & risk summary.',
  },
  {
    title: 'ESG Summary',
    icon: '📊',
    color: 'var(--reports)',
    description: 'Executive overview: all 4 scores + dept comparison.',
  },
];

export default function Reports({ view }: { view: ReportView }) {
  const dashboard = useDashboard();

  /* ─── ESG Summary view ─── */
  if (view === 'summary') {
    if (dashboard.isLoading) return <LoadingState label="Loading ESG summary…" />;
    if (dashboard.error || !dashboard.data)
      return (
        <ErrorState
          message={
            dashboard.error instanceof Error
              ? dashboard.error.message
              : 'Unable to load ESG summary.'
          }
          onRetry={() => dashboard.refetch()}
        />
      );

    const kpis = dashboard.data.kpis;
    const scores = dashboard.data.charts.esg_scores;

    const radarOption = {
      tooltip: {},
      radar: {
        indicator: scores.labels.map((l) => ({ name: l, max: 100 })),
        axisName: { color: '#91a1af' },
        splitArea: { areaStyle: { color: ['transparent'] } },
        splitLine: { lineStyle: { color: '#293842' } },
        axisLine: { lineStyle: { color: '#293842' } },
      },
      series: [
        {
          type: 'radar' as const,
          data: [
            {
              value: scores.series[0]?.data ?? [],
              name: 'ESG Scores',
              areaStyle: { color: 'rgba(74, 155, 233, 0.2)' },
              lineStyle: { color: '#4a9be9' },
              itemStyle: { color: '#4a9be9' },
            },
          ],
        },
      ],
    };

    return (
      <>
        <div className="page-heading">
          <div>
            <p className="eyebrow">REPORTS</p>
            <h2>ESG Summary</h2>
            <p className="page-description">
              Consolidated view of all ESG scores and operational metrics.
            </p>
          </div>
        </div>

        <div className="kpi-grid report-kpis">
          <Card>
            <span>Total Goals</span>
            <strong>{kpis.total_goals}</strong>
          </Card>
          <Card>
            <span>Completed Goals</span>
            <strong>{kpis.completed_goals}</strong>
          </Card>
          <Card>
            <span>Carbon Emissions</span>
            <strong>{kpis.total_carbon_emissions.toLocaleString()}</strong>
            <span className="kpi-caption">kg CO₂e</span>
          </Card>
          <Card>
            <span>Open Issues</span>
            <strong>{kpis.open_compliance_issues}</strong>
          </Card>
        </div>

        <div className="dashboard-grid">
          <Card title="ESG Score Radar">
            {scores.labels.length > 0 ? (
              <ReactECharts
                option={radarOption}
                style={{ height: 300 }}
                notMerge
                lazyUpdate
              />
            ) : (
              <EmptyState
                title="No scores available"
                detail="ESG scores have not been calculated yet."
              />
            )}
          </Card>
          <Card title="CSR Activities">
            <div className="metric-large">
              <strong>{kpis.csr_activities}</strong>
              <span>total activities</span>
            </div>
          </Card>
        </div>
      </>
    );
  }

  /* ─── Report catalog / Custom ─── */
  const title = view === 'custom' ? 'Custom Report Builder' : 'Reports';
  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">REPORTS</p>
          <h2>{title}</h2>
          <p className="page-description">
            {view === 'custom'
              ? 'Configure filters and generate a custom cross-module report.'
              : 'Available report formats are shown below.'}
          </p>
        </div>
      </div>

      {/* Report cards */}
      <div className="report-cards">
        {reportCards.map((report) => (
          <section
            key={report.title}
            style={{ borderTopColor: report.color, borderTopWidth: 3 }}
          >
            <h3>
              {report.icon} {report.title}
            </h3>
            <p>{report.description}</p>
            <button disabled title="Report generation is not exposed by the current API">
              Generate
            </button>
          </section>
        ))}
      </div>

      {/* Custom report builder filters */}
      {view === 'custom' && (
        <Card className="custom-builder">
          <h3>⚙ Custom Report Builder: Filters</h3>
          <div className="filter-grid">
            <input
              aria-label="Date range"
              placeholder="Date Range ▾"
              disabled
            />
            <input
              aria-label="Department"
              placeholder="Department ▾"
              disabled
            />
            <input aria-label="Module" placeholder="Module ▾" disabled />
            <input
              aria-label="Employee"
              placeholder="Employee ▾"
              disabled
            />
            <input
              aria-label="Challenge"
              placeholder="Challenge ▾"
              disabled
            />
            <input
              aria-label="ESG Category"
              placeholder="ESG Category ▾"
              disabled
            />
          </div>
          <div className="report-actions">
            <button disabled className="button button-primary btn-sm">
              ▶ Run Report
            </button>
            <button disabled className="button button-secondary btn-sm">
              Export: PDF
            </button>
            <button disabled className="button button-secondary btn-sm">
              Export: Excel
            </button>
            <button disabled className="button button-secondary btn-sm">
              Export: CSV
            </button>
          </div>
          <p className="page-description" style={{ marginTop: 16 }}>
            Report generation and export are not exposed by the current backend
            API. These controls are shown for visual reference.
          </p>
        </Card>
      )}
    </>
  );
}
