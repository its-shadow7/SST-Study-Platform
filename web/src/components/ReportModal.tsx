import React, { useState, useEffect } from 'react';
import { AlertTriangle, X, Loader2, CheckCircle2 } from 'lucide-react';
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
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={(e) => {
        if (e.target === e.currentTarget && !submitting) {
          onClose();
        }
      }}
    >
      <div className="relative w-full max-w-md overflow-hidden rounded-2xl border border-slate-700/60 bg-slate-900 shadow-2xl shadow-black/60 text-slate-100 p-6 animate-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="flex items-start justify-between gap-3 mb-4">
          <div className="flex items-center gap-2.5">
            <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400">
              <AlertTriangle size={18} />
            </div>
            <div>
              <h3 id="report-modal-title" className="text-lg font-semibold text-slate-100">
                Report Comment
              </h3>
              <p className="text-xs text-slate-400">
                Help maintain community guidelines on SST Study Platform.
              </p>
            </div>
          </div>
          <button
            type="button"
            onClick={onClose}
            disabled={submitting}
            aria-label="Close report modal"
            className="text-slate-400 hover:text-slate-200 p-1.5 rounded-lg hover:bg-slate-800/60 transition-colors disabled:opacity-50"
          >
            <X size={18} />
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="report-reason"
              className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-2"
            >
              Reason for reporting
            </label>
            <div className="relative">
              <select
                id="report-reason"
                value={selectedReason}
                onChange={(e) => setSelectedReason(e.target.value as ReportReason)}
                disabled={submitting}
                className="w-full appearance-none rounded-xl border border-slate-700 bg-slate-800/80 px-3.5 py-2.5 text-sm text-slate-100 shadow-inner focus:border-amber-400 focus:outline-none focus:ring-1 focus:ring-amber-400 transition-colors disabled:opacity-60 cursor-pointer"
              >
                {REPORT_REASONS.map((reason) => (
                  <option key={reason} value={reason} className="bg-slate-900 text-slate-100 py-1">
                    {reason}
                  </option>
                ))}
              </select>
              <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-slate-400">
                <svg className="w-4 h-4 fill-current" viewBox="0 0 20 20">
                  <path d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" />
                </svg>
              </div>
            </div>
          </div>

          {selectedReason === 'Other' && (
            <div className="space-y-1.5 animate-in fade-in duration-150">
              <label
                htmlFor="report-details"
                className="block text-xs font-medium text-slate-300"
              >
                Additional Details (optional)
              </label>
              <textarea
                id="report-details"
                rows={3}
                maxLength={300}
                value={details}
                onChange={(e) => setDetails(e.target.value)}
                placeholder="Briefly describe the issue..."
                disabled={submitting}
                className="w-full rounded-xl border border-slate-700 bg-slate-800/80 px-3 py-2 text-sm text-slate-100 placeholder-slate-500 shadow-inner focus:border-amber-400 focus:outline-none focus:ring-1 focus:ring-amber-400 resize-none transition-colors disabled:opacity-60"
              />
              <div className="text-right text-[11px] text-slate-500">
                {details.length}/300
              </div>
            </div>
          )}

          <div className="rounded-xl border border-slate-800 bg-slate-800/40 p-3 text-xs text-slate-400 flex items-start gap-2">
            <CheckCircle2 size={15} className="text-emerald-400 mt-0.5 shrink-0" />
            <span>
              Reported comments remain visible pending moderator review to prevent abuse.
            </span>
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-end gap-2.5 pt-2">
            <button
              type="button"
              onClick={onClose}
              disabled={submitting}
              className="px-4 py-2 text-sm font-medium text-slate-300 hover:text-slate-100 rounded-xl hover:bg-slate-800 transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="inline-flex items-center gap-1.5 px-4 py-2 text-sm font-semibold text-white bg-amber-600 hover:bg-amber-500 active:bg-amber-700 rounded-xl shadow-md shadow-amber-600/20 transition-all duration-200 disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {submitting ? (
                <>
                  <Loader2 size={16} className="animate-spin" />
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
