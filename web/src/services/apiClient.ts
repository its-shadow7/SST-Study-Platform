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

let refreshPromise: Promise<string | null> | null = null;

/**
 * Deduplicated auth session refresh.
 * Calls /api/auth/refresh to rotate refresh token, obtain fresh cookies,
 * and fetch a renewed server-side registered CSRF token.
 */
export async function refreshAuthSession(): Promise<string | null> {
  if (refreshPromise) {
    return refreshPromise;
  }

  refreshPromise = (async () => {
    try {
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        return null;
      }

      const data = await response.json();
      if (data?.csrf_token) {
        setCsrfToken(data.csrf_token);
        return data.csrf_token as string;
      }
      return null;
    } catch {
      return null;
    } finally {
      refreshPromise = null;
    }
  })();

  return refreshPromise;
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {},
  isRetry = false
): Promise<T> {
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
    credentials: 'include', // Send and receive HttpOnly cookies
  });

  if (response.status === 204) {
    return {} as T;
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const errorMsg = String(data.message || data.detail || '');
    const isCsrfError =
      response.status === 403 &&
      (errorMsg.toLowerCase().includes('csrf') || errorMsg.toLowerCase().includes('unrecognised'));
    const isAuthError = response.status === 401 && !endpoint.includes('/api/auth/');

    // Auto-refresh CSRF / session token and retry mutation once
    if (!isRetry && (isCsrfError || isAuthError) && !endpoint.includes('/api/auth/refresh')) {
      const newCsrf = await refreshAuthSession();
      if (newCsrf) {
        const retryHeaders = new Headers(options.headers || {});
        if (!retryHeaders.has('Content-Type') && options.body && typeof options.body === 'string') {
          retryHeaders.set('Content-Type', 'application/json');
        }
        if (['POST', 'PUT', 'DELETE', 'PATCH'].includes(method)) {
          retryHeaders.set('x-csrf-token', newCsrf);
        }
        return request<T>(endpoint, { ...options, headers: retryHeaders }, true);
      }
    }

    const error: ApiError = {
      status: response.status,
      error: data.error || 'API_ERROR',
      message: errorMsg || `Request failed with status ${response.status}`,
      request_id: data.request_id,
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
  patch: <T>(url: string, body?: any, options?: RequestInit) =>
    request<T>(url, { ...options, method: 'PATCH', body: body ? JSON.stringify(body) : undefined }),
  delete: <T>(url: string, options?: RequestInit) =>
    request<T>(url, { ...options, method: 'DELETE' }),
};
