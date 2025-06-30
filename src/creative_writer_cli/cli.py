import os
from creative_writer_cli.data.repositories.project_repository import ProjectRepository
from creative_writer_cli.ui.cli_app import CLIApp

def _get_project_base_dir():
    # Check for environment variable
    projects_dir = os.environ.get('CREATIVE_WRITER_PROJECTS_DIR')

    if projects_dir:
        # Use the path from the environment variable
        projects_dir = os.path.expanduser(projects_dir)
    else:
        # Default to ~/.creative_writer_cli/projects
        home_dir = os.path.expanduser("~")
        projects_dir = os.path.join(home_dir, ".creative_writer_cli", "projects")

    # Ensure the directory exists
    os.makedirs(projects_dir, exist_ok=True)
    return projects_dir

def main():
    # Get the base directory for projects
    project_base_dir = _get_project_base_dir()
    
    # Pass the determined base directory to the ProjectRepository
    project_repository = ProjectRepository(base_dir=project_base_dir)
    
    app = CLIApp(project_repository)
    app.main_menu()

if __name__ == "__main__":
    main()