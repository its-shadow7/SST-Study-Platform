import React, { useState, useEffect, useRef, useCallback } from 'react';
import { api } from '@/services/apiClient';
import { useAuth } from '@/context/AuthContext';
import { ScratchpadData, ScratchpadSaveStatus } from '@/types/scratchpad';
import { MarkdownViewer } from '@/components/MarkdownViewer';
import {
  Edit3,
  Eye,
  Check,
  Loader2,
  AlertCircle,
  FileText,
  LogIn,
  Clock
} from 'lucide-react';

interface ScratchpadProps {
  noteId: string;
  onHasNotesChange?: (hasNotes: boolean) => void;
}

export const Scratchpad: React.FC<ScratchpadProps> = ({ noteId, onHasNotesChange }) => {
  const { user } = useAuth();
  const [content, setContent] = useState<string>('');
  const [saveStatus, setSaveStatus] = useState<ScratchpadSaveStatus>('saved');
  const [mode, setMode] = useState<'write' | 'preview'>('write');
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [lastSavedAt, setLastSavedAt] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // References for bulletproof debouncing & zero-data-loss race condition prevention
  const pendingSaveRef = useRef<{ noteId: string; content: string } | null>(null);
  const debounceTimerRef = useRef<NodeJS.Timeout | null>(null);
  const currentNoteIdRef = useRef<string>(noteId);
  const activeFetchIdRef = useRef<number>(0);

  // Save worker executing the atomic PUT API call
  const executeSave = useCallback(async (targetNoteId: string, textToSave: string) => {
    if (!user) return;
    setSaveStatus('saving');
    setErrorMessage(null);

    try {
      const data = await api.put<ScratchpadData>(
        `/api/notes/${targetNoteId}/scratchpad`,
        { content: textToSave }
      );

      // Only update local UI state if the student is still viewing this note
      if (currentNoteIdRef.current === targetNoteId) {
        if (pendingSaveRef.current?.content === textToSave) {
          pendingSaveRef.current = null;
        }
        setSaveStatus('saved');
        const formattedTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        setLastSavedAt(formattedTime);
        onHasNotesChange?.(textToSave.trim().length > 0);
      }
    } catch (err: any) {
      console.error(`Failed to save scratchpad for ${targetNoteId}:`, err);
      if (currentNoteIdRef.current === targetNoteId) {
        setSaveStatus('error');
        setErrorMessage(err?.message || 'Failed to auto-save notes');
      }
    }
  }, [user, onHasNotesChange]);

  // Handle noteId switching & initial load with race condition cleanup
  useEffect(() => {
    const prevNoteId = currentNoteIdRef.current;
    currentNoteIdRef.current = noteId;

    // Critical Cleanup Rule:
    // If switching note_id while a debounced save is still pending for the previous note,
    // immediately flush/fire the pending PUT request before loading the new note's scratchpad!
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
      debounceTimerRef.current = null;
    }

    if (pendingSaveRef.current && pendingSaveRef.current.noteId !== noteId) {
      const toFlush = pendingSaveRef.current;
      pendingSaveRef.current = null;
      api.put<ScratchpadData>(
        `/api/notes/${toFlush.noteId}/scratchpad`,
        { content: toFlush.content }
      ).catch((err) => {
        console.error(`[RaceGuard] Error flushing pending auto-save for ${toFlush.noteId}:`, err);
      });
    }

    if (!user) {
      setIsLoading(false);
      setContent('');
      setSaveStatus('saved');
      return;
    }

    const fetchId = ++activeFetchIdRef.current;
    setIsLoading(true);
    setErrorMessage(null);
    setSaveStatus('saved');

    api.get<ScratchpadData>(`/api/notes/${noteId}/scratchpad`)
      .then((data) => {
        // Race-condition guard: verify this response corresponds to the active lecture
        if (activeFetchIdRef.current === fetchId) {
          const loadedContent = data?.content || '';
          setContent(loadedContent);
          setIsLoading(false);
          setSaveStatus('saved');
          if (data?.updated_at) {
            setLastSavedAt(new Date(data.updated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }));
          } else {
            setLastSavedAt(null);
          }
          onHasNotesChange?.(loadedContent.trim().length > 0);
        }
      })
      .catch((err) => {
        if (activeFetchIdRef.current === fetchId) {
          console.error(`Failed to load scratchpad for ${noteId}:`, err);
          setContent('');
          setIsLoading(false);
          setSaveStatus('error');
          setErrorMessage('Failed to load saved notes');
        }
      });

    // Cleanup on unmount: flush any pending save
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
        debounceTimerRef.current = null;
      }
      if (pendingSaveRef.current) {
        const toFlush = pendingSaveRef.current;
        pendingSaveRef.current = null;
        api.put<ScratchpadData>(
          `/api/notes/${toFlush.noteId}/scratchpad`,
          { content: toFlush.content }
        ).catch((err) => {
          console.error(`[UnmountGuard] Error flushing scratchpad save for ${toFlush.noteId}:`, err);
        });
      }
    };
  }, [noteId, user, executeSave, onHasNotesChange]);

  // Handle typing inside the textarea with 1000ms debounce
  const handleContentChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newContent = e.target.value;
    if (newContent.length > 30000) return; // Strict 30k char ceiling

    setContent(newContent);
    setSaveStatus('unsaved');
    pendingSaveRef.current = { noteId, content: newContent };

    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }

    debounceTimerRef.current = setTimeout(() => {
      executeSave(noteId, newContent);
    }, 1000);
  };

  // If user is not logged in
  if (!user) {
    return (
      <div className="flex flex-col items-center justify-center p-6 text-center h-[calc(100vh-10rem)] space-y-4">
        <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-600 dark:text-blue-400">
          <FileText className="w-6 h-6" />
        </div>
        <div className="space-y-1">
          <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Personal Study Scratchpad</h3>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 max-w-[240px] leading-relaxed">
            Sign in with your SST Google account to write private notes and paste AI explanations alongside lectures.
          </p>
        </div>
        <div className="pt-2">
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-zinc-100 dark:bg-white/5 border border-zinc-200 dark:border-white/10 text-xs text-zinc-700 dark:text-zinc-300">
            <LogIn className="w-3.5 h-3.5 text-zinc-500 dark:text-zinc-400" />
            <span>Sign in via top navigation</span>
          </span>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-[calc(100vh-8.5rem)] select-text">
      {/* 1. Header Toolbar: Mode Toggle (Write / Preview) */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-zinc-200 dark:border-white/[0.08] bg-zinc-50 dark:bg-black/20 shrink-0">
        <div className="flex items-center p-0.5 rounded-md bg-zinc-200/60 dark:bg-white/[0.04] border border-zinc-300/80 dark:border-white/[0.08] text-xs">
          <button
            onClick={() => setMode('write')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded transition-all ${
              mode === 'write'
                ? 'bg-white dark:bg-white/10 text-zinc-900 dark:text-zinc-100 font-medium shadow-sm'
                : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
            }`}
          >
            <Edit3 className="w-3 h-3" />
            <span>Write</span>
          </button>
          <button
            onClick={() => setMode('preview')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded transition-all ${
              mode === 'preview'
                ? 'bg-white dark:bg-white/10 text-zinc-900 dark:text-zinc-100 font-medium shadow-sm'
                : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
            }`}
          >
            <Eye className="w-3 h-3" />
            <span>Preview</span>
          </button>
        </div>

        <span className="text-[11px] font-mono text-zinc-500 dark:text-zinc-400">
          Markdown & KaTeX
        </span>
      </div>

      {/* 2. Main Editor / Preview Body */}
      <div className="flex-1 overflow-hidden relative">
        {isLoading ? (
          <div className="flex items-center justify-center h-full space-x-2 text-zinc-500 dark:text-zinc-400 text-xs">
            <Loader2 className="w-4 h-4 animate-spin text-blue-500 dark:text-blue-400" />
            <span>Loading your notes...</span>
          </div>
        ) : mode === 'write' ? (
          <textarea
            value={content}
            onChange={handleContentChange}
            placeholder="Paste or write notes, equations ($E = mc^2$), code snippets, or explanations copied from Gemini/ChatGPT..."
            className="w-full h-full bg-transparent resize-none outline-none font-mono text-xs text-zinc-800 dark:text-zinc-300 leading-relaxed placeholder:text-zinc-400 dark:placeholder:text-zinc-600 focus:ring-0 p-4 overflow-y-auto"
            spellCheck={false}
          />
        ) : (
          <div className="p-4 h-full overflow-y-auto">
            {content.trim().length > 0 ? (
              <div className="prose dark:prose-invert max-w-none text-xs">
                <MarkdownViewer content={content} />
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-full text-center p-6 space-y-2 text-zinc-500 dark:text-zinc-400">
                <FileText className="w-8 h-8 opacity-40 text-zinc-400" />
                <p className="text-xs">No personal notes yet for this lecture.</p>
                <button
                  onClick={() => setMode('write')}
                  className="text-xs text-blue-600 dark:text-blue-400 hover:underline pt-1"
                >
                  Switch to Write mode to add notes
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* 3. Bottom Status Bar */}
      <div className="px-3 py-2 border-t border-zinc-200 dark:border-white/[0.08] bg-zinc-50 dark:bg-black/40 flex items-center justify-between text-[11px] text-zinc-500 dark:text-zinc-400 shrink-0 select-none">
        <div className="flex items-center gap-1.5">
          {saveStatus === 'saving' && (
            <>
              <Loader2 className="w-3 h-3 animate-spin text-blue-600 dark:text-blue-400" />
              <span className="text-blue-600 dark:text-blue-400">Saving...</span>
            </>
          )}
          {saveStatus === 'saved' && (
            <>
              <Check className="w-3 h-3 text-emerald-600 dark:text-emerald-400" />
              <span className="text-zinc-600 dark:text-zinc-400">
                {lastSavedAt ? `Saved ${lastSavedAt}` : 'Saved'}
              </span>
            </>
          )}
          {saveStatus === 'unsaved' && (
            <>
              <Clock className="w-3 h-3 text-amber-600 dark:text-amber-400/90" />
              <span className="text-amber-600 dark:text-amber-400/90">Unsaved changes</span>
            </>
          )}
          {saveStatus === 'error' && (
            <>
              <AlertCircle className="w-3 h-3 text-red-500 dark:text-red-400" />
              <span className="text-red-500 dark:text-red-400">{errorMessage || 'Save error'}</span>
            </>
          )}
        </div>

        <div className="font-mono text-zinc-500 dark:text-zinc-400">
          <span>{content.length.toLocaleString()}</span>
          <span className="opacity-50"> / 30,000</span>
        </div>
      </div>
    </div>
  );
};
