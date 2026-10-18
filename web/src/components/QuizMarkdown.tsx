import React, { useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

interface QuizMarkdownProps {
  content?: string | null;
  className?: string;
  isInline?: boolean;
}

/**
 * Pre-processes text to ensure LaTeX math formulas render properly via KaTeX:
 * 1. Handles escaped dollar signs (\$ -> &dollar;).
 * 2. Normalizes known ASCII/pseudo-math formulas (e.g. sqrt( sum (x_j - z_j)^2 )).
 * 3. Auto-wraps un-delimited LaTeX commands (e.g. \frac{...}{...}, \nabla, \eta) in $...$
 *    if not already enclosed in dollar signs.
 */
export function preprocessQuizMath(text: string): string {
  if (!text) return '';

  let processed = text;

  // 1. Transform known pseudo-math patterns to standard LaTeX if present
  // Handle Euclidean/Manhattan/Chebyshev distance formula options
  processed = processed.replace(/\bsqrt\(\s*sum\s*\(\s*x_j\s*-\s*z_j\s*\)\^2\s*\)/gi, '$\\sqrt{\\sum_{j=1}^d (x_j - z_j)^2}$');
  processed = processed.replace(/\bsum\s*\|x_j\s*-\s*z_j\|/gi, '$\\sum_{j=1}^d |x_j - z_j|$');
  processed = processed.replace(/\bmax\s*\|x_j\s*-\s*z_j\|/gi, '$\\max_{j \\in \\{1, \\dots, d\\}} |x_j - z_j|$');
  processed = processed.replace(/\b1\s*-\s*\(\s*x\s*\.\s*z\s*\)/gi, '$1 - (\\mathbf{x} \\cdot \\mathbf{z})$');

  // Handle common single expressions without $ delimiters
  // If the entire text begins with a LaTeX command and has no $, wrap it in $
  const trimmed = processed.trim();
  if (!trimmed.includes('$')) {
    // Check if the entire string is a standalone formula starting with a backslash
    // e.g. "\frac{1}{m} \sum_{i=1}^m (\hat{y}_i - y_i)"
    // or "\eta < \frac{2}{\lambda_{\max}(\mathbf{H})}, where \lambda_{\max}..."
    if (
      trimmed.startsWith('\\') &&
      !trimmed.startsWith('\\text') &&
      !trimmed.match(/^\\(?:An|The|What|Why|Which|How|Suppose|In|Because|By|When)\b/i)
    ) {
      // Check if it's purely a formula or formula with explanation clause
      const clauseMatch = trimmed.match(/^(\\[^,;]+(?:,\s*where\s+.*)?)$/s);
      if (clauseMatch && !trimmed.includes('\n')) {
        // If it contains ", where ", separate math part and text part
        const whereIdx = trimmed.indexOf(', where ');
        if (whereIdx !== -1) {
          const formulaPart = trimmed.substring(0, whereIdx);
          const restPart = trimmed.substring(whereIdx + 8);
          // Auto-wrap restPart's LaTeX commands if any
          const wrappedRest = restPart.replace(/(\\[a-zA-Z]+(?:_\{[^}]+\}|_\w+)?)/g, '$$$1$$');
          return `$${formulaPart}$, where ${wrappedRest}`;
        }
        return `$${trimmed}$`;
      }
    }

    // Replace un-delimited LaTeX sequences in sentences or options
    // E.g. "\nabla J(\mathbf{w})" or "\mathbf{w}^{(t+1)} := ..." or "\frac{\partial J}{\partial w_j}" or "\eta"
    processed = processed.replace(
      /(\\(?:frac\{[^{}]*\}\{[^{}]*\}|nabla(?:\^2|_\{[^}]+\})?(?:\s*[A-Z]\([^)]+\))?|mathbf\{[^{}]*\}(?:[\^_]\{?[^{}\s]*\}?)?|hat\{[^{}]*\}(?:[\^_]\{?[^{}\s]*\}?)?|partial(?:J)?(?:\/\\partial\s*\w+)?|sum(?:_\{[^{}]*\}|\^[^{}\s]*)?|sqrt\{[^{}]*\}|(?:eta|alpha|beta|theta|lambda|sigma|mu|epsilon|gamma|delta|omega|phi|psi|tau|kappa)(?:_\{[^{}]*\}|_\w+)?|approx|le|ge|neq|times|cdot|in|to)\b[^\s,\.\?\)]*(?:\s*[\+\-\*\=\<\>\/]\s*[^,\.\?\)]+)?)/g,
      (match) => {
        const mTrimmed = match.trim();
        if (mTrimmed.startsWith('$') && mTrimmed.endsWith('$')) return match;
        return `$${mTrimmed}$`;
      }
    );
  }

  // Convert escaped dollar signs (\$ or \\$) to HTML entity &dollar; so they don't break KaTeX
  processed = processed.replace(/\\(\$)/g, () => '&dollar;');

  return processed;
}

export const QuizMarkdown: React.FC<QuizMarkdownProps> = ({
  content,
  className = '',
  isInline = false,
}) => {
  const sanitized = useMemo(() => {
    return preprocessQuizMath(content || '');
  }, [content]);

  if (!sanitized) return null;

  return (
    <div
      className={`quiz-markdown ${isInline ? 'inline align-middle' : 'block'} text-inherit ${className}`}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[[rehypeKatex, { trust: false, strict: false }]]}
        skipHtml={false}
        components={{
          p: isInline
            ? ({ children }) => <span className="inline leading-relaxed">{children}</span>
            : ({ children }) => <p className="mb-2 last:mb-0 leading-relaxed">{children}</p>,
          code: ({ children }) => (
            <code className="px-1.5 py-0.5 rounded bg-white/[0.06] text-amber-300 font-mono text-[0.85em] border border-white/10">
              {children}
            </code>
          ),
          a: ({ ...props }) => (
            <a
              {...props}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-400 hover:underline underline-offset-2"
            />
          ),
        }}
      >
        {sanitized}
      </ReactMarkdown>
    </div>
  );
};
