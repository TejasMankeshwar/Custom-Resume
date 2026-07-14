import json
from typing import Dict, Any, List
from backend.services.gemini_service import GeminiService
from backend.schemas.gemini import ChangeGenerationSchema, JobAnalysisSchema
from backend.prompts.change_generation import CHANGE_GENERATION_SYSTEM_PROMPT
from backend.services.validation_pipeline import ChangeValidationPipeline

class TailoringService:
    @staticmethod
    def generate_changes(api_key: str, parsed_resume: Dict[str, Any], jd_analysis: JobAnalysisSchema, match_analysis: Dict[str, Any]) -> Dict[str, Any]:
        
        # Prepare the context for Gemini
        context = {
            "jd_analysis": jd_analysis.model_dump(),
            "match_analysis": match_analysis,
            "parsed_resume": parsed_resume
        }
        
        prompt_content = f"Context:\n{json.dumps(context, indent=2)}"
        
        # Call Gemini
        generation_result = GeminiService.generate_structured(
            api_key=api_key,
            prompt=CHANGE_GENERATION_SYSTEM_PROMPT,
            content=prompt_content,
            schema=ChangeGenerationSchema,
            max_retries=2
        )
        
        # Pass through the strict validation pipeline
        pipeline = ChangeValidationPipeline(parsed_resume, jd_analysis)
        valid_changes, warnings = pipeline.validate_changes(generation_result.changes)
        
        # Convert valid changes to dict for easier JSON serialization
        valid_changes_dicts = [change.model_dump() for change in valid_changes]
        
        return {
            "validated_changes": valid_changes_dicts,
            "valid_count": len(valid_changes_dicts),
            "rejected_count": len(generation_result.changes) - len(valid_changes_dicts),
            "rejection_warnings": warnings
        }

tailoring_service = TailoringService()
