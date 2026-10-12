import React from 'react';

export const NoteSkeleton: React.FC = () => {
  return (
    <div className="w-full max-w-reader mx-auto animate-pulse space-y-8 py-4">
      {/* Badges Shimmer */}
      <div className="flex items-center gap-2.5">
        <div className="h-5 w-16 bg-white/10 rounded-full" />
        <div className="h-5 w-20 bg-white/10 rounded-full" />
        <div className="h-5 w-28 bg-white/10 rounded-full" />
      </div>

      {/* Main Title Shimmer */}
      <div className="space-y-3">
        <div className="h-9 w-4/5 bg-white/10 rounded-md" />
        <div className="h-9 w-2/3 bg-white/10 rounded-md" />
      </div>

      {/* Summary Box Shimmer */}
      <div className="p-4 rounded-lg border border-white/5 bg-white/[0.02] space-y-2.5">
        <div className="h-4 w-full bg-white/10 rounded" />
        <div className="h-4 w-11/12 bg-white/10 rounded" />
        <div className="h-4 w-3/4 bg-white/10 rounded" />
      </div>

      {/* Action Buttons Shimmer */}
      <div className="flex items-center gap-3 pt-2 border-b border-white/10 pb-6">
        <div className="h-8 w-28 bg-white/10 rounded-md" />
        <div className="h-8 w-24 bg-white/10 rounded-md" />
      </div>

      {/* Body Section 1 */}
      <div className="space-y-4 pt-2">
        <div className="h-7 w-1/2 bg-white/10 rounded-md" />
        <div className="h-4 w-full bg-white/5 rounded" />
        <div className="h-4 w-full bg-white/5 rounded" />
        <div className="h-4 w-5/6 bg-white/5 rounded" />
        <div className="h-4 w-4/5 bg-white/5 rounded" />
      </div>

      {/* Code Block Shimmer */}
      <div className="h-48 w-full bg-white/[0.04] border border-white/10 rounded-lg" />

      {/* Body Section 2 */}
      <div className="space-y-4">
        <div className="h-7 w-2/5 bg-white/10 rounded-md" />
        <div className="h-4 w-full bg-white/5 rounded" />
        <div className="h-4 w-11/12 bg-white/5 rounded" />
        <div className="h-4 w-3/4 bg-white/5 rounded" />
      </div>
    </div>
  );
};
