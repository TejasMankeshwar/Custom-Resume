import { useQuery } from '@tanstack/react-query';
import { checkHealth } from './api';
import { useAppStore } from './store';
import { FileText, CheckCircle2, XCircle } from 'lucide-react';
import { SessionSetup } from './components/SessionSetup';
import { JobInput } from './components/JobInput';
import { AnalysisView } from './components/AnalysisView';
import { ChangesReview } from './components/ChangesReview';

function App() {
  const { workflowState } = useAppStore();
  const { data: health, isError } = useQuery({ queryKey: ['health'], queryFn: checkHealth });

  return (
    <div className="min-h-screen bg-[var(--background)] text-[var(--text-primary)]">
      <header className="border-b border-[var(--border)] bg-[var(--surface)] px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-[var(--accent)]" />
          <h1 className="font-semibold text-lg">Resume Tailor</h1>
        </div>
        <div className="flex items-center gap-2 text-sm text-[var(--text-secondary)]">
          {isError ? (
            <span className="flex items-center gap-1 text-[var(--danger)]">
              <XCircle className="w-4 h-4" /> Backend Offline
            </span>
          ) : health ? (
            <span className="flex items-center gap-1 text-[var(--success)]">
              <CheckCircle2 className="w-4 h-4" /> Backend Connected
            </span>
          ) : (
            <span>Connecting...</span>
          )}
        </div>
      </header>
      
      <div className="max-w-[1400px] mx-auto px-6 py-8">
        {/* Simple Workflow Progress Indicator */}
        <div className="flex items-center justify-center gap-4 mb-12 text-sm overflow-x-auto whitespace-nowrap">
          <div className={`flex items-center gap-2 ${workflowState === 'SESSION_SETUP' ? 'text-[var(--accent)] font-medium' : 'text-[var(--text-muted)]'}`}>
            <span>1. Setup</span>
          </div>
          <div className="w-8 h-px bg-[var(--border-strong)]" />
          <div className={`flex items-center gap-2 ${workflowState === 'JOB_INPUT' ? 'text-[var(--accent)] font-medium' : 'text-[var(--text-muted)]'}`}>
            <span>2. Job Input</span>
          </div>
          <div className="w-8 h-px bg-[var(--border-strong)]" />
          <div className={`flex items-center gap-2 ${['ANALYSIS_READY', 'ANALYZING', 'GENERATING_CHANGES'].includes(workflowState) ? 'text-[var(--accent)] font-medium' : 'text-[var(--text-muted)]'}`}>
            <span>3. Analysis</span>
          </div>
          <div className="w-8 h-px bg-[var(--border-strong)]" />
          <div className={`flex items-center gap-2 ${workflowState === 'REVIEWING_CHANGES' ? 'text-[var(--accent)] font-medium' : 'text-[var(--text-muted)]'}`}>
            <span>4. Review Changes</span>
          </div>
          <div className="w-8 h-px bg-[var(--border-strong)]" />
          <div className={`flex items-center gap-2 ${workflowState === 'PREVIEW_READY' ? 'text-[var(--accent)] font-medium' : 'text-[var(--text-muted)]'}`}>
            <span>5. Preview</span>
          </div>
        </div>

        <main>
          {workflowState === 'SESSION_SETUP' && <SessionSetup />}
          {(workflowState === 'JOB_INPUT' || workflowState === 'ANALYZING') && <JobInput />}
          {(workflowState === 'ANALYSIS_READY' || workflowState === 'GENERATING_CHANGES') && <AnalysisView />}
          {workflowState === 'REVIEWING_CHANGES' && <ChangesReview />}
          {workflowState === 'PREVIEW_READY' && (
             <div className="p-8 border border-[var(--border)] rounded-lg bg-[var(--surface)] text-center">
               <h2 className="text-xl font-semibold mb-2">Phase 2 Complete</h2>
               <p className="text-[var(--text-secondary)]">The AI workflow and validation logic are fully implemented.</p>
               <p className="text-[var(--text-muted)] text-sm mt-4">Phase 3 will cover the actual LaTeX compilation and generation.</p>
             </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
