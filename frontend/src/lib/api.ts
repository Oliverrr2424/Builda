export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'

type HttpMethod = 'GET' | 'POST' | 'DELETE'

interface RequestOptions<TBody> {
  method?: HttpMethod
  body?: TBody
  signal?: AbortSignal
}

export async function request<TResponse, TBody = unknown>(
  path: string,
  options: RequestOptions<TBody> = {}
): Promise<TResponse> {
  const headers: HeadersInit = {
    'Content-Type': 'application/json'
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method: options.method ?? 'GET',
    headers,
    body: options.body ? JSON.stringify(options.body) : undefined,
    signal: options.signal,
  })

  if (!response.ok) {
    const errorBody = await response.text()
    throw new Error(errorBody || 'API 请求失败')
  }

  return response.json() as Promise<TResponse>
}
