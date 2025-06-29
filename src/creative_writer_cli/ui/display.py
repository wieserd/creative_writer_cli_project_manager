from rich.console import Console
from rich.table import Table
import json

console = Console()

def display_character_table(data):
    if not data:
        console.print("[yellow]No characters found.[/yellow]")
        return

    table = Table(title="Characters Summary")
    table.add_column("Name", style="cyan")
    table.add_column("Race", style="magenta")
    table.add_column("Class", style="green")

    for character in data:
        table.add_row(
            character.get("Name", "N/A"),
            character.get("Race", "N/A"),
            character.get("Class", "N/A"),
        )
    console.print(table)

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

def display_plot_table(data):
    if not data:
        console.print("[yellow]No plot points found.[/yellow]")
        return

    table = Table(title="Plot Summary")
    table.add_column("Order", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Status", style="green")

    sorted_data = sorted(data, key=lambda x: int(x.get("Timeline/Order", 0) or 0))

    for plot_point in sorted_data:
        table.add_row(
            plot_point.get("Timeline/Order", "N/A"),
            plot_point.get("Name", "N/A"),
            plot_point.get("Status", "N/A"),
        )
    console.print(table)

def display_worldbuilding_table(data):
    if not data:
        console.print("[yellow]No worldbuilding elements found.[/yellow]")
        return

    table = Table(title="Worldbuilding Summary")
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="magenta")

    for element in data:
        table.add_row(
            element.get("Name", "N/A"),
            element.get("Type", "N/A"),
        )
    console.print(table)

def display_themes_table(data):
    if not data:
        console.print("[yellow]No themes found.[/yellow]")
        return

    table = Table(title="Themes Summary")
    table.add_column("Theme Name", style="cyan")

    for theme in data:
        table.add_row(theme.get("Theme Name", "N/A"))
    console.print(table)

def display_notes_table(data):
    if not data:
        console.print("[yellow]No notes/ideas found.[/yellow]")
        return

    table = Table(title="Notes/Ideas Summary")
    table.add_column("Title", style="cyan")
    table.add_column("Tags", style="magenta")

    for note in data:
        table.add_row(note.get("Title", "N/A"), note.get("Tags", "N/A"))
    console.print(table)

def display_references_table(data):
    if not data:
        console.print("[yellow]No references found.[/yellow]")
        return

    table = Table(title="References Summary")
    table.add_column("Title", style="cyan")
    table.add_column("Author(s)", style="magenta")
    table.add_column("Year", style="green")

    for ref in data:
        table.add_row(
            ref.get("Title", "N/A"),
            ref.get("Author(s)", "N/A"),
            ref.get("Year", "N/A"),
        )
    console.print(table)

def display_chapters_table(data):
    if not data:
        console.print("[yellow]No chapters found.[/yellow]")
        return

    table = Table(title="Chapters Summary")
    table.add_column("Chapter Title", style="cyan")
    table.add_column("Status", style="magenta")

    for chapter in data:
        table.add_row(
            chapter.get("Chapter Title", "N/A"),
            chapter.get("Status", "N/A"),
        )
    console.print(table)

def display_text_content(data):
    if not data:
        console.print("[yellow]No content found.[/yellow]")
        return
    if isinstance(data, list) and len(data) == 1 and isinstance(data[0], str):
        console.print(data[0])
    else:
        console.print(json.dumps(data, indent=2))

def project_overview(project_name, sections, project_type):
    table = Table(title=f"Project Overview: {project_name}")
    table.add_column("Section", style="cyan")
    table.add_column("Status", style="magenta")

    for section in sections:
        # This part needs to fetch data from the repository, but display.py shouldn't have direct access
        # For now, we'll assume data is passed or fetched by the caller (CLI)
        # This is a placeholder for the actual logic that will be in CLI
        # For now, we'll just show a generic status
        status = "[green]Implemented[/green]" # Placeholder

        if project_type == "Scientific Article":
            # This logic needs to be moved to CLI, which has access to project_repository
            # For now, we'll just show a generic status
            status = "[yellow]Under Development[/yellow]" # Placeholder

        table.add_row(section, status)

    console.print(table)