import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/context/AuthContext';
import {
  Settings as SettingsIcon,
  User as UserIcon,
  Mail,
  Fingerprint,
  LogOut,
  Trash2,
  AlertTriangle,
  X,
  ShieldCheck,
  AtSign,
  Layers,
  Image as ImageIcon,
  FileText,
  Save,
  CheckCircle2,
  GraduationCap
} from 'lucide-react';
import { toast } from 'sonner';
import { RoleBadge } from '@/components/RoleBadge';

export const SettingsPage: React.FC = () => {
  const { user, logout, deleteAccount, updateProfile } = useAuth();
  const navigate = useNavigate();

  // Profile Form state
  const [username, setUsername] = useState(user?.username || '');
  const [activeTerm, setActiveTerm] = useState<number>(user?.active_term || 1);
  const [avatarUrl, setAvatarUrl] = useState(user?.avatar_url || '');
  const [bio, setBio] = useState(user?.bio || '');
  const [isSaving, setIsSaving] = useState(false);
  const [avatarLoadError, setAvatarLoadError] = useState(false);

  // Danger zone state
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  // Sync state whenever user object refreshes
  useEffect(() => {
    if (user) {
      setUsername(user.username || '');
      setActiveTerm(user.active_term || 1);
      setAvatarUrl(user.avatar_url || '');
      setBio(user.bio || '');
      setAvatarLoadError(false);
    }
  }, [user]);

  const hasChanges =
    user &&
    (username !== (user.username || '') ||
      activeTerm !== (user.active_term || 1) ||
      avatarUrl !== (user.avatar_url || '') ||
      bio !== (user.bio || ''));

  const handleSaveProfile = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    const trimmedUsername = username.trim().toLowerCase();
    if (trimmedUsername.length < 3 || trimmedUsername.length > 30) {
      toast.error('Username must be between 3 and 30 characters');
      return;
    }
    if (!/^[a-zA-Z0-9_]+$/.test(trimmedUsername)) {
      toast.error('Username can only contain letters, numbers, and underscores');
      return;
    }

    if (activeTerm < 1 || activeTerm > 12) {
      toast.error('Active term must be between 1 and 12');
      return;
    }

    setIsSaving(true);
    try {
      await updateProfile({
        username: trimmedUsername,
        active_term: activeTerm,
        avatar_url: avatarUrl.trim() || null,
        bio: bio.trim() || null,
      });
      toast.success('Profile settings updated successfully');
    } catch (err: any) {
      const msg = err.message || err.detail || 'Failed to update profile';
      toast.error(msg);
    } finally {
      setIsSaving(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
    toast.info('Signed out of SST Study Platform');
  };

  const handleDeleteAccount = async () => {
    setIsDeleting(true);
    try {
      await deleteAccount();
      navigate('/login');
      toast.success('Account and session data removed successfully');
    } catch (err: any) {
      toast.error(`Account deletion failed: ${err.message || 'Error'}`);
    } finally {
      setIsDeleting(false);
      setShowDeleteModal(false);
    }
  };

  if (!user) {
    return (
      <div className="min-h-[calc(100vh-3.5rem)] bg-[#09090b] text-zinc-200 py-16 px-4 text-center space-y-4">
        <p className="text-zinc-400 text-sm">Please sign in to view your settings.</p>
        <button
          onClick={() => navigate('/login')}
          className="px-4 py-2 rounded-lg bg-blue-600 text-xs text-white"
        >
          Sign In
        </button>
      </div>
    );
  }

  const initials = (user.display_name || user.email)
    .split(' ')
    .map((n) => n[0])
    .join('')
    .slice(0, 2)
    .toUpperCase();

  return (
    <div className="min-h-[calc(100vh-3.5rem)] bg-[#09090b] text-zinc-200 py-10 px-4 sm:px-8 max-w-3xl mx-auto space-y-8">
      {/* Header */}
      <div className="border-b border-white/[0.08] pb-6">
        <div className="flex items-center gap-2.5 mb-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-blue-500/20 bg-blue-500/10 text-xs font-medium text-blue-400">
            <SettingsIcon className="w-3.5 h-3.5" />
            <span>Student Account</span>
          </div>
          <RoleBadge role={user.role} size="md" />
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-zinc-100">
          Account & Profile Settings
        </h1>
        <p className="text-xs text-zinc-400 mt-1">
          Customize your public handle for discussion forums, choose your current active term, and manage platform preferences.
        </p>
      </div>

      {/* 1. Public Profile Customization Card */}
      <form onSubmit={handleSaveProfile} className="p-6 rounded-2xl border border-white/10 bg-white/[0.02] space-y-6">
        <div className="flex items-center justify-between border-b border-white/[0.06] pb-4">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
              <UserIcon className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-zinc-100">Public Student Profile</h2>
              <p className="text-[11px] text-zinc-400">
                Visible across discussion threads, comments, and study peer groups.
              </p>
            </div>
          </div>

          {hasChanges && (
            <span className="text-[11px] text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20 font-mono">
              Unsaved Changes
            </span>
          )}
        </div>

        {/* Avatar Section */}
        <div className="flex flex-col sm:flex-row sm:items-center gap-5">
          <div className="relative w-16 h-16 rounded-2xl overflow-hidden bg-gradient-to-br from-blue-600 to-indigo-800 border border-white/20 flex items-center justify-center shrink-0 shadow-lg">
            {avatarUrl && !avatarLoadError ? (
              <img
                src={avatarUrl}
                alt={user.display_name}
                onError={() => setAvatarLoadError(true)}
                className="w-full h-full object-cover"
              />
            ) : (
              <span className="text-lg font-bold text-white tracking-wider font-mono">
                {initials}
              </span>
            )}
          </div>

          <div className="flex-1 space-y-1.5">
            <label className="text-xs font-medium text-zinc-300 flex items-center gap-1.5">
              <ImageIcon className="w-3.5 h-3.5 text-zinc-400" />
              <span>Avatar Image URL</span>
            </label>
            <input
              type="url"
              value={avatarUrl}
              onChange={(e) => {
                setAvatarUrl(e.target.value);
                setAvatarLoadError(false);
              }}
              placeholder="https://example.com/your-avatar.png (Optional)"
              className="w-full bg-zinc-900 border border-white/10 rounded-lg px-3 py-2 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-blue-500 transition-colors"
            />
            <p className="text-[11px] text-zinc-500">
              Leave blank to use your default Scaler account initials or Google profile avatar.
            </p>
          </div>
        </div>

        {/* Username & Active Term Row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Username Input */}
          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label className="text-xs font-medium text-zinc-300 flex items-center gap-1.5">
                <AtSign className="w-3.5 h-3.5 text-zinc-400" />
                <span>Public Handle / Username</span>
              </label>
              <RoleBadge role={user.role} size="sm" />
            </div>
            <div className="relative flex items-center">
              <span className="absolute left-3 text-xs text-zinc-500 font-mono select-none">@</span>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                maxLength={30}
                required
                placeholder="username"
                className="w-full bg-zinc-900 border border-white/10 rounded-lg pl-7 pr-3 py-2 text-xs font-mono text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-blue-500 transition-colors"
              />
            </div>
            <p className="text-[11px] text-zinc-500">
              Unique handle for comments & discussions (letters, numbers, underscores only).
            </p>
          </div>

          {/* Active Term Dropdown */}
          <div className="space-y-1.5">
            <label className="text-xs font-medium text-zinc-300 flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-zinc-400" />
              <span>Active Curriculum Term</span>
            </label>
            <select
              value={activeTerm}
              onChange={(e) => setActiveTerm(parseInt(e.target.value, 10))}
              className="w-full bg-zinc-900 border border-white/10 rounded-lg px-3 py-2 text-xs text-zinc-100 focus:outline-none focus:border-blue-500 transition-colors cursor-pointer"
            >
              {Array.from({ length: 12 }, (_, i) => i + 1).map((t) => {
                const year = Math.ceil(t / 4);
                return (
                  <option key={t} value={t} className="bg-zinc-900 text-zinc-100">
                    Term {t} (Year {year} Curriculum)
                  </option>
                );
              })}
            </select>
            <p className="text-[11px] text-zinc-500">
              Restricted to Terms 1–12. Sets your primary term across the study platform.
            </p>
          </div>
        </div>

        {/* Bio Textarea */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <label className="text-xs font-medium text-zinc-300 flex items-center gap-1.5">
              <FileText className="w-3.5 h-3.5 text-zinc-400" />
              <span>Student Bio</span>
            </label>
            <span className="text-[11px] text-zinc-500 font-mono">
              {bio.length}/300
            </span>
          </div>
          <textarea
            value={bio}
            onChange={(e) => setBio(e.target.value.slice(0, 300))}
            rows={3}
            placeholder="Tell fellow students about your interests, study group focus, or domain (e.g. Systems & ML)..."
            className="w-full bg-zinc-900 border border-white/10 rounded-lg p-3 text-xs text-zinc-100 placeholder-zinc-500 focus:outline-none focus:border-blue-500 transition-colors resize-none leading-relaxed"
          />
        </div>

        {/* Action button */}
        <div className="pt-2 flex items-center justify-end">
          <button
            type="submit"
            disabled={isSaving || !hasChanges}
            className="flex items-center gap-2 px-5 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-xs font-semibold text-white transition-all disabled:opacity-40 disabled:hover:bg-blue-600 shadow-lg shadow-blue-600/20"
          >
            <Save className="w-4 h-4" />
            <span>{isSaving ? 'Saving Changes...' : 'Save Profile Changes'}</span>
          </button>
        </div>
      </form>

      {/* 2. Identity & Academic Standing Information Card */}
      <div className="p-6 rounded-2xl border border-white/10 bg-white/[0.02] space-y-5">
        <h2 className="text-sm font-semibold tracking-wider uppercase text-zinc-400 flex items-center gap-2">
          <GraduationCap className="w-4 h-4 text-blue-400" />
          <span>Academic & Session Information</span>
        </h2>

        <div className="space-y-4 text-xs divide-y divide-white/[0.04]">
          <div className="flex items-center justify-between pt-2">
            <span className="text-zinc-400 flex items-center gap-2">
              <UserIcon className="w-3.5 h-3.5 text-zinc-500" />
              <span>Username & Role</span>
            </span>
            <div className="flex items-center gap-2">
              <span className="font-mono text-zinc-100">@{user.username}</span>
              <RoleBadge role={user.role} size="sm" />
            </div>
          </div>

          <div className="flex items-center justify-between pt-3">
            <span className="text-zinc-400 flex items-center gap-2">
              <UserIcon className="w-3.5 h-3.5 text-zinc-500" />
              <span>Display Name</span>
            </span>
            <span className="font-medium text-zinc-100">{user.display_name}</span>
          </div>

          <div className="flex items-center justify-between pt-3">
            <span className="text-zinc-400 flex items-center gap-2">
              <Mail className="w-3.5 h-3.5 text-zinc-500" />
              <span>Institutional Email</span>
            </span>
            <span className="font-mono text-zinc-200">{user.email}</span>
          </div>

          <div className="flex items-center justify-between pt-3">
            <span className="text-zinc-400 flex items-center gap-2">
              <GraduationCap className="w-3.5 h-3.5 text-zinc-500" />
              <span>Academic Standing</span>
            </span>
            <span className="font-medium text-blue-400">
              Year {user.year_of_study || 4} Student
              {user.batch_year ? ` (Batch '${String(user.batch_year).slice(2)})` : ''}
            </span>
          </div>

          <div className="flex items-center justify-between pt-3">
            <span className="text-zinc-400 flex items-center gap-2">
              <Layers className="w-3.5 h-3.5 text-zinc-500" />
              <span>Current Active Term</span>
            </span>
            <span className="font-mono text-emerald-400 font-semibold">
              Term {user.active_term || 1}
            </span>
          </div>

          <div className="flex items-center justify-between pt-3">
            <span className="text-zinc-400 flex items-center gap-2">
              <Layers className="w-3.5 h-3.5 text-zinc-500" />
              <span>Unlocked Curriculum</span>
            </span>
            <span className="font-mono text-zinc-300">
              Terms 1–{user.max_allowed_term || 16}
            </span>
          </div>

          <div className="flex items-center justify-between pt-3">
            <span className="text-zinc-400 flex items-center gap-2">
              <Fingerprint className="w-3.5 h-3.5 text-zinc-500" />
              <span>Internal Student ID</span>
            </span>
            <span className="font-mono text-[11px] text-zinc-400 truncate max-w-[200px]" title={user.user_id}>
              {user.user_id}
            </span>
          </div>

          <div className="flex items-center justify-between pt-3">
            <span className="text-zinc-400 flex items-center gap-2">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span>Verification Status</span>
            </span>
            <span className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
              Verified Scaler Student
            </span>
          </div>
        </div>
      </div>

      {/* 3. Session Management Card */}
      <div className="p-6 rounded-2xl border border-white/10 bg-white/[0.02] flex items-center justify-between">
        <div>
          <h3 className="text-sm font-semibold text-zinc-200">Sign Out</h3>
          <p className="text-xs text-zinc-400 mt-0.5">
            End your active JWT session on this device.
          </p>
        </div>
        <button
          onClick={handleLogout}
          className="flex items-center gap-2 px-4 py-2 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 text-xs font-medium text-zinc-200 transition-colors"
        >
          <LogOut className="w-4 h-4 text-zinc-400" />
          <span>Sign Out</span>
        </button>
      </div>

      {/* 4. Danger Zone: Delete Account */}
      <div className="p-6 rounded-2xl border border-rose-500/20 bg-rose-500/[0.02] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h3 className="text-sm font-semibold text-rose-400 flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" />
            <span>Delete Account & Student Data</span>
          </h3>
          <p className="text-xs text-zinc-400 mt-1 max-w-md">
            Permanently delete your profile record, refresh session tokens, and saved bookmarks from MongoDB Atlas.
          </p>
        </div>
        <button
          onClick={() => setShowDeleteModal(true)}
          className="self-start sm:self-auto flex items-center gap-2 px-4 py-2 rounded-xl border border-rose-500/40 bg-rose-500/10 hover:bg-rose-500/20 text-xs font-semibold text-rose-300 transition-colors"
        >
          <Trash2 className="w-4 h-4" />
          <span>Delete Account</span>
        </button>
      </div>

      {/* Confirmation Modal */}
      {showDeleteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div
            className="fixed inset-0 bg-black/80 backdrop-blur-sm"
            onClick={() => setShowDeleteModal(false)}
          />
          <div className="relative w-full max-w-md rounded-2xl border border-rose-500/30 bg-[#0d0d10] p-6 shadow-2xl space-y-4 z-10">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 text-rose-400 font-semibold text-sm">
                <AlertTriangle className="w-5 h-5" />
                <span>Confirm Account Deletion</span>
              </div>
              <button
                onClick={() => setShowDeleteModal(false)}
                className="text-zinc-500 hover:text-zinc-300"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-zinc-300 leading-relaxed">
              Are you sure you want to permanently delete your account (<strong>{user.email}</strong>)?
              All bookmarked lectures and session keys will be purged from MongoDB Atlas. This action cannot be undone.
            </p>

            <div className="flex items-center justify-end gap-3 pt-3">
              <button
                onClick={() => setShowDeleteModal(false)}
                className="px-3.5 py-1.5 rounded-lg border border-white/10 text-xs text-zinc-400 hover:text-zinc-200 hover:bg-white/5"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteAccount}
                disabled={isDeleting}
                className="px-4 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-700 text-xs font-semibold text-white disabled:opacity-50"
              >
                {isDeleting ? 'Deleting...' : 'Yes, Delete My Account'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
