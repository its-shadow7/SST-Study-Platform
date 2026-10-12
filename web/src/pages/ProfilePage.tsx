import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import {
  Award,
  MessageSquare,
  ThumbsUp,
  GraduationCap,
  Calendar,
  ExternalLink,
  Loader2,
  ArrowLeft,
  Settings as SettingsIcon,
  BookOpen,
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
    currentUser && profile && currentUser.username.toLowerCase() === profile.username.toLowerCase();

  return (
    <div className="min-h-[calc(100vh-3.5rem)] bg-[#09090b] text-zinc-200 py-10 px-4 sm:px-8 max-w-4xl mx-auto space-y-8">
      {/* Back button */}
      <div>
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-1.5 text-xs text-zinc-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back</span>
        </button>
      </div>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-24 text-zinc-400 gap-3">
          <Loader2 className="w-8 h-8 animate-spin text-blue-400" />
          <span className="text-sm">Loading student profile...</span>
        </div>
      ) : error || !profile ? (
        <div className="py-20 text-center rounded-2xl border border-white/5 bg-zinc-900/50 p-8 space-y-4">
          <div className="w-12 h-12 rounded-full bg-rose-500/10 border border-rose-500/20 text-rose-400 flex items-center justify-center mx-auto">
            <GraduationCap className="w-6 h-6" />
          </div>
          <h2 className="text-xl font-bold text-zinc-100">Student Profile Not Found</h2>
          <p className="text-xs text-zinc-400 max-w-sm mx-auto">
            {error || `No user registered with username @${username}.`}
          </p>
          <Link
            to="/terms"
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 text-xs font-semibold text-white hover:bg-blue-500 transition-colors shadow-md shadow-blue-600/20"
          >
            <span>Explore Curriculum</span>
          </Link>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Hero Profile Card */}
          <div className="rounded-3xl border border-zinc-800 bg-zinc-900/60 overflow-hidden shadow-2xl backdrop-blur-sm">
            {/* Gradient Banner */}
            <div className="h-36 w-full bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 relative" />

            <div className="p-6 sm:p-8 pt-0 space-y-6">
              {/* Avatar row with Action Button */}
              <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4 -mt-16 sm:-mt-14">
                <div className="w-28 h-28 rounded-3xl bg-zinc-800 border-4 border-zinc-900 overflow-hidden shadow-2xl flex items-center justify-center text-3xl font-bold text-white shrink-0">
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
                      className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-xs font-semibold text-zinc-200 transition-colors"
                    >
                      <SettingsIcon className="w-3.5 h-3.5" />
                      <span>Edit Profile</span>
                    </Link>
                  )}
                </div>
              </div>

              {/* Title & Metadata */}
              <div className="space-y-2">
                <div className="flex flex-wrap items-center gap-3">
                  <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-zinc-100">
                    {profile.display_name}
                  </h1>
                  <RoleBadge role={profile.role} size="md" />
                </div>

                <div className="flex flex-wrap items-center gap-3 text-xs text-zinc-400 font-mono">
                  <span>@{profile.username}</span>
                  <span>•</span>
                  <span className="text-emerald-400 font-semibold">Term {profile.active_term}</span>
                  {profile.batch_year && (
                    <>
                      <span>•</span>
                      <span>Batch of {profile.batch_year}</span>
                    </>
                  )}
                </div>

                {profile.bio && (
                  <p className="text-sm text-zinc-300 leading-relaxed pt-2 max-w-2xl">
                    {profile.bio}
                  </p>
                )}
              </div>

              {/* Reputation & Community Stats */}
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2">
                <div className="p-4 rounded-2xl border border-white/5 bg-white/[0.02] flex items-center gap-3.5">
                  <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 shrink-0">
                    <ThumbsUp className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="text-xl font-bold text-zinc-100">{profile.total_upvotes}</span>
                    <p className="text-xs text-zinc-400">Upvotes Received</p>
                  </div>
                </div>

                <div className="p-4 rounded-2xl border border-white/5 bg-white/[0.02] flex items-center gap-3.5">
                  <div className="w-10 h-10 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 shrink-0">
                    <MessageSquare className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="text-xl font-bold text-zinc-100">{profile.total_comments}</span>
                    <p className="text-xs text-zinc-400">Total Discussions</p>
                  </div>
                </div>

                <div className="p-4 rounded-2xl border border-white/5 bg-white/[0.02] col-span-2 sm:col-span-1 flex items-center gap-3.5">
                  <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 shrink-0">
                    <Award className="w-5 h-5" />
                  </div>
                  <div>
                    <span className="text-xl font-bold text-zinc-100">{profile.badges.length}</span>
                    <p className="text-xs text-zinc-400">Badges Earned</p>
                  </div>
                </div>
              </div>

              {/* Badges Showcase */}
              <div className="space-y-3 pt-3 border-t border-white/[0.06]">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-zinc-400 flex items-center gap-2">
                  <Award className="w-4 h-4 text-amber-400" />
                  <span>Reputation & Academic Honors</span>
                </h3>
                <div className="flex flex-wrap gap-2">
                  {profile.badges.map((badge, idx) => (
                    <div
                      key={idx}
                      className="px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-500/10 to-orange-500/10 border border-amber-500/20 text-xs font-medium text-amber-300 shadow-sm"
                    >
                      {badge}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Recent Discussions Section */}
          <div className="rounded-3xl border border-zinc-800 bg-zinc-900/60 p-6 sm:p-8 space-y-4 backdrop-blur-sm">
            <div className="flex items-center justify-between border-b border-white/[0.06] pb-3">
              <h3 className="text-base font-semibold text-zinc-100 flex items-center gap-2">
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
              <div className="space-y-2.5">
                {profile.recent_comments.map((rc) => (
                  <Link
                    key={rc.id}
                    to={`/read/${rc.note_id}`}
                    className="block p-4 rounded-2xl border border-white/5 bg-white/[0.02] hover:bg-white/[0.05] transition-all group"
                  >
                    <div className="flex items-center justify-between text-xs text-zinc-400 font-mono mb-2">
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
                    <p className="text-sm text-zinc-200 line-clamp-2 leading-relaxed font-sans">
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
