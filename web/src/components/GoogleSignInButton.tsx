import React, { useEffect, useRef, useState, useId } from 'react';
import { useAuth } from '../context/AuthContext';

declare global {
  interface Window {
    google?: any;
  }
}

interface GoogleSignInButtonProps {
  theme?: 'outline' | 'filled_blue' | 'filled_black';
  size?: 'large' | 'medium' | 'small';
}

// Module-level singleton state to prevent duplicate google.accounts.id.initialize calls
let isGoogleInitialized = false;
let globalAuthHandler: ((credential: string) => Promise<void>) | null = null;
let globalErrorHandler: ((err: string) => void) | null = null;

export const GoogleSignInButton: React.FC<GoogleSignInButtonProps> = ({
  theme = 'outline',
  size = 'medium'
}) => {
  const { loginWithGoogle } = useAuth();
  const buttonRef = useRef<HTMLDivElement>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [isRendered, setIsRendered] = useState<boolean>(false);
  const containerId = useId();
  const clientId =
    import.meta.env.VITE_GOOGLE_CLIENT_ID ||
    '444963267728-lorfogrhkf1dscm0nhfrj9ath23n2p6h.apps.googleusercontent.com';

  useEffect(() => {
    // Keep active handler pointed to current instance
    globalAuthHandler = loginWithGoogle;
    globalErrorHandler = (msg: string) => setErrorMessage(msg);
  }, [loginWithGoogle]);

  useEffect(() => {
    let checkInterval: ReturnType<typeof setInterval> | null = null;
    let isCancelled = false;

    const setupGoogleButton = () => {
      if (isCancelled) return false;

      if (window.google?.accounts?.id && buttonRef.current) {
        try {
          // 1. Initialize GIS once globally
          if (!isGoogleInitialized) {
            window.google.accounts.id.initialize({
              client_id: clientId,
              callback: async (response: any) => {
                if (response?.credential && globalAuthHandler) {
                  try {
                    setErrorMessage(null);
                    await globalAuthHandler(response.credential);
                  } catch (err: any) {
                    const msg = err.message || 'Google verification failed.';
                    if (globalErrorHandler) globalErrorHandler(msg);
                  }
                }
              },
              auto_select: false,
              context: 'signin'
            });
            isGoogleInitialized = true;
          }

          // 2. Render Google button inside dedicated container
          // Container has no React children, preventing React removeChild DOM conflicts
          buttonRef.current.innerHTML = '';
          window.google.accounts.id.renderButton(buttonRef.current, {
            theme,
            size,
            shape: 'rectangular',
            text: 'signin_with',
            logo_alignment: 'left'
          });

          if (!isCancelled) {
            setIsRendered(true);
          }
          return true;
        } catch (e) {
          console.error('[GoogleAuth] Error rendering button:', e);
        }
      }
      return false;
    };

    if (!setupGoogleButton()) {
      checkInterval = setInterval(() => {
        if (setupGoogleButton() && checkInterval) {
          clearInterval(checkInterval);
          checkInterval = null;
        }
      }, 200);
    }

    const timeout = setTimeout(() => {
      if (checkInterval) {
        clearInterval(checkInterval);
        checkInterval = null;
      }
    }, 6000);

    return () => {
      isCancelled = true;
      if (checkInterval) clearInterval(checkInterval);
      clearTimeout(timeout);
    };
  }, [clientId, theme, size]);

  const handleManualTrigger = () => {
    if (window.google?.accounts?.id) {
      window.google.accounts.id.prompt();
    } else {
      setErrorMessage(
        'Google Services loading. Please check if an ad-blocker or shields is blocking accounts.google.com.'
      );
    }
  };

  return (
    <div
      data-container-id={containerId}
      style={{ display: 'inline-flex', flexDirection: 'column', alignItems: 'center' }}
    >
      {/* 
        Dedicated empty DOM container strictly for Google GIS to mount iframe.
        React renders NO children into this div to guarantee zero DOM collisions.
      */}
      <div
        ref={buttonRef}
        style={{
          display: isRendered ? 'flex' : 'none',
          minHeight: size === 'large' ? '40px' : '36px',
          alignItems: 'center'
        }}
      />

      {/* 
        React fallback button rendered as a sibling outside buttonRef while GIS is loading
      */}
      {!isRendered && (
        <button
          type="button"
          onClick={handleManualTrigger}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.65rem',
            background: '#ffffff',
            color: '#3c4043',
            border: '1px solid #dadce0',
            borderRadius: '4px',
            padding: size === 'large' ? '0.55rem 1.15rem' : '0.4rem 0.85rem',
            fontSize: size === 'large' ? '0.92rem' : '0.85rem',
            fontWeight: 500,
            cursor: 'pointer',
            boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
            fontFamily: 'Roboto, sans-serif'
          }}
        >
          <svg width="18" height="18" viewBox="0 0 48 48">
            <path
              fill="#EA4335"
              d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"
            />
            <path
              fill="#4285F4"
              d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"
            />
            <path
              fill="#FBBC05"
              d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.28-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"
            />
            <path
              fill="#34A853"
              d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"
            />
          </svg>
          <span>Sign in with Google</span>
        </button>
      )}

      {errorMessage && (
        <span
          style={{
            fontSize: '0.75rem',
            color: 'var(--accent-rose)',
            marginTop: '0.35rem',
            textAlign: 'center',
            maxWidth: '240px'
          }}
        >
          {errorMessage}
        </span>
      )}
    </div>
  );
};
