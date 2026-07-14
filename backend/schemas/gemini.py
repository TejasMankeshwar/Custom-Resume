from pydantic import BaseModel, Field
from typing import List, Optional

class JobAnalysisSchema(BaseModel):
    job_title: str = Field(description="The title of the job position.")
    company_name: Optional[str] = Field(None, description="The name of the company.")
    seniority_level: Optional[str] = Field(None, description="Inferred seniority level (e.g., Junior, Mid, Senior).")
    required_skills: List[str] = Field(default_factory=list, description="Strictly required skills mentioned.")
    preferred_skills: List[str] = Field(default_factory=list, description="Nice-to-have or preferred skills.")
    technologies: List[str] = Field(default_factory=list, description="Specific technologies or tools.")
    programming_languages: List[str] = Field(default_factory=list, description="Programming languages required.")
    frameworks: List[str] = Field(default_factory=list, description="Frameworks or libraries.")
    responsibilities: List[str] = Field(default_factory=list, description="Core responsibilities of the role.")
    experience_requirements: List[str] = Field(default_factory=list, description="Required experience or years.")
    education_requirements: List[str] = Field(default_factory=list, description="Required education or degree.")
    keywords: List[str] = Field(default_factory=list, description="Other important buzzwords or keywords.")

class ResumeChangeSchema(BaseModel):
    change_id: str = Field(description="A unique ID for this specific change suggestion.")
    change_type: str = Field(description="Must be one of: REWRITE, REORDER, REMOVE, KEYWORD_ALIGNMENT, EMPHASIS, FORMATTING.")
    target_id: str = Field(description="The stable ID of the target section, entry, or bullet from the parsed resume.")
    section: str = Field(description="The section name where the change occurs (e.g., Experience, Skills).")
    original_content: str = Field(description="The EXACT original text content being targeted for modification.")
    proposed_content: str = Field(description="The new proposed text content to replace the original.")
    reason: str = Field(description="A clear, logical explanation of why this change improves alignment with the JD.")
    jd_requirements: List[str] = Field(description="The specific JD requirements (skills, keywords) this change addresses.")
    keywords: List[str] = Field(description="Keywords inserted or emphasized in this change.")
    confidence: int = Field(description="Confidence level of this change from 1 to 100.")

class ChangeGenerationSchema(BaseModel):
    changes: List[ResumeChangeSchema] = Field(description="A list of proposed changes to the resume.")
