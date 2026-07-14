import re
from typing import List, Dict, Any

class ResumeParser:
    @staticmethod
    def parse(latex_content: str) -> Dict[str, Any]:
        """
        Parses the specific structure of the Custom-Resume LaTeX file.
        Returns a structured dictionary with stable deterministic IDs.
        """
        parsed_resume = {
            "sections": []
        }
        
        # Split by \section{...}
        section_splits = re.split(r'\\section{([^}]+)}', latex_content)
        
        # section_splits[0] is the preamble/heading before the first section
        parsed_resume["preamble"] = section_splits[0].strip()
        
        section_count = 0
        for i in range(1, len(section_splits), 2):
            section_name = section_splits[i].strip()
            section_content = section_splits[i+1]
            
            section_id = f"section_{ResumeParser._slugify(section_name)}"
            
            section_data = {
                "id": section_id,
                "name": section_name,
                "entries": [],
                "raw_content": section_content.strip()
            }
            
            # Now parse entries inside the section
            # Check if it contains \resumeSubheading
            subheading_pattern = r'\\resumeSubheading\s*\{([^}]*)\}\s*\{([^}]*)\}\s*\{([^}]*)\}\s*\{([^}]*)\}'
            # Also need to capture the content between subheadings (the item list)
            # Actually, splitting by \resumeSubheading is easier
            subheading_splits = re.split(subheading_pattern, section_content)
            
            if len(subheading_splits) > 1:
                # subheading_splits[0] is before the first \resumeSubheading
                entry_count = 1
                for j in range(1, len(subheading_splits), 5):
                    title = subheading_splits[j]
                    location = subheading_splits[j+1]
                    subtitle = subheading_splits[j+2]
                    date = subheading_splits[j+3]
                    content_after = subheading_splits[j+4]
                    
                    entry_id = f"{section_id}_entry_{entry_count:02d}"
                    
                    entry_data = {
                        "id": entry_id,
                        "title": title.strip(),
                        "location": location.strip(),
                        "subtitle": subtitle.strip(),
                        "date": date.strip(),
                        "bullets": []
                    }
                    
                    # Parse bullets (\resumeItem or \resumeItemNH) inside this entry
                    # \resumeItem{name}{description}
                    # \resumeItemNH{description}
                    bullet_matches = re.finditer(r'\\resumeItem(?:NH)?(?:\{([^}]*)\})?\{([^}]*)\}', content_after)
                    bullet_count = 1
                    for match in bullet_matches:
                        bullet_id = f"{entry_id}_bullet_{bullet_count:02d}"
                        
                        b_name = match.group(1)
                        b_desc = match.group(2)
                        
                        bullet_data = {
                            "id": bullet_id,
                            "type": "resumeItemNH" if not b_name else "resumeItem",
                            "name": b_name.strip() if b_name else None,
                            "description": b_desc.strip()
                        }
                        entry_data["bullets"].append(bullet_data)
                        bullet_count += 1
                        
                    section_data["entries"].append(entry_data)
                    entry_count += 1
            
            # Check for \resumeSubItem (often used for Skills / Publications)
            subitem_matches = re.finditer(r'\\resumeSubItem\{([^}]*)\}\s*\{([^}]*)\}', section_content)
            item_count = 1
            for match in subitem_matches:
                item_name = match.group(1).strip()
                item_desc = match.group(2).strip()
                
                # For skills, try to make a skill-specific ID
                item_id = f"{section_id}_item_{ResumeParser._slugify(item_name)}"
                
                section_data["entries"].append({
                    "id": item_id,
                    "type": "resumeSubItem",
                    "name": item_name,
                    "description": item_desc
                })
                item_count += 1

            parsed_resume["sections"].append(section_data)
            section_count += 1
            
        return parsed_resume

    @staticmethod
    def _slugify(text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^a-z0-9]+', '_', text)
        return text.strip('_')
