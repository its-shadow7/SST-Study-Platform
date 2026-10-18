import React, { useState } from 'react';
import { useAuth } from '@/context/AuthContext';
import { 
  Sparkles, 
  User as UserIcon, 
  AtSign, 
  BookOpen, 
  FileText, 
  Image as ImageIcon, 
  Check, 
  AlertCircle, 
  Loader2 
} from 'lucide-react';

interface ProfileSetupModalProps {
  isOpen: boolean;
}

export const ProfileSetupModal: React.FC<ProfileSetupModalProps> = ({ isOpen }) => {
  const { user, updateProfile } = useAuth();

  const [displayName, setDisplayName] = useState(user?.display_name || '');
  const [username, setUsername] = useState(user?.username || '');
  const [activeTerm, setActiveTerm] = useState<number>(user?.active_term || 1);
  const [bio, setBio] = useState(user?.bio || '');
  const [avatarUrl, setAvatarUrl] = useState(user?.avatar_url || '');

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!isOpen || !user) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const cleanUsername = username.trim().toLowerCase();
    if (cleanUsername.length < 3 || cleanUsername.length > 30) {
      setError('Username must be between 3 and 30 characters.');
      return;
    }
    if (!/^[a-zA-Z0-9_]+$/.test(cleanUsername)) {
      setError('Username can only contain letters, numbers, and underscores.');
      return;
    }

    try {
      setSaving(true);
      await updateProfile({
        display_name: displayName.trim() || user.display_name,
        username: cleanUsername,
        active_term: activeTerm,
        bio: bio.trim() || null,
        avatar_url: avatarUrl.trim() || null,
        needs_profile_setup: false,
      });
    } catch (err: any) {
      setError(err.message || 'Failed to complete profile setup. Please try again.');
    } finally {
      setSaving(false);
    }
  };

  const handleSkip = async () => {
    try {
      setSaving(true);
      await updateProfile({
        needs_profile_setup: false,
      });
    } catch (err: any) {
      setError(err.message || 'Error dismissing onboarding.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md animate-in fade-in duration-200">
      <div 
        className="relative w-full max-w-lg rounded-2xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0d0e12] p-6 sm:p-8 shadow-2xl space-y-6 text-zinc-800 dark:text-zinc-200 overflow-hidden"
      >
        {/* Glow accent */}
        <div className="absolute -top-24 -left-24 w-48 h-48 bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-24 -right-24 w-48 h-48 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-2">
              <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-blue-500/15 text-blue-600 dark:text-blue-400 border border-blue-500/30">
                <Sparkles className="w-3 h-3" />
                Special Access Account
              </span>
            </div>
            <h2 className="text-xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
              Welcome to SST Study Platform
            </h2>
            <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
              Set up your public profile and default study term. You can update these anytime in Settings.
            </p>
          </div>

          {/* Email avatar pill */}
          <div className="w-11 h-11 rounded-full bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white font-semibold text-sm shrink-0 border border-white/10 shadow-inner">
            {displayName ? displayName.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
          </div>
        </div>

        {error && (
          <div className="p-3 rounded-xl border border-rose-500/30 bg-rose-500/10 text-rose-600 dark:text-rose-300 text-xs flex items-center gap-2.5">
            <AlertCircle className="w-4 h-4 shrink-0 text-rose-500 dark:text-rose-400" />
            <span>{error}</span>
          </div>
        )}

        {/* Setup Form */}
        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          {/* Full Name */}
          <div className="space-y-1.5">
            <label className="text-zinc-700 dark:text-zinc-300 font-medium flex items-center gap-1.5">
              <UserIcon className="w-3.5 h-3.5 text-zinc-400" />
              Full Name / Display Name
            </label>
            <input
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              placeholder="e.g. Alex Morgan"
              className="w-full px-3.5 py-2.5 rounded-xl bg-zinc-50 dark:bg-white/[0.04] border border-zinc-200 dark:border-white/10 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 dark:placeholder:text-zinc-600 outline-none transition-all"
            />
          </div>

          {/* Username */}
          <div className="space-y-1.5">
            <label className="text-zinc-700 dark:text-zinc-300 font-medium flex items-center gap-1.5">
              <AtSign className="w-3.5 h-3.5 text-zinc-400" />
              Public Handle / Username
            </label>
            <div className="relative">
              <span className="absolute left-3.5 top-1/2 -translate-y-1/2 text-zinc-400 font-mono">
                @
              </span>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value.toLowerCase().replace(/[^a-z0-9_]/g, ''))}
                placeholder="alex_morgan"
                className="w-full pl-8 pr-3.5 py-2.5 rounded-xl bg-zinc-50 dark:bg-white/[0.04] border border-zinc-200 dark:border-white/10 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 dark:placeholder:text-zinc-600 font-mono outline-none transition-all"
                maxLength={30}
              />
            </div>
          </div>

          {/* Active Curriculum Term */}
          <div className="space-y-1.5">
            <label className="text-zinc-700 dark:text-zinc-300 font-medium flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-zinc-400" />
              Default Starting Term
            </label>
            <select
              value={activeTerm}
              onChange={(e) => setActiveTerm(Number(e.target.value))}
              className="w-full px-3.5 py-2.5 rounded-xl bg-zinc-50 dark:bg-[#14151a] border border-zinc-200 dark:border-white/10 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-zinc-900 dark:text-zinc-100 outline-none transition-all cursor-pointer"
            >
              {Array.from({ length: 12 }, (_, i) => i + 1).map((term) => (
                <option key={term} value={term} className="bg-white dark:bg-[#14151a] text-zinc-900 dark:text-zinc-200">
                  Term {term}
                </option>
              ))}
            </select>
          </div>

          {/* Bio / Role */}
          <div className="space-y-1.5">
            <label className="text-zinc-700 dark:text-zinc-300 font-medium flex items-center justify-between">
              <span className="flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-zinc-400" />
                Bio / Role Description
              </span>
              <span className="text-[10px] text-zinc-400 dark:text-zinc-500 font-mono">{bio.length}/300</span>
            </label>
            <textarea
              value={bio}
              onChange={(e) => setBio(e.target.value)}
              placeholder="e.g. Academic Mentor / Visiting Faculty / SST Scholar"
              rows={2}
              maxLength={300}
              className="w-full px-3.5 py-2 rounded-xl bg-zinc-50 dark:bg-white/[0.04] border border-zinc-200 dark:border-white/10 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 dark:placeholder:text-zinc-600 outline-none resize-none transition-all"
            />
          </div>

          {/* Avatar URL (Optional) */}
          <div className="space-y-1.5">
            <label className="text-zinc-700 dark:text-zinc-300 font-medium flex items-center gap-1.5">
              <ImageIcon className="w-3.5 h-3.5 text-zinc-400" />
              Avatar Image URL <span className="text-zinc-400 dark:text-zinc-500 font-normal">(Optional)</span>
            </label>
            <input
              type="url"
              value={avatarUrl}
              onChange={(e) => setAvatarUrl(e.target.value)}
              placeholder="https://example.com/avatar.jpg"
              className="w-full px-3.5 py-2 rounded-xl bg-zinc-50 dark:bg-white/[0.04] border border-zinc-200 dark:border-white/10 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-zinc-900 dark:text-zinc-100 placeholder:text-zinc-400 dark:placeholder:text-zinc-600 outline-none transition-all"
            />
          </div>

          {/* Buttons */}
          <div className="pt-3 flex items-center justify-end gap-3 border-t border-zinc-100 dark:border-white/[0.08]">
            <button
              type="button"
              onClick={handleSkip}
              disabled={saving}
              className="px-4 py-2 rounded-xl border border-zinc-200 dark:border-white/10 bg-zinc-100 hover:bg-zinc-200 dark:bg-white/5 dark:hover:bg-white/10 text-zinc-700 dark:text-zinc-300 font-medium transition-colors disabled:opacity-50"
            >
              Skip for now
            </button>
            <button
              type="submit"
              disabled={saving}
              className="flex items-center gap-2 px-5 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-semibold shadow-lg shadow-blue-500/20 transition-all disabled:opacity-50"
            >
              {saving ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Saving...</span>
                </>
              ) : (
                <>
                  <Check className="w-3.5 h-3.5" />
                  <span>Save & Continue</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
