import React from 'react';
import { ShieldAlert, Shield } from 'lucide-react';
import { UserRole } from '../types/comment';

interface RoleBadgeProps {
  role?: UserRole | 'student' | 'moderator' | 'admin' | string | null;
  className?: string;
  size?: 'sm' | 'md';
}

export const RoleBadge: React.FC<RoleBadgeProps> = ({ role, className = '', size = 'sm' }) => {
  if (!role || role === 'student') {
    return null;
  }

  const isSmall = size === 'sm';
  const iconSize = isSmall ? 11 : 12;

  if (role === 'admin') {
    return (
      <span
        title="Platform Administrator"
        className={`inline-flex items-center gap-1 font-medium tracking-wide text-amber-400 bg-amber-400/10 border border-amber-400/20 text-xs px-2 py-0.5 rounded-md select-none transition-all duration-150 shadow-[0_0_12px_rgba(251,191,36,0.12)] ${className}`}
      >
        <ShieldAlert size={iconSize} className="text-amber-400 shrink-0" />
        <span>Admin</span>
      </span>
    );
  }

  if (role === 'moderator') {
    return (
      <span
        title="Community Moderator"
        className={`inline-flex items-center gap-1 font-medium tracking-wide text-emerald-400 bg-emerald-400/10 border border-emerald-400/20 text-xs px-2 py-0.5 rounded-md select-none transition-all duration-150 shadow-[0_0_12px_rgba(52,211,153,0.12)] ${className}`}
      >
        <Shield size={iconSize} className="text-emerald-400 shrink-0" />
        <span>Mod</span>
      </span>
    );
  }

  return null;
};
