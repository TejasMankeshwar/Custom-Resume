from typing import List, Dict, Any

from backend.schemas.gemini import JobAnalysisSchema

class ScoringService:
    @staticmethod
    def calculate_score(jd_analysis: JobAnalysisSchema, parsed_resume: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates a deterministic match score based on JD analysis and parsed resume.
        Weighting:
        - Required Skills Coverage: 35%
        - Preferred Skills Coverage: 10%
        - Keyword Alignment: 20%
        - Experience Alignment: 15%
        - Project Alignment: 10%
        - Education Alignment: 10%
        """
        
        # Flatten the resume content to make it easier to search
        resume_text = ""
        for section in parsed_resume.get("sections", []):
            resume_text += section.get("raw_content", "") + " "
        resume_text = resume_text.lower()
        
        def match_percentage(items: List[str]) -> float:
            if not items:
                return 1.0 # If no items are requested, it's a perfect match
            matched = sum(1 for item in items if item.lower() in resume_text)
            return matched / len(items)

        def get_matched_missing(items: List[str]):
            matched = []
            missing = []
            if not items:
                return matched, missing
            for item in items:
                if item.lower() in resume_text:
                    matched.append(item)
                else:
                    missing.append(item)
            return matched, missing

        required_skills = jd_analysis.required_skills
        preferred_skills = jd_analysis.preferred_skills
        keywords = jd_analysis.keywords
        
        req_score = match_percentage(required_skills) * 35
        pref_score = match_percentage(preferred_skills) * 10
        key_score = match_percentage(keywords) * 20
        
        # For experience, project, education alignment, we'll do simple keyword checks on the JD requirements.
        exp_reqs = jd_analysis.experience_requirements
        exp_score = match_percentage(exp_reqs) * 15
        
        edu_reqs = jd_analysis.education_requirements
        edu_score = match_percentage(edu_reqs) * 10
        
        proj_score = 10.0 # Without Gemini, we'll assume a base project score or we can check keywords.

        total_score = round(req_score + pref_score + key_score + exp_score + proj_score + edu_score)

        req_matched, req_missing = get_matched_missing(required_skills)
        pref_matched, pref_missing = get_matched_missing(preferred_skills)
        
        matched_requirements = req_matched + pref_matched
        missing_requirements = req_missing + pref_missing

        return {
            "total_score": total_score,
            "required_skills_score": round(req_score, 1),
            "preferred_skills_score": round(pref_score, 1),
            "keyword_score": round(key_score, 1),
            "experience_score": round(exp_score, 1),
            "project_score": round(proj_score, 1),
            "education_score": round(edu_score, 1),
            "matched_requirements": matched_requirements,
            "missing_requirements": missing_requirements,
            "unsupported_requirements": [] # For Phase 1, we just return empty or same as missing
        }


scoring_service = ScoringService()
