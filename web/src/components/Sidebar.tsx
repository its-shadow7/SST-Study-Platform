import React, { useState, useMemo, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { NoteIndexItem } from '@/types/note';
import { useBookmarks } from '@/context/BookmarkContext';
import { useAuth } from '@/context/AuthContext';
import {
  ChevronDown,
  ChevronRight,
  Search,
  BookOpen,
  Bookmark as BookmarkIcon,
  PanelLeftClose,
  X,
  Layers,
  Sparkles
} from 'lucide-react';

interface SidebarProps {
  notes: NoteIndexItem[];
  currentTerm: string;
  onSelectTerm: (term: string) => void;
  activeSubjectCode?: string;
  activeNoteId?: string;
  isZenMode: boolean;
  onToggleZenMode: () => void;
  isMobileOpen: boolean;
  onCloseMobile: () => void;
}

const ALL_TERMS = Array.from({ length: 16 }, (_, i) => `Term ${i + 1}`);

export const Sidebar: React.FC<SidebarProps> = ({
  notes,
  currentTerm,
  onSelectTerm,
  activeSubjectCode,
  activeNoteId,
  isZenMode,
  onToggleZenMode,
  isMobileOpen,
  onCloseMobile,
}) => {
  const navigate = useNavigate();
  const { isBookmarked } = useBookmarks();
  const { user } = useAuth();
  const isDevOrPrivileged = import.meta.env.DEV || user?.role === 'admin' || user?.role === 'moderator' || user?.is_special;
  const maxAllowedTerm = isDevOrPrivileged ? 16 : (user?.max_allowed_term ?? 16);
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedSubjects, setExpandedSubjects] = useState<Record<string, boolean>>({});

  // Auto-expand current active subject
  useEffect(() => {
    if (activeSubjectCode) {
      setExpandedSubjects((prev) => ({ ...prev, [activeSubjectCode]: true }));
    }
  }, [activeSubjectCode]);

  // Handle Escape key to close mobile drawer
  useEffect(() => {
    if (!isMobileOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onCloseMobile();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isMobileOpen, onCloseMobile]);

  // Filter notes by current term and search input
  const termNotes = useMemo(() => {
    return notes.filter((n) => n.term.toLowerCase() === currentTerm.toLowerCase());
  }, [notes, currentTerm]);

  // Group notes by subject
  const subjectsMap = useMemo(() => {
    const q = searchQuery.toLowerCase().trim();
    const map: Record<string, NoteIndexItem[]> = {};

    termNotes.forEach((n) => {
      const matchesSearch =
        !q ||
        n.topic_title.toLowerCase().includes(q) ||
        n.subject_code.toLowerCase().includes(q) ||
        n.tags.some((t) => t.toLowerCase().includes(q));

      if (matchesSearch) {
        if (!map[n.subject_code]) {
          map[n.subject_code] = [];
        }
        map[n.subject_code].push(n);
      }
    });

    return map;
  }, [termNotes, searchQuery]);

  const subjectCodes = Object.keys(subjectsMap).sort();

  const toggleSubject = (sub: string) => {
    setExpandedSubjects((prev) => ({
      ...prev,
      [sub]: prev[sub] !== undefined ? !prev[sub] : false,
    }));
  };

  const handleSelectNote = (note: NoteIndexItem) => {
    const termSlug = note.term.toLowerCase().replace(/\s+/g, '-');
    navigate(`/term/${termSlug}/${note.subject_code.toLowerCase()}/${note.note_id}`);
    onCloseMobile();
  };

  const sidebarContent = (
    <div className="flex flex-col h-full bg-[#09090b] text-zinc-300 select-none">
      {/* Top Header: Term Switcher & Zen Mode */}
      <div className="p-4 border-b border-white/[0.08] space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-[11px] font-semibold tracking-wider uppercase text-zinc-400 flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-zinc-400" />
            Curriculum Term
          </label>
          <div className="flex items-center gap-1">
            <button
              onClick={onToggleZenMode}
              title={isZenMode ? 'Expand sidebar' : 'Zen Mode (collapse sidebar)'}
              aria-label={isZenMode ? 'Expand navigation sidebar' : 'Zen mode (collapse sidebar)'}
              className="p-1.5 rounded-md text-zinc-400 hover:text-zinc-200 hover:bg-white/5 transition-colors hidden lg:flex"
            >
              <PanelLeftClose className="w-4 h-4" />
            </button>
            {isMobileOpen && (
              <button
                onClick={onCloseMobile}
                aria-label="Close course navigation drawer"
                className="p-1.5 rounded-md text-zinc-400 hover:text-zinc-200 hover:bg-white/5 transition-colors lg:hidden"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* Term Switcher Dropdown */}
        <div className="relative">
          <select
            value={currentTerm}
            onChange={(e) => onSelectTerm(e.target.value)}
            aria-label="Select curriculum term"
            className="w-full appearance-none bg-zinc-900/90 text-zinc-200 text-sm font-medium rounded-lg px-3 py-2 border border-white/10 hover:border-white/20 focus:outline-none focus:border-blue-500 transition-colors cursor-pointer"
          >
            {ALL_TERMS.map((t, idx) => {
              const termNum = idx + 1;
              const isLocked = termNum > maxAllowedTerm;
              return (
                <option
                  key={t}
                  value={t}
                  disabled={isLocked}
                  className={`bg-zinc-900 ${isLocked ? 'text-zinc-600' : 'text-zinc-200'}`}
                >
                  {t} {isLocked ? '🔒 (Locked)' : ''}
                </option>
              );
            })}
          </select>
          <ChevronDown className="w-4 h-4 text-zinc-400 absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>

        {/* Real-time Filter Input */}
        <div className="relative">
          <Search className="w-3.5 h-3.5 text-zinc-400 absolute left-3 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={`Filter ${currentTerm} notes...`}
            className="w-full bg-black/40 text-xs text-zinc-200 placeholder-zinc-500 rounded-md pl-8 pr-3 py-1.5 border border-white/[0.08] focus:outline-none focus:border-white/20 transition-colors"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-zinc-300 text-xs"
            >
              ×
            </button>
          )}
        </div>
      </div>

      {/* Accordion List of Subjects */}
      <div className="flex-1 overflow-y-auto p-3 space-y-1">
        {subjectCodes.length === 0 ? (
          <div className="py-8 text-center text-xs text-zinc-500">
            {termNotes.length === 0
              ? `No approved notes available for ${currentTerm}.`
              : 'No notes match your filter.'}
          </div>
        ) : (
          subjectCodes.map((code) => {
            const subjectNotes = subjectsMap[code];
            const isExpanded = expandedSubjects[code] ?? true;

            return (
              <div key={code} className="mb-2">
                {/* Subject Header Accordion Toggle */}
                <button
                  onClick={() => toggleSubject(code)}
                  className="w-full flex items-center justify-between px-2.5 py-1.5 rounded-md hover:bg-white/[0.04] text-xs font-semibold uppercase tracking-wider text-zinc-400 hover:text-zinc-200 transition-colors"
                >
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-blue-500/80" />
                    <span>{code}</span>
                    <span className="text-[10px] font-normal text-zinc-400 bg-white/5 px-1.5 py-0.2 rounded">
                      {subjectNotes.length}
                    </span>
                  </div>
                  {isExpanded ? (
                    <ChevronDown className="w-3.5 h-3.5 text-zinc-400" />
                  ) : (
                    <ChevronRight className="w-3.5 h-3.5 text-zinc-400" />
                  )}
                </button>

                {/* Subject Notes List */}
                {isExpanded && (
                  <div className="mt-1 space-y-0.5 pl-2">
                    {subjectNotes.map((note) => {
                      const isActive = note.note_id === activeNoteId;
                      const bookmarked = isBookmarked(note.note_id);

                      return (
                        <button
                          key={note.note_id}
                          onClick={() => handleSelectNote(note)}
                          className={`w-full group flex items-center justify-between text-left px-2.5 py-2 rounded-md text-xs transition-all ${isActive
                              ? 'border-l-2 border-blue-500 bg-white/[0.06] text-zinc-100 font-medium pl-2'
                              : 'border-l-2 border-transparent text-zinc-400 hover:text-zinc-200 hover:bg-white/[0.03]'
                            }`}
                        >
                          <div className="flex items-center gap-2 truncate pr-2">
                            <BookOpen
                              className={`w-3.5 h-3.5 shrink-0 ${isActive ? 'text-blue-400' : 'text-zinc-500 group-hover:text-zinc-400'
                                }`}
                            />
                            <span className="truncate">{note.topic_title}</span>
                          </div>

                          {bookmarked && (
                            <BookmarkIcon className="w-3 h-3 text-amber-400 fill-amber-400 shrink-0" />
                          )}
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {/* Footer Info */}
      <div className="p-3 border-t border-white/[0.08] text-[11px] text-zinc-400 flex items-center justify-between bg-black/20">
        <span>SST Study Platform</span>
        <span>v1.1</span>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Island Sidebar (w-80) */}
      <aside
        className={`shrink-0 sticky top-14 h-[calc(100vh-3.5rem)] border-r border-white/[0.08] transition-all duration-200 hidden lg:block ${isZenMode ? 'w-0 overflow-hidden border-r-0' : 'w-80'
          }`}
      >
        {sidebarContent}
      </aside>

      {/* Mobile Slide-over Drawer */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 z-50 lg:hidden"
          role="dialog"
          aria-modal="true"
          aria-label="Course curriculum navigation drawer"
        >
          {/* Backdrop */}
          <div
            onClick={onCloseMobile}
            aria-hidden="true"
            className="fixed inset-0 bg-black/80 backdrop-blur-sm transition-opacity"
          />
          {/* Drawer panel */}
          <div className="fixed inset-y-0 left-0 w-80 max-w-[85vw] shadow-2xl z-50">
            {sidebarContent}
          </div>
        </div>
      )}
    </>
  );
};
