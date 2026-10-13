import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { NoteIndexItem } from '@/types/note';
import { fetchNoteById } from '@/services/notesService';
import { useAuth } from '@/context/AuthContext';
import { Loader2 } from 'lucide-react';
import { toast } from 'sonner';

interface NoteRedirectorProps {
  notesIndex: NoteIndexItem[];
  indexLoading: boolean;
}

export const NoteRedirector: React.FC<NoteRedirectorProps> = ({
  notesIndex,
  indexLoading,
}) => {
  const { noteId } = useParams<{ noteId: string }>();
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();
  const [, setResolving] = useState(false);

  useEffect(() => {
    if (!noteId) {
      navigate('/terms', { replace: true });
      return;
    }

    const normalizedId = noteId.replace(/-l(\d)$/i, '-l0$1');

    // 1. Try to match from loaded notesIndex
    const matched = notesIndex.find((n) => n.note_id === noteId || n.note_id === normalizedId);
    if (matched) {
      const termSlug = `term-${matched.term.replace(/\D/g, '') || '1'}`;
      const subjectCode = matched.subject_code.toLowerCase();
      const targetUrl = `/term/${termSlug}/${subjectCode}/${matched.note_id}${location.search}${location.hash}`;
      navigate(targetUrl, { replace: true });
      return;
    }

    // 2. If notesIndex is still loading, wait
    if (indexLoading) {
      return;
    }

    // 3. Fallback: try fetching note directly by ID
    let isCancelled = false;
    setResolving(true);
    fetchNoteById(normalizedId)
      .then((note) => {
        if (isCancelled) return;
        const termSlug = `term-${note.term.replace(/\D/g, '') || '1'}`;
        const subjectCode = note.subject_code.toLowerCase();
        const targetUrl = `/term/${termSlug}/${subjectCode}/${note.note_id}${location.search}${location.hash}`;
        navigate(targetUrl, { replace: true });
      })
      .catch(() => {
        if (isCancelled) return;
        toast.error(`Could not locate note '${noteId}'`);
        navigate('/terms', { replace: true });
      })
      .finally(() => {
        if (!isCancelled) setResolving(false);
      });

    return () => {
      isCancelled = true;
    };
  }, [noteId, notesIndex, indexLoading, navigate, location.search, location.hash, user]);

  return (
    <div className="min-h-[50vh] flex flex-col items-center justify-center space-y-3 text-zinc-400">
      <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
      <p className="text-xs font-mono">Redirecting to lecture note...</p>
    </div>
  );
};
