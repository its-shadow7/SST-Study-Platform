import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { Quiz, QuizQuestion } from '@/types/note';
import { api } from '@/services/apiClient';
import { useAuth } from '@/context/AuthContext';
import { QuizMarkdown } from './QuizMarkdown';
import {
  CheckCircle2,
  XCircle,
  Award,
  RotateCcw,
  ChevronRight,
  ChevronLeft,
  Clock,
  Sparkles,
  BookOpen,
  AlertTriangle,
  X,
  Keyboard,
  Target,
  Check,
} from 'lucide-react';
import { toast } from 'sonner';

interface QuizSectionProps {
  quiz: Quiz;
  noteId?: string;
  onSwitchToNotes?: () => void;
}

interface SavedQuizAttempt {
  note_id: string;
  selected_answers: Record<string, string[]>;
  checked_questions: Record<string, boolean>;
  is_completed: boolean;
  score: number;
  total_questions: number;
  percentage: number;
}

export const QuizSection: React.FC<QuizSectionProps> = ({
  quiz,
  noteId,
  onSwitchToNotes,
}) => {
  const { user } = useAuth();

  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string[]>>({});
  const [checkedQuestions, setCheckedQuestions] = useState<Record<string, boolean>>({});
  const [isCompleted, setIsCompleted] = useState<boolean>(false);
  const [isLoadingSaved, setIsLoadingSaved] = useState<boolean>(Boolean(noteId));
  const [showResetModal, setShowResetModal] = useState<boolean>(false);
  const [isResetting, setIsResetting] = useState<boolean>(false);

  const totalQuestions = quiz.questions.length;
  const currentQ: QuizQuestion = quiz.questions[currentIndex] || quiz.questions[0];
  const currentSelected = selectedAnswers[currentQ.id] || [];
  const isChecked = checkedQuestions[currentQ.id] || false;

  // ---------------------------------------------------------------------------
  // Check correctness of any given question
  // ---------------------------------------------------------------------------
  const isQuestionCorrect = useCallback(
    (qId: string, answersMap = selectedAnswers) => {
      const q = quiz.questions.find((item) => item.id === qId);
      if (!q) return false;
      const userAns = answersMap[qId] || [];
      const correctAns = q.correctOptionIds || [];
      return (
        userAns.length === correctAns.length &&
        userAns.every((id) => correctAns.includes(id))
      );
    },
    [quiz.questions, selectedAnswers]
  );

  // Live Score Statistics (for checked questions)
  const { checkedCount, correctCount, liveAccuracy } = useMemo(() => {
    let checked = 0;
    let correct = 0;
    quiz.questions.forEach((q) => {
      if (checkedQuestions[q.id]) {
        checked++;
        if (isQuestionCorrect(q.id)) {
          correct++;
        }
      }
    });
    const acc = checked > 0 ? Math.round((correct / checked) * 100) : 0;
    return { checkedCount: checked, correctCount: correct, liveAccuracy: acc };
  }, [quiz.questions, checkedQuestions, isQuestionCorrect]);

  // Overall Score Calculation (all questions)
  const calculateFinalScore = useCallback(
    (answersMap = selectedAnswers) => {
      let count = 0;
      quiz.questions.forEach((q) => {
        if (isQuestionCorrect(q.id, answersMap)) {
          count++;
        }
      });
      return count;
    },
    [quiz.questions, isQuestionCorrect]
  );

  // ---------------------------------------------------------------------------
  // Database Sync: Load previous attempt on mount
  // ---------------------------------------------------------------------------
  useEffect(() => {
    if (!noteId || !user) {
      setIsLoadingSaved(false);
      return;
    }

    let isMounted = true;
    api
      .get<SavedQuizAttempt>(`/api/notes/${encodeURIComponent(noteId)}/quiz/attempt`)
      .then((attempt) => {
        if (!isMounted || !attempt) return;

        const savedAnswers = attempt.selected_answers || {};
        const savedChecked = attempt.checked_questions || {};
        const savedCompleted = Boolean(attempt.is_completed);

        setSelectedAnswers(savedAnswers);
        setCheckedQuestions(savedChecked);
        setIsCompleted(savedCompleted);

        // Resume at first unanswered/unchecked question (if not already completed)
        if (!savedCompleted) {
          const firstUncheckedIdx = quiz.questions.findIndex((q) => !savedChecked[q.id]);
          if (firstUncheckedIdx >= 0) {
            setCurrentIndex(firstUncheckedIdx);
          }
        }
      })
      .catch((err) => {
        console.warn('Could not load saved quiz attempt from server:', err);
      })
      .finally(() => {
        if (isMounted) setIsLoadingSaved(false);
      });

    return () => {
      isMounted = false;
    };
  }, [noteId, user, quiz.questions]);

  // ---------------------------------------------------------------------------
  // Database Sync: Persist attempt on progress change
  // ---------------------------------------------------------------------------
  const persistAttempt = useCallback(
    async (
      newAnswers: Record<string, string[]>,
      newChecked: Record<string, boolean>,
      newCompleted: boolean
    ) => {
      if (!noteId || !user) return;

      let score = 0;
      quiz.questions.forEach((q) => {
        const ans = newAnswers[q.id] || [];
        const correct = q.correctOptionIds || [];
        if (ans.length === correct.length && ans.every((id) => correct.includes(id))) {
          score++;
        }
      });

      const percentage = totalQuestions > 0 ? Math.round((score / totalQuestions) * 100) : 0;

      try {
        await api.put(`/api/notes/${encodeURIComponent(noteId)}/quiz/attempt`, {
          selected_answers: newAnswers,
          checked_questions: newChecked,
          is_completed: newCompleted,
          score,
          total_questions: totalQuestions,
          percentage,
        });
      } catch (err) {
        console.error('Failed to sync quiz attempt to database:', err);
      }
    },
    [noteId, user, quiz.questions, totalQuestions]
  );

  // ---------------------------------------------------------------------------
  // Option Selection Handler
  // ---------------------------------------------------------------------------
  const handleSelectOption = (optId: string) => {
    if (isChecked) return; // Cannot change after checking

    if (currentQ.type === 'single_choice') {
      setSelectedAnswers((prev) => {
        const current = prev[currentQ.id] || [];
        if (current.includes(optId)) {
          // Deselect if already selected
          const next = { ...prev };
          delete next[currentQ.id];
          return next;
        }
        return {
          ...prev,
          [currentQ.id]: [optId],
        };
      });
    } else {
      setSelectedAnswers((prev) => {
        const existing = prev[currentQ.id] || [];
        const next = existing.includes(optId)
          ? existing.filter((id) => id !== optId)
          : [...existing, optId];
        return {
          ...prev,
          [currentQ.id]: next,
        };
      });
    }
  };

  // ---------------------------------------------------------------------------
  // Check Answer Handler
  // ---------------------------------------------------------------------------
  const handleCheckAnswer = () => {
    if (currentSelected.length === 0) return;

    const nextChecked = {
      ...checkedQuestions,
      [currentQ.id]: true,
    };
    setCheckedQuestions(nextChecked);

    // Auto-persist immediately
    void persistAttempt(selectedAnswers, nextChecked, isCompleted);
  };

  // ---------------------------------------------------------------------------
  // Reset Current Question (Try Again)
  // ---------------------------------------------------------------------------
  const handleResetCurrentQuestion = () => {
    setSelectedAnswers((prev) => {
      const next = { ...prev };
      delete next[currentQ.id];
      return next;
    });

    const nextChecked = { ...checkedQuestions };
    delete nextChecked[currentQ.id];
    setCheckedQuestions(nextChecked);

    // If quiz was marked completed, mark it back to active
    if (isCompleted) {
      setIsCompleted(false);
    }

    const updatedAnswers = { ...selectedAnswers };
    delete updatedAnswers[currentQ.id];
    void persistAttempt(updatedAnswers, nextChecked, false);
    toast.info(`Question ${currentIndex + 1} reset. You can try again.`);
  };

  // ---------------------------------------------------------------------------
  // Reset Entire Topic Quiz (Modal Triggered)
  // ---------------------------------------------------------------------------
  const handleConfirmResetEntireQuiz = async () => {
    setIsResetting(true);
    try {
      if (noteId && user) {
        await api.delete(`/api/notes/${encodeURIComponent(noteId)}/quiz/attempt`);
      }
      setSelectedAnswers({});
      setCheckedQuestions({});
      setCurrentIndex(0);
      setIsCompleted(false);
      setShowResetModal(false);
      toast.success('All questions in this topic quiz have been reset.');
    } catch (err: any) {
      toast.error(err?.message || 'Failed to reset quiz. Please try again.');
    } finally {
      setIsResetting(false);
    }
  };

  // ---------------------------------------------------------------------------
  // Navigation: Next & Previous
  // ---------------------------------------------------------------------------
  const handleNext = () => {
    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      setIsCompleted(true);
      void persistAttempt(selectedAnswers, checkedQuestions, true);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  const handleRetakeFromSummary = () => {
    setShowResetModal(true);
  };

  // ---------------------------------------------------------------------------
  // Keyboard Shortcuts Support
  // ---------------------------------------------------------------------------
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ignore if focus is in an input, textarea, or contentEditable element
      const target = e.target as HTMLElement;
      if (
        target.tagName === 'INPUT' ||
        target.tagName === 'TEXTAREA' ||
        target.isContentEditable ||
        showResetModal
      ) {
        return;
      }

      // Strictly ignore any shortcut if Ctrl, Meta (Cmd), or Alt is pressed (e.g. Ctrl+C)
      if (e.ctrlKey || e.metaKey || e.altKey) {
        return;
      }

      const key = e.key.toLowerCase();

      // Enter to Check Answer or Next Question
      if (e.key === 'Enter') {
        e.preventDefault();
        if (!isChecked && currentSelected.length > 0) {
          handleCheckAnswer();
        } else if (isChecked) {
          handleNext();
        }
        return;
      }

      // Arrow navigation
      if (e.key === 'ArrowLeft' && currentIndex > 0) {
        e.preventDefault();
        handlePrev();
        return;
      }
      if (e.key === 'ArrowRight' && currentIndex < totalQuestions - 1) {
        e.preventDefault();
        handleNext();
        return;
      }

      // 'R' key to retry / reset current question when checked
      if (key === 'r' && isChecked) {
        e.preventDefault();
        handleResetCurrentQuestion();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [
    isChecked,
    currentSelected,
    currentQ,
    currentIndex,
    totalQuestions,
    showResetModal,
    handleCheckAnswer,
    handleNext,
    handlePrev,
    handleResetCurrentQuestion,
  ]);

  // Difficulty badge styling
  const getDifficultyBadge = (diff: string) => {
    switch (diff) {
      case 'easy':
        return (
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Easy
          </span>
        );
      case 'hard':
        return (
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
            Hard
          </span>
        );
      case 'medium':
      default:
        return (
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            Medium
          </span>
        );
    }
  };

  // ---------------------------------------------------------------------------
  // View 1: Quiz Completed / Review Screen
  // ---------------------------------------------------------------------------
  if (isCompleted) {
    const finalScore = calculateFinalScore();
    const percentage = totalQuestions > 0 ? Math.round((finalScore / totalQuestions) * 100) : 0;

    return (
      <div className="max-w-3xl mx-auto py-6 px-4 animate-in fade-in duration-300">
        <div className="bg-[#0c0c0f] border border-white/10 rounded-2xl p-8 shadow-2xl text-center relative overflow-hidden">
          <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500" />

          <div className="inline-flex p-4 rounded-2xl bg-blue-500/10 text-blue-400 mb-4 border border-blue-500/20 shadow-inner">
            <Award className="w-12 h-12" />
          </div>
          <h2 className="text-3xl font-bold tracking-tight text-zinc-100 mb-2">Topic Quiz Completed!</h2>
          <p className="text-zinc-400 text-sm max-w-md mx-auto mb-6">
            You scored <span className="font-bold text-zinc-100">{finalScore}</span> out of{' '}
            <span className="font-bold text-zinc-100">{totalQuestions}</span> questions ({percentage}%).
            Your progress is saved to your student profile.
          </p>

          <div className="grid grid-cols-3 gap-3 max-w-md mx-auto mb-8">
            <div className="p-4 rounded-xl bg-white/[0.03] border border-white/[0.08]">
              <div className="text-2xl font-bold text-emerald-400">{finalScore}</div>
              <div className="text-xs text-zinc-400 mt-1">Correct</div>
            </div>
            <div className="p-4 rounded-xl bg-white/[0.03] border border-white/[0.08]">
              <div className="text-2xl font-bold text-rose-400">{totalQuestions - finalScore}</div>
              <div className="text-xs text-zinc-400 mt-1">Incorrect</div>
            </div>
            <div className="p-4 rounded-xl bg-white/[0.03] border border-white/[0.08]">
              <div className="text-2xl font-bold text-blue-400">{percentage}%</div>
              <div className="text-xs text-zinc-400 mt-1">Accuracy</div>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3">
            <button
              onClick={() => {
                setIsCompleted(false);
                setCurrentIndex(0);
              }}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 text-white font-semibold text-xs hover:bg-blue-500 transition-colors shadow-lg shadow-blue-500/20"
            >
              <span>Review Questions</span>
              <ChevronRight className="w-4 h-4" />
            </button>
            <button
              onClick={handleRetakeFromSummary}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-zinc-200 font-semibold text-xs transition-colors"
            >
              <RotateCcw className="w-4 h-4 text-zinc-400" />
              <span>Reset Entire Quiz</span>
            </button>
            {onSwitchToNotes && (
              <button
                onClick={onSwitchToNotes}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-zinc-300 font-semibold text-xs transition-colors"
              >
                <BookOpen className="w-4 h-4" />
                <span>Back to Notes</span>
              </button>
            )}
          </div>
        </div>

        {/* Detailed Question Review List */}
        <div className="mt-10 space-y-4">
          <div className="flex items-center justify-between pb-2 border-b border-white/[0.08]">
            <h3 className="text-base font-bold text-zinc-100">Question-by-Question Audit</h3>
            <span className="text-xs text-zinc-400 font-mono">
              {finalScore}/{totalQuestions} Correct
            </span>
          </div>

          {quiz.questions.map((q, idx) => {
            const userAns = selectedAnswers[q.id] || [];
            const isCorrect =
              userAns.length === q.correctOptionIds.length &&
              userAns.every((id) => q.correctOptionIds.includes(id));

            return (
              <div
                key={q.id}
                className={`p-5 rounded-xl border text-left transition-all ${
                  isCorrect
                    ? 'bg-emerald-500/[0.04] border-emerald-500/30'
                    : 'bg-rose-500/[0.04] border-rose-500/30'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2 text-xs font-semibold text-zinc-400">
                    <span>Q{idx + 1}</span>
                    <span>•</span>
                    {getDifficultyBadge(q.difficulty)}
                    {q.subtopic && (
                      <>
                        <span className="hidden sm:inline">•</span>
                        <span className="hidden sm:inline text-xs text-zinc-400">{q.subtopic}</span>
                      </>
                    )}
                  </div>
                  {isCorrect ? (
                    <span className="flex items-center gap-1.5 text-xs font-semibold text-emerald-400">
                      <CheckCircle2 className="w-4 h-4" /> Correct
                    </span>
                  ) : (
                    <span className="flex items-center gap-1.5 text-xs font-semibold text-rose-400">
                      <XCircle className="w-4 h-4" /> Incorrect
                    </span>
                  )}
                </div>

                <div className="font-semibold text-sm text-zinc-100 mb-3 leading-relaxed">
                  <QuizMarkdown content={q.question} />
                </div>

                <div className="text-xs space-y-2 mb-3">
                  <div className="text-zinc-400 flex flex-wrap items-baseline gap-1.5">
                    <span>Your answer:</span>
                    {userAns.length > 0 ? (
                      <span className="font-semibold text-zinc-200 inline-flex flex-wrap items-center gap-1">
                        {userAns.map((id, uIdx) => (
                          <span key={id} className="inline-flex items-center">
                            {uIdx > 0 && <span className="mr-1 text-zinc-500">,</span>}
                            <QuizMarkdown content={q.options.find((o) => o.id === id)?.text || id} isInline />
                          </span>
                        ))}
                      </span>
                    ) : (
                      <span className="font-semibold text-zinc-400 italic">Not answered</span>
                    )}
                  </div>
                  <div className="text-emerald-400 font-semibold flex flex-wrap items-baseline gap-1.5">
                    <span>Correct answer:</span>
                    <span className="inline-flex flex-wrap items-center gap-1">
                      {q.correctOptionIds.map((id, cIdx) => (
                        <span key={id} className="inline-flex items-center">
                          {cIdx > 0 && <span className="mr-1 text-emerald-500/60">,</span>}
                          <QuizMarkdown content={q.options.find((o) => o.id === id)?.text || id} isInline />
                        </span>
                      ))}
                    </span>
                  </div>
                </div>

                <div className="text-xs p-3 rounded-lg bg-black/40 border border-white/[0.06] text-zinc-300">
                  <span className="font-bold text-zinc-100">Explanation: </span>
                  <QuizMarkdown content={q.explanation} isInline />
                </div>
              </div>
            );
          })}
        </div>

        {/* Confirmation Modal for Reset */}
        {showResetModal && renderResetModal()}
      </div>
    );
  }

  // ---------------------------------------------------------------------------
  // Confirmation Modal Component
  // ---------------------------------------------------------------------------
  function renderResetModal() {
    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
        <div className="w-full max-w-md rounded-2xl bg-[#0c0c0f] border border-white/10 p-6 shadow-2xl space-y-5 text-left">
          <div className="flex items-center justify-between pb-3 border-b border-white/[0.08]">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 flex items-center justify-center shrink-0">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-zinc-100">Reset Entire Topic Quiz?</h3>
            </div>
            <button
              onClick={() => setShowResetModal(false)}
              className="p-1 rounded-lg text-zinc-400 hover:text-zinc-200 hover:bg-white/5 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <p className="text-xs text-zinc-400 leading-relaxed">
            This will permanently clear your answers, scores, and saved question history for this
            lecture note. You will start over fresh from Question 1.
          </p>

          <div className="flex items-center justify-end gap-2.5 pt-2">
            <button
              onClick={() => setShowResetModal(false)}
              disabled={isResetting}
              className="px-4 py-2 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-xs font-semibold text-zinc-300 transition-colors"
            >
              Cancel
            </button>
            <button
              onClick={handleConfirmResetEntireQuiz}
              disabled={isResetting}
              className="flex items-center gap-2 px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-xs font-semibold text-white transition-colors shadow-lg shadow-rose-600/20"
            >
              <RotateCcw className={`w-3.5 h-3.5 ${isResetting ? 'animate-spin' : ''}`} />
              <span>{isResetting ? 'Resetting...' : 'Yes, Reset All Questions'}</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ---------------------------------------------------------------------------
  // View 2: Active Question Card View
  // ---------------------------------------------------------------------------
  const isCurrentQuestionCorrect = isChecked && isQuestionCorrect(currentQ.id);

  return (
    <div className="max-w-3xl mx-auto py-6 px-4 animate-in fade-in duration-300">
      {/* Compact Top Bar (Removed bulky Topic Quiz, title, description, and 30 mins) */}
      <div className="mb-4 flex items-center justify-between gap-3 pb-3 border-b border-white/[0.08]">
        <div className="flex items-center gap-2">
          {checkedCount > 0 ? (
            <span className="flex items-center gap-1.5 text-xs font-mono px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300">
              <Target className="w-3.5 h-3.5 text-emerald-400" />
              <span className="font-bold">{correctCount}/{checkedCount} Correct</span>
              <span className="text-emerald-500/60">•</span>
              <span>{liveAccuracy}%</span>
            </span>
          ) : (
            <span className="text-xs font-semibold text-zinc-400 font-mono">
              {totalQuestions} Questions
            </span>
          )}
        </div>

        <div className="flex items-center gap-2 shrink-0">
          {/* Reset Entire Topic Quiz Button */}
          <button
            onClick={() => setShowResetModal(true)}
            title="Reset all questions in this quiz"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-white/10 bg-white/5 hover:bg-rose-500/10 hover:border-rose-500/30 hover:text-rose-300 text-xs font-semibold text-zinc-400 transition-all"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Reset Quiz</span>
            <span className="sm:hidden">Reset</span>
          </button>

          {onSwitchToNotes && (
            <button
              onClick={onSwitchToNotes}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 text-xs font-semibold text-zinc-300 transition-colors"
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>Notes</span>
            </button>
          )}
        </div>
      </div>

      {/* Progress Bar & Numbered Question Dots */}
      <div className="mb-6 space-y-3">
        <div className="flex items-center justify-between text-xs text-zinc-400 font-mono">
          <span>Question {currentIndex + 1} of {totalQuestions}</span>
          <span>{Math.round(((currentIndex + 1) / totalQuestions) * 100)}% Traversed</span>
        </div>
        <div className="w-full h-1.5 bg-zinc-800 rounded-full overflow-hidden">
          <div
            className="h-full bg-blue-500 transition-all duration-300 rounded-full"
            style={{ width: `${((currentIndex + 1) / totalQuestions) * 100}%` }}
          />
        </div>

        {/* Numbered Dots (Color-coded: Green = Correct, Red = Incorrect, Blue Ring = Active) */}
        <div className="flex flex-wrap gap-1.5 pt-1">
          {quiz.questions.map((q, idx) => {
            const hasAnswer = (selectedAnswers[q.id] || []).length > 0;
            const isCheckedQ = checkedQuestions[q.id];
            const isCurrent = idx === currentIndex;
            const isCorrect = isQuestionCorrect(q.id);

            let dotColor = 'bg-white/[0.04] text-zinc-400 border-white/[0.06] hover:bg-white/10';

            if (isCheckedQ) {
              if (isCorrect) {
                // Correct -> Green dot
                dotColor = 'bg-emerald-500/20 text-emerald-400 border-emerald-500/60 font-bold hover:bg-emerald-500/30';
              } else {
                // Incorrect -> Red dot
                dotColor = 'bg-rose-500/20 text-rose-400 border-rose-500/60 font-bold hover:bg-rose-500/30';
              }
            } else if (hasAnswer) {
              // Answered but unchecked
              dotColor = 'bg-blue-500/20 text-blue-300 border-blue-500/40 font-medium';
            }

            // Current Question Accent Ring
            const ringStyle = isCurrent
              ? 'ring-2 ring-blue-500 ring-offset-2 ring-offset-[#09090b] shadow-md z-10 scale-105'
              : '';

            return (
              <button
                key={q.id}
                onClick={() => setCurrentIndex(idx)}
                aria-label={`Jump to question ${idx + 1}`}
                className={`w-7 h-7 text-xs rounded-lg border flex items-center justify-center transition-all ${dotColor} ${ringStyle}`}
              >
                {idx + 1}
              </button>
            );
          })}
        </div>
      </div>

      {/* Active Question Card */}
      <div className="bg-[#0c0c0f] border border-white/10 rounded-2xl p-6 sm:p-8 shadow-xl relative">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-4">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-zinc-300 font-mono">
              Question {currentIndex + 1}
            </span>
            <span className="text-zinc-600">•</span>
            {getDifficultyBadge(currentQ.difficulty)}
            {currentQ.subtopic && (
              <>
                <span className="hidden sm:inline text-zinc-600">•</span>
                <span className="hidden sm:inline text-xs text-zinc-400 font-mono">{currentQ.subtopic}</span>
              </>
            )}
          </div>

          <div className="flex items-center gap-2">
            <span className="text-[11px] px-2.5 py-0.5 rounded-md bg-white/[0.04] border border-white/[0.08] text-zinc-400 font-mono">
              {currentQ.type === 'single_choice' ? 'Single Choice' : 'Multiple Choice (Select all)'}
            </span>

            {/* Reset Current Question button (Visible when checked) */}
            {isChecked && (
              <button
                onClick={handleResetCurrentQuestion}
                title="Reset this question to attempt it again"
                className="flex items-center gap-1 px-2.5 py-0.5 rounded-md border border-white/10 bg-white/5 hover:bg-white/10 text-[11px] font-semibold text-zinc-300 transition-colors"
              >
                <RotateCcw className="w-3 h-3 text-zinc-400" />
                <span>Try Again</span>
              </button>
            )}
          </div>
        </div>

        <div className="text-base sm:text-lg font-semibold text-zinc-100 mb-6 leading-relaxed">
          <QuizMarkdown content={currentQ.question} />
        </div>

        {/* Options List */}
        <div className="space-y-3 mb-6">
          {currentQ.options.map((opt) => {
            const isSelected = currentSelected.includes(opt.id);
            const isCorrectOption = currentQ.correctOptionIds.includes(opt.id);

            let optionStyle = 'bg-white/[0.02] border-white/10 hover:bg-white/[0.05] text-zinc-200';

            if (isChecked) {
              if (isCorrectOption) {
                optionStyle = 'bg-emerald-500/10 border-emerald-500/60 text-emerald-300 font-semibold shadow-sm';
              } else if (isSelected && !isCorrectOption) {
                optionStyle = 'bg-rose-500/10 border-rose-500/60 text-rose-300';
              } else {
                optionStyle = 'bg-white/[0.01] border-white/[0.06] text-zinc-500 opacity-60';
              }
            } else if (isSelected) {
              optionStyle = 'bg-blue-500/15 border-blue-500 text-blue-200 font-semibold ring-1 ring-blue-500';
            }

            return (
              <button
                key={opt.id}
                onClick={() => handleSelectOption(opt.id)}
                disabled={isChecked}
                className={`w-full p-4 rounded-xl border text-left flex items-start gap-3 transition-all ${optionStyle}`}
              >
                {/* Circular Radio or Checkbox Indicator (No Letters) */}
                <div
                  className={`w-5 h-5 ${
                    currentQ.type === 'single_choice' ? 'rounded-full' : 'rounded-md'
                  } flex items-center justify-center shrink-0 mt-0.5 border transition-all ${
                    isChecked && isCorrectOption
                      ? 'bg-emerald-500 border-emerald-500 text-white shadow-sm shadow-emerald-500/30'
                      : isChecked && isSelected && !isCorrectOption
                      ? 'bg-rose-500 border-rose-500 text-white shadow-sm shadow-rose-500/30'
                      : isSelected
                      ? 'bg-blue-600 border-blue-500 text-white shadow-sm shadow-blue-500/30'
                      : 'border-white/20 bg-white/[0.04]'
                  }`}
                >
                  {isChecked && isCorrectOption ? (
                    <Check className="w-3.5 h-3.5 stroke-[3]" />
                  ) : isChecked && isSelected && !isCorrectOption ? (
                    <X className="w-3.5 h-3.5 stroke-[3]" />
                  ) : isSelected ? (
                    currentQ.type === 'single_choice' ? (
                      <div className="w-2 h-2 rounded-full bg-white" />
                    ) : (
                      <Check className="w-3.5 h-3.5 stroke-[3]" />
                    )
                  ) : null}
                </div>
                <div className="text-sm leading-relaxed flex-1">
                  <QuizMarkdown content={opt.text} isInline />
                </div>
                {isChecked && isCorrectOption && (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                )}
                {isChecked && isSelected && !isCorrectOption && (
                  <XCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
                )}
              </button>
            );
          })}
        </div>

        {/* Explanation Card (Revealed after check) */}
        {isChecked && (
          <div
            className={`p-4 rounded-xl border text-sm mb-6 animate-in fade-in slide-in-from-top-2 duration-200 ${
              isCurrentQuestionCorrect
                ? 'bg-emerald-500/[0.06] border-emerald-500/30'
                : 'bg-rose-500/[0.06] border-rose-500/30'
            }`}
          >
            <div className="flex items-center justify-between mb-1.5">
              <div className="flex items-center gap-1.5 font-bold text-zinc-100">
                <Sparkles className="w-4 h-4 text-blue-400" />
                <span>Explanation</span>
              </div>
              {!isCurrentQuestionCorrect && (
                <button
                  onClick={handleResetCurrentQuestion}
                  className="inline-flex items-center gap-1 text-xs font-semibold text-rose-300 hover:text-white underline underline-offset-2 transition-colors"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>Try this question again</span>
                </button>
              )}
            </div>
            <div className="text-xs sm:text-sm text-zinc-300 leading-relaxed font-sans">
              <QuizMarkdown content={currentQ.explanation} />
            </div>
          </div>
        )}

        {/* Footer Navigation & Actions */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-4 border-t border-white/[0.08]">
          <div className="flex items-center gap-2 w-full sm:w-auto justify-between sm:justify-start">
            <button
              onClick={handlePrev}
              disabled={currentIndex === 0}
              className="inline-flex items-center gap-1 px-4 py-2 rounded-xl border border-white/10 bg-white/5 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-white/10 text-xs font-semibold text-zinc-300 transition-colors"
            >
              <ChevronLeft className="w-4 h-4" /> Previous
            </button>

            {isChecked && (
              <button
                onClick={handleResetCurrentQuestion}
                className="sm:hidden inline-flex items-center gap-1 px-3 py-2 rounded-xl border border-white/10 bg-white/5 text-xs font-semibold text-zinc-300"
              >
                <RotateCcw className="w-3.5 h-3.5 text-zinc-400" />
                <span>Retry</span>
              </button>
            )}
          </div>

          <div className="flex items-center gap-2 w-full sm:w-auto justify-end">
            {!isChecked ? (
              <button
                onClick={handleCheckAnswer}
                disabled={currentSelected.length === 0}
                className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-blue-600 text-white font-semibold text-xs disabled:opacity-40 disabled:cursor-not-allowed hover:bg-blue-500 transition-all shadow-lg shadow-blue-600/20"
              >
                Check Answer
              </button>
            ) : (
              <button
                onClick={handleNext}
                className="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-6 py-2.5 rounded-xl bg-blue-600 text-white font-semibold text-xs hover:bg-blue-500 transition-all shadow-lg shadow-blue-600/20"
              >
                <span>{currentIndex === totalQuestions - 1 ? 'View Results' : 'Next Question'}</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        {/* Keyboard Shortcut Cheatsheet Hint */}
        <div className="hidden sm:flex items-center justify-center gap-2 pt-4 mt-2 border-t border-white/[0.04] text-[11px] text-zinc-500 font-mono select-none">
          <Keyboard className="w-3.5 h-3.5 text-zinc-600" />
          <span>Shortcuts:</span>
          <span className="text-zinc-400">[Enter] Check / Next</span>
          <span>•</span>
          <span className="text-zinc-400">[← / →] Navigate</span>
          {isChecked && (
            <>
              <span>•</span>
              <span className="text-zinc-400">[R] Retry</span>
            </>
          )}
        </div>
      </div>

      {/* Confirmation Modal for Reset Entire Topic Quiz */}
      {showResetModal && renderResetModal()}
    </div>
  );
};
