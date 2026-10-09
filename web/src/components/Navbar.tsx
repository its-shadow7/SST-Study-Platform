import React from 'react';
import { Search, Moon, Sun, Bookmark, LogIn, LogOut, Trash2, GraduationCap } from 'lucide-react';
import { Theme } from '../types/note';
import { useAuth } from '../context/AuthContext';

import { GoogleSignInButton } from './GoogleSignInButton';

interface NavbarProps {
  currentTheme: Theme;
  onThemeChange: (theme: Theme) => void;
  onOpenSearch: () => void;
  showBookmarksOnly: boolean;
  onToggleBookmarksOnly: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentTheme,
  onThemeChange,
  onOpenSearch,
  showBookmarksOnly,
  onToggleBookmarksOnly
}) => {
  const { user, loginDevMock, logout, deleteAccount } = useAuth();

  return (
    <header className="navbar">
      <div className="brand-section">
        <span className="brand-logo-badge">SST</span>
        <div>
          <span className="brand-title">Study Platform</span>
          <span className="brand-sub">Notes Portal</span>
        </div>
      </div>

      <div className="nav-actions">
        {/* Search trigger */}
        <button
          className="search-trigger-btn"
          onClick={onOpenSearch}
          title="Search notes (Ctrl+K or Cmd+K)"
        >
          <Search size={15} />
          <span>Search notes...</span>
          <span className="kbd-shortcut">Ctrl K</span>
        </button>

        {/* Bookmarks filter */}
        <button
          className={`auth-btn ${showBookmarksOnly ? 'auth-btn-primary' : 'auth-btn-ghost'}`}
          onClick={onToggleBookmarksOnly}
          title="Filter saved bookmarks"
        >
          <Bookmark size={15} fill={showBookmarksOnly ? 'currentColor' : 'none'} />
          <span>Bookmarks</span>
        </button>

        {/* Theme selector */}
        <select
          className="theme-select"
          value={currentTheme}
          onChange={(e) => onThemeChange(e.target.value as Theme)}
          title="Select theme style"
        >
          <option value="oled-slate">OLED Slate</option>
          <option value="minimalist-midnight">Minimalist Midnight</option>
          <option value="clean-light">Clean Light</option>
        </select>

        {/* Auth section */}
        {user ? (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span
              style={{
                fontSize: '0.8rem',
                color: 'var(--text-secondary)',
                maxWidth: '140px',
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis'
              }}
              title={user.email}
            >
              {user.display_name || user.email.split('@')[0]}
            </span>
            <button
              className="auth-btn auth-btn-ghost"
              onClick={logout}
              title="Sign out of student account"
            >
              <LogOut size={15} />
              <span>Sign Out</span>
            </button>
            <button
              className="auth-btn auth-btn-ghost"
              onClick={() => {
                if (window.confirm('Are you sure you want to delete your profile and all bookmarks?')) {
                  deleteAccount();
                }
              }}
              title="Delete account data"
              style={{ color: 'var(--accent-rose)' }}
            >
              <Trash2 size={15} />
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            <GoogleSignInButton
              theme={currentTheme === 'clean-light' ? 'outline' : 'filled_black'}
              size="medium"
            />
            <button
              className="auth-btn auth-btn-ghost"
              onClick={() => {
                loginDevMock('student@sst.scaler.com').catch((e) => {
                  console.error('Navbar dev login bypass error:', e);
                });
              }}
              title="Quick dev login bypass (student@sst.scaler.com)"
              style={{ fontSize: '0.75rem', padding: '0.35rem 0.65rem' }}
            >
              <LogIn size={13} />
              <span>Dev Login</span>
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
