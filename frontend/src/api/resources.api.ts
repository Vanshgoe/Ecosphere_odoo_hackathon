import { jsonRpc, jsonRpcEnvelope } from './client';
import type {
  ApiRecord,
  ListParams,
  ListResult,
  ResourceName,
  CarbonSummary,
  CsrSummary,
  LeaderboardEntry,
} from '../types/api';

/* ─── List with pagination ─── */
export async function listResource<T extends ApiRecord>(
  resource: ResourceName,
  params: ListParams = {},
): Promise<ListResult<T>> {
  const resp = await jsonRpcEnvelope<T[]>(`${resource}/list`, params);
  return {
    rows: resp.data ?? [],
    pagination: resp.pagination ?? {
      limit: params.limit ?? 20,
      offset: params.offset ?? 0,
      total: 0,
    },
  };
}

/* ─── Single record ─── */
export const getResource = <T extends ApiRecord>(
  resource: ResourceName,
  id: number,
) => jsonRpc<T>(`${resource}/get`, { id });

/* ─── Create ─── */
export const createResource = <T extends ApiRecord>(
  resource: ResourceName,
  values: Record<string, unknown>,
) => jsonRpc<T>(`${resource}/create`, { values });

/* ─── Update ─── */
export const updateResource = <T extends ApiRecord>(
  resource: ResourceName,
  id: number,
  values: Record<string, unknown>,
) => jsonRpc<T>(`${resource}/update`, { id, values });

/* ─── Delete ─── */
export const deleteResource = (resource: ResourceName, id: number) =>
  jsonRpc<{ id: number; deleted: boolean }>(`${resource}/delete`, { id });

/* ─── Summaries ─── */
export const getCarbonSummary = (params: ListParams = {}) =>
  jsonRpc<CarbonSummary>('carbon/summary', params);

export const getCsrSummary = (params: ListParams = {}) =>
  jsonRpc<CsrSummary>('csr/summary', params);

/* ─── Leaderboard ─── */
export const getLeaderboard = (
  params: { company_id?: number; limit?: number } = {},
) => jsonRpc<LeaderboardEntry[]>('gamification/leaderboard', params);
