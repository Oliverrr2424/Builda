import { useMutation, useQuery, UseQueryOptions } from '@tanstack/react-query'

import { request } from '../lib/api'

type QueryKey = [string, Record<string, unknown>?]

export function useApiQuery<TData>(
  key: QueryKey,
  path: string,
  options?: Omit<UseQueryOptions<TData, Error, TData, QueryKey>, 'queryKey' | 'queryFn'>
) {
  return useQuery<TData, Error, TData, QueryKey>({
    queryKey: key,
    queryFn: () => request<TData>(path),
    ...options,
  })
}

export function useApiMutation<TResponse, TBody = unknown>(path: string) {
  return useMutation<TResponse, Error, TBody>({
    mutationFn: (body: TBody) =>
      request<TResponse, TBody>(path, { method: 'POST', body }),
  })
}
