import os
import questionary
from rich.console import Console

from ...data.repositories.project_repository import ProjectRepository
from ...core.templates import TEMPLATES

class NoteImportService:
    def __init__(self, project_repository: ProjectRepository, console: Console):
        self.project_repository = project_repository
        self.console = console

    def import_general_notes(self):
        import_choice = questionary.select(
            "Do you want to import a single note or multiple notes?",
            choices=["Import Single Note", "Import Multiple Notes"]
        ).ask()

        if import_choice == "Import Single Note":
            self._import_single_note()
        elif import_choice == "Import Multiple Notes":
            self._import_multiple_notes()

    def _import_single_note(self):
        file_path = questionary.text("Enter the absolute path to the .txt file:").ask()
        if not file_path:
            self.console.print("[bold red]File path cannot be empty.[/bold red]")
            return
        
        if not os.path.exists(file_path):
            self.console.print(f"[bold red]Error: File not found at {file_path}[/bold red]")
            return
        
        if not file_path.lower().endswith(".txt"):
            self.console.print("[bold red]Error: Only .txt files are supported for import.[/bold red]")
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.console.print(f"[bold red]Error reading file: {e}[/bold red]")
            return

        project_name = os.path.splitext(os.path.basename(file_path))[0]
        project_type = "General Notes"

        success, message = self.project_repository.create_project(project_name, project_type)
        if success:
            self.console.print(f"[bold green]{message}[/bold green]")
            self.project_repository.save_section_content(project_name, "Notes", content)
            self.console.print(f"[bold green]Content from {os.path.basename(file_path)} imported into '{project_name}' project.[/bold green]")
        else:
            self.console.print(f"[bold red]{message}[/bold red]")

    def _import_multiple_notes(self):
        folder_path = questionary.text("Enter the absolute path to the folder containing .txt files:").ask()
        if not folder_path:
            self.console.print("[bold red]Folder path cannot be empty.[/bold red]")
            return

        if not os.path.isdir(folder_path):
            self.console.print(f"[bold red]Error: Directory not found at {folder_path}[/bold red]")
            return

        import_mode = questionary.select(
            "How do you want to import these notes?",
            choices=["As individual General Notes", "As sections in a new Notebook"]
        ).ask()

        if import_mode == "As individual General Notes":
            self._import_multiple_notes_as_individual(folder_path)
        elif import_mode == "As sections in a new Notebook":
            self._import_multiple_notes_as_notebook_sections(folder_path)
        else:
            self.console.print("[yellow]Import cancelled.[/yellow]")

    def _import_multiple_notes_as_individual(self, folder_path: str):
        imported_count = 0
        skipped_count = 0
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(".txt"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    project_name = os.path.splitext(filename)[0]
                    project_type = "General Notes"

                    success, message = self.project_repository.create_project(project_name, project_type)
                    if success:
                        self.project_repository.save_section_content(project_name, "Notes", content)
                        self.console.print(f"[green]Successfully imported '{filename}' as project '{project_name}'[/green]")
                        imported_count += 1
                    else:
                        self.console.print(f"[bold red]Failed to create project for '{filename}': {message}[/bold red]")
                        skipped_count += 1

                except Exception as e:
                    self.console.print(f"[bold red]Error reading file '{filename}': {e}[/bold red]")
                    skipped_count += 1
            elif os.path.isfile(file_path):
                self.console.print(f"[yellow]Skipping non-txt file: {filename}[/yellow]")
                skipped_count += 1
        
        self.console.print(f"\n[bold]Import complete.[/bold]")
        self.console.print(f"- [green]Successfully imported files: {imported_count}[/green]")
        self.console.print(f"- [yellow]Skipped files: {skipped_count}[/yellow]")

    def _import_multiple_notes_as_notebook_sections(self, folder_path: str):
        notebook_name = questionary.text("Enter the name for the new Notebook project:").ask()
        if not notebook_name:
            self.console.print("[bold red]Notebook name cannot be empty. Import cancelled.[/bold red]")
            return

        success, message = self.project_repository.create_project(notebook_name, "Notebook")
        if not success:
            self.console.print(f"[bold red]Failed to create Notebook project '{notebook_name}': {message}[/bold red]")
            return

        self.console.print(f"[green]Notebook '{notebook_name}' created successfully.[/green]")
        imported_count = 0
        skipped_count = 0

        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and filename.lower().endswith(".txt"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    section_name = os.path.splitext(filename)[0] # Use filename as section name
                    
                    add_success, add_message = self.project_repository.add_section_to_project(notebook_name, section_name, content)
                    if add_success:
                        self.console.print(f"[green]Successfully added '{filename}' as section '{section_name}' to '{notebook_name}'[/green]")
                        imported_count += 1
                    else:
                        self.console.print(f"[bold red]Failed to add '{filename}' to '{notebook_name}': {add_message}[/bold red]")
                        skipped_count += 1

                except Exception as e:
                    self.console.print(f"[bold red]Error reading file '{filename}': {e}[/bold red]")
                    skipped_count += 1
            elif os.path.isfile(file_path):
                self.console.print(f"[yellow]Skipping non-txt file: {filename}[/yellow]")
                skipped_count += 1
        
        self.console.print(f"\n[bold]Import into Notebook complete.[/bold]")
        self.console.print(f"- [green]Successfully imported sections: {imported_count}[/green]")
        self.console.print(f"- [yellow]Skipped files: {skipped_count}[/yellow]")