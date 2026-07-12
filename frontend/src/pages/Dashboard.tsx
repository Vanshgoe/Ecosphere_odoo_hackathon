import ReactECharts from 'echarts-for-react';
import { Link } from 'react-router-dom';
import { useDashboard } from '../hooks/useDashboard';
import { Card, EmptyState, ErrorState, LoadingState, StatusBadge } from '../components/common';

function Kpi({
  label,
  value,
  tone,
}: {
  label: string;
  value: number;
  tone: string;
}) {
  return (
    <Card className={`kpi ${tone}`}>
      <span>{label}</span>
      <strong>
        {value.toFixed(0)}
        <small> / 100</small>
      </strong>
      <span className="kpi-caption">Current ESG score</span>
    </Card>
  );
}

function KpiCount({
  label,
  value,
  unit,
}: {
  label: string;
  value: number;
  unit?: string;
}) {
  return (
    <Card className="kpi dashboard">
      <span>{label}</span>
      <strong>
        {typeof value === 'number' ? value.toLocaleString() : value}
      </strong>
      {unit && <span className="kpi-caption">{unit}</span>}
    </Card>
  );
}

export default function Dashboard() {
  const { data, isLoading, error, refetch } = useDashboard();

  if (isLoading) return <LoadingState label="Loading dashboard data…" />;
  if (error || !data)
    return (
      <ErrorState
        message={
          error instanceof Error
            ? error.message
            : 'No dashboard response was received.'
        }
        onRetry={() => refetch()}
      />
    );

  const scores = data.charts.esg_scores.series[0]?.data ?? [0, 0, 0];
  const emission = data.charts.emissions_by_scope;
  const goalStatus = data.charts.goal_status;
  const issueStatus = data.charts.issue_status;

  /* Emissions by scope chart */
  const scopeOption = {
    tooltip: { trigger: 'axis' as const },
    grid: { left: 48, right: 18, top: 32, bottom: 36 },
    xAxis: {
      type: 'category' as const,
      data: emission.labels,
      axisLabel: { color: '#91a1af' },
      axisLine: { lineStyle: { color: '#293842' } },
    },
    yAxis: {
      type: 'value' as const,
      axisLabel: { color: '#91a1af' },
      splitLine: { lineStyle: { color: '#1e2d38' } },
    },
    series: [
      {
        name: emission.series[0]?.name ?? 'kg CO₂e',
        type: 'bar' as const,
        data: emission.series[0]?.data ?? [],
        itemStyle: {
          color: '#38b56b',
          borderRadius: [5, 5, 0, 0],
        },
      },
    ],
  };

  /* Goal status chart */
  const goalPieOption = {
    tooltip: { trigger: 'item' as const },
    legend: {
      bottom: 0,
      textStyle: { color: '#91a1af', fontSize: 11 },
    },
    series: [
      {
        name: 'Goal Status',
        type: 'pie' as const,
        radius: ['40%', '70%'],
        data: goalStatus.labels.map((label, i) => ({
          name: label,
          value: goalStatus.series[0]?.data[i] ?? 0,
        })),
        emphasis: {
          itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0,0,0,0.5)' },
        },
        label: { show: false },
      },
    ],
  };

  /* Issue status chart */
  const issueBarOption = {
    tooltip: { trigger: 'axis' as const },
    grid: { left: 48, right: 18, top: 28, bottom: 36 },
    xAxis: {
      type: 'category' as const,
      data: issueStatus.labels,
      axisLabel: { color: '#91a1af' },
      axisLine: { lineStyle: { color: '#293842' } },
    },
    yAxis: {
      type: 'value' as const,
      axisLabel: { color: '#91a1af' },
      splitLine: { lineStyle: { color: '#1e2d38' } },
    },
    series: [
      {
        name: 'Issues',
        type: 'bar' as const,
        data: issueStatus.series[0]?.data ?? [],
        itemStyle: { color: '#9b70ef', borderRadius: [5, 5, 0, 0] },
      },
    ],
  };

  return (
    <>
      {/* Page heading */}
      <div className="page-heading">
        <div>
          <p className="eyebrow">EXECUTIVE OVERVIEW</p>
          <h2>ESG performance at a glance</h2>
        </div>
        <span className="company-chip">
          Company #{data.metadata.company_id}
        </span>
      </div>

      {/* ESG Score KPIs */}
      <div className="kpi-grid">
        <Kpi label="Environmental Score" value={scores[0] ?? 0} tone="environmental" />
        <Kpi label="Social Score" value={scores[1] ?? 0} tone="social" />
        <Kpi label="Governance Score" value={scores[2] ?? 0} tone="governance" />
        <Kpi label="Overall ESG Score" value={data.kpis.overall_esg_progress} tone="dashboard" />
      </div>

      {/* Operational KPIs */}
      <div className="kpi-grid kpi-grid-secondary">
        <KpiCount label="Total Goals" value={data.kpis.total_goals} />
        <KpiCount label="Completed Goals" value={data.kpis.completed_goals} />
        <KpiCount
          label="Total Carbon"
          value={data.kpis.total_carbon_emissions}
          unit="kg CO₂e"
        />
        <KpiCount
          label="Open Compliance Issues"
          value={data.kpis.open_compliance_issues}
        />
      </div>

      {/* Charts & cards grid */}
      <div className="dashboard-grid">
        <Card title="Emissions by Scope">
          {emission.labels.length > 0 ? (
            <ReactECharts
              option={scopeOption}
              style={{ height: 280 }}
              notMerge
              lazyUpdate
            />
          ) : (
            <EmptyState
              title="No emissions data"
              detail="No carbon transactions recorded yet."
            />
          )}
        </Card>

        <Card title="Goal Status Distribution">
          {goalStatus.labels.length > 0 ? (
            <ReactECharts
              option={goalPieOption}
              style={{ height: 280 }}
              notMerge
              lazyUpdate
            />
          ) : (
            <EmptyState
              title="No goals yet"
              detail="Create goals to see status distribution."
            />
          )}
        </Card>

        <Card title="Compliance Issues by Status">
          {issueStatus.labels.length > 0 ? (
            <ReactECharts
              option={issueBarOption}
              style={{ height: 280 }}
              notMerge
              lazyUpdate
            />
          ) : (
            <EmptyState
              title="No compliance issues"
              detail="No compliance issues recorded."
            />
          )}
        </Card>

        <Card title="Department ESG Ranking">
          <EmptyState
            title="Ranking unavailable"
            detail="The current backend does not expose a department-ranking endpoint."
          />
        </Card>

        <Card title="Recent Activity">
          <EmptyState
            title="No activity feed API"
            detail="Recent cross-module activity is not currently available from the backend."
          />
        </Card>

        <Card title="Quick Actions">
          <div className="action-list">
            <Link
              className="button button-environmental"
              to="/environmental/carbon"
            >
              + Log Carbon Data
            </Link>
            <Link
              className="button button-gamification"
              to="/gamification/challenges"
            >
              🏆 Start Challenge
            </Link>
            <Link
              className="button button-secondary"
              to="/reports/esg-summary"
            >
              📊 View Reports
            </Link>
          </div>
        </Card>
      </div>
    </>
  );
}
