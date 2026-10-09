export interface NoteSection {
  section_id: string;
  heading: string;
  body: string;
  citations: string[];
}

export interface Note {
  schema_version: number;
  note_id: string;
  term: string;
  subject_code: string;
  topic_title: string;
  tags: string[];
  learning_objectives: string[];
  summary: string;
  key_takeaways: string[];
  sections: NoteSection[];
  last_updated: string;
  approval_status: string;
}

export interface NoteIndexItem {
  note_id: string;
  term: string;
  subject_code: string;
  topic_title: string;
  tags: string[];
  summary: string;
  learning_objectives: string[];
  last_updated: string;
}

export interface User {
  user_id: string;
  email: string;
  display_name: string;
  status: string;
  csrf_token?: string;
}

export interface Bookmark {
  note_id: string;
  created_at: string;
}

export interface BookmarkListResponse {
  bookmarks: Bookmark[];
}

export type Theme = 'oled-slate' | 'minimalist-midnight' | 'clean-light';
