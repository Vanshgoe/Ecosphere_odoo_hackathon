import axios, { AxiosError } from 'axios';
import type { ApiEnvelope, JsonRpcResponse } from '../types/api';

const configuredOrigin = import.meta.env.VITE_ODOO_URL as string | undefined;
// During Vite dev the proxy rewrites /odoo/* → Odoo origin.
// In production the frontend is served from the same origin as Odoo.
const baseURL = configuredOrigin ? configuredOrigin.replace(/\/$/, '') : '/odoo';

/** Typed application-level API error. */
export class EcoSphereApiError extends Error {
  constructor(
    public readonly code: string,
    message: string,
  ) {
    super(message);
    this.name = 'EcoSphereApiError';
  }
}

const client = axios.create({
  baseURL,
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
});

/**
 * Execute a JSON-RPC call to the EcoSphere API.
 * Unwraps the JSON-RPC envelope, the success envelope, and returns `data`.
 */
export async function jsonRpc<T>(
  path: string,
  params: Record<string, unknown> = {},
): Promise<T> {
  const envelope = await jsonRpcEnvelope<T>(path, params);
  return envelope.data as T;
}

/**
 * Like `jsonRpc` but returns the full `ApiEnvelope` so callers can read pagination, etc.
 */
export async function jsonRpcEnvelope<T>(
  path: string,
  params: Record<string, unknown> = {},
): Promise<ApiEnvelope<T>> {
  try {
    const response = await client.post<JsonRpcResponse<T>>(
      `/api/ecosphere/v1/${path}`,
      { jsonrpc: '2.0', method: 'call', params, id: Date.now() },
    );

    // Odoo may return a JSON-RPC-level error (e.g. missing session)
    if (response.data.error) {
      throw new EcoSphereApiError(
        'json_rpc_error',
        response.data.error.message ?? 'The Odoo server returned an error.',
      );
    }

    const envelope: ApiEnvelope<T> | undefined = response.data.result;
    if (!envelope) {
      throw new EcoSphereApiError(
        'invalid_response',
        'The server returned an invalid API response.',
      );
    }

    if (!envelope.success) {
      throw new EcoSphereApiError(
        envelope.error?.code ?? 'api_error',
        envelope.error?.message ?? 'The request failed.',
      );
    }

    return envelope;
  } catch (error) {
    if (error instanceof EcoSphereApiError) throw error;
    const axiosErr = error as AxiosError<{ message?: string }>;
    throw new EcoSphereApiError(
      'network_error',
      axiosErr.response?.data?.message ??
        'Unable to connect to the EcoSphere backend. Sign in to Odoo and try again.',
    );
  }
}
