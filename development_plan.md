**Development Plan: Convert to Python Package**

**Goal:** Transform the current CLI application into a distributable Python package, enabling installation via `pip` and easier sharing.

**1. Project Setup for Packaging:**
    *   **`pyproject.toml` (Modern Packaging Standard):** Create a `pyproject.toml` file at the root of the project. This file will define project metadata, dependencies, and build system. This is the preferred modern approach over `setup.py` and `setup.cfg`.
        *   Define `[project]` section: `name`, `version`, `description`, `readme`, `requires-python`, `dependencies`, `authors`, `keywords`, `classifiers`.
        *   Define `[build-system]` to specify `setuptools` or `hatchling` as the backend. `setuptools` is a common choice.
    *   **`src/` Layout:** Ensure the project adheres to the `src/` layout (which it already does, with `src/creative_writer_cli`). This is a best practice for packaging.

**2. Refine `creative_writer_cli` Module:**
    *   **`__init__.py` files:** Ensure all subdirectories within `src/creative_writer_cli` (e.g., `data`, `ui`, `utils`, `core`, `data/repositories`, `ui/display`, `ui/wizards`) have `__init__.py` files to mark them as Python packages. (Already present based on previous `list_directory` outputs).
    *   **Main Entry Point:** The `main.py` file in `src/main.writer_cli.cli.py` and its main function should be exposed for the `[project.scripts]` entry point. I'll choose `src/creative_writer_cli/cli.py` and update `main.py` to call it.

**3. Dependency Management:**
    *   **`requirements.txt` to `pyproject.toml`:** Migrate all dependencies from `requirements.txt` to the `dependencies` list in `pyproject.toml`. `requirements.txt` can then be used for development environment setup (e.g., `pip install -r requirements.txt` after `pip install .`).
    *   **Pinning Versions:** Consider pinning exact versions for dependencies in `pyproject.toml` for reproducibility, especially for a distributable package.

**4. Testing (Pre-packaging):**
    *   **Unit Tests:** If not already present, write unit tests for core functionalities (e.g., `JsonStore`, `ProjectRepository`, `word_counter`). This is crucial for maintaining code quality and ensuring the package works as expected after refactoring.
    *   **Test Runner:** Identify or set up a test runner (e.g., `pytest`).

**5. Build and Distribution:**
    *   **Build Wheel and Source Distribution:** Use `build` (or `setuptools` directly) to create a wheel (`.whl`) and a source distribution (`.tar.gz`).
        *   `python -m build`
    *   **Local Installation Test:** Install the package locally using `pip install .` (from the project root) or `pip install dist/*.whl` to verify installation and functionality.
    *   **`run.sh` Update:** Modify `run.sh` to install the package locally and then run the CLI entry point.

**6. Documentation and Metadata:**
    *   **`README.md`:** Ensure `README.md` is up-to-date with installation instructions for the package (using `pip`).
    *   **License:** Confirm the `LICENSE` file is present and correctly referenced in `pyproject.toml`. **SUCCESS**
    *   **`CHANGELOG.md` (Optional but Recommended):** Start a `CHANGELOG.md` to track changes for future releases.

**7. Version Control:**
    *   **Git Tagging:** Use Git tags for releases (e.g., `git tag v1.0.0`).

**Detailed Steps & Commands:**

*   **Create `pyproject.toml`:**
    ```toml
    [project]
    name = "creative-writer-cli"
    version = "0.1.0"
    description = "A minimalistic CLI tool for creative writing project management."
    readme = "README.md"
    requires-python = ">=3.8"
    license = { file = "LICENSE" }
    authors = [
        { name = "Daniel Wieser", email = "your.email@example.com" } # Replace with actual author info
    ]
    keywords = ["cli", "writing", "project-management", "creative"]
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Assuming MIT based on LICENSE file
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Text Processing :: General",
    ]
    dependencies = [
        "markdown-it-py==3.0.0",
        "mdurl==0.1.2",
        "prompt_toolkit==3.0.51",
        "Pygments==2.19.2",
        "questionary==2.1.0",
        "rich==14.0.0",
        "wcwidth==0.2.13",
        "requests",
    ]

    [project.scripts]
    creative-writer = "creative_writer_cli.cli:main" # New entry point

    [build-system]
    requires = ["setuptools>=61.0"]
    build-backend = "setuptools.build_meta"
    ```

*   **Move `main.py`:**
    *   Rename `src/main.py` to `src/creative_writer_cli/cli.py`.
    *   Modify `src/creative_writer_cli/cli.py` to have a `main()` function that contains the CLI application logic.

*   **Update `run.sh`:**
    ```bash
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
    pip install -e .

    # Run the CLI application
    echo "Starting Creative Writer CLI..."
    creative-writer
    ```

*   **Remove `requirements.txt` (Optional, but good practice once dependencies are in `pyproject.toml`):**
    *   `rm requirements.txt`

**Detailed Plan for Improving Distribution and Ease of Use**

To make your `creative_writer_cli` project as accessible and easy to run as possible, here's a multi-pronged approach:

#### 1. Publish to PyPI (Python Package Index) - The Standard Way:

This is the most crucial step for broad distribution. Once on PyPI, users can simply `pip install` your package.

*   **Action:**
    *   **Register on PyPI:** SUCCESS
    *   **Build Distribution Files:** SUCCESS
    *   **Upload to TestPyPI (First):** SUCCESS
    *   **Upload to PyPI (Once confident):** SUCCESS

#### 2. Recommend `pipx` - The Python Equivalent of `npx`:

`pipx` is a fantastic tool specifically designed for installing and running Python applications in isolated environments, much like `npx` for Node.js. It's ideal for CLI tools.

*   **Action:**
    *   **Add `pipx` to your `README.md`'s installation instructions.** SUCCESS

#### 3. Improve GitHub README for Direct Git Installation:

Even with PyPI, some users might prefer to install directly from your GitHub repository.

*   **Action:**
    *   **Update `README.md`:** Clearly show how to install directly from Git. SUCCESS

#### 4. Continuous Integration/Deployment (CI/CD) for Automation:

To streamline the process of publishing new versions, set up CI/CD.

*   **Action:**
    *   **GitHub Actions (Recommended):** Create a GitHub Actions workflow (`.github/workflows/publish.yml`) that automatically runs tests and, upon a new tag or release, builds and uploads your package to PyPI. SUCCESS

#### 5. One-Liner Execution from GitHub:

*   **Action:**
    *   **Create `run_from_github.sh` script:** This script will allow users to run the CLI directly from GitHub with a single command.
    *   **Update `README.md`:** Add instructions for using the `run_from_github.sh` script. SUCCESS
*   **Benefits:**
    *   Provides a quick and easy way for users to try out the CLI without a full installation.
    *   Mirrors the `npx` experience for Python projects.

*   **Automated testing ensures quality.
*   Automated publishing reduces manual effort and errors.
*   Automated publishing reduces manual effort and errors.
*   Users get access to the latest versions quickly.