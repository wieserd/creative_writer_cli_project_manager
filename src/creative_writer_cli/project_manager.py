import os
import json
import shutil
from .templates import TEMPLATES

class ProjectManager:
    def __init__(self, projects_dir="projects"):
        self.projects_dir = projects_dir
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)

    def create_project(self, project_name, project_type):
        project_path = os.path.join(self.projects_dir, project_name)
        if os.path.exists(project_path):
            return False, "Project with this name already exists."

        os.makedirs(project_path)

        meta = {"type": project_type, "created": __import__('datetime').datetime.now().isoformat()}
        with open(os.path.join(project_path, "meta.json"), "w") as f:
            json.dump(meta, f, indent=4)

        for section in TEMPLATES[project_type]:
            with open(os.path.join(project_path, f"{section.lower().replace(' ', '_').replace('/', '_')}.json"), "w") as f:
                json.dump([], f, indent=4)
        
        return True, f"Project '{project_name}' of type '{project_type}' created successfully."

    def get_projects(self):
        return [d for d in os.listdir(self.projects_dir) if os.path.isdir(os.path.join(self.projects_dir, d))]

    def delete_project(self, project_name):
        project_path = os.path.join(self.projects_dir, project_name)
        if os.path.exists(project_path):
            shutil.rmtree(project_path)
            return True, f"Project '{project_name}' deleted."
        return False, "Project not found."

    def get_project_meta(self, project_name):
        with open(os.path.join(self.projects_dir, project_name, "meta.json")) as f:
            return json.load(f)

    def get_project_sections(self, project_name):
        meta = self.get_project_meta(project_name)
        return TEMPLATES[meta['type']]

    def get_section_content(self, project_name, section_name):
        section_file = os.path.join(self.projects_dir, project_name, f"{section_name.lower().replace(' ', '_').replace('/', '_')}.json")
        try:
            with open(section_file) as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_section_content(self, project_name, section_name, data):
        section_file = os.path.join(self.projects_dir, project_name, f"{section_name.lower().replace(' ', '_').replace('/', '_')}.json")
        with open(section_file, "w") as f:
            json.dump(data, f, indent=4)

    def export_project(self, project_name, export_format):
        project_path = os.path.join(self.projects_dir, project_name)
        output_content = ""

        if export_format == "Markdown":
            output_content += f"# {project_name}\n\n"
            for section_file in os.listdir(project_path):
                if section_file.endswith(".json") and section_file != "meta.json":
                    section_name = section_file.replace('.json', '').replace('_', ' ').title()
                    output_content += f"## {section_name}\n\n"
                    with open(os.path.join(project_path, section_file)) as f:
                        data = json.load(f)
                    output_content += f"```json\n{json.dumps(data, indent=2)}\n```\n\n"
        elif export_format == "JSON":
            all_data = {}
            for section_file in os.listdir(project_path):
                if section_file.endswith(".json"):
                    section_name = section_file.replace('.json', '')
                    with open(os.path.join(project_path, section_file)) as f:
                        all_data[section_name] = json.load(f)
            output_content = json.dumps(all_data, indent=4)
        elif export_format == "TXT":
            output_content += f"Project: {project_name}\n\n"
            for section_file in os.listdir(project_path):
                if section_file.endswith(".json") and section_file != "meta.json":
                    section_name = section_file.replace('.json', '').replace('_', ' ').title()
                    output_content += f"--- {section_name} ---\n\n"
                    with open(os.path.join(project_path, section_file)) as f:
                        data = json.load(f)
                    output_content += f"{json.dumps(data, indent=2)}\n\n"

        export_filename = f"{project_name}_export.{export_format.lower()}"
        with open(export_filename, "w") as f:
            f.write(output_content)
        return f"Project exported to {export_filename}"