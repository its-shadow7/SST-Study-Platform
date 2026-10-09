import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { api } from '../services/apiClient';
import { Bookmark, BookmarkListResponse } from '../types/note';
import { useAuth } from './AuthContext';

interface BookmarkContextType {
  bookmarkedIds: Set<string>;
  loading: boolean;
  toggleBookmark: (noteId: string) => Promise<boolean>;
  isBookmarked: (noteId: string) => boolean;
  toastMessage: string | null;
  clearToast: () => void;
}

const BookmarkContext = createContext<BookmarkContextType | undefined>(undefined);

export const BookmarkProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { user } = useAuth();
  const [bookmarkedIds, setBookmarkedIds] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState<boolean>(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  const clearToast = () => setToastMessage(null);

  const fetchBookmarks = async () => {
    if (!user) {
      setBookmarkedIds(new Set());
      return;
    }
    setLoading(true);
    try {
      const res = await api.get<BookmarkListResponse>('/api/bookmarks');
      const ids = new Set(res.bookmarks.map((b) => b.note_id));
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

  const toggleBookmark = async (noteId: string): Promise<boolean> => {
    if (!user) {
      setToastMessage('Please sign in with your @sst.scaler.com account to bookmark notes.');
      return false;
    }

    const wasBookmarked = bookmarkedIds.has(noteId);
    
    // 1. Optimistic UI update
    setBookmarkedIds((prev) => {
      const next = new Set(prev);
      if (wasBookmarked) {
        next.delete(noteId);
      } else {
        next.add(noteId);
      }
      return next;
    });

    try {
      if (wasBookmarked) {
        await api.delete(`/api/bookmarks/${noteId}`);
        setToastMessage(`Removed bookmark for ${noteId}`);
      } else {
        await api.put(`/api/bookmarks/${noteId}`);
        setToastMessage(`Bookmarked ${noteId}`);
      }
      return !wasBookmarked;
    } catch (err: any) {
      // 2. Server rollback on failure (TDD Section 8)
      setBookmarkedIds((prev) => {
        const rollback = new Set(prev);
        if (wasBookmarked) {
          rollback.add(noteId);
        } else {
          rollback.delete(noteId);
        }
        return rollback;
      });
      setToastMessage(`Failed to update bookmark (${err.message || 'Network error'}). Rolled back.`);
      return wasBookmarked;
    }
  };

  return (
    <BookmarkContext.Provider
      value={{
        bookmarkedIds,
        loading,
        toggleBookmark,
        isBookmarked,
        toastMessage,
        clearToast
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
