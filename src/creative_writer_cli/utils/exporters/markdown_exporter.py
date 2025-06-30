import json
from typing import Any, Callable, Dict, List

from .markdown_formatters import (
    format_characters_to_markdown,
    format_plot_points_to_markdown,
    format_worldbuilding_to_markdown,
    format_themes_to_markdown,
    format_notes_to_markdown,
    format_references_to_markdown,
    format_chapters_to_markdown,
    format_generic_text_section_to_markdown
)

def export_to_markdown(
    project_name: str,
    project_meta: Dict[str, Any],
    sections: List[str],
    get_section_content: Callable[[str, str], Any]
) -> str:
    output_content = f"# {project_name}\n\n"
    project_type = project_meta.get('type')

    for section_name in sections:
        content = get_section_content(project_name, section_name)
        
        if section_name == "Characters":
            output_content += format_characters_to_markdown(content)
        elif section_name == "Plot":
            output_content += format_plot_points_to_markdown(content)
        elif section_name == "Worldbuilding":
            output_content += format_worldbuilding_to_markdown(content)
        elif section_name == "Themes":
            output_content += format_themes_to_markdown(content)
        elif section_name == "Notes/Ideas":
            # For General Notes, content is a string, not a list
            if project_type == "General Notes" and section_name == "Notes":
                output_content += f"## {section_name}\n\n{content}\n\n"
            else:
                output_content += format_notes_to_markdown(content)
        elif section_name == "References":
            output_content += format_references_to_markdown(content)
        elif project_type == "Scientific Book" and section_name in ["Chapter 1", "Chapter 2", "Chapter 3", "Conclusion"]:
            output_content += format_chapters_to_markdown(content)
        elif project_type in ["Scientific Article", "Scientific Book"] and section_name in ["Title", "Abstract", "Introduction", "Methods", "Results", "Discussion"]:
            output_content += format_generic_text_section_to_markdown(content, section_name)
        else:
            # Fallback for any other sections not explicitly handled, or generic sections
            if content:
                output_content += f"## {section_name}\n\n"
                if isinstance(content, list) and len(content) == 1 and isinstance(content[0], str):
                    output_content += f"{content[0]}\n\n"
                else:
                    output_content += f"```json\n{json.dumps(content, indent=2)}\n```\n\n"
            else:
                output_content += f"## {section_name}\n\nNo content found.\n\n"
    return output_content