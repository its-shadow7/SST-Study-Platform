export type UserRole = 'student' | 'moderator' | 'admin';

export interface Comment {
  id: string;
  note_id: string;
  user_id: string;
  content: string;
  parent_id?: string | null;
  score: number;
  upvoted_by: string[];
  downvoted_by: string[];
  status?: 'published' | 'quarantined' | 'reported' | 'deleted';
  moderation_reasons?: string[];
  reported_by?: string[];
  created_at: string;
  updated_at: string;
  username?: string | null;
  avatar_url?: string | null;
  author_role?: UserRole | null;
  initialRank?: number;
}

export interface ThreadedComment extends Comment {
  replies: ThreadedComment[];
}

export interface CommentListResponse {
  comments: Comment[];
  total: number;
}

export interface VoteResponse {
  id: string;
  score: number;
  user_vote?: 'upvote' | 'downvote' | null;
}
