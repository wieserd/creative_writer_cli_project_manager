import questionary
import os

def get_simple_text_input(prompt, default_value=""):
    return questionary.text(prompt, default=default_value, multiline=True).ask()

def prompt_for_project_directory():
    while True:
        path = questionary.text(
            "Enter the path where you want to store your projects (e.g., ~/Documents/MyWriterProjects):",
            validate=lambda text: "Path cannot be empty." if not text else True
        ).ask()

        if not path:
            return None # User cancelled

        expanded_path = os.path.expanduser(path)

        if os.path.exists(expanded_path):
            if os.path.isdir(expanded_path):
                return expanded_path
            else:
                questionary.print(f"Error: '{expanded_path}' is a file, not a directory. Please enter a valid directory path.", style="red")
        else:
            confirm_create = questionary.confirm(
                f"The directory '{expanded_path}' does not exist. Do you want to create it?"
            ).ask()
            if confirm_create:
                try:
                    os.makedirs(expanded_path)
                    questionary.print(f"Directory '{expanded_path}' created successfully.", style="green")
                    return expanded_path
                except OSError as e:
                    questionary.print(f"Error creating directory: {e}. Please try again.", style="red")
            else:
                questionary.print("Directory not created. Please enter an existing directory or allow creation.", style="yellow")
