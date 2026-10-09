import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

interface MarkdownViewerProps {
  content: string;
}

export const MarkdownViewer: React.FC<MarkdownViewerProps> = ({ content }) => {
  return (
    <div className="markdown-body">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[[rehypeKatex, { trust: false }]]}
        skipHtml={true} // Strictly disable raw HTML (TDD Section 8)
        components={{
          // Safe link handling with rel="noopener noreferrer"
          a: ({ node, href, children, ...props }) => {
            const isExternal = href?.startsWith('http://') || href?.startsWith('https://');
            return (
              <a
                href={href}
                target={isExternal ? '_blank' : undefined}
                rel={isExternal ? 'noopener noreferrer' : undefined}
                style={{ color: 'var(--primary)', textDecoration: 'underline' }}
                {...props}
              >
                {children}
              </a>
            );
          },
          // Render Mermaid and code blocks safely without running eval/exec
          code: ({ node, className, children, ...props }) => {
            const match = /language-(\w+)/.exec(className || '');
            const lang = match ? match[1] : '';

            // Even if mermaid is tagged, render as safe code block (TDD Section 8)
            return (
              <code className={className} {...props}>
                {children}
              </code>
            );
          }
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};
