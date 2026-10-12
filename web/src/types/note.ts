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
  username: string;
  active_term: number;
  avatar_url?: string | null;
  bio?: string | null;
  csrf_token?: string;
  role?: 'student' | 'moderator' | 'admin';
  batch_year?: number;
  year_of_study?: number;
  max_allowed_term?: number;
  is_special?: boolean;
  needs_profile_setup?: boolean;
}

export interface Bookmark {
  note_id: string;
  created_at: string;
}

export interface BookmarkListResponse {
  bookmarks: Bookmark[];
}

export type Theme = 'oled-slate' | 'minimalist-midnight' | 'clean-light';

export interface NotificationItem {
  id: string;
  user_id: string;
  type: 'reply' | 'report_resolved' | 'comment_status' | 'system';
  title: string;
  message: string;
  link?: string | null;
  read: boolean;
  created_at: string;
}

export interface NotificationListResponse {
  notifications: NotificationItem[];
  unread_count: number;
}

export interface ModerationAuditLogItem {
  id: string;
  action: 'approved' | 'deleted' | 'auto_quarantined' | 'quarantined';
  comment_id: string;
  note_id?: string | null;
  comment_content?: string | null;
  moderator_id: string;
  moderator_name: string;
  moderator_role: string;
  reason?: string | null;
  created_at: string;
}

export interface ModerationAuditLogResponse {
  logs: ModerationAuditLogItem[];
  total: number;
}

