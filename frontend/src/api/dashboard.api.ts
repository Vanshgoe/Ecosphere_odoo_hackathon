import { jsonRpc } from './client';
import type { DashboardData } from '../types/api';

export const getDashboard = (
  params: { company_id?: number; date_from?: string; date_to?: string } = {},
) => jsonRpc<DashboardData>('dashboard', params);
