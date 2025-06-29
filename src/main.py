from creative_writer_cli.data.repositories import ProjectRepository
from creative_writer_cli.ui.cli_app import CLIApp

def main():
    project_repository = ProjectRepository()
    app = CLIApp(project_repository)
    app.main_menu()

if __name__ == "__main__":
    main()
