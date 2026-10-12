import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from '@/services/apiClient';
import { Bookmark, BookmarkListResponse } from '@/types/note';
import { useAuth } from './AuthContext';
import { toast } from 'sonner';

interface BookmarkContextType {
  bookmarks: Bookmark[];
  bookmarkedIds: Set<string>;
  loading: boolean;
  toggleBookmark: (noteId: string, noteTitle?: string) => Promise<boolean>;
  isBookmarked: (noteId: string) => boolean;
  refetchBookmarks: () => Promise<void>;
}

const BookmarkContext = createContext<BookmarkContextType | undefined>(undefined);

export const BookmarkProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [bookmarkedIds, setBookmarkedIds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState<boolean>(false);

  const fetchBookmarks = async () => {
    if (!user) {
      setBookmarks([]);
      setBookmarkedIds(new Set());
      return;
    }
    setLoading(true);
    try {
      const res = await api.get<BookmarkListResponse>('/api/bookmarks');
      setBookmarks(res.bookmarks || []);
      const ids = new Set((res.bookmarks || []).map((b) => b.note_id));
      setBookmarkedIds(ids);
    } catch (err) {
      console.warn('Failed to load bookmarks', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookmarks();
  }, [user]);

  const isBookmarked = (noteId: string): boolean => {
    return bookmarkedIds.has(noteId);
  };

  const toggleBookmark = async (noteId: string, noteTitle?: string): Promise<boolean> => {
    if (!user) {
      toast.error('Please sign in with your @sst.scaler.com account to bookmark notes.');
      return false;
    }

    const wasBookmarked = bookmarkedIds.has(noteId);
    const label = noteTitle || noteId;

    // 1. Optimistic UI update immediately to mask serverless cold starts
    setBookmarkedIds((prev) => {
      const next = new Set(prev);
      if (wasBookmarked) {
        next.delete(noteId);
      } else {
        next.add(noteId);
      }
      return next;
    });

    setBookmarks((prev) => {
      if (wasBookmarked) {
        return prev.filter((b) => b.note_id !== noteId);
      } else {
        return [{ note_id: noteId, created_at: new Date().toISOString() }, ...prev];
      }
    });

    if (wasBookmarked) {
      toast.info(`Removed "${label}" from bookmarks`);
    } else {
      toast.success(`Bookmarked "${label}"`);
    }

    try {
      if (wasBookmarked) {
        await api.delete(`/api/bookmarks/${noteId}`);
      } else {
        await api.put(`/api/bookmarks/${noteId}`);
      }
      return !wasBookmarked;
    } catch (err: any) {
      // 2. Rollback optimistic update on server error
      setBookmarkedIds((prev) => {
        const rollback = new Set(prev);
        if (wasBookmarked) {
          rollback.add(noteId);
        } else {
          rollback.delete(noteId);
        }
        return rollback;
      });
      setBookmarks((prev) => {
        if (wasBookmarked) {
          return [{ note_id: noteId, created_at: new Date().toISOString() }, ...prev];
        } else {
          return prev.filter((b) => b.note_id !== noteId);
        }
      });
      toast.error(`Bookmark sync failed: ${err.message || 'Server error'}. Rolled back.`);
      return wasBookmarked;
    }
  };

  return (
    <BookmarkContext.Provider
      value={{
        bookmarks,
        bookmarkedIds,
        loading,
        toggleBookmark,
        isBookmarked,
        refetchBookmarks: fetchBookmarks,
      }}
    >
      {children}
    </BookmarkContext.Provider>
  );
};

export const useBookmarks = () => {
  const context = useContext(BookmarkContext);
  if (!context) {
    throw new Error('useBookmarks must be used within a BookmarkProvider');
  }
  return context;
};
