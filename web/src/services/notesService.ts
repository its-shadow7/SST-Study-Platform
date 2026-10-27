import { Note, NoteIndexItem } from '../types/note';
import { api, ApiError } from './apiClient';

// In-memory cache for fast navigation between reader and studio
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL_MS = 60 * 1000; // 1 minute

export function clearNotesCache(): void {
  cache.clear();
}

/**
 * Fetches the catalogue index of notes accessible to the current student.
 * If includeDrafts is true (moderator/admin), includes draft status notes.
 */
export async function fetchNotesIndex(includeDrafts: boolean = false): Promise<NoteIndexItem[]> {
  const cacheKey = `notes_index_${includeDrafts}`;
  const cached = cache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    return cached.data as NoteIndexItem[];
  }

  try {
    const data = await api.get<NoteIndexItem[]>(
      `/api/notes?include_drafts=${includeDrafts ? 'true' : 'false'}`
    );
    cache.set(cacheKey, { data, timestamp: Date.now() });
    return data;
  } catch (err: any) {
    if (err?.status === 401 || err?.status === 403) {
      throw new Error('AUTH_REQUIRED');
    }
    throw new Error(err?.message || 'Failed to load course note catalogue');
  }
}

/**
 * Fetches complete note content by ID (including all sections and topic quiz).
 * Term gating is enforced by the FastAPI backend (403 FORBIDDEN if higher term than allowed).
 */
export async function fetchNoteById(noteId: string): Promise<Note> {
  const cleanId = noteId.toLowerCase().trim();
  const cacheKey = `note_${cleanId}`;
  const cached = cache.get(cacheKey);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    return cached.data as Note;
  }

  try {
    const data = await api.get<Note>(`/api/notes/${encodeURIComponent(cleanId)}`);
    cache.set(cacheKey, { data, timestamp: Date.now() });
    return data;
  } catch (err: any) {
    if (err?.status === 401) {
      throw new Error('AUTH_REQUIRED');
    }
    if (err?.status === 403) {
      throw new Error('TERM_LOCKED');
    }
    if (err?.status === 404) {
      throw new Error('NOTE_NOT_FOUND');
    }
    throw new Error(err?.message || `Failed to load note '${cleanId}'`);
  }
}

/**
 * Saves or updates a note in MongoDB Atlas (moderator/admin only).
 * Automatically invalidates local note caches.
 */
export async function saveNote(noteData: Partial<Note> & { note_id: string }): Promise<Note> {
  const cleanId = noteData.note_id.toLowerCase().trim();
  try {
    // Uses PUT /api/notes/{id} which upserts atomically
    const saved = await api.put<Note>(`/api/notes/${encodeURIComponent(cleanId)}`, noteData);
    clearNotesCache();
    return saved;
  } catch (err: any) {
    throw new Error(err?.message || `Failed to save note '${cleanId}'`);
  }
}

/**
 * Deletes a note permanently from MongoDB Atlas (moderator/admin only).
 * Automatically invalidates local note caches.
 */
export async function deleteNote(noteId: string): Promise<void> {
  const cleanId = noteId.toLowerCase().trim();
  try {
    await api.delete(`/api/notes/${encodeURIComponent(cleanId)}`);
    clearNotesCache();
  } catch (err: any) {
    throw new Error(err?.message || `Failed to delete note '${cleanId}'`);
  }
}
