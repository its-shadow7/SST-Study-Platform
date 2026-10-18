import React, { useState, useEffect, useCallback, useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { formatDistanceToNow } from 'date-fns';
import { toast } from 'sonner';
import {
  MessageSquare,
  Send,
  Trash2,
  Loader2,
  Sparkles,
  ArrowUp,
  ArrowDown,
  Reply,
  Clock,
  Flame,
  Flag,
  AlertTriangle,
  X,
  Copy,
  Check,
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/apiClient';
import { RoleBadge } from './RoleBadge';
import { ReportModal } from './ReportModal';
import { StudentProfileModal } from './StudentProfileModal';
import {
  Comment,
  ThreadedComment,
  CommentListResponse,
  VoteResponse,
} from '../types/comment';

interface CommentSectionProps {
  noteId: string;
}

// Code Block with Syntax Highlighting and Copy Action for Comments
const CommentCodeBlock: React.FC<{ language: string; value: string }> = ({ language, value }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Ignored
    }
  };

  return (
    <div className="relative group my-2.5 rounded-xl overflow-hidden border border-white/10 bg-[#0c0c0f]">
      <div className="flex items-center justify-between px-3 py-1.5 bg-white/[0.03] border-b border-white/[0.06] text-[11px] text-zinc-400 font-mono select-none">
        <span className="uppercase tracking-wider font-semibold text-zinc-400">
          {language || 'code'}
        </span>
        <button
          onClick={handleCopy}
          aria-label="Copy code block"
          className="flex items-center gap-1 px-2 py-0.5 rounded border border-white/10 bg-white/5 hover:bg-white/10 text-zinc-300 text-[10px] transition-all"
        >
          {copied ? (
            <>
              <Check className="w-3 h-3 text-emerald-400" />
              <span className="text-emerald-400 font-medium">Copied!</span>
            </>
          ) : (
            <>
              <Copy className="w-3 h-3 text-zinc-400" />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>
      <div className="p-3 overflow-x-auto text-xs font-mono">
        <SyntaxHighlighter
          language={language || 'text'}
          style={vscDarkPlus}
          customStyle={{
            background: 'transparent',
            padding: 0,
            margin: 0,
            fontSize: '0.8rem',
            lineHeight: '1.5',
            fontFamily: 'JetBrains Mono, monospace',
          }}
          wrapLongLines={false}
        >
          {value.replace(/\n$/, '')}
        </SyntaxHighlighter>
      </div>
    </div>
  );
};

// User Avatar with initial fallback circle
const Avatar: React.FC<{ avatarUrl?: string | null; name?: string | null }> = ({
  avatarUrl,
  name,
}) => {
  const [imageError, setImageError] = useState(false);
  const initial = (name || 'S').charAt(0).toUpperCase();

  if (avatarUrl && !imageError) {
    return (
      <img
        src={avatarUrl}
        alt={name || 'Author avatar'}
        onError={() => setImageError(true)}
        className="w-8 h-8 rounded-full object-cover ring-1 ring-white/10 flex-shrink-0"
      />
    );
  }

  return (
    <div
      className="w-8 h-8 rounded-full bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-white/10 flex items-center justify-center text-xs font-semibold text-zinc-700 dark:text-zinc-300 select-none flex-shrink-0"
      aria-label={name || 'User avatar'}
    >
      {initial}
    </div>
  );
};

// Tree constructor from flat comments array
export function buildCommentTree(
  comments: Comment[],
  sortMode: 'newest' | 'top'
): ThreadedComment[] {
  const map = new Map<string, ThreadedComment>();
  const roots: ThreadedComment[] = [];

  comments.forEach((c, idx) => {
    map.set(c.id, {
      ...c,
      initialRank: c.initialRank ?? idx,
      score: c.score ?? 0,
      upvoted_by: c.upvoted_by || [],
      downvoted_by: c.downvoted_by || [],
      replies: [],
    });
  });

  comments.forEach((c) => {
    const item = map.get(c.id)!;
    if (c.parent_id && map.has(c.parent_id)) {
      map.get(c.parent_id)!.replies.push(item);
    } else {
      roots.push(item);
    }
  });

  // Sort child replies using initialRank (or created_at in newest) to keep position stable during voting
  const sortReplies = (node: ThreadedComment) => {
    if (sortMode === 'top') {
      node.replies.sort((a, b) => {
        const rankA = a.initialRank ?? 999999;
        const rankB = b.initialRank ?? 999999;
        return rankA - rankB || b.created_at.localeCompare(a.created_at);
      });
    } else {
      node.replies.sort((a, b) => a.created_at.localeCompare(b.created_at));
    }
    node.replies.forEach(sortReplies);
  };

  if (sortMode === 'top') {
    roots.sort((a, b) => {
      const rankA = a.initialRank ?? 999999;
      const rankB = b.initialRank ?? 999999;
      return rankA - rankB || b.created_at.localeCompare(a.created_at);
    });
  }

  roots.forEach(sortReplies);
  return roots;
}

// Single Recursive Comment Thread Item
interface CommentThreadProps {
  comment: ThreadedComment;
  currentUserId?: string;
  onVote: (commentId: string, action: 'upvote' | 'downvote') => void;
  onReply: (content: string, parentId?: string | null) => Promise<void>;
  onDelete: (commentId: string) => void;
  onReport: (commentId: string) => void;
  getRelativeTime: (isoString: string) => string;
  onViewProfile?: (username: string) => void;
  highlightedCommentId?: string | null;
}

const CommentThread: React.FC<CommentThreadProps> = ({
  comment,
  currentUserId,
  onVote,
  onReply,
  onDelete,
  onReport,
  getRelativeTime,
  onViewProfile,
  highlightedCommentId,
}) => {
  const [isReplying, setIsReplying] = useState(false);
  const [replyContent, setReplyContent] = useState('');
  const [isSubmittingReply, setIsSubmittingReply] = useState(false);

  const isAuthor = Boolean(currentUserId && currentUserId === comment.user_id);
  const isDeleted = comment.content === '[Deleted]';
  const isHighlighted = Boolean(highlightedCommentId && highlightedCommentId === comment.id);

  const isUpvoted = Boolean(
    currentUserId && (comment.upvoted_by || []).includes(currentUserId)
  );
  const isDownvoted = Boolean(
    currentUserId && (comment.downvoted_by || []).includes(currentUserId)
  );

  const handleSendReply = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!replyContent.trim()) return;
    try {
      setIsSubmittingReply(true);
      await onReply(replyContent.trim(), comment.id);
      setReplyContent('');
      setIsReplying(false);
    } catch {
      // Handled in parent
    } finally {
      setIsSubmittingReply(false);
    }
  };

  const handleReplyKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      void handleSendReply();
    }
  };

  return (
    <div className="space-y-3">
      {/* Comment Card */}
      <div
        id={`comment-${comment.id}`}
        className={`group p-4 rounded-xl border transition-all duration-300 scroll-mt-24 ${
          isHighlighted
            ? 'border-blue-500 bg-blue-500/10 shadow-lg shadow-blue-500/20 ring-2 ring-blue-500/50'
            : isDeleted
            ? 'border-zinc-200/60 dark:border-white/5 bg-transparent opacity-60'
            : 'border-zinc-200/80 dark:border-white/10 bg-white dark:bg-transparent hover:border-zinc-300 dark:hover:border-white/20 shadow-sm dark:shadow-none'
        } space-y-2.5`}
      >
        {/* Author Metadata Bar */}
        <div className="flex items-center justify-between">
          <div
            className={`flex items-center gap-2.5 ${!isDeleted && comment.username ? 'cursor-pointer group/author' : ''}`}
            onClick={() => {
              if (!isDeleted && comment.username && onViewProfile) {
                onViewProfile(comment.username);
              }
            }}
          >
            <Avatar
              avatarUrl={isDeleted ? null : comment.avatar_url}
              name={isDeleted ? 'Deleted' : comment.username || 'student'}
            />
            <div className="flex items-center gap-2 flex-wrap">
              <span className={`text-xs font-semibold ${!isDeleted && comment.username ? 'text-zinc-900 dark:text-zinc-200 group-hover/author:text-blue-600 dark:group-hover/author:text-blue-400 group-hover/author:underline underline-offset-2' : 'text-zinc-900 dark:text-zinc-200'}`}>
                {isDeleted ? 'Deleted User' : `@${comment.username || 'student'}`}
              </span>
              {!isDeleted && <RoleBadge role={comment.author_role} size="sm" />}
              <span className="text-zinc-400 dark:text-zinc-600 text-xs">•</span>
              <span className="text-xs text-zinc-500 dark:text-zinc-400">
                {getRelativeTime(comment.created_at)}
              </span>
            </div>
          </div>

          {/* Delete button (Author only, and not already redacted) */}
          {isAuthor && !isDeleted && (
            <button
              onClick={() => onDelete(comment.id)}
              title="Delete comment"
              aria-label="Delete comment"
              className="p-1 rounded text-zinc-400 hover:text-red-500 dark:text-zinc-500 dark:hover:text-red-400 hover:bg-zinc-100 dark:hover:bg-white/5 opacity-0 group-hover:opacity-100 focus:opacity-100 transition-all"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          )}
        </div>

        {/* Content Body */}
        <div className="pl-10 text-sm text-zinc-800 dark:text-zinc-200 leading-relaxed break-words">
          {isDeleted ? (
            <p className="italic text-zinc-400 dark:text-zinc-500 text-xs">[Deleted]</p>
          ) : (
            <ReactMarkdown
              remarkPlugins={[remarkGfm, remarkMath]}
              rehypePlugins={[[rehypeKatex, { trust: false }]]}
              components={{
                a: ({ ...props }) => (
                  <a
                    {...props}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 dark:text-blue-400 hover:underline underline-offset-2"
                  />
                ),
                code({ node, inline, className, children, ...props }: any) {
                  const match = /language-(\w+)/.exec(className || '');
                  const codeString = String(children).replace(/\n$/, '');
                  if (!inline && (match || codeString.includes('\n'))) {
                    return (
                      <CommentCodeBlock
                        language={match ? match[1] : ''}
                        value={codeString}
                      />
                    );
                  }
                  return (
                    <code
                      className="px-1.5 py-0.5 rounded bg-zinc-100 dark:bg-white/10 text-emerald-700 dark:text-emerald-300 font-mono text-xs"
                      {...props}
                    >
                      {children}
                    </code>
                  );
                },
                p: ({ ...props }) => <p className="mb-1.5 last:mb-0" {...props} />,
              }}
            >
              {comment.content}
            </ReactMarkdown>
          )}

          {/* Quarantined Warning Notice at bottom of comment */}
          {comment.status === 'quarantined' && (
            <div className="mt-3 p-3 rounded-xl border border-rose-500/30 bg-rose-500/10 text-xs text-rose-700 dark:text-rose-200 flex items-start gap-2.5 animate-in fade-in duration-200">
              <AlertTriangle className="w-4 h-4 text-rose-500 dark:text-rose-400 shrink-0 mt-0.5" />
              <div className="space-y-0.5">
                <p className="font-semibold text-rose-800 dark:text-rose-200">
                  Comment quarantined for {comment.moderation_reasons && comment.moderation_reasons.length > 0 ? comment.moderation_reasons.join(', ') : 'community guidelines'} and repeated offence may lead to ban.
                </p>
                <p className="text-[11px] text-rose-600/80 dark:text-rose-300/70">
                  This comment is currently held in the moderation queue and hidden from other students.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Interaction Action Row (Reddit-style Voting & Reply) */}
        {!isDeleted && comment.status !== 'quarantined' && (
          <div className="pl-10 pt-1 flex items-center gap-3 text-xs">
            {/* Reddit-style Vote Controls: Up Arrow | Score | Down Arrow */}
            <div className="inline-flex items-center rounded-lg border border-zinc-200 dark:border-white/10 bg-zinc-50 dark:bg-white/[0.02]">
              {/* Upvote Button */}
              <button
                onClick={() => onVote(comment.id, 'upvote')}
                title="Upvote"
                aria-label="Upvote comment"
                className={`p-1 rounded-l-md transition-colors ${isUpvoted
                    ? 'text-orange-600 bg-orange-500/15'
                    : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-white/5'
                  }`}
              >
                <ArrowUp className="w-3.5 h-3.5" />
              </button>

              {/* Score Number */}
              <span
                className={`px-2 text-xs font-mono font-medium select-none ${isUpvoted
                    ? 'text-orange-600 dark:text-orange-500 font-semibold'
                    : isDownvoted
                      ? 'text-blue-600 dark:text-blue-500 font-semibold'
                      : 'text-zinc-600 dark:text-zinc-400'
                  }`}
              >
                {comment.score}
              </span>

              {/* Downvote Button */}
              <button
                onClick={() => onVote(comment.id, 'downvote')}
                title="Downvote"
                aria-label="Downvote comment"
                className={`p-1 rounded-r-md transition-colors ${isDownvoted
                    ? 'text-blue-600 bg-blue-500/15'
                    : 'text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-white/5'
                  }`}
              >
                <ArrowDown className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Reply Button */}
            {currentUserId && (
              <button
                onClick={() => setIsReplying((prev) => !prev)}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md border border-transparent hover:border-zinc-200 dark:hover:border-white/10 text-xs transition-colors ${isReplying
                    ? 'text-zinc-900 bg-zinc-100 dark:text-zinc-200 dark:bg-white/5'
                    : 'text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/5'
                  }`}
              >
                <Reply className="w-3.5 h-3.5" />
                <span>Reply</span>
              </button>
            )}

            {/* Report Button */}
            {!isAuthor && (
              <button
                onClick={() => onReport(comment.id)}
                title="Report comment"
                aria-label="Report comment"
                className="flex items-center gap-1.5 px-2 py-1 rounded-md border border-transparent hover:border-red-400/20 text-xs text-zinc-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-400/10 transition-colors ml-auto sm:ml-0"
              >
                <Flag className="w-3.5 h-3.5" />
                <span className="hidden sm:inline">Report</span>
              </button>
            )}
          </div>
        )}
      </div>

      {/* Embedded Reply Input Box */}
      {isReplying && (
        <div className="ml-6 md:ml-8 pl-3 md:pl-4 border-l border-zinc-200 dark:border-white/10 animate-in fade-in duration-150">
          <form
            onSubmit={handleSendReply}
            className="rounded-xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-transparent p-3 focus-within:border-zinc-400 dark:focus-within:border-white/20 shadow-sm dark:shadow-none transition-colors"
          >
            <textarea
              value={replyContent}
              onChange={(e) => setReplyContent(e.target.value)}
              onKeyDown={handleReplyKeyDown}
              placeholder={`Replying to @${comment.username || 'student'}... (Ctrl+Enter to post)`}
              rows={2}
              maxLength={1000}
              disabled={isSubmittingReply}
              autoFocus
              className="w-full bg-transparent text-xs text-zinc-800 dark:text-zinc-200 placeholder:text-zinc-400 dark:placeholder:text-zinc-500 resize-none outline-none focus:ring-0 leading-relaxed min-h-[52px]"
            />

            <div className="flex items-center justify-between pt-2 border-t border-zinc-100 dark:border-white/5 text-xs">
              <span className="text-[10px] font-mono text-zinc-500 dark:text-zinc-400">
                {replyContent.length} / 1000
              </span>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => {
                    setIsReplying(false);
                    setReplyContent('');
                  }}
                  className="px-2.5 py-1 rounded-md text-[11px] text-zinc-500 hover:text-zinc-800 dark:text-zinc-400 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/5 transition-colors"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmittingReply || !replyContent.trim()}
                  className="flex items-center gap-1.5 px-3 py-1 rounded-md border border-zinc-200 dark:border-white/10 bg-zinc-100 hover:bg-zinc-200 dark:bg-white/5 dark:hover:bg-white/10 active:scale-95 text-[11px] font-medium text-zinc-800 dark:text-zinc-200 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                >
                  {isSubmittingReply ? (
                    <>
                      <Loader2 className="w-3 h-3 animate-spin" />
                      <span>Posting...</span>
                    </>
                  ) : (
                    <>
                      <Send className="w-3 h-3 text-zinc-500 dark:text-zinc-400" />
                      <span>Reply</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </form>
        </div>
      )}

      {/* Visually Nested Replies */}
      {comment.replies && comment.replies.length > 0 && (
        <div className="ml-6 md:ml-8 pl-3 md:pl-4 border-l border-zinc-200 dark:border-white/10 space-y-3">
          {comment.replies.map((reply) => (
            <CommentThread
              key={reply.id}
              comment={reply}
              currentUserId={currentUserId}
              onVote={onVote}
              onReply={onReply}
              onDelete={onDelete}
              onReport={onReport}
              getRelativeTime={getRelativeTime}
              onViewProfile={onViewProfile}
              highlightedCommentId={highlightedCommentId}
            />
          ))}
        </div>
      )}
    </div>
  );
};

// Main Comment Section Component
export const CommentSection: React.FC<CommentSectionProps> = ({ noteId }) => {
  const { user } = useAuth();
  const [flatComments, setFlatComments] = useState<Comment[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [newComment, setNewComment] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [sortMode, setSortMode] = useState<'top' | 'newest'>('top');
  const [reportingCommentId, setReportingCommentId] = useState<string | null>(null);
  const [quarantineWarning, setQuarantineWarning] = useState<string | null>(null);
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);
  const [isDeleting, setIsDeleting] = useState<boolean>(false);
  const [selectedProfileUsername, setSelectedProfileUsername] = useState<string | null>(null);
  const [highlightedCommentId, setHighlightedCommentId] = useState<string | null>(null);

  // Extract target comment ID from query parameter (?commentId=...) or URL hash (#comment-...)
  const targetCommentId = useMemo(() => {
    if (typeof window === 'undefined') return null;
    try {
      const params = new URLSearchParams(window.location.search);
      const q = params.get('commentId');
      if (q) return q;
      if (window.location.hash && window.location.hash.startsWith('#comment-')) {
        return window.location.hash.replace('#comment-', '');
      }
    } catch {
      // fallback for non-browser environments
    }
    return null;
  }, []);

  // Smooth scroll and pulse highlight when target comment is in DOM
  useEffect(() => {
    if (loading || !targetCommentId || flatComments.length === 0) return;

    const timer = setTimeout(() => {
      const el = document.getElementById(`comment-${targetCommentId}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        setHighlightedCommentId(targetCommentId);
        const clearTimer = setTimeout(() => {
          setHighlightedCommentId((prev) => (prev === targetCommentId ? null : prev));
        }, 4000);
        return () => clearTimeout(clearTimer);
      }
    }, 300);

    return () => clearTimeout(timer);
  }, [loading, flatComments, targetCommentId]);

  // Close delete confirmation modal on ESC
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && deleteConfirmId && !isDeleting) {
        setDeleteConfirmId(null);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [deleteConfirmId, isDeleting]);

  const handleConfirmDelete = async () => {
    if (!deleteConfirmId || isDeleting) return;
    setIsDeleting(true);
    const targetId = deleteConfirmId;
    try {
      await handleDelete(targetId);
      setDeleteConfirmId(null);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleOpenReport = (commentId: string) => {
    if (!user) {
      toast.error('Please sign in to report comments.');
      return;
    }
    setReportingCommentId(commentId);
  };

  // Fetch comments for current lecture note with sort mode
  const fetchComments = useCallback(async () => {
    if (!noteId) return;
    try {
      setLoading(true);
      const res = await api.get<CommentListResponse>(
        `/api/notes/${encodeURIComponent(noteId)}/comments?sort=${sortMode}`
      );
      const commentsWithRank = (res.comments || []).map((c, index) => ({
        ...c,
        initialRank: c.initialRank ?? index,
      }));
      setFlatComments(commentsWithRank);
    } catch (err: any) {
      if (err?.status !== 401) {
        toast.error(err.message || 'Unable to load comments.');
      }
    } finally {
      setLoading(false);
    }
  }, [noteId, sortMode]);

  useEffect(() => {
    void fetchComments();
  }, [fetchComments]);

  // Relative time helper via date-fns
  const getRelativeTime = (isoString: string): string => {
    try {
      const date = new Date(isoString);
      if (isNaN(date.getTime())) return 'Just now';
      return formatDistanceToNow(date, { addSuffix: true });
    } catch {
      return 'Just now';
    }
  };

  // Turn flat list into nested tree structure
  const threadedTree = useMemo(() => {
    return buildCommentTree(flatComments, sortMode);
  }, [flatComments, sortMode]);

  // Optimistic posting (both root comments and replies)
  const handlePost = async (content: string, parentId?: string | null) => {
    if (!user) {
      toast.error('Please sign in to join the discussion.');
      return;
    }
    const trimmed = content.trim();
    if (!trimmed) return;

    if (trimmed.length > 1000) {
      toast.error('Comment cannot exceed 1000 characters.');
      return;
    }

    const tempId = `temp-${Date.now()}`;
    const nowIso = new Date().toISOString();
    const optimisticComment: Comment = {
      id: tempId,
      note_id: noteId,
      user_id: user.user_id,
      content: trimmed,
      parent_id: parentId || null,
      score: 0,
      upvoted_by: [],
      downvoted_by: [],
      created_at: nowIso,
      updated_at: nowIso,
      username: user.username,
      avatar_url: user.avatar_url,
      initialRank: parentId ? 999999 : -1,
    };

    const rollbackComments = [...flatComments];
    // Optimistically update flatComments array
    setFlatComments((prev) => [optimisticComment, ...prev]);

    try {
      const created = await api.post<Comment>(
        `/api/notes/${encodeURIComponent(noteId)}/comments`,
        { content: trimmed, parent_id: parentId || null }
      );

      if (created.status === 'quarantined') {
        const reasonsStr =
          created.moderation_reasons && created.moderation_reasons.length > 0
            ? created.moderation_reasons.join(', ')
            : 'community safety';
        const warningMsg = `comment quarantined for reason (${reasonsStr}) and repeated offence may lead to ban`;
        setQuarantineWarning(warningMsg);
        toast.error(
          `Comment quarantined for reason (${reasonsStr}) and repeated offence may lead to ban.`,
          { duration: 10000 }
        );
      } else {
        setQuarantineWarning(null);
      }

      // Replace temporary placeholder with persistent server comment
      setFlatComments((prev) =>
        prev.map((c) => (c.id === tempId ? { ...created, initialRank: c.initialRank } : c))
      );
    } catch (err: any) {
      // Rollback on failure: immediately remove optimistic comment from UI state
      setFlatComments(rollbackComments);
      if (
        err?.status === 400 ||
        err?.message?.toLowerCase()?.includes('community guidelines') ||
        err?.message?.toLowerCase()?.includes('violates')
      ) {
        toast.error('Comment violates community guidelines.');
      } else {
        toast.error(err.message || 'Failed to post comment. Maximum 10 per minute allowed.');
      }
      throw err;
    }
  };

  // Submit handler for root input
  const handleRootSubmit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!newComment.trim()) return;
    setIsSubmitting(true);
    const originalInput = newComment;
    setNewComment('');
    try {
      await handlePost(originalInput, null);
    } catch {
      setNewComment(originalInput);
    } finally {
      setIsSubmitting(false);
    }
  };

  // Optimistic 3-State Vote Handler (Upvote / Downvote)
  const handleVote = async (commentId: string, action: 'upvote' | 'downvote') => {
    if (!user) {
      toast.error('Please sign in to vote.');
      return;
    }

    const rollbackComments = [...flatComments];

    // Optimistically calculate new vote state and score
    setFlatComments((prev) =>
      prev.map((c) => {
        if (c.id !== commentId) return c;

        const upSet = new Set(c.upvoted_by || []);
        const downSet = new Set(c.downvoted_by || []);
        const isUpvoted = upSet.has(user.user_id);
        const isDownvoted = downSet.has(user.user_id);
        let delta = 0;

        if (action === 'upvote') {
          if (isUpvoted) {
            // Already upvoted -> toggle off (-1)
            upSet.delete(user.user_id);
            delta = -1;
          } else if (isDownvoted) {
            // Currently downvoted -> switch to upvote (+2)
            downSet.delete(user.user_id);
            upSet.add(user.user_id);
            delta = 2;
          } else {
            // Neutral -> upvote (+1)
            upSet.add(user.user_id);
            delta = 1;
          }
        } else {
          // action === 'downvote'
          if (isDownvoted) {
            // Already downvoted -> toggle off (+1)
            downSet.delete(user.user_id);
            delta = 1;
          } else if (isUpvoted) {
            // Currently upvoted -> switch to downvote (-2)
            upSet.delete(user.user_id);
            downSet.add(user.user_id);
            delta = -2;
          } else {
            // Neutral -> downvote (-1)
            downSet.add(user.user_id);
            delta = -1;
          }
        }

        return {
          ...c,
          score: (c.score || 0) + delta,
          upvoted_by: Array.from(upSet),
          downvoted_by: Array.from(downSet),
        };
      })
    );

    try {
      const res = await api.post<VoteResponse>(
        `/api/comments/${encodeURIComponent(commentId)}/vote`,
        { action }
      );

      // Reconcile with authoritative server response
      setFlatComments((prev) =>
        prev.map((c) => {
          if (c.id !== commentId) return c;
          const upSet = new Set(c.upvoted_by || []);
          const downSet = new Set(c.downvoted_by || []);

          if (res.user_vote === 'upvote') {
            upSet.add(user.user_id);
            downSet.delete(user.user_id);
          } else if (res.user_vote === 'downvote') {
            downSet.add(user.user_id);
            upSet.delete(user.user_id);
          } else {
            upSet.delete(user.user_id);
            downSet.delete(user.user_id);
          }

          return {
            ...c,
            score: res.score,
            upvoted_by: Array.from(upSet),
            downvoted_by: Array.from(downSet),
          };
        })
      );
    } catch (err: any) {
      setFlatComments(rollbackComments);
      toast.error(err.message || 'Failed to submit vote.');
    }
  };

  // Optimistic Delete / Redaction
  const handleDelete = async (commentId: string) => {
    const rollbackComments = [...flatComments];
    const hasChildren = flatComments.some((c) => c.parent_id === commentId);

    // Optimistically redact if has children or remove if leaf
    if (hasChildren) {
      setFlatComments((prev) =>
        prev.map((c) => (c.id === commentId ? { ...c, content: '[Deleted]' } : c))
      );
    } else {
      setFlatComments((prev) => prev.filter((c) => c.id !== commentId));
    }

    try {
      const res = await api.delete<{ status: string; id: string }>(
        `/api/comments/${encodeURIComponent(commentId)}`
      );
      if (res.status === 'redacted') {
        setFlatComments((prev) =>
          prev.map((c) => (c.id === commentId ? { ...c, content: '[Deleted]' } : c))
        );
      } else {
        setFlatComments((prev) => prev.filter((c) => c.id !== commentId));
      }
      toast.success('Comment deleted.');
    } catch (err: any) {
      setFlatComments(rollbackComments);
      toast.error(err.message || 'Failed to delete comment.');
    }
  };

  // Keyboard shortcut: Cmd/Ctrl + Enter to submit root comment
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') {
      e.preventDefault();
      void handleRootSubmit();
    }
  };

  return (
    <section
      aria-label="Discussion"
      className="mt-14 pt-8 border-t border-zinc-200 dark:border-white/10 space-y-6"
    >
      {/* Header and Sorting Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex items-center gap-2.5">
          <MessageSquare className="w-5 h-5 text-zinc-500 dark:text-zinc-400" />
          <h3 className="text-base font-semibold tracking-tight text-zinc-900 dark:text-zinc-100">
            Discussion
          </h3>
          <span className="px-2 py-0.5 text-xs font-mono rounded-full bg-zinc-100 dark:bg-white/5 border border-zinc-200 dark:border-white/10 text-zinc-600 dark:text-zinc-400">
            {flatComments.length}
          </span>
        </div>

        {/* Sleek Linear Sort Toggle: Top | Newest (default Top) */}
        <div className="inline-flex items-center rounded-lg border border-zinc-200 dark:border-white/10 bg-zinc-100/50 dark:bg-transparent p-0.5 text-xs self-start sm:self-auto">
          <button
            onClick={() => setSortMode('top')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-all ${sortMode === 'top'
                ? 'bg-white dark:bg-white/10 text-zinc-900 dark:text-zinc-100 font-medium shadow-sm'
                : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/5'
              }`}
          >
            <Flame className="w-3.5 h-3.5" />
            <span>Top</span>
          </button>
          <button
            onClick={() => setSortMode('newest')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-all ${sortMode === 'newest'
                ? 'bg-white dark:bg-white/10 text-zinc-900 dark:text-zinc-100 font-medium shadow-sm'
                : 'text-zinc-500 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-white/5'
              }`}
          >
            <Clock className="w-3.5 h-3.5" />
            <span>Newest</span>
          </button>
        </div>
      </div>

      {/* Main Input area */}
      {user ? (
        <form onSubmit={handleRootSubmit} className="space-y-2">
          <div className="rounded-xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-transparent p-3 focus-within:border-zinc-400 dark:focus-within:border-white/20 shadow-sm dark:shadow-none transition-colors">
            <div className="flex items-start gap-3">
              <Avatar avatarUrl={user.avatar_url} name={user.username || user.display_name} />
              <textarea
                value={newComment}
                onChange={(e) => setNewComment(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Leave a comment... (Markdown supported, Ctrl+Enter to post)"
                rows={2}
                maxLength={1000}
                disabled={isSubmitting}
                className="w-full bg-transparent text-sm text-zinc-800 dark:text-zinc-200 placeholder:text-zinc-400 dark:placeholder:text-zinc-500 resize-none outline-none focus:ring-0 leading-relaxed min-h-[64px]"
              />
            </div>

            <div className="flex items-center justify-between pt-2.5 mt-2 border-t border-zinc-100 dark:border-white/5 text-xs">
              <span className="text-[11px] font-mono text-zinc-500 dark:text-zinc-400">
                {newComment.length} / 1000
              </span>

              <div className="flex items-center gap-2">
                <button
                  type="submit"
                  disabled={isSubmitting || !newComment.trim()}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-zinc-200 dark:border-white/10 bg-zinc-100 hover:bg-zinc-200 dark:bg-transparent dark:hover:bg-white/5 active:scale-95 text-xs font-medium text-zinc-800 dark:text-zinc-200 disabled:opacity-40 disabled:cursor-not-allowed transition-all"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      <span>Posting...</span>
                    </>
                  ) : (
                    <>
                      <Send className="w-3.5 h-3.5 text-zinc-500 dark:text-zinc-400" />
                      <span>Post</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </form>
      ) : (
        <div className="p-4 rounded-xl border border-zinc-200 dark:border-white/10 bg-zinc-50/50 dark:bg-transparent text-center text-sm text-zinc-500 dark:text-zinc-400">
          Sign in with your SST account to participate in the discussion.
        </div>
      )}

      {/* Quarantined Warning Alert Banner */}
      {quarantineWarning && (
        <div className="p-3.5 rounded-xl border border-rose-500/30 bg-rose-500/10 text-rose-700 dark:text-rose-200 flex items-start gap-3 shadow-lg shadow-rose-950/20 animate-in fade-in slide-in-from-bottom-2 duration-200">
          <AlertTriangle className="w-4 h-4 text-rose-500 dark:text-rose-400 shrink-0 mt-0.5" />
          <div className="flex-1 space-y-0.5">
            <p className="text-xs font-semibold text-rose-800 dark:text-rose-200">
              {quarantineWarning}
            </p>
            <p className="text-[11px] text-rose-600/80 dark:text-rose-300/70">
              Your message was flagged by automated content safety and held for moderation review.
            </p>
          </div>
          <button
            onClick={() => setQuarantineWarning(null)}
            className="text-rose-500 hover:text-rose-700 dark:text-rose-400 dark:hover:text-rose-200 p-1 rounded-md hover:bg-rose-500/20 transition-colors"
            title="Dismiss notice"
            aria-label="Dismiss notice"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Threaded Comment Tree List */}
      <div className="space-y-4 pt-2">
        {loading ? (
          <div className="flex items-center justify-center py-10 text-zinc-500 dark:text-zinc-400 gap-2">
            <Loader2 className="w-4 h-4 animate-spin text-zinc-400" />
            <span className="text-xs">Loading comments...</span>
          </div>
        ) : threadedTree.length === 0 ? (
          <div className="py-10 text-center rounded-xl border border-zinc-200/80 dark:border-white/5 bg-zinc-50/40 dark:bg-transparent space-y-2">
            <Sparkles className="w-5 h-5 text-zinc-400 dark:text-zinc-500 mx-auto" />
            <p className="text-sm text-zinc-600 dark:text-zinc-400">No comments yet.</p>
            <p className="text-xs text-zinc-400 dark:text-zinc-500">
              Be the first student to start the discussion for this lecture note.
            </p>
          </div>
        ) : (
          threadedTree.map((rootComment) => (
            <CommentThread
              key={rootComment.id}
              comment={rootComment}
              currentUserId={user?.user_id}
              onVote={handleVote}
              onReply={handlePost}
              onDelete={(commentId) => setDeleteConfirmId(commentId)}
              onReport={handleOpenReport}
              getRelativeTime={getRelativeTime}
              onViewProfile={(uname) => setSelectedProfileUsername(uname)}
              highlightedCommentId={highlightedCommentId}
            />
          ))
        )}
      </div>

      {/* Report Comment Modal */}
      <ReportModal
        isOpen={Boolean(reportingCommentId)}
        commentId={reportingCommentId || ''}
        onClose={() => setReportingCommentId(null)}
        onReportSubmitted={(reportedId) => {
          setFlatComments((prev) =>
            prev.map((c) =>
              c.id === reportedId
                ? {
                  ...c,
                  status: 'reported',
                  reported_by: [...(c.reported_by || []), user?.user_id || ''],
                }
                : c
            )
          );
        }}
      />

      {/* Delete Comment Confirmation Modal */}
      {deleteConfirmId && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="delete-confirm-modal-title"
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200"
          onClick={(e) => {
            if (e.target === e.currentTarget && !isDeleting) {
              setDeleteConfirmId(null);
            }
          }}
        >
          <div className="relative w-full max-w-sm overflow-hidden rounded-2xl border border-zinc-200 dark:border-zinc-700/60 bg-white dark:bg-zinc-900 shadow-2xl p-6 text-zinc-900 dark:text-zinc-100 space-y-4 animate-in zoom-in-95 duration-200">
            <div className="flex items-start gap-3.5">
              <div className="w-10 h-10 rounded-xl bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-500 dark:text-rose-400 shrink-0">
                <Trash2 className="w-5 h-5" />
              </div>
              <div className="space-y-1">
                <h3 id="delete-confirm-modal-title" className="text-base font-semibold text-zinc-900 dark:text-zinc-100">
                  Delete Comment?
                </h3>
                <p className="text-xs text-zinc-500 dark:text-zinc-400 leading-relaxed">
                  Are you sure you want to delete this comment? If students have replied, the content will be redacted to <span className="font-mono text-zinc-700 dark:text-zinc-300">[Deleted]</span> to preserve thread context.
                </p>
              </div>
            </div>

            <div className="flex items-center justify-end gap-2.5 pt-2">
              <button
                type="button"
                disabled={isDeleting}
                onClick={() => setDeleteConfirmId(null)}
                className="px-4 py-2 text-xs font-medium text-zinc-600 dark:text-zinc-300 hover:text-zinc-900 dark:hover:text-white rounded-xl hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                type="button"
                disabled={isDeleting}
                onClick={handleConfirmDelete}
                className="inline-flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-white bg-rose-600 hover:bg-rose-500 active:bg-rose-700 rounded-xl shadow-md shadow-rose-600/20 transition-all disabled:opacity-60"
              >
                {isDeleting ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Deleting...</span>
                  </>
                ) : (
                  <span>Delete</span>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Student Profile Preview Modal */}
      {selectedProfileUsername && (
        <StudentProfileModal
          username={selectedProfileUsername}
          onClose={() => setSelectedProfileUsername(null)}
        />
      )}
    </section>
  );
};
export default CommentSection;
