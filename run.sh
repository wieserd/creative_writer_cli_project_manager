#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Define virtual environment path
VENV_PATH="$SCRIPT_DIR/venv"

# Always remove existing virtual environment to ensure a clean setup
if [ -d "$VENV_PATH" ]; then
    echo "Removing existing virtual environment..."
    rm -rf "$VENV_PATH"
fi

echo "Creating virtual environment..."
python3 -m venv "$VENV_PATH"

# Ensure pip is installed and upgraded immediately after venv creation
echo "Ensuring pip is installed and up-to-date in the new virtual environment..."
"$VENV_PATH/bin/python" -m ensurepip --upgrade
"$VENV_PATH/bin/pip" install --upgrade pip

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

# Install dependencies if requirements.txt exists
if [ -f "$SCRIPT_DIR/requirements.txt" ]; then
    echo "Installing dependencies..."
    "$VENV_PATH/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"
fi

# Run the main application
python "$SCRIPT_DIR/src/main.py"
