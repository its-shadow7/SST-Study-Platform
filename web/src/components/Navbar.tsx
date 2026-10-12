import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { NotificationsDropdown } from './NotificationsDropdown';
import {
  Search,
  Bookmark,
  Layers,
  Settings as SettingsIcon,
  LogIn,
  LogOut,
  Menu,
  GraduationCap,
  ShieldAlert
} from 'lucide-react';

interface NavbarProps {
  onOpenSearch: () => void;
  onOpenMobileMenu?: () => void;
  showMobileMenuButton?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  onOpenSearch,
  onOpenMobileMenu,
  showMobileMenuButton = false,
}) => {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isCurrent = (path: string) => location.pathname.startsWith(path);

  return (
    <header className="sticky top-0 z-40 h-14 w-full border-b border-white/[0.08] bg-black/60 backdrop-blur-md px-4 sm:px-6 flex items-center justify-between select-none">
      {/* Left: Mobile Toggle & Brand Logo */}
      <div className="flex items-center gap-3">
        {showMobileMenuButton && (
          <button
            onClick={onOpenMobileMenu}
            className="p-1.5 rounded-md text-zinc-400 hover:text-zinc-200 hover:bg-white/5 lg:hidden transition-colors"
            title="Open navigation menu"
            aria-label="Open course navigation menu"
          >
            <Menu className="w-5 h-5" />
          </button>
        )}

        <Link to="/terms" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center font-bold text-xs text-white shadow-lg shadow-blue-500/20 group-hover:scale-105 transition-transform">
            SST
          </div>
          <div className="flex flex-col">
            <span className="text-sm font-semibold tracking-tight text-zinc-100 group-hover:text-white transition-colors">
              SST Study Platform
            </span>
            <span className="text-[10px] text-zinc-400 tracking-wider font-mono">
              Scaler School of Tech
            </span>
          </div>
        </Link>
      </div>

      {/* Center: Search Trigger & Navigation Links */}
      <div className="flex items-center gap-3">
        {/* Command Palette Trigger */}
        <button
          onClick={onOpenSearch}
          aria-label="Search lecture notes"
          className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg border border-white/10 bg-white/[0.03] hover:bg-white/[0.06] hover:border-white/20 text-xs text-zinc-400 transition-all w-48 sm:w-64"
        >
          <Search className="w-3.5 h-3.5 text-zinc-400" />
          <span className="flex-1 text-left truncate text-zinc-400">Search notes...</span>
          <kbd className="hidden sm:inline-flex items-center gap-0.5 px-1.5 py-0.5 text-[10px] font-mono rounded bg-white/5 border border-white/10 text-zinc-400">
            Ctrl K
          </kbd>
        </button>

        {/* Global Navigation links */}
        <nav className="hidden md:flex items-center gap-1 text-xs">
          <Link
            to="/terms"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md transition-colors ${
              isCurrent('/terms') || isCurrent('/term')
                ? 'bg-white/10 text-zinc-100 font-medium'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-white/5'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Curriculum</span>
          </Link>

          <Link
            to="/bookmarks"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md transition-colors ${
              isCurrent('/bookmarks')
                ? 'bg-white/10 text-zinc-100 font-medium'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-white/5'
            }`}
          >
            <Bookmark className="w-3.5 h-3.5" />
            <span>Bookmarks</span>
          </Link>

          {(user?.role === 'admin' || user?.role === 'moderator') && (
            <Link
              to="/moderation"
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md transition-colors ${
                isCurrent('/moderation')
                  ? 'bg-amber-500/20 text-amber-300 border border-amber-500/30 font-medium shadow-sm'
                  : 'text-amber-400 hover:text-amber-300 hover:bg-amber-500/10'
              }`}
            >
              <ShieldAlert className="w-3.5 h-3.5" />
              <span>Moderation</span>
            </Link>
          )}
        </nav>
      </div>

      {/* Right: User / Settings / Login */}
      <div className="flex items-center gap-2">
        {user ? (
          <div className="flex items-center gap-2">
            <NotificationsDropdown />

            <Link
              to="/settings"
              className={`flex items-center gap-2 px-2 py-1 rounded-lg transition-colors border ${
                isCurrent('/settings')
                  ? 'bg-white/10 border-white/20 text-zinc-100'
                  : 'border-transparent hover:border-white/10 hover:bg-white/5 text-zinc-300'
              }`}
              title="Account & Profile Settings"
            >
              <div className="w-7 h-7 rounded-full overflow-hidden bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center text-[11px] font-bold text-white shadow-sm border border-white/10 shrink-0">
                {user.avatar_url ? (
                  <img
                    src={user.avatar_url}
                    alt={user.display_name}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      (e.currentTarget as HTMLElement).style.display = 'none';
                    }}
                  />
                ) : (
                  <span>{(user.display_name || user.email).charAt(0).toUpperCase()}</span>
                )}
              </div>

              <div className="hidden sm:flex flex-col text-left leading-tight">
                <span className="text-xs font-medium text-zinc-200 truncate max-w-[120px]">
                  {user.display_name}
                </span>
                <span className="text-[10px] text-zinc-400 font-mono truncate max-w-[120px]">
                  @{user.username || 'student'} • <span className="text-emerald-400 font-semibold">T{user.active_term || 1}</span>
                </span>
              </div>
            </Link>

            <button
              onClick={() => logout()}
              title="Sign Out"
              aria-label="Sign out of account"
              className="p-1.5 rounded-md text-zinc-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <Link
            to="/login"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-blue-500/30 bg-blue-500/10 hover:bg-blue-500/20 text-xs font-medium text-blue-400 transition-colors"
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>Sign In</span>
          </Link>
        )}
      </div>
    </header>
  );
};
