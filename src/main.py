from creative_writer_cli.data.project_repository import ProjectRepository
from creative_writer_cli.ui.cli import CLI

def main():
    project_repository = ProjectRepository()
    cli = CLI(project_repository)
    cli.main_menu()

if __name__ == "__main__":
    main()