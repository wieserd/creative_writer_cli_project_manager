#!/bin/bash

# Determine the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Navigate to the project root
cd "$PROJECT_ROOT" || exit

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install the package in editable mode
echo "Installing/Updating package dependencies..."
pip install -e "$PROJECT_ROOT"

# Run the CLI application
echo "Starting Creative Writer CLI..."
creative-writer