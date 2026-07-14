import { useAppStore } from '../store';
import { CheckCircle2, AlertTriangle, FileDiff, ArrowRight, Info } from 'lucide-react';

export function ChangesReview() {
  const { tailoringResult, setWorkflowState } = useAppStore();

  if (!tailoringResult) return null;

  const { validated_changes, valid_count, rejected_count, rejection_warnings } = tailoringResult;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <CheckCircle2 className="w-5 h-5 text-[var(--success)]" />
            <h3 className="font-semibold text-[var(--text-secondary)]">Valid Changes</h3>
          </div>
          <p className="text-3xl font-bold text-[var(--text-primary)]">{valid_count}</p>
        </div>
        
        <div className="p-6 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="w-5 h-5 text-[var(--warning)]" />
            <h3 className="font-semibold text-[var(--text-secondary)]">Rejected Changes</h3>
          </div>
          <p className="text-3xl font-bold text-[var(--text-primary)]">{rejected_count}</p>
        </div>
        
        <div className="p-6 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm flex flex-col justify-center">
          <button 
            onClick={() => setWorkflowState('PREVIEW_READY')}
            className="w-full py-3 bg-[var(--accent)] text-white rounded-lg font-medium hover:bg-blue-600 transition-colors flex items-center justify-center gap-2"
          >
            Continue to Preview <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Warnings (if any) */}
      {rejection_warnings?.length > 0 && (
        <div className="p-6 border border-[var(--warning)]/30 rounded-xl bg-[var(--warning)]/5 shadow-sm">
          <h3 className="text-lg font-semibold mb-3 flex items-center gap-2 text-[var(--warning)]">
            <AlertTriangle className="w-5 h-5" /> Validation Warnings
          </h3>
          <p className="text-sm text-[var(--text-secondary)] mb-4">
            The following suggestions were rejected by the strict validation pipeline (e.g. they attempted to fabricate skills or modify unchangeable facts):
          </p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-[var(--text-muted)]">
            {rejection_warnings.map((warn: string, i: number) => (
              <li key={i}>{warn}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Approved Changes */}
      <div className="space-y-4">
        <h3 className="text-xl font-semibold flex items-center gap-2">
          <FileDiff className="w-6 h-6 text-[var(--accent)]" /> 
          Approved Enhancements
        </h3>
        
        {validated_changes?.length === 0 ? (
          <div className="p-8 border border-[var(--border)] rounded-xl bg-[var(--surface)] text-center text-[var(--text-secondary)]">
            No valid changes could be generated. Your resume might already be highly optimized or Gemini struggled to find valid keyword insertions.
          </div>
        ) : (
          validated_changes.map((change: any) => (
            <div key={change.change_id} className="p-6 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                    {change.change_type}
                  </span>
                  <span className="ml-2 text-sm text-[var(--text-secondary)]">
                    Target: {change.section}
                  </span>
                </div>
                <div className="flex items-center gap-1 text-xs text-[var(--text-muted)] bg-[var(--background)] px-2 py-1 rounded border border-[var(--border)]">
                  <Info className="w-3 h-3" /> Confidence: {change.confidence}%
                </div>
              </div>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
                <div className="p-4 bg-[var(--danger)]/5 border border-[var(--danger)]/20 rounded-lg">
                  <h4 className="text-xs font-semibold text-[var(--danger)] mb-2 uppercase tracking-wider">Original</h4>
                  <p className="text-sm font-mono text-[var(--text-secondary)] whitespace-pre-wrap">{change.original_content}</p>
                </div>
                <div className="p-4 bg-[var(--success)]/5 border border-[var(--success)]/20 rounded-lg">
                  <h4 className="text-xs font-semibold text-[var(--success)] mb-2 uppercase tracking-wider">Proposed</h4>
                  <p className="text-sm font-mono text-[var(--text-primary)] whitespace-pre-wrap">{change.proposed_content}</p>
                </div>
              </div>
              
              <div className="mt-4 pt-4 border-t border-[var(--border)] text-sm">
                <p className="text-[var(--text-secondary)] mb-2"><strong>Reason:</strong> {change.reason}</p>
                {change.jd_requirements?.length > 0 && (
                  <p className="text-[var(--text-muted)] text-xs">
                    <strong>Aligns with:</strong> {change.jd_requirements.join(', ')}
                  </p>
                )}
              </div>
            </div>
          ))
        )}
      </div>
      
    </div>
  );
}
