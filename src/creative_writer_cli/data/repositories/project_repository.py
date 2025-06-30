import os
import json
import shutil
from datetime import datetime

from ...core.models import Character, PlotPoint, WorldbuildingElement, Theme, NoteIdea, Reference, Chapter, Project
from ...core.templates import TEMPLATES
from .json_store import JsonStore
from ...utils.exporters import markdown_exporter, json_exporter, txt_exporter
from ...utils.exporters import bibtex_formatter, ris_formatter, zotero_rdf_formatter
from ...utils.word_counter import calculate_word_count

from ...utils.path_helpers import get_section_filepath

class ProjectRepository:
    def __init__(self, base_dir="projects"):
        self._base_dir = base_dir
        self._json_store = JsonStore(base_dir)
        if not os.path.exists(self._base_dir):
            os.makedirs(self._base_dir)

    @property
    def base_dir(self):
        return self._base_dir

    @base_dir.setter
    def base_dir(self, new_base_dir):
        self._base_dir = new_base_dir
        self._json_store = JsonStore(new_base_dir)
        if not os.path.exists(self._base_dir):
            os.makedirs(self._base_dir)

    @property
    def json_store(self):
        return self._json_store

    def create_project(self, project_name: str, project_type: str) -> tuple[bool, str]:
        project_path = os.path.join(self.base_dir, project_name)
        if os.path.exists(project_path):
            return False, "Project with this name already exists."

        os.makedirs(project_path)

        meta_data = {"name": project_name, "type": project_type, "created": datetime.now().isoformat()}
        self.json_store.write_json(os.path.join(project_name, "meta.json"), meta_data)

        for section in TEMPLATES[project_type]:
            # Initialize 'Notes' section for 'General Notes' as an empty string
            if project_type == "General Notes" and section == "Notes":
                self.json_store.write_json(get_section_filepath(project_name, section), "")
            else:
                self.json_store.write_json(get_section_filepath(project_name, section), [])
        
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
        project_type = meta.get('type')
        
        # Start with sections from the template
        sections = TEMPLATES.get(project_type, [])

        # For Notebooks, also include dynamically added sections (notes)
        if project_type == "Notebook":
            project_dir = os.path.join(self.base_dir, project_name)
            # List all .json files in the project directory, excluding meta.json
            dynamic_sections = [
                os.path.splitext(f)[0] for f in os.listdir(project_dir)
                if f.endswith('.json') and f != 'meta.json' and os.path.isfile(os.path.join(project_dir, f))
            ]
            # Add dynamic sections, ensuring no duplicates and maintaining order if possible
            # For simplicity, we'll just append them for now.
            for ds in dynamic_sections:
                if ds not in sections:
                    sections.append(ds)
        return sections

    def add_section_to_project(self, project_name: str, section_name: str, content: str) -> tuple[bool, str]:
        project_path = os.path.join(self.base_dir, project_name)
        if not os.path.exists(project_path):
            return False, "Project not found."
        
        section_filepath = get_section_filepath(project_name, section_name)
        if os.path.exists(section_filepath):
            return False, f"Section '{section_name}' already exists in project '{project_name}'."
        
        try:
            self.json_store.write_json(section_filepath, content)
            return True, f"Section '{section_name}' added to project '{project_name}'."
        except Exception as e:
            return False, f"Error adding section: {e}"

    def get_section_content(self, project_name: str, section_name: str):
        # For 'Notes' section in 'General Notes' project, return content as string
        project_meta = self.get_project_meta(project_name)
        if project_meta.get('type') == "General Notes" and section_name == "Notes":
            return self.json_store.read_json(get_section_filepath(project_name, section_name), default_value="")
        else:
            return self.json_store.read_json(get_section_filepath(project_name, section_name), default_value=[])

    def save_section_content(self, project_name: str, section_name: str, data):
        # For 'Notes' section in 'General Notes' project, save content as string
        project_meta = self.get_project_meta(project_name)
        if project_meta.get('type') == "General Notes" and section_name == "Notes":
            self.json_store.write_json(get_section_filepath(project_name, section_name), data)
        else:
            self.json_store.write_json(get_section_filepath(project_name, section_name), data)

    def export_project(self, project_name: str, export_format: str) -> str:
        project_abs_path = os.path.join(self.base_dir, project_name)
        output_content = ""
        project_meta = self.get_project_meta(project_name)
        sections = self.get_project_sections(project_name)

        if export_format == "Markdown":
            output_content = markdown_exporter.export_to_markdown(project_name, project_meta, sections, self.get_section_content)
        elif export_format == "TXT":
            output_content = txt_exporter.export_to_txt(project_name, project_meta, sections, self.get_section_content)
        elif export_format == "JSON":
            output_content = json_exporter.export_to_json(project_name, project_meta, sections, self.get_section_content)
        elif export_format in ["BibTeX", "RIS", "Zotero RDF"]:
            references_content = self.get_section_content(project_name, "References")
            if not references_content:
                return f"No references found in project '{project_name}' to export to {export_format}."

            formatted_references = []
            for ref in references_content:
                if export_format == "BibTeX":
                    formatted_references.append(reference_export_formatter.format_to_bibtex(ref))
                elif export_format == "RIS":
                    formatted_references.append(reference_export_formatter.format_to_ris(ref))
                elif export_format == "Zotero RDF":
                    formatted_references.append(reference_export_formatter.format_to_zotero_rdf(ref))
            output_content = "\n\n".join(formatted_references)

        export_extension = export_format.lower()
        if export_extension == "markdown":
            export_extension = "md"
        elif export_extension == "bibtex":
            export_extension = "bib"
        elif export_extension == "ris":
            export_extension = "ris"
        elif export_extension == "zotero rdf":
            export_extension = "rdf"
        export_filename = f"{project_name}_export.{export_extension}"
        if export_format in ["BibTeX", "RIS", "Zotero RDF"]:
            export_filename = f"{project_name}_references_export.{export_extension}"
        with open(export_filename, "w") as f:
            f.write(output_content)
        return f"Project exported to {export_filename}"

    def rename_project(self, old_project_name: str, new_project_name: str) -> tuple[bool, str]:
        old_project_path = os.path.join(self.base_dir, old_project_name)
        new_project_path = os.path.join(self.base_dir, new_project_name)

        if not os.path.exists(old_project_path):
            return False, "Original project not found."

        if os.path.exists(new_project_path):
            return False, "A project with the new name already exists."

        try:
            shutil.move(old_project_path, new_project_path)

            # Update the project name in the meta.json file
            meta_filepath = os.path.join(new_project_path, "meta.json")
            meta_data = self.json_store.read_json(os.path.join(new_project_name, "meta.json")) # Read from new path
            meta_data["name"] = new_project_name
            self.json_store.write_json(os.path.join(new_project_name, "meta.json"), meta_data) # Write to new path

            return True, f"Project '{old_project_name}' renamed to '{new_project_name}' successfully."
        except Exception as e:
            return False, f"Error renaming project: {e}"

    def merge_notebooks(self, source_notebook_name: str, target_notebook_name: str) -> tuple[bool, str]:
        # Validate source notebook exists and is a Notebook
        source_meta = self.get_project_meta(source_notebook_name)
        if not source_meta or source_meta.get('type') != "Notebook":
            return False, f"Source project '{source_notebook_name}' not found or is not a Notebook."

        # Validate target notebook exists and is a Notebook
        target_meta = self.get_project_meta(target_notebook_name)
        if not target_meta or target_meta.get('type') != "Notebook":
            return False, f"Target project '{target_notebook_name}' not found or is not a Notebook."

        # Get all sections from the source notebook
        source_sections = self.get_project_sections(source_notebook_name)

        # Transfer each section to the target notebook
        for section_name in source_sections:
            # Skip the default 'Introduction' section if it's empty in the source
            if section_name == "Introduction" and not self.get_section_content(source_notebook_name, section_name):
                continue
            
            content = self.get_section_content(source_notebook_name, section_name)
            
            # Attempt to add the section to the target notebook
            # If a section with the same name already exists, append content or handle as needed
            # For now, we'll try to add. If it fails due to name conflict, we'll report it.
            success, message = self.add_section_to_project(target_notebook_name, section_name, content)
            if not success:
                # If section already exists, try to append content (simple concatenation for text)
                if "already exists" in message:
                    existing_content = self.get_section_content(target_notebook_name, section_name)
                    new_content = f"{existing_content}\n\n--- Merged from {source_notebook_name} ---\n\n{content}"
                    self.save_section_content(target_notebook_name, section_name, new_content)
                    # No need to report success here, as it's handled by the final message
                else:
                    return False, f"Failed to merge section '{section_name}' from '{source_notebook_name}' to '{target_notebook_name}': {message}"

        # Delete the source notebook after successful transfer
        delete_success, delete_message = self.delete_project(source_notebook_name)
        if not delete_success:
            return False, f"Successfully merged sections, but failed to delete source notebook '{source_notebook_name}': {delete_message}"

        return True, f"Notebook '{source_notebook_name}' successfully merged into '{target_notebook_name}'. '{source_notebook_name}' has been deleted."

    def get_project_word_count(self, project_name: str) -> int:
        project_meta = self.get_project_meta(project_name)
        sections = self.get_project_sections(project_name)
        return calculate_word_count(project_name, project_meta, sections, self.get_section_content)
