export interface ScratchpadData {
  id: string | null;
  user_id?: string | null;
  note_id: string;
  content: string;
  updated_at: string | null;
}

export interface ScratchpadSummary {
  note_ids: string[];
}

export type ScratchpadSaveStatus = 'saved' | 'saving' | 'unsaved' | 'error';
