import { Note, NoteIndexItem } from '../types/note';

export async function fetchNotesIndex(): Promise<NoteIndexItem[]> {
  const response = await fetch('/data/notes-index.json', {
    credentials: 'include'
  });

  if (!response.ok) {
    if (response.status === 401 || response.status === 403) {
      throw new Error('AUTH_REQUIRED');
    }
    throw new Error(`Failed to load course note catalogue (${response.status})`);
  }

  return response.json();
}

export async function fetchNoteById(noteId: string): Promise<Note> {
  const response = await fetch(`/data/notes/${noteId}.json`, {
    credentials: 'include'
  });

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
