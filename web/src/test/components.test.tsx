import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { MarkdownViewer } from '@/components/MarkdownViewer';
import { SearchModal } from '@/components/SearchModal';
import { Sidebar } from '@/components/Sidebar';
import { MobileTableOfContents } from '@/components/TableOfContents';
import { BookmarkProvider, useBookmarks } from '@/context/BookmarkContext';
import { api } from '@/services/apiClient';
import { App } from '@/App';

// Mock Sonner toast
vi.mock('sonner', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
    info: vi.fn(),
  },
}));

vi.mock('@/services/notesService', () => ({
  fetchNotesIndex: vi.fn().mockResolvedValue([]),
  fetchNoteById: vi.fn().mockResolvedValue(null),
}));

// Mock AuthContext
const mockUser = {
  user_id: 'user_123',
  email: 'student@sst.scaler.com',
  display_name: 'SST Student',
  status: 'active',
  created_at: '2026-01-01T00:00:00Z',
  active_term: 1,
  year_of_study: 1,
  max_allowed_term: 4,
};

let currentMockUser: any = mockUser;
let currentMockAuthLoading = false;

vi.mock('@/context/AuthContext', () => ({
  useAuth: () => ({
    user: currentMockUser,
    loading: currentMockAuthLoading,
    loginWithGoogle: vi.fn(),
    logout: vi.fn(),
    refreshSession: vi.fn(),
  }),
}));

const mockNotesIndex = [
  {
    note_id: 'cn-lecture-01-introduction',
    term: 'Term 1',
    subject_code: 'CN',
    topic_title: 'Introduction to Computer Networks',
    tags: ['Networking', 'OSI'],
    summary: 'Foundations of computer networks.',
    learning_objectives: ['Learn OSI model'],
    last_updated: '2026-10-01T00:00:00Z',
  },
  {
    note_id: 'cml-lecture-01-linear-regression',
    term: 'Term 1',
    subject_code: 'CML',
    topic_title: 'Linear Regression and Gradient Descent',
    tags: ['ML', 'Math'],
    summary: 'Linear regression formulation.',
    learning_objectives: ['Learn MSE'],
    last_updated: '2026-10-01T00:00:00Z',
  },
];

describe('Frontend Component Acceptance Suite', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    currentMockUser = mockUser;
    currentMockAuthLoading = false;
  });

  // 1. Session Restoration Test
  it('renders session restoration loading state when authLoading is true', () => {
    currentMockAuthLoading = true;
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    expect(screen.getByText('Restoring session...')).toBeDefined();
    currentMockAuthLoading = false;
  });

  // 2. Search Modal Filtering and Keyboard Navigation Test
  it('filters notes in SearchModal by query and subject code', () => {
    const handleClose = vi.fn();
    render(
      <BrowserRouter>
        <SearchModal
          isOpen={true}
          onClose={handleClose}
          notes={mockNotesIndex}
        />
      </BrowserRouter>
    );

    const searchInput = screen.getByRole('textbox');
    expect(searchInput).toBeDefined();

    // Type "Linear"
    fireEvent.change(searchInput, { target: { value: 'Linear' } });

    // Should match CML Linear Regression and not Computer Networks
    expect(screen.getByText('Linear Regression and Gradient Descent')).toBeDefined();
    expect(screen.queryByText('Introduction to Computer Networks')).toBeNull();

    // Escape closes search
    fireEvent.keyDown(searchInput, { key: 'Escape' });
    expect(handleClose).toHaveBeenCalled();
  });

  // 3. Bookmark Optimistic Update & Rollback Test
  it('optimistically updates bookmark and rolls back on API failure', async () => {
    // Mock API failure on put
    const putSpy = vi.spyOn(api, 'put').mockRejectedValue(new Error('Network offline'));
    vi.spyOn(api, 'get').mockResolvedValue({ bookmarks: [] });

    const BookmarkTestConsumer = () => {
      const { isBookmarked, toggleBookmark } = useBookmarks();
      return (
        <div>
          <span data-testid="status">
            {isBookmarked('cn-lecture-01-introduction') ? 'BOOKMARKED' : 'UNBOOKMARKED'}
          </span>
          <button
            onClick={() => toggleBookmark('cn-lecture-01-introduction', 'Intro to CN')}
          >
            Toggle
          </button>
        </div>
      );
    };

    render(
      <BookmarkProvider>
        <BookmarkTestConsumer />
      </BookmarkProvider>
    );

    const statusEl = screen.getByTestId('status');
    const toggleBtn = screen.getByText('Toggle');

    expect(statusEl.textContent).toBe('UNBOOKMARKED');

    // Click toggle — should immediately update optimistically
    fireEvent.click(toggleBtn);
    expect(statusEl.textContent).toBe('BOOKMARKED');

    // After API failure, it should rollback to UNBOOKMARKED
    await waitFor(() => {
      expect(statusEl.textContent).toBe('UNBOOKMARKED');
    });

    expect(putSpy).toHaveBeenCalledWith('/api/bookmarks/cn-lecture-01-introduction');
  });

  // 4. Mobile Drawer & Mobile TOC Behavior
  it('handles mobile drawer dialog accessibility, escape key, and mobile TOC toggle', () => {
    const handleCloseMobile = vi.fn();

    render(
      <BrowserRouter>
        <BookmarkProvider>
          <Sidebar
            notes={mockNotesIndex}
            currentTerm="Term 1"
            onSelectTerm={vi.fn()}
            isZenMode={false}
            onToggleZenMode={vi.fn()}
            isMobileOpen={true}
            onCloseMobile={handleCloseMobile}
          />
        </BookmarkProvider>
      </BrowserRouter>
    );

    // Dialog accessibility attributes
    const drawer = screen.getByRole('dialog');
    expect(drawer).toBeDefined();
    expect(drawer.getAttribute('aria-modal')).toBe('true');

    // Press Escape to close drawer
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(handleCloseMobile).toHaveBeenCalled();

    // Test MobileTableOfContents
    const mockSections = [
      { section_id: 'sec-1', heading: 'First Section', body: 'Body 1', citations: ['Ref 1'] },
      { section_id: 'sec-2', heading: 'Second Section', body: 'Body 2', citations: ['Ref 2'] },
    ];

    const { unmount } = render(<MobileTableOfContents sections={mockSections} />);
    const toggleTOC = screen.getByLabelText('Toggle mobile table of contents');
    expect(toggleTOC).toBeDefined();
    expect(toggleTOC.getAttribute('aria-expanded')).toBe('false');

    // Open Mobile TOC
    fireEvent.click(toggleTOC);
    expect(toggleTOC.getAttribute('aria-expanded')).toBe('true');
    expect(screen.getAllByText('First Section').length).toBeGreaterThanOrEqual(1);
    expect(screen.getAllByText('Second Section').length).toBeGreaterThanOrEqual(1);

    unmount();
  });

  // 5. Unsafe Markdown Link Sanitization Test
  it('sanitizes unsafe javascript: and data: links while preserving safe https: and relative links', () => {
    const markdownContent = `
[Safe External Link](https://scaler.com)
[Safe Relative Link](/term/term-1)
[Unsafe Javascript Link](javascript:alert("hacked"))
[Unsafe Data URI Link](data:text/html,<script>alert(1)</script>)
`;

    const { container } = render(<MarkdownViewer content={markdownContent} />);

    // Safe external links are preserved with target="_blank"
    const safeExternal = container.querySelector('a[href="https://scaler.com"]');
    expect(safeExternal).not.toBeNull();
    expect(safeExternal?.getAttribute('target')).toBe('_blank');

    // Safe relative links are preserved
    const safeRelative = container.querySelector('a[href="/term/term-1"]');
    expect(safeRelative).not.toBeNull();

    // Dangerous schemes must NEVER be present in the rendered DOM href attributes
    const dangerousJs = container.querySelector('a[href*="javascript:"]');
    expect(dangerousJs).toBeNull();

    const dangerousData = container.querySelector('a[href*="data:"]');
    expect(dangerousData).toBeNull();
  });

  // 6. Comment Section Tests
  it('renders comments, performs optimistic posting, and handles rollback on error', async () => {
    const { CommentSection } = await import('@/components/CommentSection');
    const getSpy = vi.spyOn(api, 'get').mockResolvedValue({
      comments: [
        {
          id: 'cmt-1',
          note_id: 'cn-lecture-01-introduction',
          user_id: 'user_other',
          content: 'Great overview of the OSI layers!',
          created_at: new Date(Date.now() - 3600000).toISOString(),
          updated_at: new Date(Date.now() - 3600000).toISOString(),
          username: 'student_bob',
          avatar_url: null,
          score: 0,
          upvoted_by: [],
          downvoted_by: [],
          parent_id: null,
        },
      ],
      total: 1,
    });

    const postSpy = vi.spyOn(api, 'post').mockRejectedValue(new Error('Rate limit exceeded: max 3 per minute'));

    render(<CommentSection noteId="cn-lecture-01-introduction" />);

    // Wait for initial comments to load
    await waitFor(() => {
      expect(screen.getByText('@student_bob')).toBeDefined();
      expect(screen.getByText('Great overview of the OSI layers!')).toBeDefined();
    });

    // Check textarea
    const textarea = screen.getByPlaceholderText(/Leave a comment.../i);
    expect(textarea).toBeDefined();

    // Type a new comment
    fireEvent.change(textarea, { target: { value: 'Optimistic comment test' } });
    const postBtn = screen.getByRole('button', { name: /Post/i });

    // Click post -> optimistic insertion
    fireEvent.click(postBtn);
    expect(screen.getByText('Optimistic comment test')).toBeDefined();

    // Because post rejected with error, it must rollback the comment from the list
    await waitFor(() => {
      expect(screen.queryByText('@SST Student')).toBeNull();
    });

    expect(postSpy).toHaveBeenCalled();
  });

  // 7. 3-State Voting Test (Upvote / Downvote)
  it('optimistically handles upvote and downvote state toggles', async () => {
    const { CommentSection } = await import('@/components/CommentSection');
    vi.spyOn(api, 'get').mockResolvedValue({
      comments: [
        {
          id: 'cmt-vote-1',
          note_id: 'cn-lecture-01-introduction',
          user_id: 'user_other',
          content: 'Vote test target comment',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          username: 'student_alice',
          avatar_url: null,
          score: 5,
          upvoted_by: [],
          downvoted_by: [],
          parent_id: null,
        },
      ],
      total: 1,
    });

    const voteSpy = vi.spyOn(api, 'post').mockResolvedValue({
      id: 'cmt-vote-1',
      score: 6,
      user_vote: 'upvote',
    });

    render(<CommentSection noteId="cn-lecture-01-introduction" />);

    await waitFor(() => {
      expect(screen.getByText('5')).toBeDefined();
    });

    // Click upvote -> score becomes 6 optimistically
    const upBtn = screen.getByRole('button', { name: /upvote comment/i });
    fireEvent.click(upBtn);
    expect(screen.getByText('6')).toBeDefined();

    expect(voteSpy).toHaveBeenCalledWith(
      '/api/comments/cmt-vote-1/vote',
      { action: 'upvote' }
    );
  });
});
