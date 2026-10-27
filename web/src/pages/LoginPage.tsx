import React from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { GoogleSignInButton } from '@/components/GoogleSignInButton';
import { ShieldCheck, Sparkles, GraduationCap } from 'lucide-react';

export const LoginPage: React.FC = () => {
  const { user, loading, loginDevMock, error } = useAuth();
  const navigate = useNavigate();

  // If already authenticated, redirect to curriculum hub
  if (!loading && user) {
    return <Navigate to="/terms" replace />;
  }

  return (
    <div className="min-h-screen w-full bg-slate-50 dark:bg-[#09090b] text-zinc-900 dark:text-zinc-100 flex flex-col items-center justify-center p-4 relative overflow-hidden select-none transition-colors duration-300">
      {/* Background radial gradient spotlight */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-500/10 dark:bg-blue-500/5 rounded-full blur-3xl pointer-events-none" />

      {/* Login Card */}
      <div className="relative w-full max-w-md rounded-2xl border border-zinc-200/80 dark:border-white/10 bg-white/90 dark:bg-black/60 backdrop-blur-xl p-8 sm:p-10 shadow-xl dark:shadow-2xl space-y-8 text-center transition-colors">
        {/* Brand Icon */}
        <div className="flex flex-col items-center space-y-3">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center text-white font-bold text-lg shadow-lg shadow-blue-500/25">
            SST
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
              SST Study Platform
            </h1>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1 font-mono">
              Scaler School of Technology
            </p>
          </div>
        </div>

        {/* Access Disclaimer */}
        <div className="p-3.5 rounded-xl border border-zinc-200/80 dark:border-white/5 bg-zinc-50 dark:bg-white/[0.02] flex items-center gap-3 text-left">
          <ShieldCheck className="w-5 h-5 text-blue-600 dark:text-blue-400 shrink-0" />
          <p className="text-xs text-zinc-600 dark:text-zinc-300 leading-relaxed">
            Restricted student portal. Only verified SST students with a valid{' '}
            <strong className="text-zinc-900 dark:text-zinc-100">@sst.scaler.com</strong> account can sign in.
          </p>
        </div>

        {/* Sign In Button Container */}
        <div className="space-y-4 pt-2">
          <div className="flex justify-center">
            <GoogleSignInButton theme="outline" size="large" />
          </div>

          {/* Dev mock login button for testing */}
          <div className="pt-4 border-t border-zinc-200 dark:border-white/[0.08] flex flex-col items-center gap-2">
            <span className="text-[11px] text-zinc-500 dark:text-zinc-400 uppercase tracking-wider font-semibold">
              Development Access
            </span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  loginDevMock('student@sst.scaler.com')
                    .then(() => navigate('/terms'))
                    .catch((e) => console.error('Dev bypass error:', e));
                }}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-zinc-200 dark:border-white/10 bg-zinc-100 hover:bg-zinc-200 dark:bg-white/5 dark:hover:bg-white/10 text-xs text-zinc-700 dark:text-zinc-300 transition-colors"
              >
                <Sparkles className="w-3.5 h-3.5 text-blue-600 dark:text-blue-400" />
                <span>Student Bypass</span>
              </button>
              <button
                onClick={() => {
                  loginDevMock('admin@sst.scaler.com')
                    .then(() => navigate('/terms'))
                    .catch((e) => console.error('Dev bypass error:', e));
                }}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-indigo-500/30 bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-500/10 dark:hover:bg-indigo-500/20 text-xs text-indigo-700 dark:text-indigo-300 transition-colors"
              >
                <Sparkles className="w-3.5 h-3.5 text-indigo-600 dark:text-indigo-400" />
                <span>Admin Bypass</span>
              </button>
            </div>
          </div>

          {error && (
            <div className="p-3 rounded-lg border border-rose-500/30 bg-rose-500/10 text-rose-600 dark:text-rose-400 text-xs">
              {error}
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="pt-2 text-[11px] text-zinc-500 dark:text-zinc-400">
          Protected by asymmetric RS256 token verification
        </div>
      </div>
    </div>
  );
};
