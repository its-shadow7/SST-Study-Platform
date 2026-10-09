import React, { useEffect, useState } from 'react';
import { NoteSection } from '../types/note';

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
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setActiveSectionId(entry.target.id);
            break;
          }
        }
      },
      {
        rootMargin: '-20% 0px -70% 0px'
      }
    );

    sections.forEach((sec) => {
      const el = document.getElementById(sec.section_id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, [sections]);

  const scrollToSection = (sectionId: string) => {
    const el = document.getElementById(sectionId);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setActiveSectionId(sectionId);
    }
  };

  return (
    <aside className="toc-sidebar">
      <div className="toc-title">On this page</div>
      <nav className="toc-nav">
        {sections.map((sec) => {
          const isActive = sec.section_id === activeSectionId;
          return (
            <button
              key={sec.section_id}
              className={`toc-link ${isActive ? 'active' : ''}`}
              onClick={() => scrollToSection(sec.section_id)}
              style={{
                background: 'transparent',
                textAlign: 'left',
                border: 'none',
                width: '100%'
              }}
            >
              {sec.heading}
            </button>
          );
        })}
      </nav>
    </aside>
  );
};
