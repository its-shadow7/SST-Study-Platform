import React from 'react';
import { Shield, ShieldAlert } from 'lucide-react';
import { UserRole } from '../types/comment';

interface RoleBadgeProps {
  role?: UserRole | string | null;
  className?: string;
  size?: 'sm' | 'md';
}

export const RoleBadge: React.FC<RoleBadgeProps> = ({ role, className = '', size = 'sm' }) => {
  if (!role || role === 'student') {
    return null;
  }

  const isSmall = size === 'sm';
  const iconSize = isSmall ? 11 : 13;

  if (role === 'admin') {
    return (
      <span
        title="Platform Administrator"
        className={`inline-flex items-center gap-1 font-semibold tracking-wide uppercase border rounded-full transition-all duration-200 select-none ${
          isSmall ? 'text-[10px] px-1.5 py-0.2' : 'text-xs px-2.5 py-0.5'
        } text-amber-400 bg-amber-400/10 border-amber-400/20 shadow-[0_0_10px_rgba(251,191,36,0.15)] hover:border-amber-400/40 ${className}`}
      >
        <ShieldAlert size={iconSize} className="text-amber-400" />
        <span>Admin</span>
      </span>
    );
  }

  if (role === 'moderator') {
    return (
      <span
        title="Community Moderator"
        className={`inline-flex items-center gap-1 font-semibold tracking-wide uppercase border rounded-full transition-all duration-200 select-none ${
          isSmall ? 'text-[10px] px-1.5 py-0.2' : 'text-xs px-2.5 py-0.5'
        } text-emerald-400 bg-emerald-400/10 border-emerald-400/20 shadow-[0_0_8px_rgba(52,211,153,0.12)] hover:border-emerald-400/40 ${className}`}
      >
        <Shield size={iconSize} className="text-emerald-400" />
        <span>Moderator</span>
      </span>
    );
  }

  return null;
};
