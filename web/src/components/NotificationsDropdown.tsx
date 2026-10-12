import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { formatDistanceToNow } from 'date-fns';
import {
  Bell,
  CheckCheck,
  MessageSquare,
  ShieldCheck,
  ShieldAlert,
  Info,
  Loader2,
  ExternalLink,
} from 'lucide-react';
import { api } from '@/services/apiClient';
import { NotificationItem, NotificationListResponse } from '@/types/note';

export const NotificationsDropdown: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [notifications, setNotifications] = useState<NotificationItem[]>([]);
  const [unreadCount, setUnreadCount] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  const [markingAll, setMarkingAll] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  const fetchNotifications = useCallback(async (showSpinner = false) => {
    try {
      if (showSpinner) setLoading(true);
      const res = await api.get<NotificationListResponse>('/api/notifications');
      setNotifications(res.notifications || []);
      setUnreadCount(res.unread_count || 0);
    } catch {
      // Background poll silently fails on unauthenticated/offline states
    } finally {
      if (showSpinner) setLoading(false);
    }
  }, []);

  // Poll every 45 seconds
  useEffect(() => {
    void fetchNotifications();
    const interval = setInterval(() => {
      void fetchNotifications();
    }, 45000);
    return () => clearInterval(interval);
  }, [fetchNotifications]);

  // Refetch when dropdown opens
  useEffect(() => {
    if (isOpen) {
      void fetchNotifications(true);
    }
  }, [isOpen, fetchNotifications]);

  // Outside click & ESC dismissal
  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setIsOpen(false);
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      document.addEventListener('keydown', handleKeyDown);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen]);

  const handleMarkAsRead = async (item: NotificationItem) => {
    if (!item.read) {
      // Optimistic update
      setNotifications((prev) =>
        prev.map((n) => (n.id === item.id ? { ...n, read: true } : n))
      );
      setUnreadCount((prev) => Math.max(0, prev - 1));
      try {
        await api.patch(`/api/notifications/${encodeURIComponent(item.id)}/read`);
      } catch {
        // Ignored
      }
    }
    if (item.link) {
      setIsOpen(false);
      navigate(item.link);
      const hashMatch = item.link.match(/#comment-([a-zA-Z0-9_-]+)/);
      const paramMatch = item.link.match(/[?&]commentId=([a-zA-Z0-9_-]+)/);
      const targetId = hashMatch ? hashMatch[1] : (paramMatch ? paramMatch[1] : null);
      if (targetId) {
        setTimeout(() => {
          const el = document.getElementById(`comment-${targetId}`);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }
        }, 150);
      }
    }
  };

  const handleMarkAllRead = async () => {
    setMarkingAll(true);
    // Optimistic update
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
    setUnreadCount(0);
    try {
      await api.post('/api/notifications/mark-all-read');
    } catch {
      void fetchNotifications();
    } finally {
      setMarkingAll(false);
    }
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'reply':
        return <MessageSquare className="w-4 h-4 text-blue-400" />;
      case 'report_resolved':
        return <ShieldCheck className="w-4 h-4 text-emerald-400" />;
      case 'comment_status':
        return <ShieldAlert className="w-4 h-4 text-amber-400" />;
      default:
        return <Info className="w-4 h-4 text-zinc-400" />;
    }
  };

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen((prev) => !prev)}
        className="relative p-1.5 rounded-lg text-zinc-400 hover:text-zinc-100 hover:bg-white/5 transition-colors"
        title="Notifications"
        aria-label="View notifications"
      >
        <Bell className="w-4 h-4" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 min-w-[16px] h-4 px-1 rounded-full bg-rose-500 text-[10px] font-bold text-white flex items-center justify-center shadow-lg shadow-rose-500/30 animate-in zoom-in duration-150">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl border border-zinc-700/60 bg-zinc-900/95 backdrop-blur-xl shadow-2xl shadow-black/80 z-50 text-zinc-100 overflow-hidden animate-in fade-in zoom-in-95 duration-150">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 border-b border-white/10 bg-white/[0.02]">
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold tracking-tight">Notifications</span>
              {unreadCount > 0 && (
                <span className="px-1.5 py-0.5 rounded-md bg-rose-500/20 text-rose-300 text-[10px] font-mono font-medium">
                  {unreadCount} unread
                </span>
              )}
            </div>
            {unreadCount > 0 && (
              <button
                onClick={handleMarkAllRead}
                disabled={markingAll}
                className="flex items-center gap-1 text-[11px] text-zinc-400 hover:text-white transition-colors disabled:opacity-50"
              >
                {markingAll ? (
                  <Loader2 className="w-3 h-3 animate-spin" />
                ) : (
                  <CheckCheck className="w-3 h-3 text-emerald-400" />
                )}
                <span>Mark all read</span>
              </button>
            )}
          </div>

          {/* List */}
          <div className="max-h-[360px] overflow-y-auto divide-y divide-white/5">
            {loading && notifications.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-10 text-zinc-400 gap-2">
                <Loader2 className="w-5 h-5 animate-spin text-blue-400" />
                <span className="text-xs">Loading notifications...</span>
              </div>
            ) : notifications.length === 0 ? (
              <div className="flex flex-col items-center justify-center py-10 px-4 text-center text-zinc-400">
                <div className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center mb-2 text-zinc-500">
                  <Bell className="w-5 h-5" />
                </div>
                <p className="text-xs font-medium text-zinc-300">You're all caught up!</p>
                <p className="text-[11px] text-zinc-400 mt-0.5">
                  Replies, moderation alerts, and updates will appear here.
                </p>
              </div>
            ) : (
              notifications.map((n) => (
                <div
                  key={n.id}
                  onClick={() => void handleMarkAsRead(n)}
                  className={`flex items-start gap-3 p-3.5 cursor-pointer transition-colors ${
                    !n.read
                      ? 'bg-blue-500/[0.07] hover:bg-blue-500/[0.12]'
                      : 'hover:bg-white/[0.04]'
                  }`}
                >
                  <div className="w-8 h-8 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center shrink-0 mt-0.5">
                    {getNotificationIcon(n.type)}
                  </div>
                  <div className="flex-1 min-w-0 space-y-0.5">
                    <div className="flex items-center justify-between gap-2">
                      <p className={`text-xs truncate ${!n.read ? 'font-semibold text-zinc-100' : 'font-medium text-zinc-300'}`}>
                        {n.title}
                      </p>
                      <span className="text-[10px] text-zinc-400 shrink-0 font-mono">
                        {formatDistanceToNow(new Date(n.created_at), { addSuffix: true })}
                      </span>
                    </div>
                    <p className="text-[11px] text-zinc-400 line-clamp-2 leading-relaxed">
                      {n.message}
                    </p>
                  </div>
                  {!n.read && (
                    <div className="w-2 h-2 rounded-full bg-blue-500 mt-1.5 shrink-0 shadow-sm shadow-blue-500/50" />
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
};
export default NotificationsDropdown;
