from typing import List, Dict, Any, Tuple
from backend.schemas.gemini import ResumeChangeSchema, JobAnalysisSchema
import re

class ChangeValidationPipeline:
    def __init__(self, parsed_resume: Dict[str, Any], jd_analysis: JobAnalysisSchema):
        self.parsed_resume = parsed_resume
        self.jd_analysis = jd_analysis
        self._build_resume_index()
        
    def _build_resume_index(self):
        """Build a flat index of stable IDs to their content for O(1) lookup."""
        self.resume_index = {}
        for section in self.parsed_resume.get("sections", []):
            self.resume_index[section["id"]] = section.get("raw_content", "")
            for entry in section.get("entries", []):
                self.resume_index[entry["id"]] = entry.get("title", "") + " " + entry.get("subtitle", "")
                for bullet in entry.get("bullets", []):
                    self.resume_index[bullet["id"]] = bullet.get("description", "")
                    
    def _is_unsupported(self, text: str) -> bool:
        """
        Check if the proposed text introduces skills/technologies that are completely unsupported by the JD 
        (i.e. not present in the original resume AND not logically derived, but for strictness in Phase 2, 
        we primarily want to ensure it doesn't fabricate skills that the user doesn't have).
        Actually, the rules state: "If a JD requirement is unsupported by the master resume... Do not allow Gemini to add it."
        We check if the proposed text introduces a requirement that is explicitly missing.
        """
        # Flatten resume text to check what the user actually has
        full_resume_text = " ".join(self.resume_index.values()).lower()
        
        # Check JD requirements
        all_reqs = self.jd_analysis.required_skills + self.jd_analysis.preferred_skills + self.jd_analysis.technologies
        
        for req in all_reqs:
            # If the requirement is in the proposed text, but NOT in the original resume text
            if req.lower() in text.lower() and req.lower() not in full_resume_text:
                return True, f"Attempted to introduce unsupported skill/requirement: {req}"
                
        return False, ""
        
    def _check_dangerous_latex(self, text: str) -> bool:
        """Check for arbitrary command execution or dangerous latex macros."""
        dangerous = ['\\input', '\\include', '\\write', '\\immediate', '\\openout', '\\def']
        for d in dangerous:
            if d in text:
                return True
        return False

    def validate_changes(self, proposed_changes: List[ResumeChangeSchema]) -> Tuple[List[ResumeChangeSchema], List[str]]:
        valid_changes = []
        warnings = []
        
        seen_targets = set()
        
        for change in proposed_changes:
            # 1. Check operation type (Pydantic already handles this mostly, but good to be strict)
            if change.change_type not in ["REWRITE", "REORDER", "REMOVE", "KEYWORD_ALIGNMENT", "EMPHASIS", "FORMATTING"]:
                warnings.append(f"Change {change.change_id}: Invalid operation type {change.change_type}.")
                continue
                
            # 2. Duplicate changes
            if change.target_id in seen_targets and change.change_type != "FORMATTING":
                warnings.append(f"Change {change.change_id}: Conflicting changes for target {change.target_id}.")
                continue
                
            # 3. Existing stable target_id
            if change.target_id not in self.resume_index:
                warnings.append(f"Change {change.change_id}: Target ID {change.target_id} not found in parsed resume.")
                continue
                
            # 4. Exact original content match (with some leniency for whitespace)
            original_in_resume = self.resume_index[change.target_id].strip()
            if change.original_content.strip() != original_in_resume:
                warnings.append(f"Change {change.change_id}: Original content mismatch for target {change.target_id}.")
                continue
                
            # 5. Non-empty proposed content when required
            if change.change_type != "REMOVE" and not change.proposed_content.strip():
                warnings.append(f"Change {change.change_id}: Proposed content is empty for a non-REMOVE operation.")
                continue
                
            # 6. Unsupported skill insertion (Fabrication check)
            if change.change_type != "REMOVE":
                is_unsupported, msg = self._is_unsupported(change.proposed_content)
                if is_unsupported:
                    warnings.append(f"Change {change.change_id}: {msg}")
                    continue
                    
            # 7. Dangerous LaTeX commands
            if self._check_dangerous_latex(change.proposed_content):
                warnings.append(f"Change {change.change_id}: Contains dangerous or unsupported LaTeX commands.")
                continue

            # If it passes all checks, it's valid
            valid_changes.append(change)
            seen_targets.add(change.target_id)
            
        return valid_changes, warnings
