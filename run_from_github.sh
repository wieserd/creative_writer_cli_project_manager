#!/bin/bash

# This script provides a one-liner execution for the creative_writer_cli project
# It clones the repository, sets up a temporary environment, runs the CLI, and cleans up.

REPO_URL="https://github.com/YOUR_GITHUB_USERNAME/creative_writer_cli_project_manager.git"
TEMP_DIR=$(mktemp -d)

echo "Cloning repository to temporary directory: $TEMP_DIR"
git clone "$REPO_URL" "$TEMP_DIR"

if [ $? -ne 0 ]; then
    echo "Error: Failed to clone repository."
    rm -rf "$TEMP_DIR"
    exit 1
fi

cd "$TEMP_DIR" || {
    echo "Error: Failed to change to temporary directory."
    rm -rf "$TEMP_DIR"
    exit 1
}

echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing creative_writer_cli..."
pip install .

if [ $? -ne 0 ]; then
    echo "Error: Failed to install creative_writer_cli."
    deactivate # Deactivate venv before cleanup
    rm -rf "$TEMP_DIR"
    exit 1
fi

echo "Starting Creative Writer CLI..."
creative-writer

# Deactivate virtual environment and clean up
deactivate
rm -rf "$TEMP_DIR"

echo "Cleanup complete."
