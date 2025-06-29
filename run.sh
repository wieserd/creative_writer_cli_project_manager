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
    echo -n "Initializing... "
    # Redirect pip install output to a temporary file
    LOG_FILE=$(mktemp)
    "$VENV_PATH/bin/pip" install -r "$SCRIPT_DIR/requirements.txt" > "$LOG_FILE" 2>&1
    PIP_STATUS=$?

    if [ $PIP_STATUS -ne 0 ]; then
        echo "Failed."
        echo "Initialization failed. Showing logs:"
        cat "$LOG_FILE"
        rm "$LOG_FILE"
        exit $PIP_STATUS
    else
        echo "Done."
        rm "$LOG_FILE"
    fi
fi

# Run the main application
python "$SCRIPT_DIR/src/main.py"