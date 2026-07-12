import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
  listResource,
  createResource,
  updateResource,
  deleteResource,
} from '../api/resources.api';
import type { ApiRecord, ListParams, ResourceName } from '../types/api';

export const resourceKey = (resource: ResourceName, params?: ListParams) =>
  ['resource', resource, params] as const;

export function useResourceList<T extends ApiRecord>(
  resource: ResourceName,
  params: ListParams = {},
) {
  return useQuery({
    queryKey: resourceKey(resource, params),
    queryFn: () => listResource<T>(resource, params),
  });
}

export function useResourceMutations<T extends ApiRecord>(
  resource: ResourceName,
) {
  const qc = useQueryClient();
  const refresh = () =>
    qc.invalidateQueries({ queryKey: ['resource', resource] });

  const create = useMutation({
    mutationFn: (values: Record<string, unknown>) =>
      createResource<T>(resource, values),
    onSuccess: refresh,
  });

  const update = useMutation({
    mutationFn: ({ id, values }: { id: number; values: Record<string, unknown> }) =>
      updateResource<T>(resource, id, values),
    onSuccess: refresh,
  });

  const remove = useMutation({
    mutationFn: (id: number) => deleteResource(resource, id),
    onSuccess: refresh,
  });

  return { create, update, remove };
}
