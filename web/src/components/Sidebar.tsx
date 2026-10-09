import React, { useState } from 'react';
import { NoteIndexItem } from '../types/note';
import { useBookmarks } from '../context/BookmarkContext';
import { Bookmark, BookOpen, Layers } from 'lucide-react';

interface SidebarProps {
  notes: NoteIndexItem[];
  selectedNoteId: string | null;
  onSelectNote: (noteId: string) => void;
  showBookmarksOnly: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({
  notes,
  selectedNoteId,
  onSelectNote,
  showBookmarksOnly
}) => {
  const [selectedSubject, setSelectedSubject] = useState<string>('ALL');
  const { isBookmarked } = useBookmarks();

  // Extract distinct subjects
  const subjects = ['ALL', ...Array.from(new Set(notes.map((n) => n.subject_code)))];

  // Filter notes
  const filteredNotes = notes.filter((n) => {
    if (selectedSubject !== 'ALL' && n.subject_code !== selectedSubject) {
      return false;
    }
    if (showBookmarksOnly && !isBookmarked(n.note_id)) {
      return false;
    }
    return true;
  });

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
            Course Catalogue
          </span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
            {filteredNotes.length} notes
          </span>
        </div>

        {/* Subject filter tabs */}
        <div className="subject-filter-tabs">
          {subjects.map((sub) => (
            <button
              key={sub}
              className={`filter-tab ${selectedSubject === sub ? 'active' : ''}`}
              onClick={() => setSelectedSubject(sub)}
            >
              {sub}
            </button>
          ))}
        </div>
      </div>

      <div className="notes-list">
        {filteredNotes.length === 0 ? (
          <div style={{ padding: '2rem 1rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
            {showBookmarksOnly
              ? 'No bookmarked notes found in this subject.'
              : 'No notes match the current filters.'}
          </div>
        ) : (
          filteredNotes.map((note) => {
            const active = note.note_id === selectedNoteId;
            const bookmarked = isBookmarked(note.note_id);

            return (
              <div
                key={note.note_id}
                className={`note-card ${active ? 'active' : ''}`}
                onClick={() => onSelectNote(note.note_id)}
              >
                <div className="note-card-meta">
                  <span className="subject-tag">{note.subject_code}</span>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem' }}>
                    <span>{note.term}</span>
                    {bookmarked && <Bookmark size={13} fill="var(--accent-amber)" color="var(--accent-amber)" />}
                  </div>
                </div>
                <h4 className="note-card-title">{note.topic_title}</h4>
                <p className="note-card-desc">{note.summary}</p>
              </div>
            );
          })
        )}
      </div>
    </aside>
  );
};
