import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import {
  Award,
  MessageSquare,
  ThumbsUp,
  GraduationCap,
  ExternalLink,
  Loader2,
  ArrowLeft,
  Settings as SettingsIcon,
  BookOpen,
  Target,
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { api } from '@/services/apiClient';
import { RoleBadge } from '@/components/RoleBadge';
import { PublicUserProfile } from '@/components/StudentProfileModal';

export const ProfilePage: React.FC = () => {
  const { username } = useParams<{ username: string }>();
  const { user: currentUser } = useAuth();
  const navigate = useNavigate();

  const [profile, setProfile] = useState<PublicUserProfile | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

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

  const isOwnProfile =
    Boolean(currentUser?.username && profile?.username && currentUser.username.toLowerCase() === profile.username.toLowerCase());

  return (
    <div className="min-h-[calc(100vh-3.5rem)] bg-[#09090b] text-zinc-200 py-8 px-4 sm:px-8 max-w-4xl mx-auto space-y-6">
      {/* Back button */}
      <div>
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-1.5 text-xs text-zinc-400 hover:text-zinc-200 transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Back</span>
        </button>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-24 text-zinc-400 gap-3">
          <Loader2 className="w-6 h-6 animate-spin text-blue-400" />
          <span className="text-xs">Loading student profile...</span>
        </div>
      ) : error || !profile ? (
        <div className="py-20 text-center rounded-xl border border-white/10 bg-[#09090b] p-8 space-y-4">
          <div className="w-12 h-12 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-400 flex items-center justify-center mx-auto">
            <GraduationCap className="w-6 h-6" />
          </div>
          <h2 className="text-lg font-bold text-zinc-100">Student Profile Not Found</h2>
          <p className="text-xs text-zinc-400 max-w-sm mx-auto">
            {error || `No user registered with username @${username}.`}
          </p>
          <Link
            to="/terms"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-blue-600 text-xs font-semibold text-white hover:bg-blue-500 transition-colors shadow-sm"
          >
            <span>Explore Curriculum</span>
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Hero Profile Card */}
          <div className="rounded-xl border border-white/10 bg-[#09090b] overflow-hidden shadow-2xl">
            {/* Subtle OLED Banner */}
            <div className="h-28 w-full bg-gradient-to-r from-blue-950/20 via-zinc-900/40 to-purple-950/20 border-b border-white/[0.06] relative" />

            <div className="p-6 pt-0 space-y-5">
              {/* Avatar row with Action Button */}
              <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 -mt-12">
                <div className="w-20 h-20 rounded-2xl bg-zinc-900 border border-white/20 overflow-hidden shadow-xl flex items-center justify-center text-2xl font-bold text-zinc-100 shrink-0">
                  {profile.avatar_url ? (
                    <img
                      src={profile.avatar_url}
                      alt={profile.display_name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <span>{profile.display_name.charAt(0).toUpperCase()}</span>
                  )}
                </div>

                <div className="flex items-center gap-2.5">
                  {isOwnProfile && (
                    <Link
                      to="/settings"
                      className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg border border-white/10 bg-white/5 hover:bg-white/10 text-xs font-medium text-zinc-200 transition-colors"
                    >
                      <SettingsIcon className="w-3.5 h-3.5 text-zinc-400" />
                      <span>Edit Profile</span>
                    </Link>
                  )}
                </div>
              </div>

              {/* Title & Metadata */}
              <div className="space-y-2">
                <div className="flex flex-wrap items-center gap-2.5">
                  <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-zinc-100">
                    {profile.display_name}
                  </h1>
                  <RoleBadge role={profile.role} size="md" />
                </div>

                <div className="flex flex-wrap items-center gap-2.5 text-xs text-zinc-400 font-mono">
                  <span>@{profile.username}</span>
                  <span>•</span>
                  <span className="text-emerald-400 font-medium">Term {profile.active_term}</span>
                  {profile.batch_year && (
                    <>
                      <span>•</span>
                      <span>Batch {profile.batch_year}</span>
                    </>
                  )}
                </div>

                {profile.bio && (
                  <p className="text-xs sm:text-sm text-zinc-300 leading-relaxed pt-1 max-w-2xl bg-white/[0.02] border border-white/[0.06] p-3 rounded-lg">
                    {profile.bio}
                  </p>
                )}
              </div>

              {/* Reputation & Community Stats */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2">
                <div className="p-3.5 rounded-xl border border-white/10 bg-white/[0.02] flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0">
                    <ThumbsUp className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-lg font-bold text-zinc-100">{profile.total_upvotes}</span>
                    <p className="text-[11px] text-zinc-400">Upvotes Received</p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl border border-white/10 bg-white/[0.02] flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 shrink-0">
                    <MessageSquare className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-lg font-bold text-zinc-100">{profile.total_comments}</span>
                    <p className="text-[11px] text-zinc-400">Discussions</p>
                  </div>
                </div>

                <div className="p-3.5 rounded-xl border border-white/10 bg-white/[0.02] col-span-2 sm:col-span-1 flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 shrink-0">
                    <Award className="w-4 h-4" />
                  </div>
                  <div>
                    <span className="text-lg font-bold text-zinc-100">{profile.badges.length}</span>
                    <p className="text-[11px] text-zinc-400">Honors</p>
                  </div>
                </div>
              </div>

              {/* Quiz Performance Card */}
              {profile.quiz_stats && profile.quiz_stats.quizzes_attempted > 0 && (
                <div className="p-4 rounded-xl border border-blue-500/20 bg-blue-500/[0.03] space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="w-7 h-7 rounded-lg bg-blue-500/10 border border-blue-500/20 text-blue-400 flex items-center justify-center">
                        <Target className="w-4 h-4" />
                      </div>
                      <h3 className="text-xs font-bold text-zinc-200 uppercase tracking-wider font-mono">
                        Topic Quiz Mastery
                      </h3>
                    </div>
                    <span className="text-xs font-mono font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      {profile.quiz_stats.accuracy}% Avg Accuracy
                    </span>
                  </div>

                  <div className="grid grid-cols-3 gap-2.5 pt-1 text-center font-mono">
                    <div className="p-2.5 rounded-lg bg-black/40 border border-white/[0.06]">
                      <span className="text-sm font-bold text-zinc-100">
                        {profile.quiz_stats.quizzes_completed}
                      </span>
                      <p className="text-[10px] text-zinc-400">Quizzes Completed</p>
                    </div>
                    <div className="p-2.5 rounded-lg bg-black/40 border border-white/[0.06]">
                      <span className="text-sm font-bold text-zinc-100">
                        {profile.quiz_stats.total_questions_answered}
                      </span>
                      <p className="text-[10px] text-zinc-400">Questions Solved</p>
                    </div>
                    <div className="p-2.5 rounded-lg bg-black/40 border border-white/[0.06]">
                      <span className="text-sm font-bold text-emerald-400">
                        {profile.quiz_stats.total_correct}
                      </span>
                      <p className="text-[10px] text-zinc-400">Correct Answers</p>
                    </div>
                  </div>
                </div>
              )}

              {/* Badges Showcase */}
              {profile.badges.length > 0 && (
                <div className="space-y-2 pt-2 border-t border-white/[0.06]">
                  <h3 className="text-xs font-semibold text-zinc-400 flex items-center gap-1.5">
                    <Award className="w-3.5 h-3.5 text-amber-400" />
                    <span>Academic & Community Honors</span>
                  </h3>
                  <div className="flex flex-wrap gap-1.5">
                    {profile.badges.map((badge, idx) => (
                      <span
                        key={idx}
                        className="px-2.5 py-1 rounded-md bg-amber-400/10 border border-amber-400/20 text-xs font-medium text-amber-300"
                      >
                        {badge}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Recent Discussions Section */}
          <div className="rounded-xl border border-white/10 bg-[#09090b] p-6 space-y-4">
            <div className="flex items-center justify-between border-b border-white/[0.06] pb-3">
              <h3 className="text-sm font-semibold text-zinc-100 flex items-center gap-2">
                <BookOpen className="w-4 h-4 text-blue-400" />
                <span>Recent Note Discussions</span>
              </h3>
              <span className="text-xs text-zinc-500 font-mono">
                {profile.recent_comments.length} listed
              </span>
            </div>

            {profile.recent_comments.length === 0 ? (
              <p className="text-xs text-zinc-500 py-6 text-center">
                This student has not participated in any public discussions yet.
              </p>
            ) : (
              <div className="space-y-2">
                {profile.recent_comments.map((rc) => (
                  <Link
                    key={rc.id}
                    to={`/read/${rc.note_id}`}
                    className="block p-3.5 rounded-lg border border-white/10 bg-white/[0.02] hover:bg-white/[0.05] transition-all group"
                  >
                    <div className="flex items-center justify-between text-xs text-zinc-400 font-mono mb-1.5">
                      <span className="text-blue-400 font-semibold group-hover:text-blue-300 transition-colors flex items-center gap-1">
                        <span>{rc.note_id}</span>
                        <ExternalLink className="w-3 h-3" />
                      </span>
                      <div className="flex items-center gap-2">
                        <span className="inline-flex items-center gap-1 text-emerald-400">
                          <ThumbsUp className="w-3 h-3" />
                          <span>{rc.score}</span>
                        </span>
                        <span>•</span>
                        <span>{formatDistanceToNow(new Date(rc.created_at), { addSuffix: true })}</span>
                      </div>
                    </div>
                    <p className="text-xs text-zinc-200 line-clamp-2 leading-relaxed">
                      {rc.content}
                    </p>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
export default ProfilePage;
