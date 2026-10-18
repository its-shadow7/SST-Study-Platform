import React, { useState, useEffect, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSanitize from 'rehype-sanitize';
import { formatDistanceToNow } from 'date-fns';
import { toast } from 'sonner';
import {
  ShieldAlert,
  ShieldCheck,
  Check,
  Trash2,
  AlertTriangle,
  Loader2,
  ExternalLink,
  RefreshCw,
  Sparkles,
  Bot,
  Flag,
} from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { api, ApiError } from '@/services/apiClient';
import { RoleBadge } from '@/components/RoleBadge';
import { Comment } from '@/types/comment';
import { ModerationAuditLogItem, ModerationAuditLogResponse } from '@/types/note';

interface ModerationQueueResponse {
  queue: Comment[];
  total: number;
}

export const ModerationPage: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [mainTab, setMainTab] = useState<'queue' | 'audit'>('queue');
  const [queue, setQueue] = useState<Comment[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [resolvingId, setResolvingId] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'reported' | 'quarantined'>('all');
  const [auditLogs, setAuditLogs] = useState<ModerationAuditLogItem[]>([]);
  const [auditLoading, setAuditLoading] = useState<boolean>(false);

  const isStaff = user?.role === 'admin' || user?.role === 'moderator';

  const fetchQueue = useCallback(async () => {
    try {
      setLoading(true);
      const res = await api.get<ModerationQueueResponse>('/api/moderation/queue');
      setQueue(res.queue || []);
    } catch (err: any) {
      const apiErr = err as ApiError;
      toast.error(apiErr.message || 'Failed to fetch moderation queue.');
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchAuditLogs = useCallback(async () => {
    try {
      setAuditLoading(true);
      const res = await api.get<ModerationAuditLogResponse>('/api/moderation/audit-log');
      setAuditLogs(res.logs || []);
    } catch (err: any) {
      const apiErr = err as ApiError;
      toast.error(apiErr.message || 'Failed to fetch moderation audit logs.');
    } finally {
      setAuditLoading(false);
    }
  }, []);

  useEffect(() => {
    if (!user) return;
    if (!isStaff) {
      toast.error('Access restricted to moderators and administrators.');
      navigate('/terms');
      return;
    }
    if (mainTab === 'queue') {
      void fetchQueue();
    } else {
      void fetchAuditLogs();
    }
  }, [user, isStaff, mainTab, fetchQueue, fetchAuditLogs, navigate]);


  const handleResolve = async (commentId: string, action: 'approve' | 'delete') => {
    try {
      setResolvingId(commentId);
      await api.post(`/api/moderation/queue/${commentId}/resolve`, { action });
      toast.success(
        action === 'approve'
          ? 'Comment approved and published to discussion.'
          : 'Comment deleted and content redacted.'
      );
      // Remove from queue locally
      setQueue((prev) => prev.filter((item) => item.id !== commentId));
    } catch (err: any) {
      const apiErr = err as ApiError;
      toast.error(apiErr.message || `Failed to ${action} comment.`);
    } finally {
      setResolvingId(null);
    }
  };

  const filteredQueue = queue.filter((item) => {
    if (filter === 'reported') return item.status === 'reported';
    if (filter === 'quarantined') return item.status === 'quarantined';
    return true;
  });

  const quarantinedCount = queue.filter((item) => item.status === 'quarantined').length;
  const reportedCount = queue.filter((item) => item.status === 'reported').length;

  if (!isStaff) {
    return null;
  }

  return (
    <div className="min-h-[calc(100vh-3.5rem)] bg-slate-50 dark:bg-[#09090b] text-zinc-800 dark:text-zinc-200 py-10 px-4 sm:px-8 max-w-5xl mx-auto space-y-6 transition-colors duration-300">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-zinc-200 dark:border-white/[0.08] pb-6">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-amber-500/20 bg-amber-500/10 text-xs font-medium text-amber-600 dark:text-amber-400">
              <ShieldAlert className="w-3.5 h-3.5" />
              <span>Moderation Dashboard</span>
            </div>
            <RoleBadge role={user?.role} size="md" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100">
            {mainTab === 'queue' ? 'Community Moderation Queue' : 'Moderation Audit History'}
          </h1>
          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
            {mainTab === 'queue'
              ? 'Review reported and AI-quarantined comments to maintain academic standards across SST Study Platform.'
              : 'Chronological audit trail of automated flags, approval decisions, and redacting actions.'}
          </p>
        </div>

        <button
          onClick={mainTab === 'queue' ? fetchQueue : fetchAuditLogs}
          disabled={loading || auditLoading}
          className="self-start sm:self-auto flex items-center gap-2 px-3.5 py-2 rounded-xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.03] hover:bg-zinc-100 dark:hover:bg-white/[0.08] text-xs font-medium text-zinc-700 dark:text-zinc-200 transition-colors shadow-sm disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${(loading || auditLoading) ? 'animate-spin' : ''}`} />
          <span>{mainTab === 'queue' ? 'Refresh Queue' : 'Refresh Audit Log'}</span>
        </button>
      </div>

      {/* Main Mode Tabs */}
      <div className="flex items-center gap-2 border-b border-zinc-200 dark:border-white/[0.06] pb-2">
        <button
          onClick={() => setMainTab('queue')}
          className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-xl transition-all ${
            mainTab === 'queue'
              ? 'bg-amber-500/15 text-amber-700 dark:text-amber-300 border border-amber-500/30 shadow-sm'
              : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/5'
          }`}
        >
          <ShieldAlert className="w-4 h-4" />
          <span>Review Queue</span>
          {queue.length > 0 && (
            <span className="px-1.5 py-0.5 rounded-full bg-amber-500/20 text-amber-800 dark:text-amber-200 text-[10px] font-mono">
              {queue.length}
            </span>
          )}
        </button>

        <button
          onClick={() => setMainTab('audit')}
          className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-xl transition-all ${
            mainTab === 'audit'
              ? 'bg-blue-500/15 text-blue-700 dark:text-blue-300 border border-blue-500/30 shadow-sm'
              : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/5'
          }`}
        >
          <ShieldCheck className="w-4 h-4" />
          <span>Audit History</span>
          {auditLogs.length > 0 && (
            <span className="px-1.5 py-0.5 rounded-full bg-blue-500/20 text-blue-800 dark:text-blue-200 text-[10px] font-mono">
              {auditLogs.length}
            </span>
          )}
        </button>
      </div>

      {/* Mode 2: Queue View */}
      {mainTab === 'queue' && (
        <div className="space-y-6">
          {/* Filter Tabs & Summary Counters */}
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="inline-flex items-center rounded-xl border border-zinc-200 dark:border-white/10 bg-zinc-100/70 dark:bg-white/[0.02] p-1 text-xs">
              <button
                onClick={() => setFilter('all')}
                className={`px-3 py-1.5 rounded-lg font-medium transition-all ${
                  filter === 'all'
                    ? 'bg-white dark:bg-white/10 text-zinc-900 dark:text-zinc-100 shadow-sm'
                    : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
                }`}
              >
                All Pending ({queue.length})
              </button>
              <button
                onClick={() => setFilter('reported')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-all ${
                  filter === 'reported'
                    ? 'bg-amber-500/20 text-amber-800 dark:text-amber-300 border border-amber-500/30'
                    : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
                }`}
              >
                <Flag className="w-3 h-3 text-amber-500 dark:text-amber-400" />
                <span>Reported ({reportedCount})</span>
              </button>
              <button
                onClick={() => setFilter('quarantined')}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg font-medium transition-all ${
                  filter === 'quarantined'
                    ? 'bg-rose-500/20 text-rose-800 dark:text-rose-300 border border-rose-500/30'
                    : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200'
                }`}
              >
                <Bot className="w-3 h-3 text-rose-500 dark:text-rose-400" />
                <span>AI Quarantined ({quarantinedCount})</span>
              </button>
            </div>

            <span className="text-xs text-zinc-500 font-mono">
              Showing {filteredQueue.length} of {queue.length} item{queue.length === 1 ? '' : 's'}
            </span>
          </div>

          {/* Queue Item List */}
          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 text-zinc-500 dark:text-zinc-400 gap-3">
              <Loader2 className="w-6 h-6 animate-spin text-amber-500" />
              <span className="text-sm">Loading moderation queue...</span>
            </div>
          ) : filteredQueue.length === 0 ? (
            <div className="py-20 text-center rounded-2xl border border-zinc-200 dark:border-white/5 bg-white dark:bg-white/[0.01] space-y-3 shadow-sm">
              <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-600 dark:text-emerald-400 mx-auto">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h3 className="text-base font-semibold text-zinc-800 dark:text-zinc-200">
                Moderation Queue is Clean
              </h3>
              <p className="text-xs text-zinc-500 dark:text-zinc-400 max-w-sm mx-auto">
                There are currently no reported or quarantined comments requiring staff action.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {filteredQueue.map((item) => {
                const isQuarantined = item.status === 'quarantined';
                const isResolving = resolvingId === item.id;

                return (
                  <div
                    key={item.id}
                    className="p-5 rounded-2xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.02] shadow-sm hover:border-zinc-300 dark:hover:border-white/20 transition-all space-y-4"
                  >
                    {/* Meta Header */}
                    <div className="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-100 dark:border-white/[0.06] pb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-white/10 flex items-center justify-center text-xs font-bold text-zinc-700 dark:text-zinc-200">
                          {(item.username || 'U').charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-semibold text-zinc-800 dark:text-zinc-200">
                              @{item.username || 'student'}
                            </span>
                            <RoleBadge role={item.author_role} size="sm" />
                          </div>
                          <span className="text-[11px] text-zinc-500 font-mono">
                            Posted{' '}
                            {item.created_at
                              ? formatDistanceToNow(new Date(item.created_at), { addSuffix: true })
                              : 'recently'}
                          </span>
                        </div>
                      </div>

                      <div className="flex items-center gap-2">
                        {/* Status Badge */}
                        {isQuarantined ? (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-rose-500/10 text-rose-700 dark:text-rose-400 border border-rose-500/20">
                            <Bot className="w-3.5 h-3.5" />
                            <span>AI Quarantined</span>
                          </span>
                        ) : (
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-500/10 text-amber-700 dark:text-amber-400 border border-amber-500/20">
                            <Flag className="w-3.5 h-3.5" />
                            <span>Reported ({item.reported_by?.length || 1})</span>
                          </span>
                        )}

                        <span className="text-xs text-zinc-500 font-mono">ID: {item.id.slice(0, 8)}</span>
                      </div>
                    </div>

                    {/* Flagged Reasons */}
                    {item.moderation_reasons && item.moderation_reasons.length > 0 && (
                      <div className="flex flex-wrap items-center gap-2 p-3 rounded-xl bg-amber-50 dark:bg-amber-500/[0.04] border border-amber-200 dark:border-amber-500/10 text-xs">
                        <AlertTriangle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400 shrink-0" />
                        <span className="font-semibold text-amber-800 dark:text-amber-300">Flagged Categories / Reasons:</span>
                        {item.moderation_reasons.map((reason, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-0.5 rounded-md bg-amber-100 dark:bg-amber-500/10 text-amber-800 dark:text-amber-300 border border-amber-300 dark:border-amber-500/20 text-[11px] font-mono"
                          >
                            {reason}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Comment Content */}
                    <div className="p-4 rounded-xl border border-zinc-200/80 dark:border-white/5 bg-zinc-50 dark:bg-black/40 text-sm text-zinc-800 dark:text-zinc-200 leading-relaxed font-sans break-words">
                      <ReactMarkdown
                        remarkPlugins={[remarkGfm]}
                        rehypePlugins={[rehypeSanitize]}
                      >
                        {item.content}
                      </ReactMarkdown>
                    </div>

                    {/* Action Bar */}
                    <div className="flex flex-wrap items-center justify-between gap-3 pt-1">
                      <span className="text-[11px] text-zinc-500 font-mono">
                        Target Note: <span className="text-zinc-700 dark:text-zinc-400">{item.note_id}</span>
                      </span>

                      <div className="flex items-center gap-2.5">
                        {/* Approve Button */}
                        <button
                          onClick={() => handleResolve(item.id, 'approve')}
                          disabled={isResolving}
                          className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold text-emerald-700 dark:text-emerald-400 bg-emerald-50 hover:bg-emerald-100 dark:bg-emerald-500/10 dark:hover:bg-emerald-500/20 border border-emerald-300 dark:border-emerald-500/20 transition-all disabled:opacity-50"
                        >
                          <Check className="w-3.5 h-3.5" />
                          <span>Approve & Publish</span>
                        </button>

                        {/* Delete Button */}
                        <button
                          onClick={() => handleResolve(item.id, 'delete')}
                          disabled={isResolving}
                          className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold text-rose-700 dark:text-rose-400 bg-rose-50 hover:bg-rose-100 dark:bg-rose-500/10 dark:hover:bg-rose-500/20 border border-rose-300 dark:border-rose-500/20 transition-all disabled:opacity-50"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                          <span>Delete & Redact</span>
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Mode 1: Audit Log View */}
      {mainTab === 'audit' && (
        <div className="space-y-4">
          {auditLoading ? (
            <div className="flex flex-col items-center justify-center py-20 text-zinc-500 dark:text-zinc-400 gap-3">
              <Loader2 className="w-6 h-6 animate-spin text-blue-500" />
              <span className="text-sm">Loading audit logs...</span>
            </div>
          ) : auditLogs.length === 0 ? (
            <div className="py-20 text-center rounded-2xl border border-zinc-200 dark:border-white/5 bg-white dark:bg-white/[0.01] space-y-3 shadow-sm">
              <div className="w-12 h-12 rounded-2xl bg-zinc-100 dark:bg-white/5 border border-zinc-200 dark:border-white/10 flex items-center justify-center text-zinc-500 mx-auto">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <p className="text-base font-semibold text-zinc-800 dark:text-zinc-200">No moderation actions recorded yet</p>
              <p className="text-xs text-zinc-500 max-w-sm mx-auto">
                Decisions made by moderators or auto-quarantine actions will appear in this audit log.
              </p>
            </div>
          ) : (
            <div className="divide-y divide-zinc-200 dark:divide-white/5 rounded-2xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-zinc-900/40 overflow-hidden shadow-sm dark:shadow-xl">
              {auditLogs.map((log) => {
                const isApproved = log.action === 'approved';
                const isDeleted = log.action === 'deleted';
                const isAuto = log.action.includes('auto') || log.moderator_id === 'system';

                return (
                  <div key={log.id} className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-start justify-between gap-4 hover:bg-zinc-50/80 dark:hover:bg-white/[0.02] transition-colors">
                    <div className="space-y-1.5 flex-1 min-w-0">
                      <div className="flex flex-wrap items-center gap-2">
                        {/* Action Badge */}
                        <span
                          className={`px-2 py-0.5 rounded-md text-[11px] font-semibold border ${
                            isApproved
                              ? 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/20'
                              : isDeleted
                              ? 'bg-rose-500/10 text-rose-700 dark:text-rose-400 border-rose-500/20'
                              : 'bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-500/20'
                          }`}
                        >
                          {log.action.toUpperCase()}
                        </span>

                        <span className="text-xs text-zinc-500 dark:text-zinc-400">by</span>
                        <span className="text-xs font-semibold text-zinc-800 dark:text-zinc-200 flex items-center gap-1.5">
                          {isAuto ? <Bot className="w-3.5 h-3.5 text-blue-500" /> : null}
                          {log.moderator_name}
                        </span>
                        <RoleBadge role={log.moderator_role as any} size="sm" />

                        <span className="text-zinc-300 dark:text-zinc-600">•</span>
                        <span className="text-xs text-zinc-500 font-mono">
                          {formatDistanceToNow(new Date(log.created_at), { addSuffix: true })}
                        </span>
                      </div>

                      {/* Content snippet */}
                      {log.comment_content && (
                        <p className="text-xs text-zinc-700 dark:text-zinc-300 font-mono bg-zinc-50 dark:bg-black/40 px-3 py-2 rounded-lg border border-zinc-200 dark:border-white/5 line-clamp-2">
                          "{log.comment_content}"
                        </p>
                      )}

                      {/* Reason */}
                      {log.reason && (
                        <p className="text-[11px] text-zinc-500 dark:text-zinc-400">
                          <span className="text-zinc-400 dark:text-zinc-500">Reason:</span> {log.reason}
                        </p>
                      )}
                    </div>

                    {/* Target Note */}
                    {log.note_id && (
                      <Link
                        to={`/read/${log.note_id}`}
                        className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg border border-zinc-200 dark:border-white/10 bg-zinc-50 hover:bg-zinc-100 dark:bg-white/[0.03] dark:hover:bg-white/[0.08] text-[11px] text-blue-600 dark:text-blue-400 hover:underline font-mono shrink-0 transition-colors"
                      >
                        <span>{log.note_id}</span>
                        <ExternalLink className="w-3 h-3" />
                      </Link>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
export default ModerationPage;
