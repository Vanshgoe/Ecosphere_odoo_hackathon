/* ─── Shared primitives ─── */
export interface ApiError {
  code: string;
  message: string;
}

export interface ApiEnvelope<T> {
  success: boolean;
  data?: T;
  error?: ApiError;
  pagination?: Pagination;
}

export interface JsonRpcResponse<T> {
  jsonrpc: string;
  id: number | string | null;
  result?: ApiEnvelope<T>;
  error?: { code: number; message: string; data?: unknown };
}

export interface Many2One {
  id: number;
  name: string;
}

export interface Pagination {
  limit: number;
  offset: number;
  total: number;
}

/* ─── Dashboard ─── */
export interface ChartSeries {
  labels: string[];
  series: Array<{ name: string; data: number[] }>;
}

export interface DashboardKpis {
  total_goals: number;
  completed_goals: number;
  overall_esg_progress: number;
  total_carbon_emissions: number;
  csr_activities: number;
  open_compliance_issues: number;
}

export interface DashboardData {
  kpis: DashboardKpis;
  charts: {
    esg_scores: ChartSeries;
    emissions_by_scope: ChartSeries;
    goal_status: ChartSeries;
    issue_status: ChartSeries;
  };
  metadata: { company_id: number; date_from?: string; date_to?: string };
}

/* ─── Current user (GET /me) ─── */
export interface CurrentUser {
  id: number;
  name: string;
  login: string;
  company: Many2One;
  allowed_companies: Many2One[];
}

/* ─── Resource names matching backend RESOURCES dict ─── */
export type ResourceName =
  | 'goals'
  | 'carbon'
  | 'csr'
  | 'policies'
  | 'compliance-issues'
  | 'risks'
  | 'audits'
  | 'challenges'
  | 'rewards';

/* ─── List request params ─── */
export interface ListParams {
  limit?: number;
  offset?: number;
  company_id?: number;
  status?: string;
  date_from?: string;
  date_to?: string;
  [key: string]: unknown; // allows passing to jsonRpc as Record<string, unknown>
}

/* ─── List response ─── */
export interface ListResult<T> {
  rows: T[];
  pagination: Pagination;
}

/* ─── Generic API record ─── */
export interface ApiRecord {
  id: number;
  [key: string]: unknown;
}

/* ─── Domain-specific records ─── */
export interface GoalRecord extends ApiRecord {
  name: string;
  company_id: Many2One | null;
  category_id: Many2One | null;
  metric_id: Many2One | null;
  baseline_value: number;
  target_value: number;
  current_value: number;
  start_date: string | null;
  target_date: string | null;
  progress_percentage: number;
  status: string | null;
  status_label: string | null;
  responsible_user_id: Many2One | null;
}

export interface CarbonRecord extends ApiRecord {
  name: string;
  company_id: Many2One | null;
  source_model: string | null;
  source_record_id: number;
  source_reference: string | null;
  source_type: string;
  activity_value: number;
  activity_unit: string;
  emission_factor_id: Many2One | null;
  emissions_kg_co2e: number;
  scope: string | null;
  scope_label: string | null;
  transaction_date: string | null;
  state: string | null;
  state_label: string | null;
}

export interface CsrRecord extends ApiRecord {
  name: string;
  description: string | null;
  company_id: Many2One | null;
  organizer_id: Many2One | null;
  start_date: string | null;
  end_date: string | null;
  target_participants: number;
  state: string | null;
  state_label: string | null;
  approved_by: Many2One | null;
  approval_date: string | null;
}

export interface PolicyRecord extends ApiRecord {
  name: string;
  code: string;
  description: string | null;
  company_id: Many2One | null;
  owner_id: Many2One | null;
  version: string | null;
  effective_date: string | null;
  review_date: string | null;
  state: string | null;
  state_label: string | null;
}

export interface ComplianceIssueRecord extends ApiRecord {
  name: string;
  company_id: Many2One | null;
  severity: string | null;
  severity_label: string | null;
  responsible_user_id: Many2One | null;
  due_date: string | null;
  resolution_date: string | null;
  state: string | null;
  state_label: string | null;
  description: string | null;
}

export interface RiskRecord extends ApiRecord {
  name: string;
  company_id: Many2One | null;
  category: string | null;
  probability: number;
  impact: number;
  risk_score: number;
  mitigation_plan: string | null;
  owner_id: Many2One | null;
  state: string | null;
  state_label: string | null;
}

export interface AuditRecord extends ApiRecord {
  name: string;
  company_id: Many2One | null;
  audit_type: string | null;
  auditor: string | null;
  start_date: string | null;
  end_date: string | null;
  findings: string | null;
  score: number;
  state: string | null;
  state_label: string | null;
}

export interface ChallengeRecord extends ApiRecord {
  name: string;
  company_id: Many2One | null;
  description: string | null;
  xp_reward: number;
  start_date: string | null;
  end_date: string | null;
  state: string | null;
  state_label: string | null;
}

export interface RewardRecord extends ApiRecord {
  name: string;
  xp_cost: number;
  active: boolean;
  company_id: Many2One | null;
}

/* ─── Leaderboard entry ─── */
export interface LeaderboardEntry {
  rank: number;
  employee: { id: number; name: string } | null;
  xp: number;
}

/* ─── Summary types ─── */
export interface CarbonSummary {
  total_emissions_kg_co2e: number;
  by_scope: Array<{ scope: string; emissions_kg_co2e: number }>;
}

export interface CsrSummary {
  total: number;
  by_state: Array<{ state: string; count: number }>;
}
