from .base_section_handler import BaseSectionHandler
import questionary

class GenericHandler(BaseSectionHandler):
    def display_content(self, data: str):
        # Assuming data for General Notes is a single string
        self.console.print("\n[bold]Current Content:[/bold]")
        self.console.print(data)

    def get_choices(self, data: str) -> list:
        # Only offer to edit content or go back
        return ["Edit Content", "Back to Project Menu"]

    def handle_section_action(self, project_name: str, section_name: str, action: str, data: str):
        if action == "Edit Content":
            new_content = questionary.text(
                "Enter new content (Ctrl+C to cancel):",
                default=data,
                multiline=True
            ).ask()
            if new_content is not None: # User might cancel with Ctrl+C
                self.project_repository.save_section_content(project_name, section_name, new_content)
                self.console.print("[green]Content updated.[/green]")
            else:
                self.console.print("[yellow]Content edit cancelled.[/yellow]")
