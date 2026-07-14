import { useState } from 'react';
import { useAppStore } from '../store';
import { analyzeJob } from '../api';
import { Briefcase, Loader2, Sparkles } from 'lucide-react';

export function JobInput() {
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { sessionId, geminiKey, setJdAnalysis, setMatchAnalysis, setWorkflowState } = useAppStore();

  const handleAnalyze = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!jobDescription.trim() || !sessionId || !geminiKey) return;
    
    setLoading(true);
    setError(null);
    setWorkflowState('ANALYZING');
    
    try {
      const result = await analyzeJob(sessionId, geminiKey, jobDescription.trim(), jobTitle.trim());
      
      setJdAnalysis(result.jd_analysis);
      setMatchAnalysis(result.match_analysis);
      setWorkflowState('ANALYSIS_READY');
      
    } catch (err: any) {
      setError(err.message || 'Failed to analyze job description');
      setWorkflowState('JOB_INPUT'); // Revert state
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto p-8 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm">
      <div className="flex items-center gap-3 mb-6 pb-6 border-b border-[var(--border)]">
        <div className="p-3 bg-[var(--background)] rounded-full border border-[var(--border)]">
          <Briefcase className="w-6 h-6 text-[var(--accent)]" />
        </div>
        <div>
          <h2 className="text-xl font-semibold">Job Description</h2>
          <p className="text-[var(--text-secondary)] text-sm">Provide the job details you want to tailor your resume for.</p>
        </div>
      </div>

      <form onSubmit={handleAnalyze} className="space-y-6">
        <div>
          <label className="block text-sm font-medium mb-1">
            Target Job Title <span className="text-[var(--text-muted)] font-normal">(Optional)</span>
          </label>
          <input
            type="text"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            placeholder="e.g. Senior Software Engineer"
            className="w-full px-4 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg focus:outline-none focus:border-[var(--accent)]"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">
            Job Description <span className="text-[var(--danger)]">*</span>
          </label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the full job description here..."
            className="w-full h-64 px-4 py-3 bg-[var(--background)] border border-[var(--border)] rounded-lg focus:outline-none focus:border-[var(--accent)] resize-y"
            required
          />
        </div>

        {error && (
          <div className="p-3 text-sm text-[var(--danger)] bg-[var(--danger)]/10 rounded-lg border border-[var(--danger)]/20">
            {error}
          </div>
        )}

        <div className="flex justify-end pt-4">
          <button
            type="submit"
            disabled={loading || !jobDescription.trim()}
            className="px-6 py-2.5 bg-[var(--accent)] text-white rounded-lg font-medium hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" /> Analyzing with Gemini...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" /> Analyze Requirements
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
