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
  geminiModel: string;
  jdAnalysis: any | null;
  matchAnalysis: any | null;
  tailoringResult: any | null;
  decisions: Record<string, string>; // change_id -> 'PENDING' | 'ACCEPTED' | 'REJECTED'
  finalMatchAnalysis: any | null;
  
  setWorkflowState: (state: WorkflowState) => void;
  setSessionId: (id: string | null) => void;
  setGeminiKey: (key: string | null) => void;
  setGeminiModel: (model: string) => void;
  setJdAnalysis: (data: any) => void;
  setMatchAnalysis: (data: any) => void;
  setTailoringResult: (data: any) => void;
  setDecision: (changeId: string, decision: string) => void;
  setDecisions: (decisions: Record<string, string>) => void;
  setFinalMatchAnalysis: (data: any) => void;
  
  resetSession: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  workflowState: 'SESSION_SETUP',
  sessionId: null,
  geminiKey: null,
  geminiModel: 'gemini-3.5-flash',
  jdAnalysis: null,
  matchAnalysis: null,
  tailoringResult: null,
  decisions: {},
  finalMatchAnalysis: null,
  
  setWorkflowState: (state) => set({ workflowState: state }),
  setSessionId: (id) => set({ sessionId: id }),
  setGeminiKey: (key) => set({ geminiKey: key }),
  setGeminiModel: (model) => set({ geminiModel: model }),
  setJdAnalysis: (data) => set({ jdAnalysis: data }),
  setMatchAnalysis: (data) => set({ matchAnalysis: data }),
  setTailoringResult: (data) => {
    // Initialize all decisions as PENDING
    const initialDecisions: Record<string, string> = {};
    if (data && data.validated_changes) {
      data.validated_changes.forEach((change: any) => {
        initialDecisions[change.change_id] = 'PENDING';
      });
    }
    set({ tailoringResult: data, decisions: initialDecisions });
  },
  setDecision: (changeId, decision) => set((state) => ({
    decisions: { ...state.decisions, [changeId]: decision }
  })),
  setDecisions: (newDecisions) => set({ decisions: newDecisions }),
  setFinalMatchAnalysis: (data) => set({ finalMatchAnalysis: data }),
  
  resetSession: () => set({
    workflowState: 'SESSION_SETUP',
    sessionId: null,
    geminiKey: null,
    geminiModel: 'gemini-3.5-flash',
    jdAnalysis: null,
    matchAnalysis: null,
    tailoringResult: null,
    decisions: {},
    finalMatchAnalysis: null
  }),
}));

