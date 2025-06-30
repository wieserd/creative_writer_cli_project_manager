import questionary
from rich.console import Console
import json
import os

from ..data.repositories.project_repository import ProjectRepository
from ..core.templates import TEMPLATES
from .wizards.generic_wizards import prompt_for_project_directory
from ..utils import config_manager
from .ascii_art import get_ascii_art
from .services.project_interaction_service import ProjectInteractionService
from .services.note_import_service import NoteImportService # Import the new service

console = Console()

class CLIApp:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository
        self.console = Console()
        self.project_interaction_service = ProjectInteractionService(project_repository, self.console)
        self.note_import_service = NoteImportService(project_repository, self.console) # Instantiate the new service

    def main_menu(self):
        self.console.print(get_ascii_art())
        while True:
            choice = questionary.select(
                "What do you want to do?",
                choices=["Create New Project", "View Existing Projects", "Delete Project", "Import General Notes", "Add Note to Notebook", "Merge Notebooks", "Configure Project Directory", "Exit"]
            ).ask()

            if choice == "Create New Project":
                self.create_project()
            elif choice == "View Existing Projects":
                self.view_projects()
            elif choice == "Delete Project":
                self.delete_project()
            elif choice == "Import General Notes":
                if not self._validate_project_directory():
                    return
                self.note_import_service.import_general_notes() # Delegate to the new service
            elif choice == "Add Note to Notebook":
                self._add_note_to_notebook()
            elif choice == "Merge Notebooks":
                self._merge_notebooks()
            elif choice == "Configure Project Directory":
                self._configure_project_directory()
            elif choice == "Exit" or choice is None:
                if questionary.confirm("Are you sure you want to exit? This will close the application.").ask():
                    break
                else:
                    continue # If user says no, continue the loop and show main menu again

    def _add_note_to_notebook():
        if not self._validate_project_directory():
            return

        all_projects = self.project_repository.get_projects()
        general_notes_projects = []
        notebook_projects = []

        for project_name in all_projects:
            meta = self.project_repository.get_project_meta(project_name)
            if meta.get('type') == "General Notes":
                general_notes_projects.append(project_name)
            elif meta.get('type') == "Notebook":
                notebook_projects.append(project_name)
        
        if not general_notes_projects:
            self.console.print("[bold yellow]No 'General Notes' projects found to add.[/bold yellow]")
            return

        if not notebook_projects:
            self.console.print("[bold yellow]No 'Notebook' projects found. Please create one first.[/bold yellow]")
            return

        note_to_add = questionary.select(
            "Select a 'General Note' project to add to a Notebook:",
            choices=general_notes_projects
        ).ask()

        if not note_to_add:
            self.console.print("[yellow]Operation cancelled.[/yellow]")
            return

        target_notebook = questionary.select(
            f"Select the 'Notebook' project to add '{note_to_add}' to:",
            choices=notebook_projects
        ).ask()

        if not target_notebook:
            self.console.print("[yellow]Operation cancelled.[/yellow]")
            return

        # Get the content of the General Note
        note_content = self.project_repository.get_section_content(note_to_add, "Notes")

        # Add the note as a new section in the target Notebook
        success, message = self.project_repository.add_section_to_project(target_notebook, note_to_add, note_content)
        if success:
            self.console.print(f"[green]Successfully added '{note_to_add}' to '{target_notebook}' as a new section.[/green]")
            # Delete the original General Note project
            delete_success, delete_message = self.project_repository.delete_project(note_to_add)
            if delete_success:
                self.console.print(f"[green]Original 'General Note' project '{note_to_add}' deleted.[/green]")
            else:
                self.console.print(f"[bold red]Error deleting original 'General Note' project: {delete_message}[/bold red]")
        else:
            self.console.print(f"[bold red]Error adding note to notebook: {message}[/bold red]")

    def _merge_notebooks(self):
        if not self._validate_project_directory():
            return

        all_projects = self.project_repository.get_projects()
        notebook_projects = [p for p in all_projects if self.project_repository.get_project_meta(p).get('type') == "Notebook"]

        if len(notebook_projects) < 2:
            self.console.print("[bold yellow]You need at least two Notebook projects to merge.[/bold yellow]")
            return

        source_notebook = questionary.select(
            "Select the Notebook to merge FROM (this Notebook will be deleted):",
            choices=notebook_projects
        ).ask()

        if not source_notebook:
            self.console.print("[yellow]Operation cancelled.[/yellow]")
            return

        # Remove source notebook from choices for target notebook
        target_notebook_choices = [nb for nb in notebook_projects if nb != source_notebook]

        target_notebook = questionary.select(
            f"Select the Notebook to merge '{source_notebook}' INTO (this Notebook will receive the sections):",
            choices=target_notebook_choices
        ).ask()

        if not target_notebook:
            self.console.print("[yellow]Operation cancelled.[/yellow]")
            return

        if questionary.confirm(f"Are you sure you want to merge '{source_notebook}' into '{target_notebook}'? '{source_notebook}' will be deleted.").ask():
            success, message = self.project_repository.merge_notebooks(source_notebook, target_notebook)
            if success:
                self.console.print(f"[bold green]{message}[/bold green]")
            else:
                self.console.print(f"[bold red]{message}[/bold red]")
        else:
            self.console.print("[yellow]Merge operation cancelled.[/yellow]")

    def _configure_project_directory():
        self.console.print("\n[bold]Configure Project Directory[/bold]")
        new_path = prompt_for_project_directory(self.project_repository.base_dir)
        if new_path is None: # User cancelled (Ctrl+C)
            self.console.print("[yellow]Project directory configuration cancelled.[/yellow]")
            return
        
        if new_path != self.project_repository.base_dir: # Only update if path actually changed
            config_manager.set_project_directory_in_config(new_path)
            self.project_repository.base_dir = new_path # This will now use the setter to re-initialize json_store
            self.console.print(f"[green]Project directory set to: {new_path}[/green]")
        else:
            self.console.print("[yellow]Project directory remains unchanged.[/yellow]")

    def _validate_project_directory(self):
        if not os.path.exists(self.project_repository.base_dir) or not os.path.isdir(self.project_repository.base_dir):
            self.console.print("[bold red]Error: Could not open specified project folder. Please configure project directory.[/bold red]")
            return False
        return True

    def create_project(self):
        if not self._validate_project_directory():
            return

        project_type = questionary.select(
            "What type of writing?",
            choices=list(TEMPLATES.keys())
        ).ask()

        if project_type is None:
            return

        project_name = questionary.text("Enter project name:").ask()

        if not project_name:
            self.console.print("[bold red]Project name cannot be empty.[/bold red]")
            return

        success, message = self.project_repository.create_project(project_name, project_type)

        if success:
            self.console.print(f"[bold green]{message}[/bold green]")
            # Initial input for Novel projects
            if project_type == "Novel":
                initial_input_choice = questionary.select(
                    "Initial input",
                    choices=["Plot", "Characters", "skip to template overview"]
                ).ask()

                if initial_input_choice and initial_input_choice != "skip to template overview":
                    self.project_interaction_service.edit_section(project_name, initial_input_choice)
        else:
            self.console.print(f"[bold red]{message}[/bold red]")

    def view_projects(self):
        if not self._validate_project_directory():
            return

        projects = self.project_repository.get_projects()
        if not projects:
            self.console.print("[bold yellow]No projects found.[/bold yellow]")
            return

        project_choices = []
        for project_name in projects:
            project_meta = self.project_repository.get_project_meta(project_name)
            project_type = project_meta.get('type', 'Unknown Type')
            project_choices.append(f"{project_name} ({project_type})")

        project_to_view_display = questionary.select(
            "Select a project to view:",
            choices=project_choices
        ).ask()

        if project_to_view_display:
            # Extract the actual project name from the display string
            project_to_view = project_to_view_display.split(' (')[-2]

        if project_to_view:
            self.project_interaction_service.project_menu(project_to_view)

    def delete_project(self):
        projects = self.project_repository.get_projects()
        if not projects:
            self.console.print("[bold yellow]No projects found.[/bold yellow]")
            return

        project_to_delete = questionary.select(
            "Select a project to delete:",
            choices=projects
        ).ask()

        if project_to_delete:
            if questionary.confirm(f"Are you sure you want to delete the project '{project_to_delete}'?").ask():
                success, message = self.project_repository.delete_project(project_to_delete)
                if success:
                    self.console.print(f"[bold green]{message}[/bold green]")
                else:
                    self.console.print(f"[bold red]{message}[/bold red]")