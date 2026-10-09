let currentCsrfToken: string | null =
  typeof window !== 'undefined' ? sessionStorage.getItem('sst_csrf_token') : null;

export function setCsrfToken(token: string | null) {
  currentCsrfToken = token;
  if (typeof window !== 'undefined') {
    if (token) {
      sessionStorage.setItem('sst_csrf_token', token);
    } else {
      sessionStorage.removeItem('sst_csrf_token');
    }
  }
}

export function getCsrfToken(): string | null {
  if (!currentCsrfToken && typeof window !== 'undefined') {
    currentCsrfToken = sessionStorage.getItem('sst_csrf_token');
  }
  return currentCsrfToken;
}

export interface ApiError {
  error: string;
  message: string;
  request_id?: string;
  status: number;
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers || {});

  if (!headers.has('Content-Type') && options.body && typeof options.body === 'string') {
    headers.set('Content-Type', 'application/json');
  }

  // Include session-bound CSRF token on state-changing requests
  const method = (options.method || 'GET').toUpperCase();
  const token = getCsrfToken();
  if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(method) && token) {
    headers.set('x-csrf-token', token);
  }

  const response = await fetch(endpoint, {
    ...options,
    headers,
    credentials: 'include' // Send and receive HttpOnly cookies
  });

  if (response.status === 204) {
    return {} as T;
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const error: ApiError = {
      status: response.status,
      error: data.error || 'API_ERROR',
      message: data.message || `Request failed with status ${response.status}`,
      request_id: data.request_id
    };
    throw error;
  }

  return data as T;
}

export const api = {
  get: <T>(url: string, options?: RequestInit) => request<T>(url, { ...options, method: 'GET' }),
  post: <T>(url: string, body?: any, options?: RequestInit) =>
    request<T>(url, { ...options, method: 'POST', body: body ? JSON.stringify(body) : undefined }),
  put: <T>(url: string, body?: any, options?: RequestInit) =>
    request<T>(url, { ...options, method: 'PUT', body: body ? JSON.stringify(body) : undefined }),
  delete: <T>(url: string, options?: RequestInit) =>
    request<T>(url, { ...options, method: 'DELETE' }),
};
