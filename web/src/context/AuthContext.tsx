import React, { createContext, useContext, useState, useEffect, useRef, ReactNode } from 'react';
import { User } from '../types/note';
import { api, getCsrfToken, setCsrfToken } from '../services/apiClient';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  loginWithGoogle: (idToken: string) => Promise<void>;
  loginDevMock: (email?: string) => Promise<void>;
  logout: () => Promise<void>;
  deleteAccount: () => Promise<void>;
  refreshSession: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const hasInitializedAuth = useRef(false);

  const initAuth = async () => {
    setLoading(true);
    try {
      // Always call /api/auth/refresh on load — it's the only endpoint that returns
      // both the user AND a fresh CSRF token. /api/users/me never returns csrf_token,
      // so using it here would leave us without a CSRF token after a page reload,
      // breaking logout and delete account.
      const authData = await api.post<{ user: User; csrf_token: string }>('/api/auth/refresh');
      setUser(authData.user);
      setCsrfToken(authData.csrf_token);
      setError(null);
    } catch {
      setUser(null);
      setCsrfToken(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // React Strict Mode intentionally runs effects twice in development. A refresh
    // token is rotated on use, so two concurrent calls race: one succeeds and the
    // other receives 401 for the already-rotated token. Keep initialization to one
    // request per mounted provider.
    if (hasInitializedAuth.current) return;
    hasInitializedAuth.current = true;
    void initAuth();
  }, []);

  const loginWithGoogle = async (idToken: string) => {
    try {
      setLoading(true);
      setError(null);
      const res = await api.post<{ user: User; csrf_token: string }>('/api/auth/google', { id_token: idToken });
      setUser(res.user);
      setCsrfToken(res.csrf_token);
    } catch (err: any) {
      setError(err.message || 'Google sign-in failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const loginDevMock = async (email: string = 'student@sst.scaler.com') => {
    try {
      setLoading(true);
      setError(null);
      const res = await api.post<{ user: User; csrf_token: string }>('/api/auth/google', { id_token: `mock:${email}` });
      setUser(res.user);
      setCsrfToken(res.csrf_token);
    } catch (err: any) {
      if (import.meta.env.DEV && (!err.status || err.status >= 500)) {
        console.warn('Backend server unavailable; activating local dev login bypass.');
        const mockUser: User = {
          user_id: 'mock_dev_student',
          email: email,
          display_name: email.split('@')[0].replace('.', ' ').replace(/^./, str => str.toUpperCase()),
          status: 'active'
        };
        setUser(mockUser);
        setCsrfToken('mock_csrf_dev');
        setError(null);
        return;
      }
      setError(err.message || 'Dev mock sign-in failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      // A restored session normally already has a CSRF token. If browser storage
      // was cleared while the HttpOnly session cookies survived, renew it before
      // attempting a state-changing request.
      if (!getCsrfToken()) {
        const restored = await refreshSession();
        if (!restored) return;
      }
      await api.post('/api/auth/logout');
    } catch (err) {
      console.warn('Logout error', err);
    } finally {
      setUser(null);
      setCsrfToken(null);
    }
  };

  const deleteAccount = async () => {
    try {
      // See logout: make the account-deletion action resilient to a missing
      // session-scoped CSRF token without weakening the backend CSRF check.
      if (!getCsrfToken()) {
        const restored = await refreshSession();
        if (!restored) return;
      }
      await api.delete('/api/users/me');
    } catch (err) {
      console.warn('Delete account error', err);
      // Do not clear local auth state after a failed deletion. Doing so makes the
      // UI look signed out while the server-side session is still active.
      return;
    }

    setUser(null);
    setCsrfToken(null);
  };

  const refreshSession = async (): Promise<boolean> => {
    try {
      const res = await api.post<{ user: User; csrf_token: string }>('/api/auth/refresh');
      setUser(res.user);
      setCsrfToken(res.csrf_token);
      return true;
    } catch {
      setUser(null);
      return false;
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        error,
        loginWithGoogle,
        loginDevMock,
        logout,
        deleteAccount,
        refreshSession
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
