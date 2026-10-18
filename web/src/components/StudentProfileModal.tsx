import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import {
  X,
  Award,
  MessageSquare,
  ThumbsUp,
  ExternalLink,
  Loader2,
  Target,
} from 'lucide-react';
import { api } from '@/services/apiClient';
import { RoleBadge } from './RoleBadge';

export interface PublicUserProfile {
  user_id: string;
  username: string;
  display_name: string;
  avatar_url?: string | null;
  bio?: string | null;
  role: 'student' | 'moderator' | 'admin';
  active_term: number;
  batch_year?: number | null;
  total_comments: number;
  total_upvotes: number;
  badges: string[];
  recent_comments: Array<{
    id: string;
    note_id: string;
    content: string;
    score: number;
    created_at: string;
  }>;
  quiz_stats?: {
    quizzes_attempted: number;
    quizzes_completed: number;
    total_questions_answered: number;
    total_correct: number;
    accuracy: number;
  };
}

interface StudentProfileModalProps {
  username: string | null;
  onClose: () => void;
}

export const StudentProfileModal: React.FC<StudentProfileModalProps> = ({
  username,
  onClose,
}) => {
  const [profile, setProfile] = useState<PublicUserProfile | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!username) return;
    const fetchProfile = async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await api.get<PublicUserProfile>(
          `/api/users/${encodeURIComponent(username)}/profile`
        );
        setProfile(data);
      } catch (err: any) {
        setError(err.message || 'Could not load student profile.');
      } finally {
        setLoading(false);
      }
    };
    void fetchProfile();
  }, [username]);

  // Handle ESC key
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!username) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-150 select-none"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="relative w-full max-w-md overflow-hidden rounded-2xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#09090b] shadow-2xl text-zinc-800 dark:text-zinc-200 animate-in zoom-in-95 duration-150">
        {/* Subtle Banner */}
        <div className="h-20 w-full bg-gradient-to-r from-blue-100 via-indigo-50 to-purple-100 dark:from-blue-950/30 dark:via-zinc-900/50 dark:to-purple-950/20 border-b border-zinc-200 dark:border-white/[0.06] relative">
          <button
            onClick={onClose}
            className="absolute top-2.5 right-2.5 p-1 rounded-md text-zinc-500 hover:text-zinc-800 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:text-zinc-200 dark:hover:bg-white/5 transition-colors"
            aria-label="Close modal"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Profile Content */}
        <div className="p-5 pt-0 space-y-4">
          {/* Avatar & Header row */}
          <div className="flex items-end justify-between -mt-10">
            <div className="w-16 h-16 rounded-xl bg-white dark:bg-zinc-900 border-2 border-white dark:border-white/20 overflow-hidden shadow-lg flex items-center justify-center text-xl font-bold text-zinc-800 dark:text-zinc-100 shrink-0">
              {profile?.avatar_url ? (
                <img
                  src={profile.avatar_url}
                  alt={profile.display_name}
                  className="w-full h-full object-cover"
                />
              ) : (
                <span>{(profile?.display_name || username).charAt(0).toUpperCase()}</span>
              )}
            </div>

            {profile && (
              <button
                onClick={() => {
                  onClose();
                  navigate(`/profile/${profile.username}`);
                }}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-zinc-200 dark:border-white/10 bg-zinc-100 hover:bg-zinc-200 dark:bg-white/5 dark:hover:bg-white/10 text-xs font-medium text-zinc-700 dark:text-zinc-200 transition-colors"
              >
                <span>Full Profile</span>
                <ExternalLink className="w-3.5 h-3.5 text-zinc-500 dark:text-zinc-400" />
              </button>
            )}
          </div>

          {loading ? (
            <div className="flex flex-col items-center justify-center py-10 text-zinc-500 dark:text-zinc-400 gap-2">
              <Loader2 className="w-5 h-5 animate-spin text-blue-500 dark:text-blue-400" />
              <span className="text-xs">Loading student profile...</span>
            </div>
          ) : error ? (
            <div className="py-6 text-center text-zinc-500 dark:text-zinc-400 space-y-2">
              <p className="text-xs text-rose-500 dark:text-rose-400">{error}</p>
              <button
                onClick={onClose}
                className="text-xs text-zinc-500 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white underline"
              >
                Close
              </button>
            </div>
          ) : profile ? (
            <>
              {/* Name & Role */}
              <div className="space-y-1">
                <div className="flex flex-wrap items-center gap-2">
                  <h2 className="text-base font-bold text-zinc-900 dark:text-zinc-100">{profile.display_name}</h2>
                  <RoleBadge role={profile.role} size="md" />
                </div>
                <div className="flex items-center gap-2.5 text-xs text-zinc-500 dark:text-zinc-400 font-mono">
                  <span>@{profile.username}</span>
                  <span>•</span>
                  <span className="text-emerald-600 dark:text-emerald-400 font-medium">Term {profile.active_term}</span>
                  {profile.batch_year && (
                    <>
                      <span>•</span>
                      <span>Batch {profile.batch_year}</span>
                    </>
                  )}
                </div>
              </div>

              {/* Bio */}
              {profile.bio ? (
                <p className="text-xs text-zinc-700 dark:text-zinc-300 leading-relaxed bg-zinc-50 dark:bg-white/[0.02] p-2.5 rounded-lg border border-zinc-200/80 dark:border-white/[0.06]">
                  {profile.bio}
                </p>
              ) : (
                <p className="text-xs text-zinc-400 dark:text-zinc-500 italic">No bio provided yet.</p>
              )}

              {/* Reputation & Activity Stats */}
              <div className="grid grid-cols-2 gap-2.5 pt-0.5">
                <div className="p-3 rounded-lg border border-zinc-200/80 dark:border-white/10 bg-zinc-50 dark:bg-white/[0.02] flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-md bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-600 dark:text-emerald-400 shrink-0">
                    <ThumbsUp className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <span className="text-base font-bold text-zinc-900 dark:text-zinc-100">{profile.total_upvotes}</span>
                    <p className="text-[10px] text-zinc-500 dark:text-zinc-400">Upvotes Received</p>
                  </div>
                </div>

                <div className="p-3 rounded-lg border border-zinc-200/80 dark:border-white/10 bg-zinc-50 dark:bg-white/[0.02] flex items-center gap-2.5">
                  <div className="w-8 h-8 rounded-md bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-600 dark:text-blue-400 shrink-0">
                    <MessageSquare className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <span className="text-base font-bold text-zinc-900 dark:text-zinc-100">{profile.total_comments}</span>
                    <p className="text-[10px] text-zinc-500 dark:text-zinc-400">Discussions</p>
                  </div>
                </div>
              </div>

              {/* Quiz Performance Banner (if attempted quizzes) */}
              {profile.quiz_stats && profile.quiz_stats.quizzes_attempted > 0 && (
                <div className="p-3 rounded-lg border border-blue-500/20 bg-blue-50/60 dark:bg-blue-500/[0.04] flex items-center justify-between">
                  <div className="flex items-center gap-2.5">
                    <div className="w-8 h-8 rounded-md bg-blue-500/10 border border-blue-500/30 flex items-center justify-center text-blue-600 dark:text-blue-400 shrink-0">
                      <Target className="w-4 h-4" />
                    </div>
                    <div>
                      <p className="text-xs font-bold text-zinc-800 dark:text-zinc-200">
                        {profile.quiz_stats.quizzes_completed} Topic Quizzes Completed
                      </p>
                      <p className="text-[10px] text-zinc-500 dark:text-zinc-400">
                        {profile.quiz_stats.total_questions_answered} questions answered
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-bold text-emerald-600 dark:text-emerald-400">
                      {profile.quiz_stats.accuracy}%
                    </span>
                    <p className="text-[10px] text-zinc-500 dark:text-zinc-400">Accuracy</p>
                  </div>
                </div>
              )}

              {/* Badges Grid */}
              {profile.badges.length > 0 && (
                <div className="space-y-1.5">
                  <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400 flex items-center gap-1.5">
                    <Award className="w-3.5 h-3.5 text-amber-500 dark:text-amber-400" />
                    <span>Academic & Community Honors</span>
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {profile.badges.map((badge, idx) => (
                      <span
                        key={idx}
                        className="px-2 py-0.5 rounded-md bg-amber-500/10 border border-amber-500/20 text-xs font-medium text-amber-700 dark:text-amber-300"
                      >
                        {badge}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {/* Recent Discussions */}
              {profile.recent_comments.length > 0 && (
                <div className="space-y-1.5 pt-1 border-t border-zinc-200 dark:border-white/[0.06]">
                  <span className="text-xs font-medium text-zinc-500 dark:text-zinc-400">
                    Recent Discussions
                  </span>
                  <div className="space-y-1.5 max-h-32 overflow-y-auto pr-1">
                    {profile.recent_comments.map((rc) => (
                      <Link
                        key={rc.id}
                        to={`/read/${rc.note_id}`}
                        onClick={onClose}
                        className="block p-2 rounded-lg border border-zinc-200/80 dark:border-white/10 bg-zinc-50/60 hover:bg-zinc-100/80 dark:bg-white/[0.02] dark:hover:bg-white/[0.05] transition-colors"
                      >
                        <div className="flex items-center justify-between text-[10px] text-zinc-500 font-mono mb-0.5">
                          <span className="text-blue-600 dark:text-blue-400 font-semibold">{rc.note_id}</span>
                          <span>{rc.score} upvotes</span>
                        </div>
                        <p className="text-xs text-zinc-700 dark:text-zinc-300 line-clamp-1">
                          {rc.content}
                        </p>
                      </Link>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
};
