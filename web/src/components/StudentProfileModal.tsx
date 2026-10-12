import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import {
  X,
  Award,
  MessageSquare,
  ThumbsUp,
  GraduationCap,
  Calendar,
  ExternalLink,
  Loader2,
  ShieldAlert,
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
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div className="relative w-full max-w-lg overflow-hidden rounded-2xl border border-zinc-700/60 bg-zinc-900 shadow-2xl shadow-black/80 text-zinc-100 animate-in zoom-in-95 duration-200">
        {/* Banner Background */}
        <div className="h-24 w-full bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 relative">
          <button
            onClick={onClose}
            className="absolute top-3 right-3 p-1.5 rounded-full bg-black/40 hover:bg-black/70 text-zinc-300 hover:text-white transition-colors"
            aria-label="Close modal"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Profile Content */}
        <div className="p-6 pt-0 space-y-5">
          {/* Avatar & Header row */}
          <div className="flex items-end justify-between -mt-12">
            <div className="w-20 h-20 rounded-2xl bg-zinc-800 border-4 border-zinc-900 overflow-hidden shadow-xl flex items-center justify-center text-2xl font-bold text-white shrink-0">
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
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-xs font-medium text-zinc-200 transition-colors"
              >
                <span>Full Profile</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

          {loading ? (
            <div className="flex flex-col items-center justify-center py-12 text-zinc-400 gap-2">
              <Loader2 className="w-6 h-6 animate-spin text-blue-400" />
              <span className="text-xs">Loading student profile...</span>
            </div>
          ) : error ? (
            <div className="py-8 text-center text-zinc-400 space-y-2">
              <p className="text-sm text-rose-400">{error}</p>
              <button
                onClick={onClose}
                className="text-xs text-zinc-400 hover:text-white underline"
              >
                Close
              </button>
            </div>
          ) : profile ? (
            <>
              {/* Name & Role */}
              <div className="space-y-1">
                <div className="flex flex-wrap items-center gap-2">
                  <h2 className="text-xl font-bold text-zinc-100">{profile.display_name}</h2>
                  <RoleBadge role={profile.role} size="md" />
                </div>
                <div className="flex items-center gap-3 text-xs text-zinc-400 font-mono">
                  <span>@{profile.username}</span>
                  <span>•</span>
                  <span className="text-emerald-400 font-semibold">Term {profile.active_term}</span>
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
                <p className="text-xs text-zinc-300 leading-relaxed bg-white/[0.02] p-3 rounded-xl border border-white/5">
                  {profile.bio}
                </p>
              ) : (
                <p className="text-xs text-zinc-500 italic">No bio provided yet.</p>
              )}

              {/* Reputation & Activity Stats */}
              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="p-3.5 rounded-xl border border-white/5 bg-white/[0.02] flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0">
                    <ThumbsUp className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-lg font-bold text-zinc-100">{profile.total_upvotes}</span>
                    <p className="text-[11px] text-zinc-400">Upvotes Received</p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl border border-white/5 bg-white/[0.02] flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 shrink-0">
                    <MessageSquare className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-lg font-bold text-zinc-100">{profile.total_comments}</span>
                    <p className="text-[11px] text-zinc-400">Contributions</p>
                  </div>
                </div>
              </div>

              {/* Badges Grid */}
              <div className="space-y-2">
                <span className="text-xs font-semibold text-zinc-300 flex items-center gap-1.5">
                  <Award className="w-3.5 h-3.5 text-amber-400" />
                  <span>Reputation & Community Badges</span>
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {profile.badges.map((badge, idx) => (
                    <span
                      key={idx}
                      className="px-2.5 py-1 rounded-lg bg-gradient-to-r from-amber-500/10 to-orange-500/10 border border-amber-500/20 text-xs font-medium text-amber-300"
                    >
                      {badge}
                    </span>
                  ))}
                </div>
              </div>

              {/* Recent Discussions */}
              {profile.recent_comments.length > 0 && (
                <div className="space-y-2 pt-1 border-t border-white/5">
                  <span className="text-xs font-semibold text-zinc-400">
                    Recent Discussions
                  </span>
                  <div className="space-y-1.5 max-h-36 overflow-y-auto">
                    {profile.recent_comments.map((rc) => (
                      <Link
                        key={rc.id}
                        to={`/read/${rc.note_id}`}
                        onClick={onClose}
                        className="block p-2.5 rounded-xl border border-white/5 bg-white/[0.02] hover:bg-white/[0.05] transition-colors"
                      >
                        <div className="flex items-center justify-between text-[11px] text-zinc-500 font-mono mb-1">
                          <span className="text-blue-400 font-semibold">{rc.note_id}</span>
                          <span>{rc.score} upvotes</span>
                        </div>
                        <p className="text-xs text-zinc-300 line-clamp-1 font-sans">
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
export default StudentProfileModal;
