from backend.services.gemini_service import GeminiService, GeminiError
from backend.schemas.gemini import JobAnalysisSchema
from backend.prompts.jd_analysis import JD_ANALYSIS_SYSTEM_PROMPT

class JDAnalyzer:
    @staticmethod
    def analyze(api_key: str, job_description: str, job_title: str = "") -> JobAnalysisSchema:
        if not job_description or not job_description.strip():
            raise ValueError("Job Description cannot be empty.")
            
        content = f"Job Description:\n{job_description}"
        if job_title and job_title.strip():
            content = f"Manually Provided Job Title (PRESERVE THIS EXACTLY): {job_title}\n\n{content}"
            
        analysis = GeminiService.generate_structured(
            api_key=api_key,
            prompt=JD_ANALYSIS_SYSTEM_PROMPT,
            content=content,
            schema=JobAnalysisSchema
        )
        
        return analysis

jd_analyzer = JDAnalyzer()
