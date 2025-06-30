from typing import Any, Callable, Dict, List
from .markdown_exporter import export_to_markdown

def export_to_txt(
    project_name: str,
    project_meta: Dict[str, Any],
    sections: List[str],
    get_section_content: Callable[[str, str], Any]
) -> str:
    markdown_content = export_to_markdown(project_name, project_meta, sections, get_section_content)
    # Convert Markdown to plain text for TXT export
    # This is a very basic conversion, a proper Markdown parser would be better
    output_content = markdown_content.replace("## ", "").replace("# ", "").replace("**", "").replace("```json", "").replace("```", "").replace("\n", "\n").replace("- ", "")
    return output_content
