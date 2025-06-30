#!/bin/bash

# This script removes the Python virtual environment directory (venv)
# from the project's root directory.

# Determine the directory where the script is located (which is the project root)
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Navigate to the project root
cd "$PROJECT_ROOT" || exit

VENV_DIR="venv"

# Check if the virtual environment directory exists
if [ -d "$VENV_DIR" ]; then
    # Ask for confirmation
    read -p "Are you sure you want to remove the virtual environment '$VENV_DIR'? [y/N] " -n 1 -r
    echo    # Move to a new line

    # Check the user's response
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing virtual environment..."
        rm -rf "$VENV_DIR"
        echo "Virtual environment removed successfully."
    else
        echo "Removal cancelled."
    fi
else
    echo "No virtual environment directory ('$VENV_DIR') found."
fi
