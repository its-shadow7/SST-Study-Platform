import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { QuizSection } from '@/components/QuizSection';
import { Quiz } from '@/types/note';

// Mock AuthContext
vi.mock('@/context/AuthContext', () => ({
  useAuth: () => ({
    user: { user_id: 'test-user', email: 'student@sst.scaler.com' },
    loading: false,
  }),
}));

// Mock Sonner toast
vi.mock('sonner', () => ({
  toast: {
    success: vi.fn(),
    error: vi.fn(),
    info: vi.fn(),
  },
}));

// Mock apiClient to prevent network calls during testing
vi.mock('@/services/apiClient', () => ({
  api: {
    get: vi.fn().mockResolvedValue(null),
    put: vi.fn().mockResolvedValue({}),
    delete: vi.fn().mockResolvedValue({}),
  },
}));

describe('QuizSection LaTeX Math Rendering Acceptance Test', () => {
  const sampleQuiz: Quiz = {
    title: 'Distance Metrics Quiz',
    description: 'Testing LaTeX math rendering in quizzes',
    estimated_minutes: 10,
    questions: [
      {
        id: 'q-cml-l09-04',
        type: 'single_choice',
        difficulty: 'easy',
        subtopic: 'Distance Metric Formulation',
        question:
          'Which mathematical distance formula corresponds to the straight-line Euclidean distance ($L_2$ norm) between vectors $\\mathbf{x}$ and $\\mathbf{z}$ in $d$ dimensions?',
        correctOptionIds: ['opt-2'],
        options: [
          {
            id: 'opt-1',
            text: '$\\sum_{j=1}^d |x_j - z_j|$',
          },
          {
            id: 'opt-2',
            text: '$\\sqrt{\\sum_{j=1}^d (x_j - z_j)^2}$',
          },
          {
            id: 'opt-3',
            text: '$\\max_{j \\in \\{1, \\dots, d\\}} |x_j - z_j|$',
          },
          {
            id: 'opt-4',
            text: '$1 - (\\mathbf{x} \\cdot \\mathbf{z})$',
          },
        ],
        explanation:
          'Euclidean distance is the square root of the sum of squared coordinate differences: $\\sqrt{\\sum_{j=1}^d (x_j - z_j)^2}$. Option 1 is Manhattan ($L_1$), and Option 3 is Chebyshev ($L_\\infty$).',
      },
    ],
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders LaTeX formulas as KaTeX mathematical elements in question and options', () => {
    const { container } = render(<QuizSection quiz={sampleQuiz} noteId="cml-t5-l09" />);

    // Verify KaTeX math elements exist in the DOM
    const katexElements = container.querySelectorAll('.katex');
    expect(katexElements.length).toBeGreaterThan(0);

    // Verify all 4 options render KaTeX math elements
    const optionButtons = screen.getAllByRole('button').filter((b) =>
      b.className.includes('w-full') && b.className.includes('p-4')
    );
    expect(optionButtons.length).toBe(4);

    optionButtons.forEach((btn) => {
      const optionKatex = btn.querySelector('.katex');
      expect(optionKatex).not.toBeNull();
    });
  });

  it('renders LaTeX in explanation card after checking the answer', () => {
    const { container } = render(<QuizSection quiz={sampleQuiz} noteId="cml-t5-l09" />);

    // Select the correct option (option 2: Euclidean distance)
    const optionButtons = screen.getAllByRole('button').filter((b) =>
      b.className.includes('w-full') && b.className.includes('p-4')
    );
    fireEvent.click(optionButtons[1]);

    // Click "Check Answer"
    const checkBtn = screen.getByRole('button', { name: /check answer/i });
    fireEvent.click(checkBtn);

    // Verify explanation card is displayed
    expect(screen.getByText('Explanation')).toBeDefined();

    // Verify explanation contains KaTeX rendered formula
    const explanationCard = container.querySelector('.animate-in');
    expect(explanationCard).not.toBeNull();
    const explanationKatex = explanationCard?.querySelectorAll('.katex');
    expect(explanationKatex && explanationKatex.length).toBeGreaterThan(0);
  });

  it('renders LaTeX math in question-by-question review screen upon completion', () => {
    const { container } = render(<QuizSection quiz={sampleQuiz} noteId="cml-t5-l09" />);

    // Select option 2
    const optionButtons = screen.getAllByRole('button').filter((b) =>
      b.className.includes('w-full') && b.className.includes('p-4')
    );
    fireEvent.click(optionButtons[1]);

    // Check answer
    const checkBtn = screen.getByRole('button', { name: /check answer/i });
    fireEvent.click(checkBtn);

    // Click "View Results" to complete the quiz
    const nextBtn = screen.getByRole('button', { name: /view results/i });
    fireEvent.click(nextBtn);

    // Verify Review / Summary screen
    expect(screen.getByText('Topic Quiz Completed!')).toBeDefined();
    expect(screen.getByText('Question-by-Question Audit')).toBeDefined();

    // Verify that the audit section renders KaTeX elements for question, answers, and explanation
    const auditKatex = container.querySelectorAll('.katex');
    expect(auditKatex.length).toBeGreaterThan(0);
  });
});
