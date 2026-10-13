import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { Note, NoteIndexItem } from '@/types/note';
import { fetchNoteById } from '@/services/notesService';
import { useBookmarks } from '@/context/BookmarkContext';
import { useAuth } from '@/context/AuthContext';
import { Sidebar } from '@/components/Sidebar';
import { TableOfContents, MobileTableOfContents } from '@/components/TableOfContents';
import { MarkdownViewer } from '@/components/MarkdownViewer';
import { NoteSkeleton } from '@/components/NoteSkeleton';
import { CommentSection } from '@/components/CommentSection';
import { QuizSection } from '@/components/QuizSection';
import {
  Bookmark as BookmarkIcon,
  CheckCircle,
  Share2,
  Calendar,
  Tag,
  BookOpen,
  PanelLeftOpen,
  Check,
  Lock,
  AlertTriangle,
  RotateCcw,
  HelpCircle,
  ArrowRight
} from 'lucide-react';
import { toast } from 'sonner';

interface ReaderPageProps {
  notesIndex: NoteIndexItem[];
  isMobileOpen: boolean;
  onCloseMobile: () => void;
}

export const ReaderPage: React.FC<ReaderPageProps> = ({
  notesIndex,
  isMobileOpen,
  onCloseMobile,
}) => {
  const { termId, subjectCode, noteId } = useParams<{
    termId: string;
    subjectCode: string;
    noteId: string;
  }>();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();
  const tabParam = searchParams.get('tab');
  const activeTab: 'notes' | 'quiz' = tabParam === 'quiz' ? 'quiz' : 'notes';

  const handleTabChange = (tab: 'notes' | 'quiz') => {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      if (tab === 'notes') {
        next.delete('tab');
      } else {
        next.set('tab', 'quiz');
      }
      return next;
    });
  };

  const [currentNote, setCurrentNote] = useState<Note | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [isZenMode, setIsZenMode] = useState<boolean>(false);
  const [linkCopied, setLinkCopied] = useState<boolean>(false);

  const { isBookmarked, toggleBookmark } = useBookmarks();
  const { user } = useAuth();

  const isDevOrPrivileged = import.meta.env.DEV || user?.role === 'admin' || user?.role === 'moderator' || user?.is_special;
  const maxAllowedTerm = isDevOrPrivileged ? 16 : (user?.max_allowed_term ?? 16);
  const requestedTermNum = parseInt(termId?.replace(/\D/g, '') || '0', 10);
  const isTermLocked = requestedTermNum > 0 && requestedTermNum > maxAllowedTerm;

  // Normalize term format from URL (defaults to student's active term)
  const currentTermFormatted = termId
    ? termId
      .split('-')
      .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
      .join(' ')
    : user?.active_term
      ? `Term ${user.active_term}`
      : 'Term 1';

  // Handle Term change from Sidebar
  const handleSelectTerm = (selectedTerm: string) => {
    const termNum = parseInt(selectedTerm.replace(/\D/g, '') || '0', 10);
    if (termNum > maxAllowedTerm) {
      toast.error(`Term ${termNum} is locked for your academic year.`);
      return;
    }

    const slug = selectedTerm.toLowerCase().replace(/\s+/g, '-');
    const firstNoteInTerm = notesIndex.find(
      (n) => n.term.toLowerCase() === selectedTerm.toLowerCase()
    );

    if (firstNoteInTerm) {
      navigate(
        `/term/${slug}/${firstNoteInTerm.subject_code.toLowerCase()}/${firstNoteInTerm.note_id}`
      );
    } else {
      navigate(`/term/${slug}`);
    }
  };

  // Auto-resolve valid note if noteId is missing or literally 'index'
  useEffect(() => {
    if (isTermLocked) {
      setLoading(false);
      return;
    }

    if (!noteId || noteId === 'index') {
      if (notesIndex.length === 0) {
        // Wait for notesIndex to arrive
        return;
      }
      const slug = currentTermFormatted.toLowerCase().replace(/\s+/g, '-');
      const firstNoteInTerm = notesIndex.find(
        (n) => n.term.toLowerCase() === currentTermFormatted.toLowerCase()
      );

      if (firstNoteInTerm) {
        navigate(
          `/term/${slug}/${firstNoteInTerm.subject_code.toLowerCase()}/${firstNoteInTerm.note_id}`,
          { replace: true }
        );
      } else {
        // Term has no notes yet
        setCurrentNote(null);
        setLoading(false);
      }
    }
  }, [noteId, notesIndex, currentTermFormatted, navigate, isTermLocked]);

  const loadNote = (id: string) => {
    setLoading(true);
    setLoadError(null);
    fetchNoteById(id)
      .then((data) => {
        setCurrentNote(data);
        setLoadError(null);
        setLoading(false);
      })
      .catch((err) => {
        console.error(`Failed to load note ${id}:`, err);
        setCurrentNote(null);
        setLoadError('Failed to load lecture note. Please check your network connection.');
        setLoading(false);
        toast.error(`Could not load note: ${id}`);
      });
  };

  // Fetch the active note
  useEffect(() => {
    if (!noteId || noteId === 'index' || isTermLocked) return;
    const normalizedId = noteId.replace(/-l(\d)$/i, '-l0$1');
    if (normalizedId !== noteId) {
      navigate(
        `/term/${termId}/${subjectCode}/${normalizedId}${window.location.search}${window.location.hash}`,
        { replace: true }
      );
      return;
    }
    loadNote(noteId);
  }, [noteId, isTermLocked, termId, subjectCode, navigate]);

  const bookmarked = noteId ? isBookmarked(noteId) : false;

  const handleCopyLink = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      setLinkCopied(true);
      toast.success('Note URL copied to clipboard');
      setTimeout(() => setLinkCopied(false), 2000);
    } catch {
      toast.error('Failed to copy link');
    }
  };

  return (
    <div className="flex w-full min-h-[calc(100vh-3.5rem)] bg-[#09090b] text-zinc-200">
      {/* 1. Left Island: Navigation (w-80) */}
      <Sidebar
        notes={notesIndex}
        currentTerm={currentTermFormatted}
        onSelectTerm={handleSelectTerm}
        activeSubjectCode={subjectCode?.toUpperCase()}
        activeNoteId={noteId}
        isZenMode={isZenMode}
        onToggleZenMode={() => setIsZenMode((prev) => !prev)}
        isMobileOpen={isMobileOpen}
        onCloseMobile={onCloseMobile}
      />

      {/* 2. Center Island: Reading Workspace */}
      <main className="flex-1 min-w-0 flex flex-col items-center px-4 sm:px-8 py-8 overflow-y-auto">
        {/* Zen Mode un-collapse button (when collapsed on desktop) */}
        {isZenMode && (
          <button
            onClick={() => setIsZenMode(false)}
            className="self-start mb-4 flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 text-xs text-zinc-300 transition-colors"
            title="Expand Navigation Sidebar"
          >
            <PanelLeftOpen className="w-4 h-4 text-zinc-400" />
            <span>Show Navigation</span>
          </button>
        )}

        <div className="w-full max-w-reader">
          {isTermLocked ? (
            <div className="py-24 text-center space-y-4">
              <div className="w-14 h-14 rounded-2xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center mx-auto text-amber-400 shadow-inner">
                <Lock className="w-7 h-7" />
              </div>
              <h2 className="text-2xl font-bold text-zinc-100">
                Access Restricted: {currentTermFormatted}
              </h2>
              <p className="text-sm text-zinc-400 max-w-md mx-auto leading-relaxed">
                This term is outside your current academic year (Year {user?.year_of_study || 1}
                {user?.batch_year ? `, Batch '${String(user.batch_year).slice(2)}` : ''}).
                You can only access terms in your current and previous years (up to <span className="text-zinc-200 font-semibold">Term {maxAllowedTerm}</span>).
              </p>
              <div className="pt-2">
                <button
                  onClick={() => navigate('/terms')}
                  className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white transition-colors shadow-lg shadow-blue-500/20"
                >
                  Return to Allowed Terms
                </button>
              </div>
            </div>
          ) : loading ? (
            <NoteSkeleton />
          ) : loadError ? (
            <div className="py-24 text-center space-y-4">
              <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center mx-auto text-rose-400">
                <AlertTriangle className="w-6 h-6" />
              </div>
              <h2 className="text-xl font-bold text-zinc-100">
                Unable to Load Lecture Note
              </h2>
              <p className="text-sm text-zinc-400 max-w-md mx-auto leading-relaxed">
                {loadError}
              </p>
              <div className="flex items-center justify-center gap-3 pt-2">
                <button
                  onClick={() => noteId && loadNote(noteId)}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white transition-colors shadow-lg shadow-blue-500/20"
                >
                  <RotateCcw className="w-3.5 h-3.5" />
                  <span>Retry Note</span>
                </button>
                <button
                  onClick={() => navigate('/terms')}
                  className="px-4 py-2 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 text-xs font-medium text-zinc-300 transition-colors"
                >
                  Browse Terms
                </button>
              </div>
            </div>
          ) : !currentNote ? (
            <div className="py-24 text-center space-y-5">
              <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mx-auto text-zinc-300 shadow-inner">
                <BookOpen className="w-7 h-7" />
              </div>
              <div className="space-y-1.5">
                <h2 className="text-xl font-bold text-zinc-100">
                  {noteId && noteId !== 'index' ? 'Note Not Found' : `${currentTermFormatted} Curriculum`}
                </h2>
                <p className="text-sm text-zinc-400 max-w-md mx-auto leading-relaxed">
                  {noteId && noteId !== 'index'
                    ? `The requested note ID "${noteId}" is not available in ${currentTermFormatted}.`
                    : `No approved lecture notes are currently published for ${currentTermFormatted}. Select an active term below to start studying.`}
                </p>
              </div>

              {/* Direct Quick Jump to Active Terms */}
              <div className="pt-2 flex flex-col items-center gap-3 max-w-md mx-auto">
                <span className="text-[11px] text-zinc-500 uppercase tracking-wider font-semibold">
                  Published Course Curricula
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5 w-full">
                  <button
                    onClick={() => navigate('/term/term-5/cn/cn-t5-l01')}
                    className="flex items-center justify-between p-3 rounded-xl bg-blue-600/10 hover:bg-blue-600/20 border border-blue-500/30 text-left transition-all group"
                  >
                    <div>
                      <div className="text-xs font-semibold text-blue-300">Term 5 • Computer Networks</div>
                      <div className="text-[11px] text-zinc-400">Lectures 1–3 + Quizzes</div>
                    </div>
                    <ArrowRight className="w-4 h-4 text-blue-400 group-hover:translate-x-0.5 transition-transform shrink-0 ml-2" />
                  </button>
                  <button
                    onClick={() => navigate('/term/term-3/cn/cn-lecture-01-introduction')}
                    className="flex items-center justify-between p-3 rounded-xl bg-indigo-600/10 hover:bg-indigo-600/20 border border-indigo-500/30 text-left transition-all group"
                  >
                    <div>
                      <div className="text-xs font-semibold text-indigo-300">Term 3 • Computer Networks</div>
                      <div className="text-[11px] text-zinc-400">Lectures 1–2 + CML</div>
                    </div>
                    <ArrowRight className="w-4 h-4 text-indigo-400 group-hover:translate-x-0.5 transition-transform shrink-0 ml-2" />
                  </button>
                </div>
                <button
                  onClick={() => navigate('/terms')}
                  className="mt-1 text-xs text-zinc-400 hover:text-zinc-200 transition-colors flex items-center gap-1.5"
                >
                  <span>Or browse all 16 terms in Curriculum Hub</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            </div>
          ) : (
            <article className="space-y-8">
              {/* Mobile Table of Contents Accordion (visible only in Notes mode) */}
              {currentNote.sections && currentNote.sections.length > 0 && activeTab === 'notes' && (
                <MobileTableOfContents sections={currentNote.sections} />
              )}

              {/* Note Header Metadata & Badges */}
              <div className="space-y-4 border-b border-white/[0.08] pb-6">
                <div className="flex flex-wrap items-center gap-2 text-xs">
                  <span className="px-2.5 py-0.5 rounded-md font-mono font-bold bg-blue-500/10 text-blue-400 border border-blue-500/20">
                    {currentNote.subject_code}
                  </span>
                  <span className="px-2.5 py-0.5 rounded-md bg-white/5 text-zinc-300 border border-white/10 font-mono">
                    {currentNote.term}
                  </span>
                  <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                    <CheckCircle className="w-3.5 h-3.5" />
                    <span>Reviewed & Approved</span>
                  </span>
                </div>

                <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-zinc-100">
                  {currentNote.topic_title}
                </h1>

                {/* Summary Abstract */}
                <p className="text-base text-zinc-300 leading-relaxed bg-white/[0.02] border border-white/[0.06] p-4 rounded-xl">
                  {currentNote.summary}
                </p>

                {/* Action Bar: Bookmark & Share */}
                <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => toggleBookmark(currentNote.note_id, currentNote.topic_title)}
                      className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg border text-xs font-medium transition-all ${bookmarked
                          ? 'border-amber-500/40 bg-amber-500/10 text-amber-400 hover:bg-amber-500/20 shadow-sm'
                          : 'border-white/10 bg-white/5 hover:bg-white/10 text-zinc-300'
                        }`}
                    >
                      <BookmarkIcon
                        className={`w-4 h-4 ${bookmarked ? 'fill-amber-400 text-amber-400' : ''}`}
                      />
                      <span>{bookmarked ? 'Bookmarked' : 'Bookmark Note'}</span>
                    </button>

                    <button
                      onClick={handleCopyLink}
                      className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 text-xs text-zinc-300 transition-colors"
                      title="Copy link to note"
                    >
                      {linkCopied ? (
                        <>
                          <Check className="w-4 h-4 text-emerald-400" />
                          <span className="text-emerald-400">Copied!</span>
                        </>
                      ) : (
                        <>
                          <Share2 className="w-4 h-4 text-zinc-400" />
                          <span>Share</span>
                        </>
                      )}
                    </button>
                  </div>

                  <div className="flex items-center gap-2 text-xs text-zinc-400 font-mono">
                    <Calendar className="w-3.5 h-3.5 text-zinc-400" />
                    <span>Updated {currentNote.last_updated}</span>
                  </div>
                </div>

                {/* Tags */}
                {currentNote.tags && currentNote.tags.length > 0 && (
                  <div className="flex flex-wrap items-center gap-1.5 pt-1">
                    <Tag className="w-3.5 h-3.5 text-zinc-400 mr-1" />
                    {currentNote.tags.map((tag) => (
                      <span
                        key={tag}
                        className="text-[11px] font-mono px-2 py-0.5 rounded bg-white/[0.04] text-zinc-400 border border-white/[0.06]"
                      >
                        #{tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>



              {/* Tab 1: Topic Quiz View */}
              {activeTab === 'quiz' && (
                currentNote.quiz ? (
                  <QuizSection
                    quiz={currentNote.quiz}
                    onSwitchToNotes={() => handleTabChange('notes')}
                  />
                ) : (
                  <div className="py-16 text-center space-y-4 border border-white/[0.06] rounded-2xl bg-white/[0.02]">
                    <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center mx-auto text-purple-400">
                      <HelpCircle className="w-6 h-6" />
                    </div>
                    <h3 className="text-lg font-bold text-zinc-100">Topic Quiz Coming Soon</h3>
                    <p className="text-sm text-zinc-400 max-w-md mx-auto">
                      Practice questions for this lecture are currently being reviewed.
                    </p>
                    <button
                      onClick={() => handleTabChange('notes')}
                      className="px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white transition-colors"
                    >
                      Return to Lecture Notes
                    </button>
                  </div>
                )
              )}

              {/* Tab 2: Notes & Markdown View */}
              {activeTab === 'notes' && (
                <>
                  {/* Note Content Sections */}
                  <div className="space-y-12">
                    {currentNote.sections.map((section, idx) => (
                      <section
                        key={section.section_id}
                        id={section.section_id}
                        className="scroll-mt-20 pt-2"
                      >
                        <h2 className="text-2xl font-bold tracking-tight text-zinc-100 mb-4 pb-2 border-b border-white/[0.08] flex items-center gap-3">
                          <span className="text-xs font-mono text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                            {String(idx + 1).padStart(2, '0')}
                          </span>
                          <span>{section.heading}</span>
                        </h2>

                        {/* Section Markdown Body */}
                        <MarkdownViewer content={section.body} />

                        {/* Citations / References if any */}
                        {section.citations && section.citations.length > 0 && (
                          <div className="mt-4 pt-3 border-t border-white/[0.04] text-xs text-zinc-500">
                            <span className="font-semibold text-zinc-400 mr-2">Citations:</span>
                            {section.citations.join('; ')}
                          </div>
                        )}
                      </section>
                    ))}
                  </div>

                  {/* Key Takeaways Bottom Card */}
                  {currentNote.key_takeaways && currentNote.key_takeaways.length > 0 && (
                    <div className="mt-12 p-6 rounded-xl border border-blue-500/20 bg-blue-500/[0.03] space-y-3">
                      <h3 className="text-base font-semibold text-blue-400 flex items-center gap-2">
                        <CheckCircle className="w-4 h-4" />
                        Key Takeaways
                      </h3>
                      <ul className="space-y-2 text-sm text-zinc-300">
                        {currentNote.key_takeaways.map((takeaway, i) => (
                          <li key={i} className="flex items-start gap-2">
                            <span className="text-blue-500 font-bold">•</span>
                            <span>{takeaway}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {/* Real-Time Comment Section */}
                  <CommentSection noteId={currentNote.note_id} />
                </>
              )}
            </article>
          )}
        </div>
      </main>

      {/* 3. Right Island: Table of Contents (w-72, visible only in Notes mode) */}
      {currentNote && currentNote.sections && activeTab === 'notes' && (
        <TableOfContents sections={currentNote.sections} />
      )}
    </div>
  );
};
