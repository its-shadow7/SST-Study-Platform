import React, { useState } from 'react';
import { Quiz, QuizQuestion } from '@/types/note';
import {
  CheckCircle2,
  XCircle,
  HelpCircle,
  Award,
  RotateCcw,
  ChevronRight,
  ChevronLeft,
  Clock,
  Sparkles,
  BookOpen
} from 'lucide-react';

interface QuizSectionProps {
  quiz: Quiz;
  onSwitchToNotes?: () => void;
}

export const QuizSection: React.FC<QuizSectionProps> = ({ quiz, onSwitchToNotes }) => {
  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string[]>>({});
  const [checkedQuestions, setCheckedQuestions] = useState<Record<string, boolean>>({});
  const [isCompleted, setIsCompleted] = useState<boolean>(false);

  const currentQ: QuizQuestion = quiz.questions[currentIndex] || quiz.questions[0];
  const totalQuestions = quiz.questions.length;

  const currentSelected = selectedAnswers[currentQ.id] || [];
  const isChecked = checkedQuestions[currentQ.id] || false;

  const handleSelectOption = (optId: string) => {
    if (isChecked) return; // Prevent changing after checking answer

    if (currentQ.type === 'single_choice') {
      setSelectedAnswers((prev) => ({
        ...prev,
        [currentQ.id]: [optId],
      }));
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

  const handleCheckAnswer = () => {
    if (currentSelected.length === 0) return;
    setCheckedQuestions((prev) => ({
      ...prev,
      [currentQ.id]: true,
    }));
  };

  const handleNext = () => {
    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex((prev) => prev + 1);
    } else {
      setIsCompleted(true);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  const handleRestart = () => {
    setSelectedAnswers({});
    setCheckedQuestions({});
    setCurrentIndex(0);
    setIsCompleted(false);
  };

  // Compute Score
  const calculateScore = () => {
    let correctCount = 0;
    quiz.questions.forEach((q) => {
      const selected = selectedAnswers[q.id] || [];
      const correct = q.correctOptionIds || [];
      if (
        selected.length === correct.length &&
        selected.every((id) => correct.includes(id))
      ) {
        correctCount++;
      }
    });
    return correctCount;
  };

  const score = calculateScore();
  const percentage = Math.round((score / totalQuestions) * 100);

  // Difficulty badge styling
  const getDifficultyBadge = (diff: string) => {
    switch (diff) {
      case 'easy':
        return (
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">
            Easy
          </span>
        );
      case 'hard':
        return (
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-500 border border-rose-500/20">
            Hard
          </span>
        );
      case 'medium':
      default:
        return (
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-500 border border-amber-500/20">
            Medium
          </span>
        );
    }
  };

  if (isCompleted) {
    return (
      <div className="max-w-3xl mx-auto py-10 px-4">
        <div className="bg-card border border-border rounded-2xl p-8 shadow-xl text-center">
          <div className="inline-flex p-4 rounded-full bg-primary/10 text-primary mb-4">
            <Award className="w-12 h-12" />
          </div>
          <h2 className="text-3xl font-bold tracking-tight mb-2">Quiz Completed!</h2>
          <p className="text-muted-foreground text-sm max-w-md mx-auto mb-6">
            You scored <span className="font-semibold text-foreground">{score}</span> out of{' '}
            <span className="font-semibold text-foreground">{totalQuestions}</span> questions ({percentage}%).
          </p>

          <div className="grid grid-cols-3 gap-4 max-w-md mx-auto mb-8">
            <div className="p-4 rounded-xl bg-muted/40 border border-border">
              <div className="text-2xl font-bold text-emerald-500">{score}</div>
              <div className="text-xs text-muted-foreground mt-1">Correct</div>
            </div>
            <div className="p-4 rounded-xl bg-muted/40 border border-border">
              <div className="text-2xl font-bold text-rose-500">{totalQuestions - score}</div>
              <div className="text-xs text-muted-foreground mt-1">Incorrect</div>
            </div>
            <div className="p-4 rounded-xl bg-muted/40 border border-border">
              <div className="text-2xl font-bold text-primary">{percentage}%</div>
              <div className="text-xs text-muted-foreground mt-1">Accuracy</div>
            </div>
          </div>

          <div className="flex flex-wrap items-center justify-center gap-3">
            <button
              onClick={handleRestart}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-primary text-primary-foreground font-semibold text-sm hover:opacity-90 transition-opacity"
            >
              <RotateCcw className="w-4 h-4" />
              Retake Quiz
            </button>
            {onSwitchToNotes && (
              <button
                onClick={onSwitchToNotes}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-secondary text-secondary-foreground font-semibold text-sm hover:bg-secondary/80 transition-colors"
              >
                <BookOpen className="w-4 h-4" />
                Back to Notes
              </button>
            )}
          </div>
        </div>

        {/* Detailed Question Review List */}
        <div className="mt-10 space-y-4">
          <h3 className="text-lg font-bold">Review Your Answers</h3>
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
                    ? 'bg-emerald-500/5 border-emerald-500/30'
                    : 'bg-rose-500/5 border-rose-500/30'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2 text-xs font-semibold text-muted-foreground">
                    <span>Q{idx + 1}</span>
                    <span>•</span>
                    {getDifficultyBadge(q.difficulty)}
                  </div>
                  {isCorrect ? (
                    <span className="flex items-center gap-1 text-xs font-semibold text-emerald-500">
                      <CheckCircle2 className="w-4 h-4" /> Correct
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-xs font-semibold text-rose-500">
                      <XCircle className="w-4 h-4" /> Incorrect
                    </span>
                  )}
                </div>
                <p className="font-medium text-sm text-foreground mb-3">{q.question}</p>
                <div className="text-xs space-y-1 mb-3">
                  <div className="text-muted-foreground">
                    Your answer: <span className="font-semibold text-foreground">{userAns.join(', ') || 'None'}</span>
                  </div>
                  <div className="text-emerald-500 font-semibold">
                    Correct answer: {q.correctOptionIds.join(', ')}
                  </div>
                </div>
                <div className="text-xs p-3 rounded-lg bg-background/50 border border-border/50 text-muted-foreground">
                  <span className="font-semibold text-foreground">Explanation: </span>
                  {q.explanation}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  // Active Question Card View
  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      {/* Quiz Header Bar */}
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-border">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="text-xs font-semibold px-2 py-0.5 rounded bg-primary/10 text-primary">
              Topic Quiz
            </span>
            <span className="text-xs text-muted-foreground flex items-center gap-1">
              <Clock className="w-3.5 h-3.5" /> {quiz.estimated_minutes} mins
            </span>
          </div>
          <h2 className="text-xl font-bold tracking-tight text-foreground">{quiz.title}</h2>
          <p className="text-xs text-muted-foreground mt-0.5">{quiz.description}</p>
        </div>

        <div className="flex items-center gap-2">
          {onSwitchToNotes && (
            <button
              onClick={onSwitchToNotes}
              className="px-3 py-1.5 rounded-lg border border-border text-xs font-semibold text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors"
            >
              View Notes
            </button>
          )}
        </div>
      </div>

      {/* Progress Chips Palette */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-xs text-muted-foreground mb-2">
          <span>Question {currentIndex + 1} of {totalQuestions}</span>
          <span>{Math.round(((currentIndex + 1) / totalQuestions) * 100)}% Completed</span>
        </div>
        <div className="w-full h-1.5 bg-muted rounded-full overflow-hidden">
          <div
            className="h-full bg-primary transition-all duration-300"
            style={{ width: `${((currentIndex + 1) / totalQuestions) * 100}%` }}
          />
        </div>

        {/* Question Selector Dots */}
        <div className="flex flex-wrap gap-1.5 mt-3">
          {quiz.questions.map((q, idx) => {
            const hasAnswer = selectedAnswers[q.id]?.length > 0;
            const isCheckedQ = checkedQuestions[q.id];
            const isCurrent = idx === currentIndex;

            let dotColor = 'bg-muted text-muted-foreground border-transparent';
            if (isCurrent) {
              dotColor = 'border-primary ring-2 ring-primary/20 bg-primary/10 text-primary font-bold';
            } else if (isCheckedQ) {
              dotColor = 'bg-emerald-500/10 text-emerald-500 border-emerald-500/30';
            } else if (hasAnswer) {
              dotColor = 'bg-primary/20 text-primary';
            }

            return (
              <button
                key={q.id}
                onClick={() => setCurrentIndex(idx)}
                className={`w-7 h-7 text-xs rounded-lg border flex items-center justify-center transition-all ${dotColor}`}
              >
                {idx + 1}
              </button>
            );
          })}
        </div>
      </div>

      {/* Question Card */}
      <div className="bg-card border border-border rounded-2xl p-6 sm:p-8 shadow-sm">
        <div className="flex items-center justify-between gap-2 mb-4">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-muted-foreground">
              Question {currentIndex + 1}
            </span>
            <span>•</span>
            {getDifficultyBadge(currentQ.difficulty)}
            {currentQ.subtopic && (
              <>
                <span className="hidden sm:inline">•</span>
                <span className="hidden sm:inline text-xs text-muted-foreground">{currentQ.subtopic}</span>
              </>
            )}
          </div>

          <span className="text-xs px-2 py-0.5 rounded bg-muted/60 text-muted-foreground font-medium">
            {currentQ.type === 'single_choice' ? 'Single Choice' : 'Multiple Choice (Select all)'}
          </span>
        </div>

        <h3 className="text-base sm:text-lg font-semibold text-foreground mb-6 leading-relaxed">
          {currentQ.question}
        </h3>

        {/* Options List */}
        <div className="space-y-3 mb-6">
          {currentQ.options.map((opt) => {
            const isSelected = currentSelected.includes(opt.id);
            const isCorrectOption = currentQ.correctOptionIds.includes(opt.id);

            let optionStyle = 'bg-muted/30 border-border hover:bg-muted/60 text-foreground';

            if (isChecked) {
              if (isCorrectOption) {
                optionStyle = 'bg-emerald-500/10 border-emerald-500/60 text-emerald-500 font-semibold';
              } else if (isSelected && !isCorrectOption) {
                optionStyle = 'bg-rose-500/10 border-rose-500/60 text-rose-500';
              } else {
                optionStyle = 'bg-muted/20 border-border/40 text-muted-foreground opacity-60';
              }
            } else if (isSelected) {
              optionStyle = 'bg-primary/10 border-primary text-primary font-semibold ring-1 ring-primary';
            }

            return (
              <button
                key={opt.id}
                onClick={() => handleSelectOption(opt.id)}
                disabled={isChecked}
                className={`w-full p-4 rounded-xl border text-left flex items-start gap-3 transition-all ${optionStyle}`}
              >
                <div
                  className={`w-6 h-6 rounded-lg text-xs font-bold flex items-center justify-center shrink-0 mt-0.5 border transition-colors ${
                    isChecked && isCorrectOption
                      ? 'bg-emerald-500 text-white border-emerald-500'
                      : isChecked && isSelected && !isCorrectOption
                      ? 'bg-rose-500 text-white border-rose-500'
                      : isSelected
                      ? 'bg-primary text-primary-foreground border-primary'
                      : 'border-border bg-background text-muted-foreground'
                  }`}
                >
                  {opt.id}
                </div>
                <div className="text-sm leading-relaxed flex-1">{opt.text}</div>
                {isChecked && isCorrectOption && (
                  <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                )}
                {isChecked && isSelected && !isCorrectOption && (
                  <XCircle className="w-5 h-5 text-rose-500 shrink-0 mt-0.5" />
                )}
              </button>
            );
          })}
        </div>

        {/* Explanation Card (Revealed after check) */}
        {isChecked && (
          <div className="p-4 rounded-xl bg-muted/40 border border-border text-sm mb-6 animate-in fade-in slide-in-from-top-2 duration-200">
            <div className="flex items-center gap-1.5 font-bold text-foreground mb-1">
              <Sparkles className="w-4 h-4 text-primary" />
              <span>Explanation</span>
            </div>
            <p className="text-xs sm:text-sm text-muted-foreground leading-relaxed">
              {currentQ.explanation}
            </p>
          </div>
        )}

        {/* Footer Actions */}
        <div className="flex items-center justify-between pt-4 border-t border-border">
          <button
            onClick={handlePrev}
            disabled={currentIndex === 0}
            className="inline-flex items-center gap-1 px-4 py-2 rounded-xl border border-border text-xs font-semibold disabled:opacity-40 disabled:cursor-not-allowed hover:bg-muted/50 transition-colors"
          >
            <ChevronLeft className="w-4 h-4" /> Previous
          </button>

          <div className="flex items-center gap-2">
            {!isChecked ? (
              <button
                onClick={handleCheckAnswer}
                disabled={currentSelected.length === 0}
                className="px-5 py-2 rounded-xl bg-primary text-primary-foreground font-semibold text-xs disabled:opacity-40 disabled:cursor-not-allowed hover:opacity-90 transition-opacity shadow-sm"
              >
                Check Answer
              </button>
            ) : (
              <button
                onClick={handleNext}
                className="inline-flex items-center gap-1 px-5 py-2 rounded-xl bg-primary text-primary-foreground font-semibold text-xs hover:opacity-90 transition-opacity shadow-sm"
              >
                {currentIndex === totalQuestions - 1 ? 'View Results' : 'Next Question'}
                <ChevronRight className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
