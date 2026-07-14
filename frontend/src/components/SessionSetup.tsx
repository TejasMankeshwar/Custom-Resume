import { useState } from 'react';
import { useAppStore } from '../store';
import { createSession, validateGeminiKey } from '../api';
import { KeyRound, Loader2 } from 'lucide-react';

export function SessionSetup() {
  const [apiKey, setApiKeyValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const { setGeminiKey, setSessionId, setWorkflowState, geminiModel, setGeminiModel } = useAppStore();

  const handleStart = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!apiKey.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      // 1. Validate API Key
      await validateGeminiKey(apiKey.trim(), geminiModel);
      
      // 2. Create Session
      const sessionRes = await createSession();
      
      // 3. Save to store
      setGeminiKey(apiKey.trim());
      setSessionId(sessionRes.session_id);
      setWorkflowState('JOB_INPUT');
      
    } catch (err: any) {
      setError(err.message || 'Failed to initialize session');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-8 border border-[var(--border)] rounded-xl bg-[var(--surface)] shadow-sm">
      <div className="flex justify-center mb-6">
        <div className="p-4 bg-[var(--background)] rounded-full border border-[var(--border)]">
          <KeyRound className="w-8 h-8 text-[var(--accent)]" />
        </div>
      </div>
      
      <h2 className="text-2xl font-semibold text-center mb-2">Welcome</h2>
      <p className="text-center text-[var(--text-secondary)] mb-8 text-sm">
        Select a model and enter your Gemini API key to start tailoring your resume. 
        Your key is stored securely in memory.
      </p>

      <form onSubmit={handleStart} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Select Model</label>
          <select
            value={geminiModel}
            onChange={(e) => setGeminiModel(e.target.value)}
            className="w-full px-4 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg focus:outline-none focus:border-[var(--accent)]"
          >
            <option value="gemini-3.5-flash">Gemini 3.5 Flash</option>
            <option value="gemini-3.5-pro">Gemini 3.5 Pro</option>
            <option value="gemini-3-flash-preview">Gemini 3 Flash Preview</option>
            <option value="gemini-3.1-pro-preview">Gemini 3.1 Pro Preview</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium mb-1">Gemini API Key</label>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKeyValue(e.target.value)}
            placeholder="AIza..."
            className="w-full px-4 py-2 bg-[var(--background)] border border-[var(--border)] rounded-lg focus:outline-none focus:border-[var(--accent)]"
            required
          />
        </div>

        {error && (
          <div className="p-3 text-sm text-[var(--danger)] bg-[var(--danger)]/10 rounded-lg border border-[var(--danger)]/20">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading || !apiKey.trim()}
          className="w-full py-2.5 px-4 bg-[var(--accent)] text-white rounded-lg font-medium hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-colors"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" /> Validating...
            </>
          ) : (
            'Start Session'
          )}
        </button>
      </form>
    </div>
  );
}
