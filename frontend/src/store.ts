import { create } from 'zustand';

type WorkflowState = 
  | 'SESSION_SETUP'
  | 'JOB_INPUT'
  | 'ANALYZING'
  | 'ANALYSIS_READY'
  | 'GENERATING_CHANGES'
  | 'REVIEWING_CHANGES'
  | 'PREVIEW_READY';

interface AppState {
  workflowState: WorkflowState;
  sessionId: string | null;
  geminiKey: string | null;
  jdAnalysis: any | null;
  matchAnalysis: any | null;
  tailoringResult: any | null;
  
  setWorkflowState: (state: WorkflowState) => void;
  setSessionId: (id: string | null) => void;
  setGeminiKey: (key: string | null) => void;
  setJdAnalysis: (data: any) => void;
  setMatchAnalysis: (data: any) => void;
  setTailoringResult: (data: any) => void;
  
  resetSession: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  workflowState: 'SESSION_SETUP',
  sessionId: null,
  geminiKey: null,
  jdAnalysis: null,
  matchAnalysis: null,
  tailoringResult: null,
  
  setWorkflowState: (state) => set({ workflowState: state }),
  setSessionId: (id) => set({ sessionId: id }),
  setGeminiKey: (key) => set({ geminiKey: key }),
  setJdAnalysis: (data) => set({ jdAnalysis: data }),
  setMatchAnalysis: (data) => set({ matchAnalysis: data }),
  setTailoringResult: (data) => set({ tailoringResult: data }),
  
  resetSession: () => set({
    workflowState: 'SESSION_SETUP',
    sessionId: null,
    geminiKey: null,
    jdAnalysis: null,
    matchAnalysis: null,
    tailoringResult: null
  }),
}));
