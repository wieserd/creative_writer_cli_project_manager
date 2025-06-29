import os
import json
import shutil
from datetime import datetime

from ..core.models import Character, PlotPoint, WorldbuildingElement, Theme, NoteIdea, Reference, Chapter, Project
from ..core.templates import TEMPLATES
from .json_store import JsonStore

class ProjectRepository:
    def __init__(self, base_dir="projects"):
        self.base_dir = base_dir
        self.json_store = JsonStore(base_dir)
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def _get_section_filepath(self, project_name, section_name):
        sanitized_section_name = section_name.lower().replace(' ', '_').replace('/', '_')
        return os.path.join(project_name, f"{sanitized_section_name}.json")

    def create_project(self, project_name: str, project_type: str) -> tuple[bool, str]:
        project_path = os.path.join(self.base_dir, project_name)
        if os.path.exists(project_path):
            return False, "Project with this name already exists."

        os.makedirs(project_path)

        meta_data = {"name": project_name, "type": project_type, "created": datetime.now().isoformat()}
        self.json_store.write_json(os.path.join(project_name, "meta.json"), meta_data)

        for section in TEMPLATES[project_type]:
            self.json_store.write_json(self._get_section_filepath(project_name, section), [])
        
        return True, f"Project '{project_name}' of type '{project_type}' created successfully."

    def get_projects(self) -> list[str]:
        # List directories directly within the base_dir
        return [d for d in os.listdir(self.base_dir) if os.path.isdir(os.path.join(self.base_dir, d))]

    def delete_project(self, project_name: str) -> tuple[bool, str]:
        project_path = os.path.join(self.base_dir, project_name)
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
            return True, f"Project '{project_name}' deleted."
        return False, "Project not found."

    def get_project_meta(self, project_name: str) -> dict:
        return self.json_store.read_json(os.path.join(project_name, "meta.json"))

    def get_project_sections(self, project_name: str) -> list[str]:
        meta = self.get_project_meta(project_name)
        return TEMPLATES[meta['type']]

    def get_section_content(self, project_name: str, section_name: str) -> list[dict]:
        return self.json_store.read_json(self._get_section_filepath(project_name, section_name))

    def save_section_content(self, project_name: str, section_name: str, data: list[dict]):
        self.json_store.write_json(self._get_section_filepath(project_name, section_name), data)

    def export_project(self, project_name: str, export_format: str) -> str:
        project_abs_path = os.path.join(self.base_dir, project_name)
        output_content = ""

        all_files = os.listdir(project_abs_path)

        if export_format == "Markdown":
            output_content += f"# {project_name}\n\n"
            for file_name in all_files:
                if file_name.endswith(".json") and file_name != "meta.json":
                    section_name_display = file_name.replace('.json', '').replace('_', ' ').title()
                    relative_file_path = os.path.join(project_name, file_name)
                    content = self.json_store.read_json(relative_file_path)
                    output_content += f"## {section_name_display}\n\n"
                    output_content += f"```json\n{json.dumps(content, indent=2)}\n```\n\n"
        elif export_format == "JSON":
            all_data = {}
            for file_name in all_files:
                if file_name.endswith(".json"):
                    section_name_key = file_name.replace('.json', '')
                    relative_file_path = os.path.join(project_name, file_name)
                    all_data[section_name_key] = self.json_store.read_json(relative_file_path)
            output_content = json.dumps(all_data, indent=4)
        elif export_format == "TXT":
            output_content += f"Project: {project_name}\n\n"
            for file_name in all_files:
                if file_name.endswith(".json") and file_name != "meta.json":
                    section_name_display = file_name.replace('.json', '').replace('_', ' ').title()
                    relative_file_path = os.path.join(project_name, file_name)
                    content = self.json_store.read_json(relative_file_path)
                    output_content += f"--- {section_name_display} ---\n\n"
                    output_content += f"{json.dumps(content, indent=2)}\n\n"

        export_filename = f"{project_name}_export.{export_format.lower()}"
        with open(export_filename, "w") as f:
            f.write(output_content)
        return f"Project exported to {export_filename}"