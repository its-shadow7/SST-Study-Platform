import React, { useState, useEffect } from 'react';
import { Theme, Note, NoteIndexItem } from './types/note';
import { fetchNotesIndex, fetchNoteById } from './services/notesService';
import { useAuth } from './context/AuthContext';
import { useBookmarks } from './context/BookmarkContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { TableOfContents } from './components/TableOfContents';
import { MarkdownViewer } from './components/MarkdownViewer';
import { SearchModal } from './components/SearchModal';
import { GoogleSignInButton } from './components/GoogleSignInButton';
import { Bookmark, CheckCircle, ShieldAlert, Sparkles, BookOpen } from 'lucide-react';

export const App: React.FC = () => {
  const [theme, setTheme] = useState<Theme>('oled-slate');
  const [notesIndex, setNotesIndex] = useState<NoteIndexItem[]>([]);
  const [selectedNoteId, setSelectedNoteId] = useState<string | null>(null);
  const [currentNote, setCurrentNote] = useState<Note | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [authRequired, setAuthRequired] = useState<boolean>(false);
  const [searchOpen, setSearchOpen] = useState<boolean>(false);
  const [showBookmarksOnly, setShowBookmarksOnly] = useState<boolean>(false);

  const { user, loading: authLoading, loginDevMock, error: authError } = useAuth();
  const { isBookmarked, toggleBookmark, toastMessage, clearToast } = useBookmarks();

  // Apply theme to document
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Global Ctrl+K shortcut listener
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

  // Fetch index
  const loadIndex = async () => {
    setLoading(true);
    try {
      const data = await fetchNotesIndex();
      setNotesIndex(data);
      setAuthRequired(false);
      if (data.length > 0 && !selectedNoteId) {
        setSelectedNoteId(data[0].note_id);
      }
    } catch (err: any) {
      if (err.message === 'AUTH_REQUIRED') {
        setAuthRequired(true);
      } else {
        console.error('Error fetching notes index:', err);
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Wait for the refresh-cookie check before requesting protected content.
    // If restoration fails, discard any previously displayed note so that the
    // signed-out UI cannot show stale course material.
    if (authLoading) return;

    if (!user) {
      setNotesIndex([]);
      setSelectedNoteId(null);
      setCurrentNote(null);
      setAuthRequired(true);
      setLoading(false);
      return;
    }

    loadIndex();
  }, [user, authLoading]);

  // Fetch active note details
  useEffect(() => {
    if (!user || !selectedNoteId) return;

    const loadNote = async () => {
      try {
        const note = await fetchNoteById(selectedNoteId);
        setCurrentNote(note);
      } catch (err: any) {
        if (err.message === 'AUTH_REQUIRED') {
          setAuthRequired(true);
        } else {
          console.error(`Error loading note ${selectedNoteId}:`, err);
        }
      }
    };

    loadNote();
  }, [selectedNoteId, user]);

  const bookmarked = selectedNoteId ? isBookmarked(selectedNoteId) : false;
  // Render authentication from the resolved session state itself, not only from
  // the asynchronous note request. This prevents a failed refresh from leaving
  // the reader indefinitely on "Loading course notes...".
  const showAuthentication = !authLoading && (!user || authRequired);

  return (
    <div className="app-container">
      {/* Top Navbar */}
      <Navbar
        currentTheme={theme}
        onThemeChange={setTheme}
        onOpenSearch={() => setSearchOpen(true)}
        showBookmarksOnly={showBookmarksOnly}
        onToggleBookmarksOnly={() => setShowBookmarksOnly((prev) => !prev)}
      />

      {/* Main 3-Panel Reader Layout */}
      <div className="main-layout">
        {/* Left: Sidebar Navigation */}
        <Sidebar
          notes={notesIndex}
          selectedNoteId={selectedNoteId}
          onSelectNote={(id) => setSelectedNoteId(id)}
          showBookmarksOnly={showBookmarksOnly}
        />

        {/* Center: Note Reader */}
        <main className="reader-container">
          <div className="reader-content-wrap">
            {showAuthentication ? (
              <div
                style={{
                  padding: '3rem 2rem',
                  textAlign: 'center',
                  background: 'var(--bg-surface)',
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius-lg)',
                  marginTop: '2rem'
                }}
              >
                <ShieldAlert size={48} color="var(--primary)" style={{ marginBottom: '1rem' }} />
                <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.75rem' }}>
                  Student Authentication Required
                </h2>
                <p style={{ color: 'var(--text-secondary)', maxWidth: '520px', margin: '0 auto 1.5rem auto' }}>
                  Course notes are restricted to Scaler School of Technology students. Please sign in
                  with your <strong>@sst.scaler.com</strong> Google Workspace account to read notes.
                </p>

                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.75rem' }}>
                  <GoogleSignInButton
                    theme={theme === 'clean-light' ? 'outline' : 'filled_black'}
                    size="large"
                  />
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>or</span>
                  <button
                    className="auth-btn auth-btn-ghost"
                    onClick={() => {
                      loginDevMock('student@sst.scaler.com').catch((e) => {
                        console.error('Quick dev login bypass error:', e);
                      });
                    }}
                    style={{ padding: '0.5rem 1.25rem', fontSize: '0.85rem' }}
                  >
                    <Sparkles size={15} />
                    <span>Quick Dev Login Bypass</span>
                  </button>
                  {authError && (
                    <span style={{ fontSize: '0.8rem', color: 'var(--accent-rose)', marginTop: '0.35rem', textAlign: 'center', maxWidth: '320px' }}>
                      {authError}
                    </span>
                  )}
                </div>
              </div>
            ) : loading || !currentNote ? (
              <div style={{ padding: '4rem 0', textAlign: 'center', color: 'var(--text-muted)' }}>
                Loading course notes...
              </div>
            ) : (
              <>
                {/* Note Header */}
                <div className="note-header">
                  <div className="note-header-badges">
                    <span className="subject-tag">{currentNote.subject_code}</span>
                    <span className="badge badge-term">{currentNote.term}</span>
                    <span className="badge badge-approved">
                      <CheckCircle size={12} style={{ display: 'inline', marginRight: '4px' }} />
                      Reviewed & Approved
                    </span>
                  </div>

                  <h1 className="note-main-title">{currentNote.topic_title}</h1>

                  <p style={{ fontSize: '1.05rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                    {currentNote.summary}
                  </p>

                  <div className="note-actions-bar">
                    <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                      {currentNote.tags.map((tag) => (
                        <span
                          key={tag}
                          style={{
                            fontSize: '0.75rem',
                            color: 'var(--text-muted)',
                            background: 'var(--bg-surface)',
                            border: '1px solid var(--border)',
                            padding: '0.2rem 0.5rem',
                            borderRadius: '4px'
                          }}
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>

                    <button
                      className={`bookmark-toggle-btn ${bookmarked ? 'bookmarked' : ''}`}
                      onClick={() => toggleBookmark(currentNote.note_id)}
                      title={bookmarked ? 'Remove from bookmarks' : 'Save bookmark'}
                    >
                      <Bookmark size={15} fill={bookmarked ? 'currentColor' : 'none'} />
                      <span>{bookmarked ? 'Bookmarked' : 'Bookmark'}</span>
                    </button>
                  </div>
                </div>

                {/* Learning Objectives Callout */}
                {currentNote.learning_objectives && currentNote.learning_objectives.length > 0 && (
                  <div className="callout-box" style={{ borderLeftColor: 'var(--accent-purple)' }}>
                    <div className="callout-title" style={{ color: 'var(--accent-purple)' }}>
                      <BookOpen size={17} />
                      <span>Learning Objectives</span>
                    </div>
                    <ul className="callout-list">
                      {currentNote.learning_objectives.map((obj, i) => (
                        <li key={i}>
                          <span>•</span>
                          <span>{obj}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Key Takeaways Callout */}
                {currentNote.key_takeaways && currentNote.key_takeaways.length > 0 && (
                  <div className="callout-box">
                    <div className="callout-title">
                      <Sparkles size={17} />
                      <span>Key Takeaways</span>
                    </div>
                    <ul className="callout-list">
                      {currentNote.key_takeaways.map((takeaway, i) => (
                        <li key={i}>
                          <span>•</span>
                          <span>{takeaway}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Markdown Sections */}
                {currentNote.sections.map((section) => (
                  <article
                    key={section.section_id}
                    id={section.section_id}
                    className="markdown-section"
                  >
                    <h2 className="markdown-section-title">{section.heading}</h2>
                    <MarkdownViewer content={section.body} />

                    {section.citations && section.citations.length > 0 && (
                      <div className="citations-box">
                        <strong>Sources & References:</strong> {section.citations.join('; ')}
                      </div>
                    )}
                  </article>
                ))}
              </>
            )}
          </div>
        </main>

        {/* Right: Table of Contents */}
        {currentNote && currentNote.sections && (
          <TableOfContents sections={currentNote.sections} />
        )}
      </div>

      {/* Spotlight Search Modal */}
      <SearchModal
        isOpen={searchOpen}
        onClose={() => setSearchOpen(false)}
        notes={notesIndex}
        onSelectNote={(id) => setSelectedNoteId(id)}
      />

      {/* Toast Alert */}
      {toastMessage && (
        <div className="toast" onClick={clearToast}>
          <span>{toastMessage}</span>
        </div>
      )}
    </div>
  );
};
