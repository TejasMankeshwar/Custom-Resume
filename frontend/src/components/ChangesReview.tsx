import { useState } from 'react';
import { useAppStore } from '../store';
import { AlertTriangle, FileDiff, ArrowRight, Check, X, Loader2 } from 'lucide-react';
import { generateResume, compileResume } from '../api';

export function ChangesReview() {
  const { tailoringResult, decisions, setDecision, setDecisions, setWorkflowState, sessionId, setFinalMatchAnalysis } = useAppStore();
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!tailoringResult) return null;

  const { validated_changes, rejected_count, rejection_warnings } = tailoringResult;

  const handleAcceptAll = () => {
    const newDecisions: Record<string, string> = {};
    validated_changes.forEach((c: any) => {
      newDecisions[c.change_id] = 'ACCEPTED';
    });
    setDecisions(newDecisions);
  };

  const handleRejectAll = () => {
    const newDecisions: Record<string, string> = {};
    validated_changes.forEach((c: any) => {
      newDecisions[c.change_id] = 'REJECTED';
    });
    setDecisions(newDecisions);
  };

  const handleReset = () => {
    const newDecisions: Record<string, string> = {};
    validated_changes.forEach((c: any) => {
      newDecisions[c.change_id] = 'PENDING';
    });
    setDecisions(newDecisions);
  };

  const handleGenerate = async () => {
    if (!sessionId) return;
    
    // Ensure all decisions are made
    const pendingCount = Object.values(decisions).filter(d => d === 'PENDING').length;
    if (pendingCount > 0) {
      setError(`Please accept or reject the remaining ${pendingCount} changes before generating.`);
      return;
    }

    try {
      setIsGenerating(true);
      setError(null);
      
      const genResult = await generateResume(sessionId, decisions);
      setFinalMatchAnalysis({ score: genResult.new_score });
      
      await compileResume(sessionId);
      
      setWorkflowState('PREVIEW_READY');
    } catch (err: any) {
      setError(err.message || "An error occurred during generation and compilation.");
    } finally {
      setIsGenerating(false);
    }
  };

  const pendingCount = Object.values(decisions).filter(d => d === 'PENDING').length;
  const acceptedCount = Object.values(decisions).filter(d => d === 'ACCEPTED').length;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Action Bar */}
      <div className="sticky top-4 z-10 p-4 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-md flex flex-col md:flex-row justify-between items-center gap-4">
        <div className="flex gap-2">
          <button onClick={handleAcceptAll} className="px-3 py-1.5 text-sm bg-[var(--success)]/10 text-[var(--success)] hover:bg-[var(--success)]/20 rounded-md font-medium transition-colors border border-[var(--success)]/20">
            Accept All
          </button>
          <button onClick={handleRejectAll} className="px-3 py-1.5 text-sm bg-[var(--danger)]/10 text-[var(--danger)] hover:bg-[var(--danger)]/20 rounded-md font-medium transition-colors border border-[var(--danger)]/20">
            Reject All
          </button>
          <button onClick={handleReset} className="px-3 py-1.5 text-sm bg-[var(--background)] text-[var(--text-secondary)] hover:bg-[var(--border)] rounded-md font-medium transition-colors border border-[var(--border)]">
            Reset
          </button>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="text-sm font-medium">
            <span className={pendingCount > 0 ? "text-[var(--warning)]" : "text-[var(--success)]"}>
              {pendingCount} Pending
            </span>
            <span className="text-[var(--text-muted)] mx-2">|</span>
            <span className="text-[var(--success)]">{acceptedCount} Accepted</span>
          </div>
          
          <button 
            onClick={handleGenerate}
            disabled={pendingCount > 0 || isGenerating}
            className="px-6 py-2 bg-[var(--accent)] text-white rounded-lg font-medium hover:bg-blue-600 transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isGenerating ? (
              <><Loader2 className="w-4 h-4 animate-spin" /> Compiling...</>
            ) : (
              <>Generate Resume <ArrowRight className="w-4 h-4" /></>
            )}
          </button>
        </div>
      </div>

      {error && (
        <div className="p-4 border border-[var(--danger)] rounded-lg bg-[var(--danger)]/10 text-[var(--danger)] text-sm flex items-center gap-2">
          <AlertTriangle className="w-4 h-4" />
          {error}
        </div>
      )}

      {/* Warnings (if any) */}
      {rejection_warnings?.length > 0 && (
        <div className="p-6 border border-[var(--warning)]/30 rounded-xl bg-[var(--warning)]/5 shadow-sm">
          <h3 className="text-lg font-semibold mb-3 flex items-center gap-2 text-[var(--warning)]">
            <AlertTriangle className="w-5 h-5" /> Auto-Rejected Changes ({rejected_count})
          </h3>
          <p className="text-sm text-[var(--text-secondary)] mb-4">
            The AI suggested changes that violated your constraints (e.g. fabricating skills). They have been automatically removed.
          </p>
          <ul className="list-disc pl-5 space-y-1 text-sm text-[var(--text-muted)]">
            {rejection_warnings.map((warn: string, i: number) => (
              <li key={i}>{warn}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Changes List */}
      <div className="space-y-4">
        <h3 className="text-xl font-semibold flex items-center gap-2">
          <FileDiff className="w-6 h-6 text-[var(--accent)]" /> 
          Review Proposed Changes
        </h3>
        
        {validated_changes?.length === 0 ? (
          <div className="p-8 border border-[var(--border)] rounded-xl bg-[var(--surface)] text-center text-[var(--text-secondary)]">
            No valid changes could be generated. Your resume might already be highly optimized or Gemini struggled to find valid keyword insertions.
          </div>
        ) : (
          validated_changes.map((change: any) => {
            const decision = decisions[change.change_id] || 'PENDING';
            let cardClasses = "p-6 border rounded-xl shadow-sm transition-colors ";
            if (decision === 'ACCEPTED') cardClasses += "bg-[var(--success)]/5 border-[var(--success)]/30";
            else if (decision === 'REJECTED') cardClasses += "bg-[var(--danger)]/5 border-[var(--danger)]/30 opacity-75";
            else cardClasses += "bg-[var(--surface)] border-[var(--border)]";

            return (
              <div key={change.change_id} className={cardClasses}>
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300">
                      {change.change_type}
                    </span>
                    <span className="ml-2 text-sm font-medium text-[var(--text-primary)]">
                      Target: {change.section}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setDecision(change.change_id, 'ACCEPTED')}
                      className={`p-2 rounded-lg transition-colors border ${decision === 'ACCEPTED' ? 'bg-[var(--success)] text-white border-[var(--success)]' : 'bg-[var(--background)] text-[var(--text-secondary)] hover:bg-[var(--success)]/10 hover:text-[var(--success)] border-[var(--border)]'}`}
                      title="Accept Change"
                    >
                      <Check className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => setDecision(change.change_id, 'REJECTED')}
                      className={`p-2 rounded-lg transition-colors border ${decision === 'REJECTED' ? 'bg-[var(--danger)] text-white border-[var(--danger)]' : 'bg-[var(--background)] text-[var(--text-secondary)] hover:bg-[var(--danger)]/10 hover:text-[var(--danger)] border-[var(--border)]'}`}
                      title="Reject Change"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4">
                  <div className="p-4 bg-[var(--danger)]/10 border border-[var(--danger)]/20 rounded-lg">
                    <h4 className="text-xs font-semibold text-[var(--danger)] mb-2 uppercase tracking-wider flex justify-between">
                      Original <span className="opacity-75 line-through">Remove</span>
                    </h4>
                    <p className="text-sm font-mono text-red-200/80 dark:text-red-200/80 whitespace-pre-wrap">{change.original_content}</p>
                  </div>
                  <div className="p-4 bg-[var(--success)]/10 border border-[var(--success)]/20 rounded-lg">
                    <h4 className="text-xs font-semibold text-[var(--success)] mb-2 uppercase tracking-wider flex justify-between">
                      Proposed <span>Add</span>
                    </h4>
                    <p className="text-sm font-mono text-green-100 dark:text-green-100 whitespace-pre-wrap">{change.proposed_content}</p>
                  </div>
                </div>
                
                <div className="mt-4 pt-4 border-t border-[var(--border)]/50 text-sm">
                  <p className="text-[var(--text-secondary)] mb-2"><strong>Reason:</strong> {change.reason}</p>
                  {change.jd_requirements?.length > 0 && (
                    <p className="text-[var(--text-muted)] text-xs">
                      <strong>Aligns with:</strong> {change.jd_requirements.join(', ')}
                    </p>
                  )}
                  {change.keywords?.length > 0 && (
                    <p className="text-[var(--text-muted)] text-xs mt-1">
                      <strong>Keywords:</strong> {change.keywords.join(', ')}
                    </p>
                  )}
                </div>
              </div>
            );
          })
        )}
      </div>
      
    </div>
  );
}
