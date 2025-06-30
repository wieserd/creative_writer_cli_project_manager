import json
from typing import Any, Callable, Dict, List

def export_to_json(
    project_name: str,
    project_meta: Dict[str, Any],
    sections: List[str],
    get_section_content: Callable[[str, str], Any]
) -> str:
    all_data = {}
    all_data["meta"] = project_meta
    for section_name in sections:
        content = get_section_content(project_name, section_name)
        all_data[section_name.lower().replace(' ', '_')] = content
    return json.dumps(all_data, indent=4)