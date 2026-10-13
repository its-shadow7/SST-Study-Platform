import React, { useState, useEffect } from 'react';
import { Flag, X, Loader2, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import { api, ApiError } from '../services/apiClient';

interface ReportModalProps {
  isOpen: boolean;
  commentId: string;
  onClose: () => void;
  onReportSubmitted?: (commentId: string) => void;
}

const REPORT_REASONS = [
  'Spam',
  'Harassment / Toxicity',
  'Off-topic',
  'Other',
] as const;

type ReportReason = (typeof REPORT_REASONS)[number];

export const ReportModal: React.FC<ReportModalProps> = ({
  isOpen,
  commentId,
  onClose,
  onReportSubmitted,
}) => {
  const [selectedReason, setSelectedReason] = useState<ReportReason>('Spam');
  const [details, setDetails] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setSelectedReason('Spam');
      setDetails('');
      setSubmitting(false);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen && !submitting) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, submitting, onClose]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!commentId || submitting) return;

    setSubmitting(true);
    const combinedReason =
      selectedReason === 'Other' && details.trim()
        ? `Other: ${details.trim()}`
        : selectedReason;

    try {
      await api.post(`/api/comments/${commentId}/report`, {
        reason: combinedReason,
      });

      toast.success('Report submitted. Thank you for keeping SST Study Platform safe!');
      onReportSubmitted?.(commentId);
      onClose();
    } catch (err: any) {
      const apiErr = err as ApiError;
      toast.error(apiErr.message || 'Failed to submit report. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="report-modal-title"
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm animate-in fade-in duration-150 select-none"
      onClick={(e) => {
        if (e.target === e.currentTarget && !submitting) {
          onClose();
        }
      }}
    >
      <div className="relative w-full max-w-md overflow-hidden rounded-xl border border-white/10 bg-[#09090b] shadow-2xl text-zinc-200 p-6 animate-in zoom-in-95 duration-150">
        {/* Header */}
        <div className="flex items-start justify-between gap-3 mb-5">
          <div className="flex items-center gap-2.5">
            <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400">
              <Flag size={15} />
            </div>
            <div>
              <h3 id="report-modal-title" className="text-sm font-semibold text-zinc-100">
                Report Comment
              </h3>
              <p className="text-xs text-zinc-400">
                Flag comment for review on SST Study Platform
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            disabled={submitting}
            aria-label="Close report modal"
            className="text-zinc-400 hover:text-zinc-200 p-1 rounded-md hover:bg-white/5 transition-colors disabled:opacity-50"
          >
            <X size={16} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="report-reason"
              className="block text-xs font-medium text-zinc-400 mb-1.5"
            >
              Reason for reporting
            </label>
            <div className="relative">
              <select
                id="report-reason"
                value={selectedReason}
                onChange={(e) => setSelectedReason(e.target.value as ReportReason)}
                disabled={submitting}
                className="w-full appearance-none rounded-lg border border-white/10 bg-transparent px-3 py-2 text-xs text-zinc-200 focus:ring-1 focus:ring-zinc-700 focus:outline-none transition-colors disabled:opacity-60 cursor-pointer"
              >
                {REPORT_REASONS.map((reason) => (
                  <option key={reason} value={reason} className="bg-[#09090b] text-zinc-200 py-1">
                    {reason}
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-zinc-500">
                <svg className="w-3.5 h-3.5 fill-current" viewBox="0 0 20 20">
                  <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                </svg>
              </div>
            </div>
          </div>

          {selectedReason === 'Other' && (
            <div className="space-y-1.5 animate-in fade-in duration-100">
              <label
                htmlFor="report-details"
                className="block text-xs font-medium text-zinc-400"
              >
                Additional Details (optional)
              </label>
              <textarea
                id="report-details"
                rows={3}
                maxLength={300}
                value={details}
                onChange={(e) => setDetails(e.target.value)}
                placeholder="Briefly describe the reason for this report..."
                disabled={submitting}
                className="w-full rounded-lg border border-white/10 bg-transparent px-3 py-2 text-xs text-zinc-200 placeholder-zinc-600 focus:ring-1 focus:ring-zinc-700 focus:outline-none resize-none transition-colors disabled:opacity-60"
              />
              <div className="text-right text-[10px] text-zinc-500 font-mono">
                {details.length}/300
              </div>
            </div>
          )}

          <div className="rounded-lg border border-white/[0.06] bg-white/[0.02] p-2.5 text-xs text-zinc-400 flex items-start gap-2">
            <AlertCircle size={14} className="text-zinc-400 mt-0.5 shrink-0" />
            <span className="text-[11px] leading-relaxed">
              Reports are queued for student moderation review. False or spam reports violate guidelines.
            </span>
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-end gap-2 pt-2 border-t border-white/[0.06]">
            <button
              type="button"
              onClick={onClose}
              disabled={submitting}
              className="px-3.5 py-1.5 text-xs font-medium text-zinc-400 hover:text-zinc-200 hover:bg-white/5 rounded-lg transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="inline-flex items-center gap-1.5 px-3.5 py-1.5 text-xs font-medium bg-red-500/10 text-red-500 border border-red-500/20 hover:bg-red-500/20 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {submitting ? (
                <>
                  <Loader2 size={13} className="animate-spin" />
                  <span>Submitting...</span>
                </>
              ) : (
                <span>Submit Report</span>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
