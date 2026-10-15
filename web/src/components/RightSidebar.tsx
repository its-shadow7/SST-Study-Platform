import React, { useState, useEffect } from 'react';
import { NoteSection } from '@/types/note';
import { Scratchpad } from '@/components/Scratchpad';
import { api } from '@/services/apiClient';
import { useAuth } from '@/context/AuthContext';
import { ScratchpadData } from '@/types/scratchpad';
import {
  AlignLeft,
  PenLine,
  Maximize2,
  Minimize2
} from 'lucide-react';

interface RightSidebarProps {
  noteId: string;
  sections: NoteSection[];
}

export const RightSidebar: React.FC<RightSidebarProps> = ({ noteId, sections }) => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState<'toc' | 'notes'>('toc');
  const [isExpanded, setIsExpanded] = useState<boolean>(false);
  const [hasPersonalNotes, setHasPersonalNotes] = useState<boolean>(false);
  const [activeSectionId, setActiveSectionId] = useState<string>('');

  // Check if current lecture note has saved scratchpad content to display indicator dot
  useEffect(() => {
    if (!user) {
      setHasPersonalNotes(false);
      return;
    }

    let isSubscribed = true;
    api.get<ScratchpadData>(`/api/notes/${noteId}/scratchpad`)
      .then((data) => {
        if (isSubscribed) {
          setHasPersonalNotes((data?.content || '').trim().length > 0);
        }
      })
      .catch(() => {
        if (isSubscribed) {
          setHasPersonalNotes(false);
        }
      });

    return () => {
      isSubscribed = false;
    };
  }, [noteId, user]);

  // Intersection observer for Table of Contents
  useEffect(() => {
    if (sections.length > 0 && !activeSectionId) {
      setActiveSectionId(sections[0].section_id);
    }

    const observer = new IntersectionObserver(
      (entries) => {
        const visibleEntries = entries.filter((e) => e.isIntersecting);
        if (visibleEntries.length > 0) {
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
  }, [sections, activeSectionId]);

  const scrollToSection = (sectionId: string) => {
    const el = document.getElementById(sectionId) || document.getElementById(`section-${sectionId}`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setActiveSectionId(sectionId);
    }
  };

  return (
    <aside
      className={`shrink-0 sticky top-14 h-[calc(100vh-3.5rem)] hidden xl:flex flex-col select-none transition-all duration-200 ${isExpanded && activeTab === 'notes'
          ? 'w-[480px] z-30 bg-[#09090b] border-l border-white/10 shadow-2xl'
          : 'w-72 border-l border-white/[0.08] bg-[#09090b]/80 backdrop-blur-sm'
        }`}
      aria-label="Sidebar utility island"
    >
      {/* 1. Header: Segmented Control [ On This Page | My Notes ] & Expand Button */}
      <div className="flex items-center justify-between px-3.5 py-3 border-b border-white/[0.08] bg-black/20 shrink-0">
        <div className="flex items-center p-0.5 rounded-lg bg-white/[0.04] border border-white/10 text-xs">
          <button
            onClick={() => setActiveTab('toc')}
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-all ${activeTab === 'toc'
                ? 'bg-white/10 text-zinc-100 shadow-sm font-medium'
                : 'text-zinc-400 hover:text-zinc-200'
              }`}
          >
            <AlignLeft className="w-3.5 h-3.5" />
            <span>On This Page</span>
          </button>

          <button
            onClick={() => setActiveTab('notes')}
            className={`relative flex items-center gap-1.5 px-2.5 py-1 rounded-md transition-all ${activeTab === 'notes'
                ? 'bg-white/10 text-zinc-100 shadow-sm font-medium'
                : 'text-zinc-400 hover:text-zinc-200'
              }`}
          >
            <PenLine className="w-3.5 h-3.5" />
            <span>My Notes</span>
            {hasPersonalNotes && (
              <span className="w-1.5 h-1.5 rounded-full bg-blue-500 ring-2 ring-[#09090b]" />
            )}
          </button>
        </div>

        {/* Expand / Minimize Drawer Toggle Button (active in My Notes tab) */}
        {activeTab === 'notes' && (
          <button
            onClick={() => setIsExpanded((prev) => !prev)}
            title={isExpanded ? 'Collapse to standard width' : 'Expand to reading drawer'}
            aria-label={isExpanded ? 'Collapse notes' : 'Expand notes'}
            className="p-1.5 rounded-md hover:bg-white/5 border border-transparent hover:border-white/10 text-zinc-400 hover:text-zinc-200 transition-colors"
          >
            {isExpanded ? (
              <Minimize2 className="w-3.5 h-3.5" />
            ) : (
              <Maximize2 className="w-3.5 h-3.5" />
            )}
          </button>
        )}
      </div>

      {/* 2. Main Content Body: Table of Contents or Scratchpad */}
      {activeTab === 'toc' ? (
        <div className="flex-1 py-4 pl-5 pr-3 overflow-y-auto">
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
        </div>
      ) : (
        <div className="flex-1 overflow-hidden">
          <Scratchpad
            noteId={noteId}
            onHasNotesChange={(has) => setHasPersonalNotes(has)}
          />
        </div>
      )}
    </aside>
  );
};
