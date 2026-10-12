import { Note, NoteIndexItem } from '../types/note';
import { setCsrfToken } from './apiClient';

let refreshPromise: Promise<boolean> | null = null;

/**
 * Deduplicated auth session refresh.
 * Calls /api/auth/refresh to rotate refresh token and obtain a fresh access_token cookie.
 */
async function refreshAuthSession(): Promise<boolean> {
  if (refreshPromise) {
    return refreshPromise;
  }

  refreshPromise = (async () => {
    try {
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        return false;
      }

      const data = await response.json();
      if (data?.csrf_token) {
        setCsrfToken(data.csrf_token);
      }
      return true;
    } catch {
      return false;
    } finally {
      refreshPromise = null;
    }
  })();

  return refreshPromise;
}

export async function fetchNotesIndex(): Promise<NoteIndexItem[]> {
  let response = await fetch('/data/notes-index.json', {
    credentials: 'include',
  });

  if (response.status === 401) {
    const refreshed = await refreshAuthSession();
    if (refreshed) {
      response = await fetch('/data/notes-index.json', {
        credentials: 'include',
      });
    }
  }

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      throw new Error('AUTH_REQUIRED');
    }
    throw new Error(`Failed to load course note catalogue (${response.status})`);
  }

  return response.json();
}

export async function fetchNoteById(noteId: string): Promise<Note> {
  let response = await fetch(`/data/notes/${noteId}.json`, {
    credentials: 'include',
  });

  if (response.status === 401) {
    const refreshed = await refreshAuthSession();
    if (refreshed) {
      response = await fetch(`/data/notes/${noteId}.json`, {
        credentials: 'include',
      });
    }
  }

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      throw new Error('AUTH_REQUIRED');
    }
    if (response.status === 404) {
      throw new Error('NOTE_NOT_FOUND');
    }
    throw new Error(`Failed to load note '${noteId}' (${response.status})`);
  }

  return response.json();
}

