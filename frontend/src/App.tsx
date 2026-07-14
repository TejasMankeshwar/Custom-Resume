import { useQuery } from '@tanstack/react-query';
import { checkHealth } from './api';
import { useAppStore } from './store';
import { FileText, CheckCircle2, XCircle } from 'lucide-react';
import { SessionSetup } from './components/SessionSetup';
import { JobInput } from './components/JobInput';
import { AnalysisView } from './components/AnalysisView';
import { ChangesReview } from './components/ChangesReview';
import { ResumePreview } from './components/ResumePreview';

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
        <div className="flex items-center md:justify-center gap-2 md:gap-4 mb-8 md:mb-12 text-xs md:text-sm overflow-x-auto whitespace-nowrap pb-4 w-full">
          <div className={`flex items-center gap-1 md:gap-2 shrink-0 ${workflowState === 'SESSION_SETUP' ? 'text-[var(--accent)] font-medium' : 'text-[var(--text-muted)]'}`}>
            <span className="w-6 h-6 rounded-full flex items-center justify-center border border-current">1</span>
            <span className="hidden sm:inline">Setup</span>
          </div>
          <div className="w-4 md:w-8 h-px bg-[var(--border-strong)] shrink-0" />
          <div className={`flex items-center gap-1 md:gap-2 shrink-0 ${workflowState === 'JOB_INPUT' ? 'text-[var(--accent)] font-medium' : 'text-[var(--text-muted)]'}`}>
            <span className="w-6 h-6 rounded-full flex items-center justify-center border border-current">2</span>
            <span className="hidden sm:inline">Job Input</span>
          </div>
          <div className="w-4 md:w-8 h-px bg-[var(--border-strong)] shrink-0" />
          <div className={`flex items-center gap-1 md:gap-2 shrink-0 ${['ANALYSIS_READY', 'ANALYZING', 'GENERATING_CHANGES'].includes(workflowState) ? 'text-[var(--accent)] font-medium' : 'text-[var(--text-muted)]'}`}>
            <span className="w-6 h-6 rounded-full flex items-center justify-center border border-current">3</span>
            <span className="hidden sm:inline">Analysis</span>
          </div>
          <div className="w-4 md:w-8 h-px bg-[var(--border-strong)] shrink-0" />
          <div className={`flex items-center gap-1 md:gap-2 shrink-0 ${workflowState === 'REVIEWING_CHANGES' ? 'text-[var(--accent)] font-medium' : 'text-[var(--text-muted)]'}`}>
            <span className="w-6 h-6 rounded-full flex items-center justify-center border border-current">4</span>
            <span className="hidden sm:inline">Review Changes</span>
          </div>
          <div className="w-4 md:w-8 h-px bg-[var(--border-strong)] shrink-0" />
          <div className={`flex items-center gap-1 md:gap-2 shrink-0 ${workflowState === 'PREVIEW_READY' ? 'text-[var(--accent)] font-medium' : 'text-[var(--text-muted)]'}`}>
            <span className="w-6 h-6 rounded-full flex items-center justify-center border border-current">5</span>
            <span className="hidden sm:inline">Preview</span>
          </div>
        </div>

        <main>
          {workflowState === 'SESSION_SETUP' && <SessionSetup />}
          {(workflowState === 'JOB_INPUT' || workflowState === 'ANALYZING') && <JobInput />}
          {(workflowState === 'ANALYSIS_READY' || workflowState === 'GENERATING_CHANGES') && <AnalysisView />}
          {workflowState === 'REVIEWING_CHANGES' && <ChangesReview />}
          {workflowState === 'PREVIEW_READY' && <ResumePreview />}
        </main>
      </div>
    </div>
  );
}

export default App;
