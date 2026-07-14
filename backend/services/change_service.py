import os
from typing import List, Dict, Any
from backend.services.file_service import file_service, MasterResumeError
from backend.schemas.gemini import ResumeChangeSchema
from backend.services.resume_parser import ResumeParser

class ChangeServiceError(Exception):
    pass

class ChangeService:
    @staticmethod
    def apply_changes(session_id: str, decisions: Dict[str, str], proposed_changes: List[Any]) -> dict:
        """
        Applies only ACCEPTED changes deterministically to a fresh copy of the master resume.
        decisions: dict mapping change_id to "ACCEPTED" or "REJECTED".
        """
        # Validate that all proposed changes have a decision
        for change_data in proposed_changes:
            # Depending on if it's a dict or model, handle accordingly.
            # session.validated_changes might be dicts or Pydantic models.
            change_id = change_data.get("change_id") if isinstance(change_data, dict) else change_data.change_id
            
            if change_id not in decisions:
                raise ChangeServiceError(f"Missing decision for change_id {change_id}")
            if decisions[change_id] not in ["ACCEPTED", "REJECTED"]:
                raise ChangeServiceError(f"Invalid decision state {decisions[change_id]} for {change_id}")

        proposed_ids = { (c.get("change_id") if isinstance(c, dict) else c.change_id) for c in proposed_changes }
        for d_id in decisions.keys():
            if d_id not in proposed_ids:
                raise ChangeServiceError(f"Decision provided for unknown change_id {d_id}")

        # Load master resume and hash
        master_content = file_service.read_master_resume()
        master_hash = file_service.compute_master_resume_hash()

        # Parse master resume to verify stable target IDs
        parsed_master = ResumeParser.parse(master_content)

        def find_element(target_id: str) -> dict:
            if target_id.startswith("section_"):
                for sec in parsed_master.get("sections", []):
                    if sec["id"] == target_id: return sec
                    for entry in sec.get("entries", []):
                        if entry["id"] == target_id: return entry
                        for bullet in entry.get("bullets", []):
                            if bullet["id"] == target_id: return bullet
            return None

        # Filter to only ACCEPTED changes
        accepted_changes = []
        rejected_changes = []
        for change_data in proposed_changes:
            c_id = change_data.get("change_id") if isinstance(change_data, dict) else change_data.change_id
            if decisions[c_id] == "ACCEPTED":
                accepted_changes.append(change_data)
            else:
                rejected_changes.append(change_data)

        modified_content = master_content
        
        # Sort accepted changes by original_content length descending to avoid subsets being replaced first
        accepted_changes.sort(
            key=lambda x: len(x.get("original_content") if isinstance(x, dict) else x.original_content), 
            reverse=True
        )

        for change in accepted_changes:
            is_dict = isinstance(change, dict)
            target_id = change.get("target_id") if is_dict else change.target_id
            change_type = change.get("change_type") if is_dict else change.change_type
            orig_content = change.get("original_content") if is_dict else change.original_content
            prop_content = change.get("proposed_content") if is_dict else change.proposed_content
            c_id = change.get("change_id") if is_dict else change.change_id

            element = find_element(target_id)
            if not element:
                raise ChangeServiceError(f"Target ID {target_id} not found in master resume.")

            if change_type in ["REWRITE", "KEYWORD_ALIGNMENT", "EMPHASIS", "FORMATTING"]:
                if orig_content not in master_content:
                    raise ChangeServiceError(f"Original content for {c_id} not found precisely in master resume.")
                modified_content = modified_content.replace(orig_content, prop_content, 1)

            elif change_type == "REMOVE":
                if orig_content not in master_content:
                    raise ChangeServiceError(f"Original content for REMOVE {c_id} not found.")
                modified_content = modified_content.replace(orig_content, "", 1)
            
            elif change_type == "REORDER":
                if orig_content not in master_content:
                    raise ChangeServiceError(f"Original content for REORDER {c_id} not found.")
                modified_content = modified_content.replace(orig_content, prop_content, 1)

        # Verify master resume integrity was preserved
        if file_service.compute_master_resume_hash() != master_hash:
            raise ChangeServiceError("Master resume integrity compromised during application!")

        # Write generated resume
        output_path = file_service.write_generated_resume(session_id, modified_content)
        
        return {
            "status": "SUCCESS",
            "accepted_count": len(accepted_changes),
            "rejected_count": len(rejected_changes),
            "generated_path": output_path
        }

change_service = ChangeService()
