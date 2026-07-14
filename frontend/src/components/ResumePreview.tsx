import { useAppStore } from '../store';
import { API_BASE_URL } from '../api';
import { ArrowRight, CheckCircle2, FileText, Download, TrendingUp } from 'lucide-react';

export function ResumePreview() {
  const { sessionId, matchAnalysis, finalMatchAnalysis, tailoringResult, decisions } = useAppStore();

  if (!sessionId || !matchAnalysis || !finalMatchAnalysis || !tailoringResult) {
    return null;
  }

  const initialScore = matchAnalysis.score;
  const finalScore = finalMatchAnalysis.score;
  const improvement = finalScore - initialScore;

  const acceptedCount = Object.values(decisions).filter(d => d === 'ACCEPTED').length;
  const rejectedCount = Object.values(decisions).filter(d => d === 'REJECTED').length;

  const pdfUrl = `${API_BASE_URL}/resume/preview/${sessionId}`;
  const exportTexUrl = `${API_BASE_URL}/resume/export/${sessionId}/tex`;
  const exportPdfUrl = `${API_BASE_URL}/resume/export/${sessionId}/pdf`;

  return (
    <div className="flex flex-col lg:flex-row gap-6 h-[calc(100vh-140px)]">
      {/* Left Column: Final Match Report */}
      <div className="w-full lg:w-[35%] flex flex-col gap-6 overflow-y-auto pr-2">
        <div className="p-6 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <TrendingUp className="w-6 h-6 text-[var(--accent)]" /> 
            Final Match Report
          </h2>

          <div className="flex items-center justify-between mb-8 px-4">
            <div className="text-center">
              <p className="text-sm text-[var(--text-secondary)] mb-1 font-medium uppercase tracking-wider">Before</p>
              <div className="text-4xl font-bold text-[var(--text-muted)]">{initialScore}</div>
            </div>
            
            <div className="flex flex-col items-center justify-center">
              <ArrowRight className="w-6 h-6 text-[var(--text-muted)] mb-1" />
              {improvement > 0 ? (
                <span className="text-sm font-bold text-[var(--success)] bg-[var(--success)]/10 px-2 py-0.5 rounded-full">
                  +{improvement}
                </span>
              ) : improvement < 0 ? (
                <span className="text-sm font-bold text-[var(--danger)] bg-[var(--danger)]/10 px-2 py-0.5 rounded-full">
                  {improvement}
                </span>
              ) : (
                <span className="text-sm font-bold text-[var(--text-secondary)] bg-[var(--border)] px-2 py-0.5 rounded-full">
                  No Change
                </span>
              )}
            </div>

            <div className="text-center">
              <p className="text-sm text-[var(--text-secondary)] mb-1 font-medium uppercase tracking-wider">After</p>
              <div className="text-4xl font-bold text-[var(--accent)]">{finalScore}</div>
            </div>
          </div>

          <div className="space-y-4 pt-6 border-t border-[var(--border)]">
            <div className="flex justify-between items-center text-sm">
              <span className="text-[var(--text-secondary)]">Changes Applied</span>
              <span className="font-semibold text-[var(--success)]">{acceptedCount} Accepted</span>
            </div>
            <div className="flex justify-between items-center text-sm">
              <span className="text-[var(--text-secondary)]">Changes Ignored</span>
              <span className="font-semibold text-[var(--danger)]">{rejectedCount} Rejected</span>
            </div>
          </div>

          <div className="mt-8 space-y-3">
            <a 
              href={exportPdfUrl}
              download="Tejas_Resume_Tailored.pdf"
              className="w-full py-3 bg-[var(--accent)] text-white rounded-lg font-medium hover:bg-blue-600 transition-colors flex items-center justify-center gap-2"
            >
              <Download className="w-4 h-4" /> Export PDF
            </a>
            
            <a 
              href={exportTexUrl}
              download="Tejas_Resume_Tailored.tex"
              className="w-full py-3 bg-[var(--background)] text-[var(--text-primary)] border border-[var(--border)] rounded-lg font-medium hover:bg-[var(--border)] transition-colors flex items-center justify-center gap-2"
            >
              <FileText className="w-4 h-4" /> Export LaTeX (.tex)
            </a>
          </div>
          
          <p className="text-xs text-[var(--text-muted)] mt-6 text-center">
            Internal resume-to-job alignment score.<br/>Not an official ATS score.
          </p>
        </div>
      </div>

      {/* Right Column: PDF Preview */}
      <div className="w-full lg:w-[65%] h-[600px] lg:h-full border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm overflow-hidden flex flex-col">
        <div className="p-3 border-b border-[var(--border)] bg-[var(--background)] flex justify-between items-center">
          <h3 className="font-semibold text-[var(--text-primary)] flex items-center gap-2">
            <FileText className="w-4 h-4 text-[var(--accent)]" /> Tailored Resume Preview
          </h3>
          <span className="text-xs font-medium px-2 py-1 bg-[var(--success)]/10 text-[var(--success)] rounded-full flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> Compilation Successful
          </span>
        </div>
        <div className="flex-1 w-full h-full bg-[#525659]">
          <object 
            data={pdfUrl} 
            type="application/pdf" 
            className="w-full h-full"
          >
            <div className="flex flex-col items-center justify-center h-full text-white p-6 text-center">
              <FileText className="w-12 h-12 mb-4 opacity-50" />
              <p className="mb-4">Your browser does not support embedded PDFs.</p>
              <a 
                href={pdfUrl} 
                className="px-4 py-2 bg-[var(--accent)] text-white rounded-lg font-medium hover:bg-blue-600 transition-colors"
                target="_blank"
                rel="noreferrer"
              >
                Open PDF in New Tab
              </a>
            </div>
          </object>
        </div>
      </div>
      
    </div>
  );
}
