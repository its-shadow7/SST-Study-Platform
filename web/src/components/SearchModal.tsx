import React, { useState, useEffect, useRef } from 'react';
import { Search, X, BookOpen } from 'lucide-react';
import { NoteIndexItem } from '../types/note';

interface SearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  notes: NoteIndexItem[];
  onSelectNote: (noteId: string) => void;
}

export const SearchModal: React.FC<SearchModalProps> = ({
  isOpen,
  onClose,
  notes,
  onSelectNote
}) => {
  const [query, setQuery] = useState('');
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setQuery('');
      setSelectedIndex(0);
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [isOpen]);

  // Filter notes by query
  const filtered = notes.filter((n) => {
    if (!query.trim()) return true;
    const q = query.toLowerCase();
    return (
      n.topic_title.toLowerCase().includes(q) ||
      n.subject_code.toLowerCase().includes(q) ||
      n.summary.toLowerCase().includes(q) ||
      n.tags.some((t) => t.toLowerCase().includes(q)) ||
      n.term.toLowerCase().includes(q)
    );
  });

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
        onSelectNote(filtered[selectedIndex].note_id);
        onClose();
      }
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="search-modal"
        onClick={(e) => e.stopPropagation()}
        onKeyDown={handleKeyDown}
      >
        <div className="search-input-wrap">
          <Search size={20} color="var(--primary)" />
          <input
            ref={inputRef}
            className="search-input"
            type="text"
            placeholder="Search notes by title, subject, tags, or summary..."
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setSelectedIndex(0);
            }}
          />
          <button
            onClick={onClose}
            style={{
              background: 'transparent',
              border: 'none',
              color: 'var(--text-muted)',
              cursor: 'pointer'
            }}
          >
            <X size={18} />
          </button>
        </div>

        <div className="search-results-list">
          {filtered.length === 0 ? (
            <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)' }}>
              No notes found matching "{query}".
            </div>
          ) : (
            filtered.map((note, idx) => {
              const isHighlight = idx === selectedIndex;
              return (
                <div
                  key={note.note_id}
                  className={`search-result-item ${isHighlight ? 'highlighted' : ''}`}
                  onClick={() => {
                    onSelectNote(note.note_id);
                    onClose();
                  }}
                  onMouseEnter={() => setSelectedIndex(idx)}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
                    <span className="subject-tag">{note.subject_code}</span>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>{note.term}</span>
                  </div>
                  <div style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                    {note.topic_title}
                  </div>
                  <div
                    style={{
                      fontSize: '0.85rem',
                      color: 'var(--text-secondary)',
                      marginTop: '0.25rem',
                      lineHeight: 1.4
                    }}
                  >
                    {note.summary}
                  </div>
                  <div style={{ display: 'flex', gap: '0.35rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
                    {note.tags.map((tag) => (
                      <span
                        key={tag}
                        style={{
                          fontSize: '0.7rem',
                          background: 'var(--bg-app)',
                          border: '1px solid var(--border)',
                          borderRadius: '4px',
                          padding: '0.1rem 0.35rem',
                          color: 'var(--text-muted)'
                        }}
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
