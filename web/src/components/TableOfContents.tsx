import React, { useEffect, useState } from 'react';
import { NoteSection } from '@/types/note';
import { AlignLeft, ChevronDown } from 'lucide-react';

interface TableOfContentsProps {
  sections: NoteSection[];
}

export const TableOfContents: React.FC<TableOfContentsProps> = ({ sections }) => {
  const [activeSectionId, setActiveSectionId] = useState<string>('');

  useEffect(() => {
    if (sections.length > 0 && !activeSectionId) {
      setActiveSectionId(sections[0].section_id);
    }

    const observer = new IntersectionObserver(
      (entries) => {
        // Find the visible section closest to the top of viewport
        const visibleEntries = entries.filter((e) => e.isIntersecting);
        if (visibleEntries.length > 0) {
          // Sort by bounding top
          visibleEntries.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
          setActiveSectionId(visibleEntries[0].target.id);
        }
      },
      {
        rootMargin: '-10% 0px -65% 0px',
        threshold: [0, 0.25, 0.5]
      }
    );

    sections.forEach((sec) => {
      const el = document.getElementById(sec.section_id) || document.getElementById(`section-${sec.section_id}`);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [sections]);

  const scrollToSection = (sectionId: string) => {
    const el = document.getElementById(sectionId) || document.getElementById(`section-${sectionId}`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setActiveSectionId(sectionId);
    }
  };

  if (!sections || sections.length === 0) {
    return null;
  }

  return (
    <aside
      className="w-72 shrink-0 sticky top-14 h-[calc(100vh-3.5rem)] hidden xl:flex flex-col py-8 pl-6 pr-4 overflow-y-auto select-none border-l border-white/[0.08]"
      aria-label="Table of contents"
    >
      <div className="flex items-center gap-2 mb-4 text-[11px] font-semibold tracking-wider uppercase text-zinc-400">
        <AlignLeft className="w-3.5 h-3.5 text-zinc-400" />
        <span>On this page</span>
      </div>

      <nav className="flex flex-col space-y-1 text-sm" aria-label="Page sections">
        {sections.map((sec) => {
          const isActive = sec.section_id === activeSectionId;
          return (
            <button
              key={sec.section_id}
              onClick={() => scrollToSection(sec.section_id)}
              className={`group flex items-start text-left py-1.5 pl-3 -ml-px transition-all duration-150 border-l ${isActive
                  ? 'border-blue-500 text-zinc-100 font-medium'
                  : 'border-transparent text-zinc-400 hover:text-zinc-200 hover:border-white/20'
                }`}
            >
              <span className="line-clamp-2 leading-snug text-[13px]">
                {sec.heading}
              </span>
            </button>
          );
        })}
      </nav>
    </aside>
  );
};

export const MobileTableOfContents: React.FC<TableOfContentsProps> = ({ sections }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [activeSectionId, setActiveSectionId] = useState<string>(sections[0]?.section_id || '');

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        const visibleEntries = entries.filter((e) => e.isIntersecting);
        if (visibleEntries.length > 0) {
          visibleEntries.sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
          setActiveSectionId(visibleEntries[0].target.id);
        }
      },
      { rootMargin: '-10% 0px -65% 0px', threshold: [0, 0.25, 0.5] }
    );

    sections.forEach((sec) => {
      const el = document.getElementById(sec.section_id) || document.getElementById(`section-${sec.section_id}`);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [sections]);

  const scrollToSection = (sectionId: string) => {
    const el = document.getElementById(sectionId) || document.getElementById(`section-${sectionId}`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setActiveSectionId(sectionId);
      setIsOpen(false);
    }
  };

  if (!sections || sections.length === 0) return null;

  const activeSection = sections.find((s) => s.section_id === activeSectionId) || sections[0];

  return (
    <div className="xl:hidden w-full mb-6">
      <div className="border border-white/10 rounded-xl bg-white/[0.02] overflow-hidden transition-all">
        <button
          onClick={() => setIsOpen((prev) => !prev)}
          className="w-full px-4 py-2.5 flex items-center justify-between text-xs text-zinc-300 hover:text-white transition-colors"
          aria-expanded={isOpen}
          aria-label="Toggle mobile table of contents"
        >
          <div className="flex items-center gap-2 truncate pr-2">
            <AlignLeft className="w-3.5 h-3.5 text-blue-400 shrink-0" />
            <span className="font-semibold text-zinc-400 uppercase tracking-wider text-[10px]">On this page:</span>
            <span className="truncate text-zinc-200 font-medium">{activeSection?.heading}</span>
          </div>
          <div className="flex items-center gap-1.5 shrink-0 text-zinc-400">
            <span className="text-[10px] font-mono bg-white/5 px-1.5 py-0.5 rounded">{sections.length}</span>
            <ChevronDown className={`w-3.5 h-3.5 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
          </div>
        </button>

        {isOpen && (
          <div className="px-3 pb-3 pt-1 border-t border-white/[0.06] space-y-1" role="region" aria-label="Mobile table of contents">
            {sections.map((sec, idx) => {
              const isActive = sec.section_id === activeSectionId;
              return (
                <button
                  key={sec.section_id}
                  onClick={() => scrollToSection(sec.section_id)}
                  className={`w-full text-left px-3 py-1.5 rounded-lg text-xs flex items-center gap-2 transition-colors ${isActive
                      ? 'bg-blue-500/15 text-blue-300 font-medium'
                      : 'text-zinc-400 hover:text-zinc-200 hover:bg-white/[0.04]'
                    }`}
                >
                  <span className="text-[10px] font-mono text-zinc-400 shrink-0">{String(idx + 1).padStart(2, '0')}</span>
                  <span className="truncate">{sec.heading}</span>
                </button>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

