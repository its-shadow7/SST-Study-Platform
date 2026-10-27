import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { fetchNoteById, saveNote, deleteNote } from '../services/notesService';
import { Note, NoteSection, QuizQuestion, QuizOption } from '../types/note';
import { MarkdownViewer } from '../components/MarkdownViewer';
import { QuizSection } from '../components/QuizSection';
import {
  Save,
  Trash2,
  Plus,
  ArrowLeft,
  Code,
  Eye,
  BookOpen,
  HelpCircle,
  ChevronDown,
  ChevronUp,
  Copy,
  UploadCloud,
  Check,
  AlertCircle,
  FileText,
  ShieldAlert,
  Columns,
  Tag,
} from 'lucide-react';
import { toast } from 'sonner';

const DEFAULT_NOTE_STATE: Note = {
  schema_version: 1,
  note_id: '',
  term: 'Term 5',
  subject_code: 'CML',
  topic_title: '',
  tags: [],
  learning_objectives: [''],
  summary: '',
  key_takeaways: [''],
  sections: [
    {
      section_id: 'sec-01',
      heading: 'Introduction',
      body: 'Write lecture content here using Markdown and LaTeX ($x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$).',
      citations: [],
    },
  ],
  quiz: {
    title: 'Topic Comprehension Quiz',
    description: 'Comprehensive quiz covering the key concepts in this lecture.',
    estimated_minutes: 15,
    questions: [
      {
        id: 'q-01',
        type: 'single_choice',
        question: 'What is the primary objective of this lecture?',
        options: [
          { id: 'opt-1', text: 'Option A: Foundation theory' },
          { id: 'opt-2', text: 'Option B: Applied architecture' },
          { id: 'opt-3', text: 'Option C: Empirical verification' },
          { id: 'opt-4', text: 'Option D: Scalability optimizations' },
        ],
        correctOptionIds: ['opt-1'],
        explanation: 'Option A is correct because the foundational theory forms the core of this module.',
        difficulty: 'medium',
        subtopic: 'Theory',
      },
    ],
  },
  last_updated: new Date().toISOString(),
  approval_status: 'approved',
};

export const NoteStudioPage: React.FC = () => {
  const { noteId } = useParams<{ noteId?: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();

  const isEditing = Boolean(noteId);
  const [note, setNote] = useState<Note>(DEFAULT_NOTE_STATE);
  const [loading, setLoading] = useState<boolean>(isEditing);
  const [saving, setSaving] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<'editor' | 'preview' | 'json'>('editor');
  const [activeSectionIdx, setActiveSectionIdx] = useState<number>(0);
  const [activeQuestionIdx, setActiveQuestionIdx] = useState<number>(0);
  const [rawJsonText, setRawJsonText] = useState<string>('');
  const [copiedJson, setCopiedJson] = useState<boolean>(false);
  const [deleteConfirmOpen, setDeleteConfirmOpen] = useState<boolean>(false);

  const isModeratorOrAdmin = user?.role === 'moderator' || user?.role === 'admin';

  useEffect(() => {
    if (!isEditing || !noteId) return;

    let mounted = true;
    setLoading(true);

    fetchNoteById(noteId)
      .then((data) => {
        if (!mounted) return;
        const normalized = { ...data };
        if (Array.isArray(normalized.quiz)) {
          normalized.quiz = {
            title: `${normalized.topic_title || 'Lecture'} Quiz`,
            description: 'Topic evaluation',
            estimated_minutes: 15,
            questions: normalized.quiz as any,
          };
        } else if (!normalized.quiz) {
          normalized.quiz = {
            title: 'Topic Quiz',
            description: 'Comprehension questions',
            estimated_minutes: 15,
            questions: [],
          };
        }
        setNote(normalized);
        setRawJsonText(JSON.stringify(normalized, null, 2));
      })
      .catch((err) => {
        toast.error(`Could not load lecture: ${err.message}`);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, [noteId, isEditing]);

  useEffect(() => {
    if (activeTab === 'json') {
      setRawJsonText(JSON.stringify(note, null, 2));
    }
  }, [activeTab, note]);

  // Access check
  if (!user || !isModeratorOrAdmin) {
    return (
      <div className="min-h-[calc(100vh-3.5rem)] bg-slate-50 dark:bg-[#09090b] text-zinc-800 dark:text-zinc-200 flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-white dark:bg-[#0e0e11] border border-zinc-200 dark:border-white/[0.08] rounded-xl p-8 text-center space-y-4 shadow-sm">
          <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-600 dark:text-amber-400 flex items-center justify-center mx-auto">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-bold text-zinc-900 dark:text-zinc-100">Access Restricted</h2>
          <p className="text-xs text-zinc-600 dark:text-zinc-400 leading-relaxed">
            Note Studio is reserved exclusively for Course Moderators and Administrators. Your current role does not have authorization to curate or publish lecture notes.
          </p>
          <button
            onClick={() => navigate('/terms')}
            className="w-full py-2 px-4 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs transition-colors"
          >
            Return to Curriculum
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-[calc(100vh-3.5rem)] bg-slate-50 dark:bg-[#09090b] text-zinc-800 dark:text-zinc-200 flex items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <p className="text-xs text-zinc-500 dark:text-zinc-400">Loading lecture note into Studio...</p>
        </div>
      </div>
    );
  }

  const handleSave = async (status: 'draft' | 'approved' = note.approval_status as any) => {
    if (!note.note_id.trim()) {
      toast.error('Note ID is required (e.g. cml-t5-l02)');
      return;
    }
    if (!note.topic_title.trim()) {
      toast.error('Topic title is required');
      return;
    }

    setSaving(true);
    const payload: Note = {
      ...note,
      approval_status: status,
      last_updated: new Date().toISOString(),
    };

    try {
      const saved = await saveNote(payload);
      setNote(saved);
      toast.success(
        status === 'approved'
          ? 'Lecture note published to catalogue.'
          : 'Lecture draft saved successfully.'
      );
      if (!isEditing) {
        navigate(`/studio/${saved.note_id}`, { replace: true });
      }
    } catch (err: any) {
      toast.error(`Save failed: ${err.message}`);
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!note.note_id) return;
    setSaving(true);
    try {
      await deleteNote(note.note_id);
      toast.success(`Note '${note.note_id}' permanently deleted.`);
      navigate('/terms');
    } catch (err: any) {
      toast.error(`Delete failed: ${err.message}`);
    } finally {
      setSaving(false);
      setDeleteConfirmOpen(false);
    }
  };

  const handleJsonImport = () => {
    try {
      const parsed = JSON.parse(rawJsonText);
      if (!parsed.note_id) {
        throw new Error("JSON must contain at least a 'note_id' string.");
      }
      setNote(parsed);
      setActiveTab('editor');
      toast.success('Imported note JSON into Studio.');
    } catch (err: any) {
      toast.error(`Invalid JSON: ${err.message}`);
    }
  };

  const copyJsonToClipboard = () => {
    navigator.clipboard.writeText(rawJsonText);
    setCopiedJson(true);
    toast.success('Note JSON copied to clipboard.');
    setTimeout(() => setCopiedJson(false), 2000);
  };

  const addSection = () => {
    const newIdx = note.sections.length + 1;
    const newSec: NoteSection = {
      section_id: `sec-${String(newIdx).padStart(2, '0')}`,
      heading: `Section ${newIdx}`,
      body: '',
      citations: [],
    };
    setNote((prev) => ({ ...prev, sections: [...prev.sections, newSec] }));
    setActiveSectionIdx(note.sections.length);
  };

  const removeSection = (idx: number) => {
    if (note.sections.length <= 1) {
      toast.error('A note must contain at least one section.');
      return;
    }
    setNote((prev) => ({
      ...prev,
      sections: prev.sections.filter((_, i) => i !== idx),
    }));
    setActiveSectionIdx(Math.max(0, idx - 1));
  };

  const moveSection = (idx: number, direction: 'up' | 'down') => {
    const targetIdx = direction === 'up' ? idx - 1 : idx + 1;
    if (targetIdx < 0 || targetIdx >= note.sections.length) return;
    const copy = [...note.sections];
    const temp = copy[idx];
    copy[idx] = copy[targetIdx];
    copy[targetIdx] = temp;
    setNote((prev) => ({ ...prev, sections: copy }));
    setActiveSectionIdx(targetIdx);
  };

  const questionsList = note.quiz?.questions || [];
  const addQuestion = () => {
    const newQId = `q-${String(questionsList.length + 1).padStart(2, '0')}`;
    const newQ: QuizQuestion = {
      id: newQId,
      type: 'single_choice',
      question: 'New question prompt with math support',
      options: [
        { id: 'opt-1', text: 'Option A' },
        { id: 'opt-2', text: 'Option B' },
      ],
      correctOptionIds: ['opt-1'],
      explanation: 'Explanation for correct choice.',
      difficulty: 'medium',
      subtopic: 'General',
    };
    setNote((prev) => ({
      ...prev,
      quiz: {
        ...(prev.quiz || { title: 'Quiz', description: '', estimated_minutes: 15, questions: [] }),
        questions: [...(prev.quiz?.questions || []), newQ],
      },
    }));
    setActiveQuestionIdx(questionsList.length);
  };

  const removeQuestion = (idx: number) => {
    setNote((prev) => ({
      ...prev,
      quiz: {
        ...(prev.quiz || { title: 'Quiz', description: '', estimated_minutes: 15, questions: [] }),
        questions: (prev.quiz?.questions || []).filter((_, i) => i !== idx),
      },
    }));
    setActiveQuestionIdx(Math.max(0, idx - 1));
  };

  return (
    <div className="h-[calc(100vh-3.5rem)] bg-slate-50 dark:bg-[#09090b] text-zinc-800 dark:text-zinc-200 flex flex-col font-sans transition-colors overflow-hidden">
      {/* Top Application Bar - Clean, fixed height directly below global Navbar */}
      <header className="shrink-0 h-14 bg-white dark:bg-[#0e0e11] border-b border-zinc-200 dark:border-white/[0.08] px-4 sm:px-6 flex items-center justify-between gap-4 z-20 select-none">
        <div className="flex items-center gap-3 min-w-0">
          <button
            onClick={() => navigate('/terms')}
            className="p-1.5 rounded-lg border border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.03] hover:bg-zinc-100 dark:hover:bg-white/[0.08] text-zinc-600 dark:text-zinc-300 transition-colors shrink-0"
            title="Back to Terms"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div className="flex items-center gap-2 truncate text-xs">
            <span className="font-semibold text-blue-600 dark:text-blue-400">Note Studio</span>
            <span className="text-zinc-400 dark:text-zinc-500">/</span>
            <span className="font-mono text-zinc-500 dark:text-zinc-400 truncate">
              {note.note_id || 'new-note'}
            </span>
          </div>
        </div>

        {/* View Mode Switcher */}
        <div className="flex items-center p-0.5 rounded-lg bg-zinc-100 dark:bg-white/[0.04] border border-zinc-200 dark:border-white/10 text-xs">
          <button
            onClick={() => setActiveTab('editor')}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-md transition-colors ${
              activeTab === 'editor'
                ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 font-medium shadow-sm'
                : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
            }`}
          >
            <Columns className="w-3.5 h-3.5" />
            <span>Split Editor</span>
          </button>
          <button
            onClick={() => setActiveTab('preview')}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-md transition-colors ${
              activeTab === 'preview'
                ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 font-medium shadow-sm'
                : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
            }`}
          >
            <Eye className="w-3.5 h-3.5" />
            <span>Full Preview</span>
          </button>
          <button
            onClick={() => setActiveTab('json')}
            className={`flex items-center gap-1.5 px-3 py-1 rounded-md transition-colors ${
              activeTab === 'json'
                ? 'bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 font-medium shadow-sm'
                : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
            }`}
          >
            <Code className="w-3.5 h-3.5" />
            <span>JSON</span>
          </button>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2 shrink-0">
          {isEditing && (
            <button
              onClick={() => setDeleteConfirmOpen(true)}
              disabled={saving}
              className="p-1.5 rounded-lg text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 border border-zinc-200 dark:border-white/10 transition-colors"
              title="Delete Note"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
          <button
            onClick={() => handleSave('draft')}
            disabled={saving}
            className="px-3 py-1.5 rounded-lg border border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.03] hover:bg-zinc-100 dark:hover:bg-white/[0.08] text-xs font-medium text-zinc-700 dark:text-zinc-200 transition-colors"
          >
            Save Draft
          </button>
          <button
            onClick={() => handleSave('approved')}
            disabled={saving}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium transition-colors shadow-sm disabled:opacity-50"
          >
            <Save className="w-3.5 h-3.5" />
            <span>{saving ? 'Saving...' : 'Publish'}</span>
          </button>
        </div>
      </header>

      {/* Main Workspace Body */}
      <main className="flex-1 flex overflow-hidden">
        {/* MODE 1: SPLIT EDITOR (Form Left + Markdown/KaTeX Live Preview Right) */}
        {activeTab === 'editor' && (
          <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
            {/* Left Form Pane */}
            <div className="w-full lg:w-1/2 border-r border-zinc-200 dark:border-white/[0.08] overflow-y-auto p-4 sm:p-6 space-y-6">
              {/* Lecture Metadata Card */}
              <section className="bg-white dark:bg-[#0e0e11] border border-zinc-200 dark:border-white/[0.08] rounded-xl p-5 space-y-4 shadow-sm dark:shadow-none">
                <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400 border-b border-zinc-100 dark:border-white/[0.06] pb-2">
                  <FileText className="w-3.5 h-3.5" />
                  <span>Lecture Metadata</span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div>
                    <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                      Note ID *
                    </label>
                    <input
                      type="text"
                      value={note.note_id}
                      onChange={(e) => setNote({ ...note, note_id: e.target.value.toLowerCase().trim() })}
                      placeholder="e.g. cml-t5-l02"
                      className="w-full text-xs font-mono px-3 py-2 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                      Academic Term
                    </label>
                    <input
                      type="text"
                      value={note.term}
                      onChange={(e) => setNote({ ...note, term: e.target.value })}
                      placeholder="Term 5"
                      className="w-full text-xs px-3 py-2 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                      Subject Code
                    </label>
                    <input
                      type="text"
                      value={note.subject_code}
                      onChange={(e) => setNote({ ...note, subject_code: e.target.value.toUpperCase().trim() })}
                      placeholder="CML"
                      className="w-full text-xs font-mono px-3 py-2 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                    Topic Title *
                  </label>
                  <input
                    type="text"
                    value={note.topic_title}
                    onChange={(e) => setNote({ ...note, topic_title: e.target.value })}
                    placeholder="e.g. 2. Data Preparation, Feature Preprocessing & Leakage Prevention Pipelines"
                    className="w-full text-xs px-3 py-2 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                    Summary / Abstract
                  </label>
                  <textarea
                    rows={3}
                    value={note.summary}
                    onChange={(e) => setNote({ ...note, summary: e.target.value })}
                    placeholder="Detailed introductory summary of this lecture module..."
                    className="w-full text-xs px-3 py-2 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 resize-y"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                    Tags (Comma-separated)
                  </label>
                  <input
                    type="text"
                    value={note.tags.join(', ')}
                    onChange={(e) =>
                      setNote({
                        ...note,
                        tags: e.target.value
                          .split(',')
                          .map((t) => t.trim())
                          .filter(Boolean),
                      })
                    }
                    placeholder="Data Preprocessing, Scikit-Learn, Feature Scaling"
                    className="w-full text-xs px-3 py-2 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                  />
                </div>
              </section>

              {/* Content Sections Editor */}
              <section className="bg-white dark:bg-[#0e0e11] border border-zinc-200 dark:border-white/[0.08] rounded-xl p-5 space-y-4 shadow-sm dark:shadow-none">
                <div className="flex items-center justify-between border-b border-zinc-100 dark:border-white/[0.06] pb-2">
                  <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
                    <BookOpen className="w-3.5 h-3.5" />
                    <span>Lecture Sections ({note.sections.length})</span>
                  </div>
                  <button
                    onClick={addSection}
                    className="flex items-center gap-1 text-xs text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium py-1 px-2.5 rounded-lg border border-blue-500/20 bg-blue-500/10 transition-colors"
                  >
                    <Plus className="w-3.5 h-3.5" />
                    <span>Add Section</span>
                  </button>
                </div>

                {/* Section navigation tabs */}
                <div className="flex gap-1.5 overflow-x-auto pb-1 text-xs">
                  {note.sections.map((sec, idx) => (
                    <button
                      key={sec.section_id || idx}
                      onClick={() => setActiveSectionIdx(idx)}
                      className={`px-3 py-1.5 rounded-lg border font-medium whitespace-nowrap transition-colors ${
                        activeSectionIdx === idx
                          ? 'bg-blue-600 text-white border-blue-600'
                          : 'bg-zinc-50 dark:bg-white/[0.02] border-zinc-200 dark:border-white/10 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-white/5'
                      }`}
                    >
                      {idx + 1}. {sec.heading ? (sec.heading.length > 20 ? sec.heading.slice(0, 20) + '...' : sec.heading) : 'Untitled'}
                    </button>
                  ))}
                </div>

                {/* Active Section Editor */}
                {note.sections[activeSectionIdx] && (
                  <div className="space-y-4 pt-1">
                    <div className="flex items-center justify-between gap-2">
                      <input
                        type="text"
                        value={note.sections[activeSectionIdx].heading}
                        onChange={(e) => {
                          const updated = [...note.sections];
                          updated[activeSectionIdx].heading = e.target.value;
                          setNote({ ...note, sections: updated });
                        }}
                        placeholder="Section Heading"
                        className="flex-1 text-xs font-semibold px-3 py-2 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                      />
                      <div className="flex items-center gap-1">
                        <button
                          onClick={() => moveSection(activeSectionIdx, 'up')}
                          disabled={activeSectionIdx === 0}
                          className="p-1.5 rounded-lg border border-zinc-200 dark:border-white/10 text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 disabled:opacity-30"
                          title="Move Up"
                        >
                          <ChevronUp className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => moveSection(activeSectionIdx, 'down')}
                          disabled={activeSectionIdx === note.sections.length - 1}
                          className="p-1.5 rounded-lg border border-zinc-200 dark:border-white/10 text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 disabled:opacity-30"
                          title="Move Down"
                        >
                          <ChevronDown className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => removeSection(activeSectionIdx)}
                          className="p-1.5 rounded-lg text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 border border-zinc-200 dark:border-white/10"
                          title="Remove Section"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>

                    <div>
                      <div className="flex items-center justify-between mb-1">
                        <label className="text-xs font-medium text-zinc-700 dark:text-zinc-300">
                          Body (Markdown, Tables, Code & LaTeX Math)
                        </label>
                        <span className="text-[11px] text-zinc-500 font-mono">
                          Inline $x$, block $$x$$
                        </span>
                      </div>
                      <textarea
                        rows={12}
                        value={note.sections[activeSectionIdx].body}
                        onChange={(e) => {
                          const updated = [...note.sections];
                          updated[activeSectionIdx].body = e.target.value;
                          setNote({ ...note, sections: updated });
                        }}
                        placeholder="Write markdown here. GFM tables, code blocks, and KaTeX math formulas are rendered live on the right..."
                        className="w-full text-xs font-mono leading-relaxed p-3 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 resize-y"
                      />
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                        Citations / References (One per line)
                      </label>
                      <textarea
                        rows={2}
                        value={note.sections[activeSectionIdx].citations.join('\n')}
                        onChange={(e) => {
                          const updated = [...note.sections];
                          updated[activeSectionIdx].citations = e.target.value
                            .split('\n')
                            .map((c) => c.trim())
                            .filter(Boolean);
                          setNote({ ...note, sections: updated });
                        }}
                        placeholder="e.g. Mitchell, T. M. (1997). Machine Learning."
                        className="w-full text-xs px-3 py-2 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 resize-y"
                      />
                    </div>
                  </div>
                )}
              </section>

              {/* Topic Quiz Builder */}
              <section className="bg-white dark:bg-[#0e0e11] border border-zinc-200 dark:border-white/[0.08] rounded-xl p-5 space-y-4 shadow-sm dark:shadow-none">
                <div className="flex items-center justify-between border-b border-zinc-100 dark:border-white/[0.06] pb-2">
                  <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
                    <HelpCircle className="w-3.5 h-3.5" />
                    <span>Topic Quiz ({questionsList.length} Questions)</span>
                  </div>
                  <button
                    onClick={addQuestion}
                    className="flex items-center gap-1 text-xs text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium py-1 px-2.5 rounded-lg border border-blue-500/20 bg-blue-500/10 transition-colors"
                  >
                    <Plus className="w-3.5 h-3.5" />
                    <span>Add Question</span>
                  </button>
                </div>

                {questionsList.length > 0 && (
                  <div className="flex gap-1.5 overflow-x-auto pb-1 text-xs">
                    {questionsList.map((q, idx) => (
                      <button
                        key={q.id || idx}
                        onClick={() => setActiveQuestionIdx(idx)}
                        className={`px-3 py-1.5 rounded-lg border font-medium transition-colors ${
                          activeQuestionIdx === idx
                            ? 'bg-blue-600 text-white border-blue-600'
                            : 'bg-zinc-50 dark:bg-white/[0.02] border-zinc-200 dark:border-white/10 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-white/5'
                        }`}
                      >
                        Q{idx + 1}
                      </button>
                    ))}
                  </div>
                )}

                {questionsList[activeQuestionIdx] && (
                  <div className="space-y-4 pt-1">
                    <div className="flex items-center justify-between gap-3">
                      <div className="flex-1">
                        <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                          Question Prompt
                        </label>
                        <textarea
                          rows={2}
                          value={questionsList[activeQuestionIdx].question}
                          onChange={(e) => {
                            const updated = [...questionsList];
                            updated[activeQuestionIdx].question = e.target.value;
                            setNote({
                              ...note,
                              quiz: { ...(note.quiz || { questions: [] }), questions: updated } as any,
                            });
                          }}
                          placeholder="What is the mathematical formulation of..."
                          className="w-full text-xs px-3 py-2 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                        />
                      </div>
                      <button
                        onClick={() => removeQuestion(activeQuestionIdx)}
                        className="p-1.5 rounded-lg text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/20 border border-zinc-200 dark:border-white/10 self-start mt-6"
                        title="Delete question"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>

                    <div className="space-y-2">
                      <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300">
                        Answer Options (Select the Radio for Correct Answer)
                      </label>
                      {questionsList[activeQuestionIdx].options.map((opt, oIdx) => {
                        const isCorrect = questionsList[activeQuestionIdx].correctOptionIds?.includes(opt.id);
                        return (
                          <div key={opt.id || oIdx} className="flex items-center gap-2">
                            <input
                              type="radio"
                              name={`correct-${questionsList[activeQuestionIdx].id}`}
                              checked={isCorrect}
                              onChange={() => {
                                const updated = [...questionsList];
                                updated[activeQuestionIdx].correctOptionIds = [opt.id];
                                setNote({
                                  ...note,
                                  quiz: { ...(note.quiz || { questions: [] }), questions: updated } as any,
                                });
                              }}
                              className="accent-blue-600 w-4 h-4"
                            />
                            <span className="text-xs font-mono text-zinc-500 dark:text-zinc-400 w-8">
                              {opt.id}:
                            </span>
                            <input
                              type="text"
                              value={opt.text}
                              onChange={(e) => {
                                const updated = [...questionsList];
                                updated[activeQuestionIdx].options[oIdx].text = e.target.value;
                                setNote({
                                  ...note,
                                  quiz: { ...(note.quiz || { questions: [] }), questions: updated } as any,
                                });
                              }}
                              className="flex-1 text-xs px-3 py-1.5 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                            />
                          </div>
                        );
                      })}
                    </div>

                    <div>
                      <label className="block text-xs font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                        Explanation
                      </label>
                      <textarea
                        rows={2}
                        value={questionsList[activeQuestionIdx].explanation}
                        onChange={(e) => {
                          const updated = [...questionsList];
                          updated[activeQuestionIdx].explanation = e.target.value;
                          setNote({
                            ...note,
                            quiz: { ...(note.quiz || { questions: [] }), questions: updated } as any,
                          });
                        }}
                        placeholder="Detailed explanation of the correct choice..."
                        className="w-full text-xs px-3 py-2 rounded-lg bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                )}
              </section>
            </div>

            {/* Right Live Preview Pane - Real MarkdownViewer Render */}
            <div className="hidden lg:flex w-1/2 flex-col overflow-y-auto p-4 sm:p-6 space-y-6 bg-zinc-50/50 dark:bg-[#09090b]">
              <div className="flex items-center justify-between border-b border-zinc-200 dark:border-white/[0.08] pb-3 text-xs">
                <span className="font-semibold text-zinc-700 dark:text-zinc-300">
                  Live Preview
                </span>
                <span className="text-zinc-500 dark:text-zinc-400 font-mono">
                  {note.sections.length} sections &bull; {questionsList.length} quiz questions
                </span>
              </div>

              {/* Title & Summary Preview */}
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-xs">
                  <span className="px-2 py-0.5 rounded font-mono font-bold bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
                    {note.subject_code || 'SUBJ'}
                  </span>
                  <span className="px-2 py-0.5 rounded bg-zinc-100 dark:bg-white/5 text-zinc-700 dark:text-zinc-300 border border-zinc-200 dark:border-white/10 font-mono">
                    {note.term || 'Term'}
                  </span>
                </div>
                <h2 className="text-xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
                  {note.topic_title || 'Untitled Lecture Note'}
                </h2>
                {note.summary && (
                  <p className="text-xs text-zinc-600 dark:text-zinc-400 leading-relaxed bg-white dark:bg-[#0e0e11] border border-zinc-200 dark:border-white/[0.06] rounded-lg p-3">
                    {note.summary}
                  </p>
                )}
              </div>

              {/* Active Section MarkdownViewer Render */}
              {note.sections[activeSectionIdx] && (
                <div className="bg-white dark:bg-[#0e0e11] border border-zinc-200 dark:border-white/[0.08] rounded-xl p-5 space-y-3 shadow-sm dark:shadow-none">
                  <div className="flex items-center gap-2 border-b border-zinc-100 dark:border-white/[0.06] pb-2">
                    <span className="text-xs font-mono text-blue-600 dark:text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                      {String(activeSectionIdx + 1).padStart(2, '0')}
                    </span>
                    <h3 className="text-base font-bold text-zinc-900 dark:text-zinc-100">
                      {note.sections[activeSectionIdx].heading || 'Untitled Section'}
                    </h3>
                  </div>
                  <div className="w-full">
                    <MarkdownViewer content={note.sections[activeSectionIdx].body} isCompact={true} />
                  </div>
                  {note.sections[activeSectionIdx].citations && note.sections[activeSectionIdx].citations.length > 0 && (
                    <div className="mt-3 pt-2 border-t border-zinc-100 dark:border-white/[0.04] text-xs text-zinc-500">
                      <span className="font-semibold text-zinc-700 dark:text-zinc-400 mr-2">Citations:</span>
                      {note.sections[activeSectionIdx].citations.join('; ')}
                    </div>
                  )}
                </div>
              )}

              {/* Quiz Component Preview */}
              {questionsList.length > 0 && note.quiz && (
                <div className="bg-white dark:bg-[#0e0e11] border border-zinc-200 dark:border-white/[0.08] rounded-xl p-5 space-y-3 shadow-sm dark:shadow-none">
                  <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-500 dark:text-zinc-400">
                    Quiz Preview
                  </h3>
                  <div className="pointer-events-none opacity-90">
                    <QuizSection quiz={note.quiz as any} />
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* MODE 2: FULL PREVIEW (Exact match with Reader Page) */}
        {activeTab === 'preview' && (
          <div className="flex-1 overflow-y-auto p-4 sm:p-8 max-w-4xl mx-auto w-full space-y-8">
            {/* Note Header Metadata & Badges */}
            <div className="space-y-4 border-b border-zinc-200 dark:border-white/[0.08] pb-6">
              <div className="flex flex-wrap items-center gap-2 text-xs">
                <span className="px-2.5 py-0.5 rounded-md font-mono font-bold bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
                  {note.subject_code}
                </span>
                <span className="px-2.5 py-0.5 rounded-md bg-zinc-100 dark:bg-white/5 text-zinc-700 dark:text-zinc-300 border border-zinc-200 dark:border-white/10 font-mono">
                  {note.term}
                </span>
                <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-md bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 font-medium">
                  <Check className="w-3.5 h-3.5" />
                  <span>{note.approval_status === 'approved' ? 'Published' : 'Draft'}</span>
                </span>
              </div>

              <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
                {note.topic_title || 'Untitled Lecture Note'}
              </h1>

              {note.summary && (
                <p className="text-sm text-zinc-700 dark:text-zinc-300 leading-relaxed bg-zinc-50 dark:bg-white/[0.02] border border-zinc-200 dark:border-white/[0.06] rounded-xl p-4 shadow-sm dark:shadow-none">
                  {note.summary}
                </p>
              )}

              {note.tags && note.tags.length > 0 && (
                <div className="flex flex-wrap items-center gap-1.5 pt-1">
                  <Tag className="w-3.5 h-3.5 text-zinc-400 mr-1" />
                  {note.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-[11px] font-mono px-2 py-0.5 rounded bg-zinc-100 dark:bg-white/[0.04] text-zinc-600 dark:text-zinc-400 border border-zinc-200 dark:border-white/[0.06]"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              )}
            </div>

            {/* Note Content Sections */}
            <div className="space-y-10">
              {note.sections.map((section, idx) => (
                <section key={section.section_id || idx} className="pt-2">
                  <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100 mb-4 pb-2 border-b border-zinc-200 dark:border-white/[0.08] flex items-center gap-3">
                    <span className="text-xs font-mono text-blue-600 dark:text-blue-400 bg-blue-500/10 px-2 py-0.5 rounded border border-blue-500/20">
                      {String(idx + 1).padStart(2, '0')}
                    </span>
                    <span>{section.heading}</span>
                  </h2>

                  <MarkdownViewer content={section.body} isCompact={false} />

                  {section.citations && section.citations.length > 0 && (
                    <div className="mt-4 pt-3 border-t border-zinc-200 dark:border-white/[0.04] text-xs text-zinc-500">
                      <span className="font-semibold text-zinc-700 dark:text-zinc-400 mr-2">Citations:</span>
                      {section.citations.join('; ')}
                    </div>
                  )}
                </section>
              ))}
            </div>

            {/* Comprehension Quiz */}
            {note.quiz && questionsList.length > 0 && (
              <div className="pt-8 border-t border-zinc-200 dark:border-white/[0.08]">
                <h2 className="text-xl font-bold mb-4 text-zinc-900 dark:text-zinc-100">
                  Comprehension Quiz
                </h2>
                <QuizSection quiz={note.quiz as any} />
              </div>
            )}
          </div>
        )}

        {/* MODE 3: RAW JSON */}
        {activeTab === 'json' && (
          <div className="flex-1 flex flex-col p-4 sm:p-6 space-y-4 max-w-5xl mx-auto w-full overflow-hidden">
            <div className="flex items-center justify-between gap-4 shrink-0">
              <div>
                <h3 className="text-sm font-semibold text-zinc-900 dark:text-zinc-100">Note Document JSON</h3>
                <p className="text-xs text-zinc-500 dark:text-zinc-400">
                  Direct raw JSON document format compatible with MongoDB Atlas.
                </p>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={copyJsonToClipboard}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.03] hover:bg-zinc-100 dark:hover:bg-white/[0.08] text-xs font-medium text-zinc-700 dark:text-zinc-300 transition-colors"
                >
                  {copiedJson ? <Check className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copiedJson ? 'Copied' : 'Copy JSON'}</span>
                </button>
                <button
                  onClick={handleJsonImport}
                  className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-medium transition-colors"
                >
                  <UploadCloud className="w-3.5 h-3.5" />
                  <span>Import JSON</span>
                </button>
              </div>
            </div>

            <textarea
              value={rawJsonText}
              onChange={(e) => setRawJsonText(e.target.value)}
              className="flex-1 font-mono text-xs p-4 rounded-xl bg-white dark:bg-[#141418] border border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-100 placeholder-zinc-400 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 leading-relaxed resize-none"
            />
          </div>
        )}
      </main>

      {/* Delete Confirmation Modal */}
      {deleteConfirmOpen && (
        <div className="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white dark:bg-[#0e0e11] border border-zinc-200 dark:border-white/10 rounded-xl p-6 max-w-md w-full space-y-4 shadow-xl">
            <div className="w-10 h-10 rounded-xl bg-red-500/10 border border-red-500/20 text-red-600 dark:text-red-400 flex items-center justify-center">
              <AlertCircle className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-zinc-900 dark:text-zinc-100">Delete Lecture Note?</h3>
              <p className="text-xs text-zinc-600 dark:text-zinc-400 mt-1 leading-relaxed">
                Are you sure you want to permanently delete <strong className="font-mono text-zinc-900 dark:text-zinc-100">{note.note_id}</strong> from MongoDB Atlas? This action cannot be undone.
              </p>
            </div>
            <div className="flex items-center justify-end gap-2 pt-2">
              <button
                onClick={() => setDeleteConfirmOpen(false)}
                className="px-3.5 py-1.5 rounded-lg text-xs font-medium border border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.03] hover:bg-zinc-100 dark:hover:bg-white/[0.08] text-zinc-700 dark:text-zinc-300 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                className="px-3.5 py-1.5 rounded-lg text-xs font-medium bg-red-600 hover:bg-red-700 text-white transition-colors"
              >
                Delete Note
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default NoteStudioPage;
