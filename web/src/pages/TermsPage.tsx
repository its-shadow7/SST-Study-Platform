import React, { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { NoteIndexItem } from '@/types/note';
import { useAuth } from '@/context/AuthContext';
import {
  Layers,
  ArrowRight,
  Lock,
  GraduationCap,
  Sparkles,
  ArrowUpDown,
  Filter,
  CheckCircle2,
  Check
} from 'lucide-react';
import { toast } from 'sonner';

interface TermsPageProps {
  notes: NoteIndexItem[];
}

type OrderMode = 'standard' | 'current-year-first' | 'unlocked-first' | 'reverse';
type YearFilter = 'all' | 'unlocked' | 1 | 2 | 3 | 4;

export const TermsPage: React.FC<TermsPageProps> = ({ notes }) => {
  const navigate = useNavigate();
  const { user } = useAuth();

  const isDevOrPrivileged = import.meta.env.DEV || user?.role === 'admin' || user?.role === 'moderator';
  const maxAllowedTerm = isDevOrPrivileged ? 16 : (user?.max_allowed_term ?? 16);
  const yearOfStudy = user?.year_of_study ?? 4;
  const batchYear = user?.batch_year;

  const [orderMode, setOrderMode] = useState<OrderMode>('standard');
  const [selectedFilter, setSelectedFilter] = useState<YearFilter>('all');

  // Compute all 16 terms
  const allTerms = useMemo(() => {
    return Array.from({ length: 16 }, (_, i) => {
      const termNumber = i + 1;
      const termName = `Term ${termNumber}`;
      const termNotes = notes.filter((n) => n.term.toLowerCase() === termName.toLowerCase());
      const subjects = Array.from(new Set(termNotes.map((n) => n.subject_code)));
      const isLocked = termNumber > maxAllowedTerm;
      const yearNumber = Math.ceil(termNumber / 4); // 4 terms per academic year
      const termInYear = ((termNumber - 1) % 4) + 1;
      const isCurrentYear = yearNumber === yearOfStudy;
      const isActiveTerm = termNumber === (user?.active_term || 1);

      return {
        id: termNumber,
        name: termName,
        slug: `term-${termNumber}`,
        yearNumber,
        termInYear,
        notesCount: termNotes.length,
        subjects,
        isLocked,
        isCurrentYear,
        isActiveTerm,
        firstNote: termNotes[0] || null,
      };
    });
  }, [notes, maxAllowedTerm, yearOfStudy, user?.active_term]);

  // Apply filters and dynamic ordering
  const displayedTerms = useMemo(() => {
    // 1. Filtering
    let result = [...allTerms];
    if (selectedFilter === 'unlocked') {
      result = result.filter((t) => !t.isLocked);
    } else if (typeof selectedFilter === 'number') {
      result = result.filter((t) => t.yearNumber === selectedFilter);
    }

    // 2. Ordering
    if (orderMode === 'current-year-first') {
      result.sort((a, b) => {
        if (a.isCurrentYear && !b.isCurrentYear) return -1;
        if (!a.isCurrentYear && b.isCurrentYear) return 1;
        return a.id - b.id;
      });
    } else if (orderMode === 'unlocked-first') {
      result.sort((a, b) => {
        if (!a.isLocked && b.isLocked) return -1;
        if (a.isLocked && !b.isLocked) return 1;
        return a.id - b.id;
      });
    } else if (orderMode === 'reverse') {
      result.sort((a, b) => b.id - a.id);
    } else {
      result.sort((a, b) => a.id - b.id);
    }

    return result;
  }, [allTerms, selectedFilter, orderMode]);

  const handleSelectTerm = (term: (typeof allTerms)[0]) => {
    if (term.isLocked) {
      toast.error(
        `Term ${term.id} is locked. As a Year ${yearOfStudy} student${batchYear ? ` (Batch '` + String(batchYear).slice(2) + `)` : ''
        }, you only have access to Terms 1–${maxAllowedTerm} (current & previous years).`
      );
      return;
    }

    if (term.firstNote) {
      navigate(
        `/term/${term.slug}/${term.firstNote.subject_code.toLowerCase()}/${term.firstNote.note_id}`
      );
    } else {
      navigate(`/term/${term.slug}`);
    }
  };

  return (
    <div className="min-h-[calc(100vh-3.5rem)] bg-slate-50 dark:bg-[#09090b] text-zinc-800 dark:text-zinc-200 py-8 sm:py-10 px-4 sm:px-6 lg:px-8 max-w-[1440px] mx-auto transition-colors">
      {/* Page Header */}
      <div className="mb-8 border-b border-zinc-200 dark:border-white/[0.08] pb-6 flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-blue-500/20 bg-blue-500/10 text-xs font-medium text-blue-600 dark:text-blue-400 mb-3">
            <Layers className="w-3.5 h-3.5" />
            <span>Curriculum Hub</span>
          </div>
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
            Academic Terms
          </h1>
          <p className="text-sm text-zinc-600 dark:text-zinc-400 mt-2 max-w-2xl leading-relaxed">
            Browse course notes, lecture materials, and curriculum archives. The degree comprises
            4 years with 4 terms per academic year (16 terms total).
          </p>
        </div>

        {/* Student Academic Standing Badge */}
        {user && (
          <div className="p-3.5 rounded-xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.02] shadow-sm dark:shadow-none flex items-center gap-3 shrink-0 self-start md:self-auto">
            <div className="w-10 h-10 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-600 dark:text-blue-400">
              <GraduationCap className="w-5 h-5" />
            </div>
            <div className="text-left text-xs">
              <div className="font-semibold text-zinc-900 dark:text-zinc-200 flex items-center gap-1.5">
                <span>Year {yearOfStudy} Student</span>
                {batchYear && (
                  <span className="text-blue-600 dark:text-blue-400 font-mono text-[11px]">
                    (Batch '{String(batchYear).slice(2)})
                  </span>
                )}
              </div>
              <div className="text-zinc-500 dark:text-zinc-400 text-[11px] font-mono mt-0.5">
                Access: Terms 1–{maxAllowedTerm} • <span className="text-emerald-600 dark:text-emerald-400 font-semibold">Current: Term {user.active_term || 1}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Dynamic Controls: Filter Pills & Dynamic Ordering */}
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        {/* Year Filter Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 scrollbar-none text-xs">
          <button
            onClick={() => setSelectedFilter('all')}
            className={`px-3 py-1.5 rounded-lg border font-medium transition-all shrink-0 ${selectedFilter === 'all'
                ? 'bg-blue-600 border-blue-500 text-white shadow-sm'
                : 'bg-white dark:bg-white/[0.03] border-zinc-200 dark:border-white/10 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/[0.06] shadow-sm dark:shadow-none'
              }`}
          >
            All Terms (16)
          </button>
          <button
            onClick={() => setSelectedFilter('unlocked')}
            className={`px-3 py-1.5 rounded-lg border font-medium transition-all shrink-0 ${selectedFilter === 'unlocked'
                ? 'bg-blue-600 border-blue-500 text-white shadow-sm'
                : 'bg-white dark:bg-white/[0.03] border-zinc-200 dark:border-white/10 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/[0.06] shadow-sm dark:shadow-none'
              }`}
          >
            Unlocked (1–{maxAllowedTerm})
          </button>
          {[1, 2, 3, 4].map((year) => (
            <button
              key={year}
              onClick={() => setSelectedFilter(year as YearFilter)}
              className={`px-3 py-1.5 rounded-lg border font-medium transition-all shrink-0 flex items-center gap-1.5 ${selectedFilter === year
                  ? 'bg-blue-600 border-blue-500 text-white shadow-sm'
                  : 'bg-white dark:bg-white/[0.03] border-zinc-200 dark:border-white/10 text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/[0.06] shadow-sm dark:shadow-none'
                }`}
            >
              <span>Year {year}</span>
              {year === yearOfStudy && (
                <span className="w-1.5 h-1.5 rounded-full bg-blue-400" title="Your Current Year" />
              )}
            </button>
          ))}
        </div>

        {/* Dynamic Order Selector */}
        <div className="flex items-center gap-2 self-start sm:self-auto shrink-0 text-xs">
          <ArrowUpDown className="w-3.5 h-3.5 text-zinc-500 dark:text-zinc-400" />
          <span className="text-zinc-600 dark:text-zinc-400 font-medium">Order:</span>
          <select
            value={orderMode}
            onChange={(e) => setOrderMode(e.target.value as OrderMode)}
            className="bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-white/10 text-zinc-800 dark:text-zinc-200 rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-blue-500 cursor-pointer shadow-sm dark:shadow-none"
          >
            <option value="standard">Curriculum (1 → 16)</option>
            <option value="current-year-first">My Year First (Year {yearOfStudy})</option>
            <option value="unlocked-first">Unlocked First</option>
            <option value="reverse">Reverse (16 → 1)</option>
          </select>
        </div>
      </div>

      {/* Terms 4x4 Grid (4 cols on lg/xl, 2 cols on tablet, 1 col on mobile) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        {displayedTerms.map((term) => {
          const hasNotes = term.notesCount > 0;
          const isLocked = term.isLocked;

          return (
            <div
              key={term.id}
              onClick={() => handleSelectTerm(term)}
              className={`group relative p-5 rounded-2xl border transition-all duration-200 flex flex-col justify-between min-h-[190px] ${isLocked
                  ? 'border-zinc-200/60 dark:border-white/[0.04] bg-zinc-100/60 dark:bg-black/40 opacity-40 cursor-not-allowed hover:opacity-60'
                  : term.isActiveTerm
                    ? 'border-emerald-500/60 bg-white dark:bg-blue-500/[0.03] hover:border-emerald-500/80 hover:shadow-xl hover:shadow-emerald-500/10 cursor-pointer ring-1 ring-emerald-500/30'
                  : term.isCurrentYear
                    ? 'border-blue-500/40 bg-white dark:bg-blue-500/[0.03] hover:border-blue-500/60 hover:shadow-xl hover:shadow-blue-500/10 cursor-pointer ring-1 ring-blue-500/20'
                    : hasNotes
                      ? 'border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.02] hover:bg-zinc-50 dark:hover:bg-white/[0.05] hover:border-zinc-300 dark:hover:border-white/20 hover:shadow-xl cursor-pointer shadow-sm dark:shadow-none'
                      : 'border-zinc-200/60 dark:border-white/5 bg-zinc-50 dark:bg-black/20 opacity-70 hover:opacity-100 hover:border-zinc-300 dark:hover:border-white/10 cursor-pointer'
                }`}
            >
              <div>
                {/* Card Top: Year/Term Label & Lock/Notes Count */}
                <div className="flex items-center justify-between mb-3.5">
                  <div className="flex items-center gap-1.5">
                    <span
                      className={`text-[11px] font-mono font-semibold uppercase tracking-wider px-2 py-0.5 rounded border ${isLocked
                          ? 'text-zinc-500 bg-zinc-100 dark:bg-white/[0.02] border-zinc-200 dark:border-white/5'
                          : term.isCurrentYear || term.isActiveTerm
                            ? 'text-blue-700 dark:text-blue-300 bg-blue-500/10 dark:bg-blue-500/20 border-blue-500/30 font-bold'
                            : 'text-zinc-700 dark:text-zinc-300 bg-zinc-100 dark:bg-white/5 border-zinc-200 dark:border-white/10'
                        }`}
                    >
                      Y{term.yearNumber} • T{term.termInYear}
                    </span>

                    {term.isActiveTerm ? (
                      <span className="text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-700 dark:text-blue-300 border border-blue-500/30 font-bold">
                        Current Term
                      </span>
                    ) : term.isCurrentYear && !isLocked ? (
                      <span className="text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20">
                        Current Year
                      </span>
                    ) : null}
                  </div>

                  {isLocked ? (
                    <span className="flex items-center gap-1 text-[11px] text-zinc-400 dark:text-zinc-500 font-mono">
                      <Lock className="w-3 h-3 text-zinc-400 dark:text-zinc-500" />
                      <span>Locked</span>
                    </span>
                  ) : (
                    <span className="text-[11px] text-zinc-500 dark:text-zinc-400 font-mono">
                      {term.notesCount} {term.notesCount === 1 ? 'note' : 'notes'}
                    </span>
                  )}
                </div>

                {/* Term Name Header */}
                <div className="flex items-center gap-2">
                  <h3
                    className={`text-lg sm:text-xl font-bold tracking-tight transition-colors ${isLocked
                        ? 'text-zinc-400 dark:text-zinc-500'
                        : term.isCurrentYear || term.isActiveTerm
                          ? 'text-zinc-900 dark:text-blue-100 group-hover:text-blue-600 dark:group-hover:text-white'
                          : 'text-zinc-900 dark:text-zinc-100 group-hover:text-blue-600 dark:group-hover:text-white'
                      }`}
                  >
                    {term.name}
                  </h3>
                  {isLocked && <Lock className="w-3.5 h-3.5 text-zinc-400 dark:text-zinc-500" />}
                </div>

                {/* Subject Badges */}
                <div className="flex flex-wrap gap-1.5 mt-2.5">
                  {isLocked ? (
                    <span className="text-[11px] text-zinc-400 dark:text-zinc-500 italic">
                      Unlocked in Year {term.yearNumber}
                    </span>
                  ) : term.subjects.length > 0 ? (
                    <>
                      {term.subjects.slice(0, 3).map((s) => (
                        <span
                          key={s}
                          className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-white/5 border border-zinc-200 dark:border-white/10 text-zinc-700 dark:text-zinc-300"
                        >
                          {s}
                        </span>
                      ))}
                      {term.subjects.length > 3 && (
                        <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-white/5 border border-zinc-200 dark:border-white/10 text-zinc-500 dark:text-zinc-400">
                          +{term.subjects.length - 3} more
                        </span>
                      )}
                    </>
                  ) : (
                    <span className="text-[11px] text-zinc-400 dark:text-zinc-500 italic">No notes uploaded yet</span>
                  )}
                </div>
              </div>

              {/* Bottom Card Action */}
              <div className="mt-4 pt-3 border-t border-zinc-100 dark:border-white/[0.06] flex items-center justify-between text-xs font-medium">
                {isLocked ? (
                  <span className="text-zinc-400 dark:text-zinc-500 flex items-center gap-1.5 font-mono text-[11px]">
                    <Lock className="w-3 h-3" />
                    <span>Future Curriculum</span>
                  </span>
                ) : (
                  <>
                    <span
                      className={`transition-colors ${term.isCurrentYear || term.isActiveTerm
                          ? 'text-blue-600 dark:text-blue-400 group-hover:text-blue-700 dark:group-hover:text-blue-300'
                          : 'text-zinc-500 dark:text-zinc-400 group-hover:text-blue-600 dark:group-hover:text-blue-400'
                        }`}
                    >
                      {hasNotes ? 'Explore notes' : 'View term'}
                    </span>
                    <ArrowRight
                      className={`w-3.5 h-3.5 transition-all group-hover:translate-x-1 ${term.isCurrentYear || term.isActiveTerm
                          ? 'text-blue-600 dark:text-blue-400 group-hover:text-blue-700 dark:group-hover:text-blue-300'
                          : 'text-zinc-500 dark:text-zinc-400 group-hover:text-blue-600 dark:group-hover:text-blue-400'
                        }`}
                    />
                  </>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
