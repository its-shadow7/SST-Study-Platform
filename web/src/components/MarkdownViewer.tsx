import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Check, Copy } from 'lucide-react';

interface MarkdownViewerProps {
  content: string;
  isCompact?: boolean;
}

const CodeBlock: React.FC<{ language: string; value: string; isCompact?: boolean }> = ({
  language,
  value,
  isCompact = true,
}) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(value);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (e) {
      console.error('Failed to copy', e);
    }
  };

  return (
    <div
      className={`relative group ${
        isCompact ? 'my-3.5' : 'my-6'
      } rounded-lg overflow-hidden border border-zinc-200 dark:border-white/10 bg-[#0f172a] shadow-sm dark:shadow-none`}
    >
      {/* Code Header bar */}
      <div
        className={`flex items-center justify-between ${
          isCompact ? 'px-3.5 py-1.5' : 'px-4 py-2'
        } bg-slate-800/90 dark:bg-white/[0.04] border-b border-slate-700/60 dark:border-white/[0.08] text-xs text-zinc-300 dark:text-zinc-400 font-mono select-none`}
      >
        <span className="uppercase tracking-wider text-[11px] font-semibold text-zinc-300 dark:text-zinc-400">
          {language || 'text'}
        </span>
        <button
          onClick={handleCopy}
          aria-label="Copy code block"
          className="flex items-center gap-1.5 px-2.5 py-1 rounded border border-slate-600/60 dark:border-white/10 bg-slate-700/50 dark:bg-white/5 hover:bg-slate-700 dark:hover:bg-white/10 text-zinc-200 dark:text-zinc-300 text-xs transition-all active:scale-95"
        >
          {copied ? (
            <>
              <Check className="w-3.5 h-3.5 text-emerald-400" />
              <span className="text-emerald-400 font-medium">Copied!</span>
            </>
          ) : (
            <>
              <Copy className="w-3.5 h-3.5 text-zinc-300 dark:text-zinc-400 group-hover:text-white" />
              <span>Copy</span>
            </>
          )}
        </button>
      </div>

      {/* Code Content */}
      <div className={`${isCompact ? 'p-3' : 'p-4'} overflow-x-auto text-[0.875rem]`}>
        <SyntaxHighlighter
          language={language || 'text'}
          style={vscDarkPlus}
          customStyle={{
            background: 'transparent',
            padding: 0,
            margin: 0,
            fontSize: isCompact ? '0.84rem' : '0.875rem',
            lineHeight: isCompact ? '1.55' : '1.65',
            fontFamily: 'JetBrains Mono, monospace',
          }}
          wrapLongLines={false}
        >
          {value.replace(/\n$/, '')}
        </SyntaxHighlighter>
      </div>
    </div>
  );
};

export const MarkdownViewer: React.FC<MarkdownViewerProps> = ({ content, isCompact = true }) => {
  const sanitizedContent = React.useMemo(() => {
    if (!content) return '';
    // Safely convert escaped dollar signs (\$ or \\$) to HTML entity &dollar;
    // Using a callback function ensures no '$' replacement pattern expansion happens.
    return content.replace(/\\(\$)/g, () => '&dollar;');
  }, [content]);

  const pClass = isCompact
    ? 'mb-3.5 leading-[1.62] text-zinc-700 dark:text-zinc-300 font-normal'
    : 'mb-6 leading-[1.85] text-zinc-700 dark:text-zinc-300 font-normal';

  const h1Class = isCompact
    ? 'text-xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100 mt-5 mb-2.5 border-b border-zinc-200 dark:border-white/10 pb-1.5'
    : 'text-2xl font-bold tracking-tight text-zinc-900 dark:text-zinc-100 mt-8 mb-4 border-b border-zinc-200 dark:border-white/10 pb-2';

  const h2Class = isCompact
    ? 'text-lg font-semibold tracking-tight text-zinc-900 dark:text-zinc-100 mt-4.5 mb-2'
    : 'text-xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-100 mt-7 mb-3';

  const h3Class = isCompact
    ? 'text-base font-medium text-zinc-800 dark:text-zinc-200 mt-3.5 mb-1.5'
    : 'text-lg font-medium text-zinc-800 dark:text-zinc-200 mt-6 mb-2';

  const listClass = isCompact
    ? 'pl-5 mb-3.5 space-y-1 text-zinc-700 dark:text-zinc-300'
    : 'pl-6 mb-6 space-y-2 text-zinc-700 dark:text-zinc-300';

  const blockquoteClass = isCompact
    ? 'border-l-2 border-blue-600 dark:border-blue-500/80 bg-blue-50/60 dark:bg-blue-500/5 px-3 py-1.5 rounded-r my-3.5 text-zinc-800 dark:text-zinc-300 italic'
    : 'border-l-2 border-blue-600 dark:border-blue-500/80 bg-blue-50/60 dark:bg-blue-500/5 px-4 py-2 rounded-r my-6 text-zinc-800 dark:text-zinc-300 italic';

  const tableContainerClass = isCompact
    ? 'overflow-x-auto my-3.5 rounded-lg border border-zinc-200 dark:border-white/10 shadow-sm dark:shadow-none'
    : 'overflow-x-auto my-6 rounded-lg border border-zinc-200 dark:border-white/10 shadow-sm dark:shadow-none';

  const thClass = isCompact
    ? 'px-3.5 py-2 bg-zinc-100/90 dark:bg-white/[0.03] border-b border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-200 font-semibold text-xs uppercase tracking-wider'
    : 'px-4 py-2.5 bg-zinc-100/90 dark:bg-white/[0.03] border-b border-zinc-200 dark:border-white/10 text-zinc-900 dark:text-zinc-200 font-semibold text-xs uppercase tracking-wider';

  const tdClass = isCompact
    ? 'px-3.5 py-2 border-b border-zinc-100 dark:border-white/5 text-zinc-700 dark:text-zinc-300 text-sm'
    : 'px-4 py-2.5 border-b border-zinc-100 dark:border-white/5 text-zinc-700 dark:text-zinc-300';

  return (
    <div
      className={`markdown-body text-zinc-700 dark:text-zinc-300 ${
        isCompact
          ? 'density-compact text-[0.9375rem] leading-[1.62]'
          : 'text-[1.0625rem] leading-markdown'
      } transition-all`}
    >
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[[rehypeKatex, { trust: false }]]}
        skipHtml={true}
        components={{
          // Off-white headings with tight letter-spacing
          h1: ({ children, ...props }) => (
            <h1 className={h1Class} {...props}>
              {children}
            </h1>
          ),
          h2: ({ children, ...props }) => (
            <h2 className={h2Class} {...props}>
              {children}
            </h2>
          ),
          h3: ({ children, ...props }) => (
            <h3 className={h3Class} {...props}>
              {children}
            </h3>
          ),
          p: ({ children, ...props }) => (
            <p className={pClass} {...props}>
              {children}
            </p>
          ),
          ul: ({ children, ...props }) => (
            <ul className={`list-disc ${listClass}`} {...props}>
              {children}
            </ul>
          ),
          ol: ({ children, ...props }) => (
            <ol className={`list-decimal ${listClass}`} {...props}>
              {children}
            </ol>
          ),
          li: ({ children, ...props }) => (
            <li className="leading-relaxed" {...props}>
              {children}
            </li>
          ),
          blockquote: ({ children, ...props }) => (
            <blockquote className={blockquoteClass} {...props}>
              {children}
            </blockquote>
          ),
          table: ({ children, ...props }) => (
            <div className={tableContainerClass}>
              <table className="w-full text-left text-sm border-collapse" {...props}>
                {children}
              </table>
            </div>
          ),
          th: ({ children, ...props }) => (
            <th className={thClass} {...props}>
              {children}
            </th>
          ),
          td: ({ children, ...props }) => (
            <td className={tdClass} {...props}>
              {children}
            </td>
          ),
          a: ({ href, children, ...props }) => {
            const isUnsafe = Boolean(href && /^(javascript|data|vbscript|file):/i.test(href.trim()));
            const safeHref = isUnsafe ? '#' : href;
            const isExternal = Boolean(safeHref && (safeHref.startsWith('http://') || safeHref.startsWith('https://')));
            return (
              <a
                href={safeHref}
                target={isExternal ? '_blank' : undefined}
                rel={isExternal ? 'noopener noreferrer' : undefined}
                data-unsafe={isUnsafe ? 'true' : undefined}
                className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 underline underline-offset-4 decoration-blue-500/40 hover:decoration-blue-500 transition-colors"
                {...props}
              >
                {children}
              </a>
            );
          },
          // Distinguish between block pre/code and inline code
          code: ({ node, className, children, ...props }) => {
            const match = /language-(\w+)/.exec(className || '');
            const isBlock = Boolean(match) || (typeof children === 'string' && children.includes('\n'));

            if (isBlock) {
              const lang = match ? match[1] : '';
              return <CodeBlock language={lang} value={String(children)} />;
            }

            return (
              <code
                className="px-1.5 py-0.5 rounded border border-zinc-200 dark:border-white/10 bg-zinc-100 dark:bg-white/5 font-mono text-[0.875em] text-zinc-800 dark:text-zinc-200"
                {...props}
              >
                {children}
              </code>
            );
          },
          pre: ({ children }) => <>{children}</>,
        }}
      >
        {sanitizedContent}
      </ReactMarkdown>
    </div>
  );
};
