#!/bin/bash

# Determine the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Create a virtual environment if it doesn't exist
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$PROJECT_ROOT/venv"
fi

# Activate the virtual environment
source "$PROJECT_ROOT/venv/bin/activate"

# Navigate to the project root and install the package in editable mode
cd "$PROJECT_ROOT" || exit

echo "Installing/Updating package dependencies..."
pip install -e .

# Run the CLI application
echo "Starting Creative Writer CLI..."
creative-writer