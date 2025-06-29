from rich.console import Console
from rich.table import Table
import questionary
import json

console = Console()

def view_details(item_data, item_name_field):
    if not item_data:
        console.print("[yellow]No items to view.[/yellow]")
        return

    item_to_view_name = questionary.select(
        f"Select {item_name_field.lower()} to view details:",
        choices=[item.get(item_name_field, f"Item {i}") for i, item in enumerate(item_data)]
    ).ask()

    if item_to_view_name:
        item = next((i for i in item_data if i.get(item_name_field) == item_to_view_name), None)
        if item:
            console.print(f"\n[bold]{item_name_field} Details: {item.get(item_name_field)}[/bold]")
            for key, value in item.items():
                console.print(f"  [bold cyan]{key}:[/bold cyan] {value}")

def display_text_content(data):
    if not data:
        console.print("[yellow]No content found.[/yellow]")
        return
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], str):
        console.print(data[0])
    else:
        console.print(json.dumps(data, indent=2))

def project_overview(project_name, sections, project_type, project_repository):
    table = Table(title=f"Project Overview: {project_name}")
    table.add_column("Section", style="cyan")
    table.add_column("Status", style="magenta")

    for section in sections:
        data = project_repository.get_section_content(project_name, section)
        status = ""

        if project_type == "Scientific Article":
            if section == "References":
                status = f"[green]{len(data)} references[/green]" if data else "[red]No references[/red]"
            elif section in ["Title", "Abstract", "Introduction", "Methods", "Results", "Discussion", "Conclusion"]:
                if data and data[0]:
                    snippet = data[0][:70]  # Take first 70 characters
                    if len(data[0]) > 70:
                        snippet += "..."
                    status = f"[green]{snippet}[/green]"
                else:
                    status = "[red]Empty[/red]"
            else: # Fallback for any other scientific article sections not explicitly handled
                status = "[green]Complete[/green]" if data else "[red]Missing[/red]"
        else: # For Novel and other project types
            status = "[green]Complete[/green]" if data else "[red]Missing[/red]"
        
        table.add_row(section, status)

    console.print(table)
