import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import { NoteIndexItem } from '@/types/note';
import { fetchNotesIndex } from '@/services/notesService';
import { Navbar } from '@/components/Navbar';
import { SearchModal } from '@/components/SearchModal';
import { LoginPage } from '@/pages/LoginPage';
import { TermsPage } from '@/pages/TermsPage';
import { ReaderPage } from '@/pages/ReaderPage';
import { BookmarksPage } from '@/pages/BookmarksPage';
import { SettingsPage } from '@/pages/SettingsPage';
import { ModerationPage } from '@/pages/ModerationPage';
import { ProfilePage } from '@/pages/ProfilePage';
import { NoteStudioPage } from '@/pages/NoteStudioPage';
import { ProfileSetupModal } from '@/components/ProfileSetupModal';
import { NoteRedirector } from '@/components/NoteRedirector';
import { Layers, AlertCircle, RotateCcw } from 'lucide-react';

export const App: React.FC = () => {
  const { user, loading: authLoading } = useAuth();
  const location = useLocation();

  const [notesIndex, setNotesIndex] = useState<NoteIndexItem[]>([]);
  const [searchOpen, setSearchOpen] = useState(false);
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [indexLoading, setIndexLoading] = useState(false);
  const [indexError, setIndexError] = useState<string | null>(null);

  // Global Ctrl+K / Cmd+K search listener
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setSearchOpen((prev) => !prev);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const loadNotesIndex = () => {
    if (!user) {
      setNotesIndex([]);
      setIndexError(null);
      return;
    }

    setIndexLoading(true);
    setIndexError(null);

    fetchNotesIndex()
      .then((data) => {
        setNotesIndex(data);
        setIndexLoading(false);
        setIndexError(null);
      })
      .catch((err) => {
        console.warn('Could not fetch notes index:', err);
        setIndexError('Failed to load course catalogue. Please verify your connection.');
        setIndexLoading(false);
      });
  };

  // Fetch approved notes index once authenticated
  useEffect(() => {
    loadNotesIndex();
  }, [user]);

  // Loading screen while checking existing auth session
  if (authLoading) {
    return (
      <div className="min-h-screen w-full bg-slate-50 dark:bg-[#09090b] flex flex-col items-center justify-center space-y-4 select-none">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center font-bold text-sm text-white animate-pulse">
          SST
        </div>
        <div className="flex items-center gap-2 text-xs text-zinc-500 font-mono">
          <Layers className="w-3.5 h-3.5 animate-spin" />
          <span>Restoring session...</span>
        </div>
      </div>
    );
  }

  const isLoginPage = location.pathname === '/login';
  const isReaderPage = location.pathname.startsWith('/term/') || location.pathname.startsWith('/read/');

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-[#09090b] text-zinc-800 dark:text-zinc-200 flex flex-col font-sans selection:bg-blue-500/30 selection:text-white">
      {/* Global Navbar (shown everywhere except login wall) */}
      {!isLoginPage && (
        <Navbar
          onOpenSearch={() => setSearchOpen(true)}
          onOpenMobileMenu={() => setIsMobileOpen(true)}
          showMobileMenuButton={isReaderPage}
        />
      )}

      {/* Course Catalogue Loading Error Alert Banner */}
      {indexError && (
        <div className="bg-rose-500/10 border-b border-rose-500/20 px-4 py-2 flex items-center justify-between text-xs text-rose-300">
          <div className="flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
            <span>{indexError}</span>
          </div>
          <button
            onClick={loadNotesIndex}
            className="flex items-center gap-1.5 px-3 py-1 rounded-md bg-rose-500/20 hover:bg-rose-500/30 text-rose-200 font-medium transition-colors"
          >
            <RotateCcw className="w-3 h-3" />
            <span>Retry Catalogue</span>
          </button>
        </div>
      )}

      {/* Main Content Router */}
      <div className="flex-1 flex flex-col">
        <Routes>
          {/* Login Wall */}
          <Route path="/login" element={<LoginPage />} />

          {/* Curriculum Hub */}
          <Route
            path="/terms"
            element={
              user ? <TermsPage notes={notesIndex} /> : <Navigate to="/login" replace />
            }
          />

          {/* 3-Island Reader Workspace */}
          <Route
            path="/term/:termId/:subjectCode/:noteId"
            element={
              user ? (
                <ReaderPage
                  notesIndex={notesIndex}
                  isMobileOpen={isMobileOpen}
                  onCloseMobile={() => setIsMobileOpen(false)}
                />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          {/* Term redirect helper */}
          <Route
            path="/term/:termId"
            element={
              user ? (
                <ReaderPage
                  notesIndex={notesIndex}
                  isMobileOpen={isMobileOpen}
                  onCloseMobile={() => setIsMobileOpen(false)}
                />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          <Route
            path="/term/:termId/:subjectCode"
            element={
              user ? (
                <ReaderPage
                  notesIndex={notesIndex}
                  isMobileOpen={isMobileOpen}
                  onCloseMobile={() => setIsMobileOpen(false)}
                />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          {/* Universal Note Permalink (/read/:noteId) */}
          <Route
            path="/read/:noteId"
            element={
              user ? (
                <NoteRedirector
                  notesIndex={notesIndex}
                  indexLoading={indexLoading}
                />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          {/* Bookmarks Page */}
          <Route
            path="/bookmarks"
            element={
              user ? (
                <BookmarksPage notesIndex={notesIndex} />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          {/* Default /term route opens student's active term if it has notes, otherwise Curriculum Hub */}
          <Route
            path="/term"
            element={
              user ? (
                <Navigate
                  to={
                    user.active_term && notesIndex.some((n) => n.term.toLowerCase() === `term ${user.active_term}`.toLowerCase())
                      ? `/term/term-${user.active_term}`
                      : '/terms'
                  }
                  replace
                />
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          {/* Account Settings Page */}
          <Route
            path="/settings"
            element={user ? <SettingsPage /> : <Navigate to="/login" replace />}
          />

          {/* Public Student Profile Page */}
          <Route
            path="/profile/:username"
            element={user ? <ProfilePage /> : <Navigate to="/login" replace />}
          />

          {/* Moderation Queue Page (Admins & Moderators) */}
          <Route
            path="/moderation"
            element={
              user ? (
                user.role === 'admin' || user.role === 'moderator' ? (
                  <ModerationPage />
                ) : (
                  <Navigate to="/terms" replace />
                )
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          {/* Note Studio Routes (Admins & Moderators) */}
          <Route
            path="/studio"
            element={
              user ? (
                user.role === 'admin' || user.role === 'moderator' ? (
                  <NoteStudioPage />
                ) : (
                  <Navigate to="/terms" replace />
                )
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="/studio/:noteId"
            element={
              user ? (
                user.role === 'admin' || user.role === 'moderator' ? (
                  <NoteStudioPage />
                ) : (
                  <Navigate to="/terms" replace />
                )
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />

          {/* Fallback route: Authenticated user defaults to Curriculum Hub */}
          <Route
            path="*"
            element={
              <Navigate
                to={user ? "/terms" : "/login"}
                replace
              />
            }
          />
        </Routes>
      </div>

      {/* Global Command Palette Search Overlay */}
      <SearchModal
        isOpen={searchOpen}
        onClose={() => setSearchOpen(false)}
        notes={notesIndex}
      />

      {/* One-time Profile Setup Modal for Special Accounts on First Login */}
      <ProfileSetupModal isOpen={Boolean(user?.needs_profile_setup)} />
    </div>
  );
};
