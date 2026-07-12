import { useQuery } from '@tanstack/react-query';
import { getDashboard } from '../api/dashboard.api';

export const dashboardQueryKey = ['dashboard'] as const;

export function useDashboard(params?: {
  company_id?: number;
  date_from?: string;
  date_to?: string;
}) {
  return useQuery({
    queryKey: [...dashboardQueryKey, params],
    queryFn: () => getDashboard(params),
  });
}
