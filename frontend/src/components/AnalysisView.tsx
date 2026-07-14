import { useState } from 'react';
import { useAppStore } from '../store';
import { generateChanges } from '../api';
import { Target, Loader2, Wand2, AlertTriangle, CheckCircle2 } from 'lucide-react';

export function AnalysisView() {
  const { jdAnalysis, matchAnalysis, sessionId, geminiKey, setWorkflowState, setTailoringResult } = useAppStore();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  if (!jdAnalysis || !matchAnalysis) return null;

  const handleGenerate = async () => {
    if (!sessionId || !geminiKey) return;
    
    setLoading(true);
    setError(null);
    setWorkflowState('GENERATING_CHANGES');
    
    try {
      const result = await generateChanges(sessionId, geminiKey);
      setTailoringResult(result);
      setWorkflowState('REVIEWING_CHANGES');
    } catch (err: any) {
      setError(err.message || 'Failed to generate resume changes');
      setWorkflowState('ANALYSIS_READY');
    } finally {
      setLoading(false);
    }
  };

  const scoreColor = matchAnalysis.total_score >= 80 ? 'text-[var(--success)]' 
                   : matchAnalysis.total_score >= 50 ? 'text-[var(--warning)]' 
                   : 'text-[var(--danger)]';

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Score Card */}
        <div className="p-6 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm flex flex-col items-center justify-center text-center">
          <Target className="w-8 h-8 text-[var(--accent)] mb-2" />
          <h3 className="text-sm font-medium text-[var(--text-secondary)]">Initial Match Score</h3>
          <div className={`text-5xl font-bold mt-2 ${scoreColor}`}>
            {matchAnalysis.total_score}%
          </div>
          <p className="text-xs text-[var(--text-muted)] mt-2">Deterministic score based on keywords</p>
        </div>

        {/* Breakdown Card */}
        <div className="md:col-span-2 p-6 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm">
          <h3 className="text-lg font-semibold mb-4 border-b border-[var(--border)] pb-2">Score Breakdown</h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex justify-between">
              <span className="text-[var(--text-secondary)]">Required Skills:</span>
              <span className="font-medium">{matchAnalysis.required_skills_score} / 35</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[var(--text-secondary)]">Preferred Skills:</span>
              <span className="font-medium">{matchAnalysis.preferred_skills_score} / 10</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[var(--text-secondary)]">Keywords:</span>
              <span className="font-medium">{matchAnalysis.keyword_score} / 20</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[var(--text-secondary)]">Experience:</span>
              <span className="font-medium">{matchAnalysis.experience_score} / 15</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[var(--text-secondary)]">Education:</span>
              <span className="font-medium">{matchAnalysis.education_score} / 10</span>
            </div>
            <div className="flex justify-between">
              <span className="text-[var(--text-secondary)]">Projects:</span>
              <span className="font-medium">{matchAnalysis.project_score} / 10</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Missing Requirements */}
        <div className="p-6 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-[var(--warning)]" /> Missing Requirements
          </h3>
          <div className="flex flex-wrap gap-2">
            {matchAnalysis.missing_requirements?.length > 0 ? (
              matchAnalysis.missing_requirements.map((req: string, i: number) => (
                <span key={i} className="px-2.5 py-1 bg-[var(--warning)]/10 text-[var(--warning)] text-xs rounded-full border border-[var(--warning)]/20">
                  {req}
                </span>
              ))
            ) : (
              <span className="text-sm text-[var(--text-muted)]">No missing requirements identified.</span>
            )}
          </div>
        </div>

        {/* Matched Requirements */}
        <div className="p-6 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-[var(--success)]" /> Matched Requirements
          </h3>
          <div className="flex flex-wrap gap-2">
            {matchAnalysis.matched_requirements?.length > 0 ? (
              matchAnalysis.matched_requirements.map((req: string, i: number) => (
                <span key={i} className="px-2.5 py-1 bg-[var(--success)]/10 text-[var(--success)] text-xs rounded-full border border-[var(--success)]/20">
                  {req}
                </span>
              ))
            ) : (
              <span className="text-sm text-[var(--text-muted)]">No matched requirements yet.</span>
            )}
          </div>
        </div>
      </div>

      {error && (
        <div className="p-4 text-sm text-[var(--danger)] bg-[var(--danger)]/10 rounded-lg border border-[var(--danger)]/20">
          {error}
        </div>
      )}

      <div className="flex justify-center pt-4">
        <button
          onClick={handleGenerate}
          disabled={loading}
          className="px-8 py-3 bg-[var(--accent)] text-white rounded-lg font-medium hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors shadow-lg shadow-blue-500/20"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" /> Generating Tailored Changes...
            </>
          ) : (
            <>
              <Wand2 className="w-5 h-5" /> Generate Resume Enhancements
            </>
          )}
        </button>
      </div>
    </div>
  );
}
