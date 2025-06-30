**Revised Development Plan: Code Refactoring for Robustness and Modularity**

**Goal:** Improve the project's code structure, readability, and maintainability by refactoring large files and logically grouping functionalities into more focused modules.

**Phase 1: Refactor `CLIApp` and UI Logic**

*   **1.1 Create `src/creative_writer_cli/ui/services/` directory:** This directory will house new service classes that encapsulate complex UI interaction logic, reducing the burden on `CLIApp`.
*   **1.2 Create `src/creative_writer_cli/ui/services/project_interaction_service.py`:**
    *   Move the `project_menu`, `rename_project`, `view_edit_sections`, `export_project_menu`, `edit_section`, and `export_references_menu` methods from `CLIApp` into a new `ProjectInteractionService` class.
    *   This service will take `project_repository` and `console` as dependencies.
    *   `CLIApp` will then instantiate and delegate to this service.
*   **1.3 Update `src/creative_writer_cli/ui/cli_app.py`:**
    *   Import the new `ProjectInteractionService`.
    *   Modify `CLIApp` to instantiate `ProjectInteractionService` and call its methods.
    *   Keep `main_menu`, `create_project`, `view_projects`, `delete_project`, and `_configure_project_directory` in `CLIApp` as they represent the top-level application flow.
*   **1.4 Refactor `edit_section` logic (within `ProjectInteractionService`):**
    *   The `edit_section` method is still quite large due to the many `if/elif` blocks for different section types. Consider creating a `SectionEditor` class or a dictionary of handlers for each section type to further modularize this. (This might be a follow-up refactoring if the initial move is too large).

**Phase 2: Review and Refactor Other Modules (if necessary)**

*   **2.1 Review `src/creative_writer_cli/data/repositories/`:** Ensure `json_store.py` and `project_repository.py` are focused on their single responsibilities. (Already done in previous steps).
*   **2.2 Review `src/creative_writer_cli/ui/display/`:** Ensure display functions are purely for rendering and don't contain interaction logic.
*   **2.3 Review `src/creative_writer_cli/ui/wizards/`:** Ensure wizard functions are purely for input gathering and validation.
*   **2.4 Review `src/creative_writer_cli/utils/`:** Ensure utility functions are generic and reusable.

**Phase 3: Update Imports and Test**

*   **3.1 Update all necessary import statements** in affected files.
*   **3.2 Run existing unit tests** to ensure no regressions.
*   **3.3 Manually test the application** to verify all functionalities.

**Phase 4: Update Documentation**

*   **4.1 Update `README.md`:** Reflect the new project structure.
*   **4.2 Update `development_plan.md`:** Mark steps as SUCCESS.
