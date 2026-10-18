import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X, BookOpen, ArrowRight, CornerDownLeft } from 'lucide-react';
import { NoteIndexItem } from '@/types/note';
import { useAuth } from '@/context/AuthContext';

interface SearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  notes: NoteIndexItem[];
}

export const SearchModal: React.FC<SearchModalProps> = ({
  isOpen,
  onClose,
  notes,
}) => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const maxAllowedTerm = user?.max_allowed_term ?? 16;

  useEffect(() => {
    if (isOpen) {
      setQuery('');
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  // Filter notes by allowed term and search query
  const filtered = notes
    .filter((n) => {
      const match = n.term.match(/\d+/);
      const termNum = match ? parseInt(match[0], 10) : 1;
      return termNum <= maxAllowedTerm;
    })
    .filter((n) => {
      if (!query.trim()) return true;
      const q = query.toLowerCase();
      return (
        n.topic_title.toLowerCase().includes(q) ||
        n.subject_code.toLowerCase().includes(q) ||
        n.summary.toLowerCase().includes(q) ||
        n.tags.some((t) => t.toLowerCase().includes(q)) ||
        n.term.toLowerCase().includes(q)
      );
    })
    .slice(0, 10); // Top 10 matches for fast keyboard navigation

  const handleSelectNote = (note: NoteIndexItem) => {
    const termSlug = note.term.toLowerCase().replace(/\s+/g, '-');
    navigate(`/term/${termSlug}/${note.subject_code.toLowerCase()}/${note.note_id}`);
    onClose();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev < filtered.length - 1 ? prev + 1 : prev));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => (prev > 0 ? prev - 1 : 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (filtered[selectedIndex]) {
        handleSelectNote(filtered[selectedIndex]);
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-20 px-4">
      {/* Frosted Backdrop */}
      <div
        className="fixed inset-0 bg-black/40 dark:bg-black/75 backdrop-blur-md transition-opacity"
        onClick={onClose}
      />

      {/* Command Palette Card */}
      <div
        className="relative w-full max-w-xl rounded-xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0d0d10] shadow-2xl overflow-hidden z-10 flex flex-col"
        onKeyDown={handleKeyDown}
      >
        {/* Search Input Bar */}
        <div className="flex items-center px-4 py-3.5 border-b border-zinc-200 dark:border-white/[0.08] bg-zinc-50/80 dark:bg-black/40">
          <Search className="w-4 h-4 text-zinc-400 mr-3 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelectedIndex(0);
            }}
            placeholder="Search all notes, subjects, or tags... (Type to filter)"
            className="w-full bg-transparent text-sm text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 dark:placeholder-zinc-500 focus:outline-none"
          />
          <button
            onClick={onClose}
            className="p-1 rounded text-zinc-400 hover:text-zinc-700 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/5 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Results List */}
        <div className="max-h-96 overflow-y-auto p-2 space-y-1">
          {filtered.length === 0 ? (
            <div className="py-12 text-center text-sm text-zinc-500">
              No matching notes found for "{query}".
            </div>
          ) : (
            filtered.map((note, idx) => {
              const isSelected = idx === selectedIndex;
              return (
                <div
                  key={note.note_id}
                  onClick={() => handleSelectNote(note)}
                  onMouseEnter={() => setSelectedIndex(idx)}
                  className={`group flex items-center justify-between p-3 rounded-lg cursor-pointer transition-colors ${
                    isSelected ? 'bg-blue-50 dark:bg-white/[0.08] text-blue-900 dark:text-white' : 'text-zinc-600 dark:text-zinc-400 hover:bg-zinc-50 dark:hover:bg-white/[0.03]'
                  }`}
                >
                  <div className="flex items-start gap-3 truncate pr-4">
                    <BookOpen
                      className={`w-4 h-4 mt-0.5 shrink-0 ${
                        isSelected ? 'text-blue-600 dark:text-blue-400' : 'text-zinc-400 dark:text-zinc-500'
                      }`}
                    />
                    <div className="flex flex-col truncate">
                      <span className="text-sm font-medium text-zinc-900 dark:text-zinc-200 group-hover:text-blue-600 dark:group-hover:text-white truncate">
                        {note.topic_title}
                      </span>
                      <span className="text-xs text-zinc-500 dark:text-zinc-400 truncate mt-0.5">
                        {note.summary}
                      </span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <span className="px-2 py-0.5 text-[10px] font-mono rounded bg-zinc-100 dark:bg-white/5 border border-zinc-200 dark:border-white/10 text-zinc-600 dark:text-zinc-400">
                      {note.subject_code}
                    </span>
                    <span className="px-2 py-0.5 text-[10px] font-mono rounded bg-zinc-100 dark:bg-white/5 border border-zinc-200 dark:border-white/10 text-zinc-600 dark:text-zinc-400">
                      {note.term}
                    </span>
                    {isSelected && (
                      <CornerDownLeft className="w-3.5 h-3.5 text-blue-600 dark:text-zinc-400 ml-1" />
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Footer shortcuts */}
        <div className="px-4 py-2 border-t border-zinc-200 dark:border-white/[0.08] bg-zinc-50 dark:bg-black/30 flex items-center justify-between text-[11px] text-zinc-500 dark:text-zinc-400 select-none">
          <div className="flex items-center gap-3">
            <span>
              <kbd className="px-1 py-0.5 rounded bg-white dark:bg-white/5 border border-zinc-200 dark:border-white/10 font-mono text-[10px] shadow-sm dark:shadow-none">
                ↑↓
              </kbd>{' '}
              Navigate
            </span>
            <span>
              <kbd className="px-1 py-0.5 rounded bg-white dark:bg-white/5 border border-zinc-200 dark:border-white/10 font-mono text-[10px] shadow-sm dark:shadow-none">
                Enter
              </kbd>{' '}
              Open
            </span>
            <span>
              <kbd className="px-1 py-0.5 rounded bg-white dark:bg-white/5 border border-zinc-200 dark:border-white/10 font-mono text-[10px] shadow-sm dark:shadow-none">
                Esc
              </kbd>{' '}
              Close
            </span>
          </div>
          <span>SST Study Platform</span>
        </div>
      </div>
    </div>
  );
};
