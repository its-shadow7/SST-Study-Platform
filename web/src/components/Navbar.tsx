import React from 'react';
import { Link, useLocation, useSearchParams } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { useTheme } from '@/context/ThemeContext';
import { NotificationsDropdown } from './NotificationsDropdown';
import { RoleBadge } from './RoleBadge';
import {
  Search,
  Bookmark,
  Layers,
  Settings as SettingsIcon,
  LogIn,
  LogOut,
  Menu,
  GraduationCap,
  ShieldAlert,
  FileText,
  HelpCircle,
  Sun,
  Moon
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
  const { resolvedTheme, toggleTheme } = useTheme();
  const location = useLocation();
  const [searchParams, setSearchParams] = useSearchParams();

  const isCurrent = (path: string) => location.pathname.startsWith(path);
  const pathParts = location.pathname.split('/').filter(Boolean);
  const isReaderPage = (pathParts[0] === 'term' && pathParts.length >= 4) || pathParts[0] === 'read';
  const activeTab = searchParams.get('tab') === 'quiz' ? 'quiz' : 'notes';

  const handleSwitchTab = (tab: 'notes' | 'quiz') => {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      if (tab === 'notes') {
        next.delete('tab');
      } else {
        next.set('tab', 'quiz');
      }
      return next;
    });
  };

  return (
    <header className="sticky top-0 z-40 h-14 w-full border-b border-zinc-200/80 dark:border-white/[0.08] bg-white/80 dark:bg-black/60 backdrop-blur-md px-4 sm:px-6 flex items-center justify-between select-none transition-colors">
      {/* Left: Mobile Toggle & Brand Logo */}
      <div className="flex items-center gap-3">
        {showMobileMenuButton && (
          <button
            onClick={onOpenMobileMenu}
            className="p-1.5 rounded-md text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/5 lg:hidden transition-colors"
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
            <span className="text-sm font-semibold tracking-tight text-zinc-900 dark:text-zinc-100 group-hover:text-blue-600 dark:group-hover:text-white transition-colors">
              SST Study Platform
            </span>
            <span className="text-[10px] text-zinc-500 dark:text-zinc-400 tracking-wider font-mono">
              Scaler School of Tech
            </span>
          </div>
        </Link>
      </div>

      {/* Center: Reader Mode Toggle & Search Trigger & Navigation Links */}
      <div className="flex items-center gap-3">
        {/* Lecture Reader Mode Toggle (Notes vs Topic Quiz) */}
        {isReaderPage && (
          <div className="flex items-center p-0.5 rounded-lg border border-zinc-200 dark:border-white/10 bg-zinc-100/90 dark:bg-zinc-900/80 shadow-inner">
            <button
              onClick={() => handleSwitchTab('notes')}
              title="View Lecture Notes"
              className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs transition-all ${
                activeTab === 'notes'
                  ? 'bg-blue-500/15 dark:bg-blue-600/25 text-blue-600 dark:text-blue-300 font-semibold border border-blue-500/30 dark:border-blue-500/40 shadow-sm shadow-blue-500/20'
                  : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-200/50 dark:hover:bg-white/5 border border-transparent'
              }`}
            >
              <FileText className={`w-3.5 h-3.5 ${activeTab === 'notes' ? 'text-blue-600 dark:text-blue-400' : 'text-zinc-500 dark:text-zinc-400'}`} />
              <span>Notes</span>
            </button>
            <button
              onClick={() => handleSwitchTab('quiz')}
              title="Practice Lecture Quiz"
              className={`flex items-center gap-1.5 px-3 py-1 rounded-md text-xs transition-all ${
                activeTab === 'quiz'
                  ? 'bg-purple-500/15 dark:bg-purple-600/25 text-purple-600 dark:text-purple-300 font-semibold border border-purple-500/30 dark:border-purple-500/40 shadow-sm shadow-purple-500/20'
                  : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-200/50 dark:hover:bg-white/5 border border-transparent'
              }`}
            >
              <HelpCircle className={`w-3.5 h-3.5 ${activeTab === 'quiz' ? 'text-purple-600 dark:text-purple-400' : 'text-zinc-500 dark:text-zinc-400'}`} />
              <span>Topic Quiz</span>
            </button>
          </div>
        )}

        {/* Command Palette Trigger */}
        <button
          onClick={onOpenSearch}
          aria-label="Search lecture notes"
          className="flex items-center gap-2.5 px-3 py-1.5 rounded-lg border border-zinc-200 dark:border-white/10 bg-zinc-100/70 dark:bg-white/[0.03] hover:bg-zinc-200/60 dark:hover:bg-white/[0.06] hover:border-zinc-300 dark:hover:border-white/20 text-xs text-zinc-500 dark:text-zinc-400 transition-all w-44 sm:w-60"
        >
          <Search className="w-3.5 h-3.5 text-zinc-500 dark:text-zinc-400" />
          <span className="flex-1 text-left truncate text-zinc-500 dark:text-zinc-400">Search notes...</span>
          <kbd className="hidden sm:inline-flex items-center gap-0.5 px-1.5 py-0.5 text-[10px] font-mono rounded bg-white dark:bg-white/5 border border-zinc-200 dark:border-white/10 text-zinc-500 dark:text-zinc-400 shadow-sm dark:shadow-none">
            Ctrl K
          </kbd>
        </button>

        {/* Global Navigation links */}
        <nav className="hidden md:flex items-center gap-1 text-xs">
          <Link
            to="/terms"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md transition-colors ${
              isCurrent('/terms') || isCurrent('/term')
                ? 'bg-zinc-200/80 dark:bg-white/10 text-zinc-900 dark:text-zinc-100 font-medium'
                : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/5'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span>Curriculum</span>
          </Link>

          <Link
            to="/bookmarks"
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md transition-colors ${
              isCurrent('/bookmarks')
                ? 'bg-zinc-200/80 dark:bg-white/10 text-zinc-900 dark:text-zinc-100 font-medium'
                : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/5'
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
                  ? 'bg-amber-500/15 dark:bg-amber-500/20 text-amber-700 dark:text-amber-300 border border-amber-500/30 font-medium shadow-sm'
                  : 'text-amber-600 dark:text-amber-400 hover:text-amber-700 dark:hover:text-amber-300 hover:bg-amber-500/10'
              }`}
            >
              <ShieldAlert className="w-3.5 h-3.5" />
              <span>Moderation</span>
            </Link>
          )}
        </nav>
      </div>

      {/* Right: Theme Toggle / User / Settings / Login */}
      <div className="flex items-center gap-2">
        {/* Light / Dark Mode Toggle Button */}
        <button
          onClick={toggleTheme}
          aria-label={`Switch to ${resolvedTheme === 'dark' ? 'light' : 'dark'} mode`}
          title={`Switch to ${resolvedTheme === 'dark' ? 'light' : 'dark'} mode`}
          className="p-1.5 sm:p-2 rounded-lg text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/5 border border-zinc-200 dark:border-white/10 transition-all flex items-center justify-center active:scale-95 shadow-sm dark:shadow-none"
        >
          {resolvedTheme === 'dark' ? (
            <Sun className="w-4 h-4 text-amber-400 transition-transform duration-300 hover:rotate-45" />
          ) : (
            <Moon className="w-4 h-4 text-blue-600 transition-transform duration-300 -rotate-12 hover:rotate-0" />
          )}
        </button>

        {user ? (
          <div className="flex items-center gap-2">
            <NotificationsDropdown />

            <Link
              to="/settings"
              className={`flex items-center gap-2 px-2 py-1 rounded-lg transition-colors border ${
                isCurrent('/settings')
                  ? 'bg-zinc-200/70 dark:bg-white/10 border-zinc-300 dark:border-white/20 text-zinc-900 dark:text-zinc-100'
                  : 'border-transparent hover:border-zinc-200 dark:hover:border-white/10 hover:bg-zinc-100 dark:hover:bg-white/5 text-zinc-700 dark:text-zinc-300'
              }`}
              title="Account & Profile Settings"
            >
              <div className="w-7 h-7 rounded-full overflow-hidden bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center text-[11px] font-bold text-white shadow-sm border border-zinc-200 dark:border-white/10 shrink-0">
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
                <div className="flex items-center gap-1.5">
                  <span className="text-xs font-medium text-zinc-800 dark:text-zinc-200 truncate max-w-[110px]">
                    {user.display_name}
                  </span>
                  <RoleBadge role={user.role} size="sm" />
                </div>
                <span className="text-[10px] text-zinc-500 dark:text-zinc-400 font-mono truncate max-w-[120px]">
                  @{user.username || 'student'} • <span className="text-emerald-600 dark:text-emerald-400 font-semibold">T{user.active_term || 1}</span>
                </span>
              </div>
            </Link>

            <button
              onClick={() => logout()}
              title="Sign Out"
              aria-label="Sign out of account"
              className="p-1.5 rounded-md text-zinc-500 dark:text-zinc-400 hover:text-rose-600 dark:hover:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-500/10 transition-colors"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <Link
            to="/login"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-blue-500/30 bg-blue-500/10 hover:bg-blue-500/20 text-xs font-medium text-blue-600 dark:text-blue-400 transition-colors"
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>Sign In</span>
          </Link>
        )}
      </div>
    </header>
  );
};
