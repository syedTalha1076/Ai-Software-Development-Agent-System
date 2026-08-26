from langchain_core.tools import tool
from pathlib import Path
import subprocess
import os


# ============================================================
# PROJECT WORKSPACE
# ============================================================

PROJECT_ROOT = Path("generated_projects").resolve()

PROJECT_ROOT.mkdir(parents=True, exist_ok=True)


def safe_path(path: str) -> Path:
    """
    Convert a relative project path into a safe absolute path.

    This prevents the agent from accessing files outside
    the generated project workspace.
    """

    target = (PROJECT_ROOT / path).resolve()

    if not str(target).startswith(str(PROJECT_ROOT)):
        raise ValueError("Access denied: path is outside project workspace.")

    return target


# ============================================================
# 1. CREATE FILE
# ============================================================

@tool
def create_file(path: str, content: str) -> str:
    """
    Create a new file inside the project workspace.

    Args:
        path: Relative path of the file.
        content: Content to write into the file.

    Example:
        create_file(
            "app/main.py",
            "print('Hello World')"
        )
    """

    try:

        file_path = safe_path(path)

        # Create parent directories
        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Prevent accidental overwrite
        if file_path.exists():
            return f"File already exists: {path}"

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return f"File created successfully: {path}"

    except Exception as e:
        return f"Error creating file: {str(e)}"


# ============================================================
# 2. READ FILE
# ============================================================

@tool
def read_file(path: str) -> str:
    """
    Read the contents of a project file.
    """

    try:

        file_path = safe_path(path)

        if not file_path.exists():
            return f"File does not exist: {path}"

        if not file_path.is_file():
            return f"Path is not a file: {path}"

        content = file_path.read_text(
            encoding="utf-8"
        )

        return content

    except Exception as e:
        return f"Error reading file: {str(e)}"


# ============================================================
# 3. UPDATE FILE
# ============================================================

@tool
def update_file(path: str, content: str) -> str:
    """
    Replace the entire contents of an existing file.

    The Developer Agent can use this tool when fixing code.
    """

    try:

        file_path = safe_path(path)

        if not file_path.exists():
            return f"File does not exist: {path}"

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return f"File updated successfully: {path}"

    except Exception as e:
        return f"Error updating file: {str(e)}"


# ============================================================
# 4. DELETE FILE
# ============================================================

@tool
def delete_file(path: str) -> str:
    """
    Delete a file from the project workspace.
    """

    try:

        file_path = safe_path(path)

        if not file_path.exists():
            return f"File does not exist: {path}"

        if not file_path.is_file():
            return f"Path is not a file: {path}"

        file_path.unlink()

        return f"File deleted successfully: {path}"

    except Exception as e:
        return f"Error deleting file: {str(e)}"


# ============================================================
# 5. LIST PROJECT FILES
# ============================================================

@tool
def list_files(directory: str = "") -> str:
    """
    List files and directories inside the project workspace.

    Example:
        list_files("")
        list_files("app")
    """

    try:

        directory_path = safe_path(directory)

        if not directory_path.exists():
            return f"Directory does not exist: {directory}"

        items = []

        for item in directory_path.rglob("*"):

            relative_path = item.relative_to(PROJECT_ROOT)

            if item.is_dir():
                items.append(f"[DIR]  {relative_path}")
            else:
                items.append(f"[FILE] {relative_path}")

        if not items:
            return "Directory is empty."

        return "\n".join(items)

    except Exception as e:
        return f"Error listing files: {str(e)}"


# ============================================================
# 6. RUN PYTHON FILE
# ============================================================

@tool
def run_python(path: str) -> str:
    """
    Run a Python file inside the project workspace.

    Example:
        run_python("app/main.py")
    """

    try:

        file_path = safe_path(path)

        if not file_path.exists():
            return f"File does not exist: {path}"

        if file_path.suffix != ".py":
            return "Only Python files can be executed."

        result = subprocess.run(
            ["python", str(file_path)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = ""

        if result.stdout:
            output += f"STDOUT:\n{result.stdout}\n"

        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"

        output += f"\nReturn code: {result.returncode}"

        return output

    except subprocess.TimeoutExpired:
        return "Execution stopped: program exceeded 30 seconds."

    except Exception as e:
        return f"Error running Python file: {str(e)}"


# ============================================================
# 7. RUN PYTEST
# ============================================================

@tool
def run_tests() -> str:
    """
    Run pytest on the generated project.
    """

    try:

        result = subprocess.run(
            ["pytest", "-v"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120
        )

        output = ""

        if result.stdout:
            output += result.stdout

        if result.stderr:
            output += "\nERRORS:\n"
            output += result.stderr

        output += f"\n\nReturn code: {result.returncode}"

        if result.returncode == 0:
            output += "\n\nTEST RESULT: PASSED"
        else:
            output += "\n\nTEST RESULT: FAILED"

        return output

    except subprocess.TimeoutExpired:
        return "Testing stopped: pytest exceeded 120 seconds."

    except Exception as e:
        return f"Error running tests: {str(e)}"


# ============================================================
# 8. RUN RUFF
# ============================================================

@tool
def run_ruff() -> str:
    """
    Run Ruff code quality checks on the generated project.
    """

    try:

        result = subprocess.run(
            ["ruff", "check", "."],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=60
        )

        output = ""

        if result.stdout:
            output += result.stdout

        if result.stderr:
            output += "\nERRORS:\n"
            output += result.stderr

        output += f"\n\nReturn code: {result.returncode}"

        if result.returncode == 0:
            output += "\n\nCODE REVIEW: PASSED"
        else:
            output += "\n\nCODE REVIEW: ISSUES FOUND"

        return output

    except Exception as e:
        return f"Error running Ruff: {str(e)}"


# ============================================================
# 9. GIT STATUS
# ============================================================

@tool
def git_status() -> str:
    """
    Show the current Git status of the generated project.
    """

    try:

        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )

        return result.stdout or "Working tree is clean."

    except Exception as e:
        return f"Git error: {str(e)}"


# ============================================================
# 10. GIT DIFF
# ============================================================

@tool
def git_diff() -> str:
    """
    Show changes made to the generated project.
    """

    try:

        result = subprocess.run(
            ["git", "diff"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )

        return result.stdout or "No changes detected."

    except Exception as e:
        return f"Git diff error: {str(e)}"


# ============================================================
# 11. GIT COMMIT
# ============================================================

@tool
def git_commit(message: str) -> str:
    """
    Commit current project changes to Git.

    Example:
        git_commit("Add student API")
    """

    try:

        # Add changes
        subprocess.run(
            ["git", "add", "."],
            cwd=PROJECT_ROOT,
            check=True
        )

        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )

        return (
            f"Git commit result:\n"
            f"{result.stdout}\n"
            f"{result.stderr}"
        )

    except Exception as e:
        return f"Git commit error: {str(e)}"