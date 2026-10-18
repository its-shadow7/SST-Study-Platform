import React, { useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { NoteIndexItem } from '@/types/note';
import { useBookmarks } from '@/context/BookmarkContext';
import { Bookmark, Trash2, ArrowUpRight, BookOpen } from 'lucide-react';

interface BookmarksPageProps {
  notesIndex: NoteIndexItem[];
}

export const BookmarksPage: React.FC<BookmarksPageProps> = ({ notesIndex }) => {
  const navigate = useNavigate();
  const { bookmarks, toggleBookmark } = useBookmarks();

  // Join bookmarks with notes index
  const bookmarkedNotes = useMemo(() => {
    return bookmarks.map((b) => {
      const noteMeta = notesIndex.find((n) => n.note_id === b.note_id);
      return {
        ...b,
        note: noteMeta || null,
      };
    });
  }, [bookmarks, notesIndex]);

  const handleOpenNote = (noteId: string, noteMeta: NoteIndexItem | null) => {
    if (noteMeta) {
      const termSlug = noteMeta.term.toLowerCase().replace(/\s+/g, '-');
      navigate(`/term/${termSlug}/${noteMeta.subject_code.toLowerCase()}/${noteId}`);
    } else {
      navigate(`/read/${noteId}`);
    }
  };

  return (
    <div className="min-h-[calc(100vh-3.5rem)] bg-slate-50 dark:bg-[#09090b] text-zinc-800 dark:text-zinc-200 py-10 px-4 sm:px-8 max-w-5xl mx-auto transition-colors">
      {/* Header */}
      <div className="mb-8 border-b border-zinc-200 dark:border-white/[0.08] pb-6 flex items-center justify-between">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-amber-500/20 bg-amber-500/10 text-xs font-medium text-amber-600 dark:text-amber-400 mb-2">
            <Bookmark className="w-3.5 h-3.5 fill-amber-500 dark:fill-amber-400" />
            <span>Saved Notes</span>
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
            Bookmarked Notes
          </h1>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
            Fast access to your bookmarked lectures, summaries, and exam references.
          </p>
        </div>

        <span className="text-xs font-mono text-zinc-600 dark:text-zinc-400 bg-zinc-100 dark:bg-white/5 px-2.5 py-1 rounded-md border border-zinc-200 dark:border-white/10 shadow-sm dark:shadow-none">
          {bookmarkedNotes.length} saved
        </span>
      </div>

      {/* Bookmarks List or Table */}
      {bookmarkedNotes.length === 0 ? (
        <div className="py-20 text-center border border-zinc-200 dark:border-white/5 rounded-2xl bg-white dark:bg-white/[0.01] shadow-sm dark:shadow-none p-8 space-y-4">
          <Bookmark className="w-10 h-10 text-zinc-400 dark:text-zinc-600 mx-auto" />
          <h3 className="text-lg font-semibold text-zinc-800 dark:text-zinc-300">No Bookmarks Saved Yet</h3>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 max-w-sm mx-auto">
            Click the bookmark icon on any note while reading to add it to your personal study collection.
          </p>
          <button
            onClick={() => navigate('/terms')}
            className="mt-2 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-medium text-white transition-colors shadow-sm"
          >
            Browse Terms
          </button>
        </div>
      ) : (
        <div className="border border-zinc-200 dark:border-white/10 rounded-xl overflow-hidden bg-white dark:bg-white/[0.01] shadow-sm dark:shadow-none">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-zinc-200 dark:border-white/10 bg-zinc-50 dark:bg-white/[0.02] text-zinc-500 dark:text-zinc-400 uppercase tracking-wider font-mono">
                  <th className="py-3 px-4 font-semibold">Subject</th>
                  <th className="py-3 px-4 font-semibold">Topic Title</th>
                  <th className="py-3 px-4 font-semibold hidden md:table-cell">Term</th>
                  <th className="py-3 px-4 font-semibold hidden sm:table-cell">Saved Date</th>
                  <th className="py-3 px-4 font-semibold text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-100 dark:divide-white/[0.05]">
                {bookmarkedNotes.map((item) => (
                  <tr
                    key={item.note_id}
                    className="hover:bg-zinc-50 dark:hover:bg-white/[0.03] transition-colors group"
                  >
                    <td className="py-3.5 px-4 font-mono font-bold text-blue-600 dark:text-blue-400">
                      {item.note?.subject_code || 'SST'}
                    </td>
                    <td className="py-3.5 px-4 font-medium text-zinc-800 dark:text-zinc-200">
                      <button
                        onClick={() => handleOpenNote(item.note_id, item.note)}
                        className="text-left hover:text-blue-600 dark:hover:text-blue-400 transition-colors flex items-center gap-1.5"
                      >
                        <span>{item.note?.topic_title || item.note_id}</span>
                        <ArrowUpRight className="w-3.5 h-3.5 opacity-0 group-hover:opacity-100 transition-opacity text-blue-600 dark:text-blue-400" />
                      </button>
                    </td>
                    <td className="py-3.5 px-4 text-zinc-500 dark:text-zinc-400 font-mono hidden md:table-cell">
                      {item.note?.term || '—'}
                    </td>
                    <td className="py-3.5 px-4 text-zinc-500 font-mono hidden sm:table-cell">
                      {item.created_at ? new Date(item.created_at).toLocaleDateString() : '—'}
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <button
                        onClick={() => toggleBookmark(item.note_id, item.note?.topic_title)}
                        className="p-1.5 rounded text-zinc-400 hover:text-rose-600 dark:hover:text-rose-400 hover:bg-rose-50 dark:hover:bg-rose-500/10 transition-colors"
                        title="Remove bookmark"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
