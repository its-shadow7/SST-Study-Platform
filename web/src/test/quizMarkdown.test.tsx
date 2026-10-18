import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { QuizMarkdown, preprocessQuizMath } from '@/components/QuizMarkdown';

describe('QuizMarkdown & Math Preprocessor', () => {
  it('converts Euclidean distance pseudo-math to LaTeX formula', () => {
    const raw = 'sqrt( sum (x_j - z_j)^2 )';
    const processed = preprocessQuizMath(raw);
    expect(processed).toContain('\\sqrt{\\sum_{j=1}^d (x_j - z_j)^2}');
  });

  it('converts Manhattan distance pseudo-math to LaTeX formula', () => {
    const raw = 'sum |x_j - z_j|';
    const processed = preprocessQuizMath(raw);
    expect(processed).toContain('\\sum_{j=1}^d |x_j - z_j|');
  });

  it('preserves existing dollar-wrapped LaTeX math', () => {
    const raw = '$\\sqrt{\\sum_{j=1}^d (x_j - z_j)^2}$';
    const processed = preprocessQuizMath(raw);
    expect(processed).toBe(raw);
  });

  it('auto-wraps standalone raw LaTeX formula in dollar signs', () => {
    const raw = '\\frac{1}{m} \\sum_{i=1}^m (\\hat{y}_i - y_i)';
    const processed = preprocessQuizMath(raw);
    expect(processed).toBe('$\\frac{1}{m} \\sum_{i=1}^m (\\hat{y}_i - y_i)$');
  });

  it('renders KaTeX math elements in DOM', () => {
    const { container } = render(
      <QuizMarkdown content="Which formula $\sqrt{\sum (x_j - z_j)^2}$ is correct?" />
    );
    // KaTeX outputs elements with class "katex"
    const katexEl = container.querySelector('.katex');
    expect(katexEl).not.toBeNull();
  });

  it('renders inline options without wrapping block paragraph', () => {
    const { container } = render(
      <QuizMarkdown content="Option A text" isInline={true} />
    );
    expect(container.querySelector('p')).toBeNull();
    expect(container.querySelector('span')).not.toBeNull();
  });
});
