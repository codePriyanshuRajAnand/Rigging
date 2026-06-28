from crewai_tools import FileReadTool, FileWriterTool
from crewai.tools import BaseTool
from pydantic import BaseModel
import os

# Directories to always exclude from directory listing
IGNORE_DIRS = {
    "__pycache__", ".venv", "venv", "env", ".git", ".hg", ".svn",
    "node_modules", "dist", "build", ".mypy_cache", ".pytest_cache",
    ".ruff_cache", ".tox", "htmlcov", "site-packages", ".eggs",
}

IGNORE_SUFFIXES = (".egg-info",)


class DirectoryReadSchema(BaseModel):
    directory: str


class FilteredDirectoryReadTool(BaseTool):
    name: str = "directory_read_tool"
    description: str = (
        "Lists all files in a directory recursively, "
        "excluding build artifacts, caches, and virtual environments."
    )
    args_schema: type[BaseModel] = DirectoryReadSchema

    def _run(self, directory: str) -> str:
        directory = directory.rstrip("/\\")
        files_list = []
        for root, dirs, files in os.walk(directory):
            # Prune ignored directories in-place so os.walk doesn't descend into them
            dirs[:] = [
                d for d in dirs
                if d not in IGNORE_DIRS
                and not any(d.endswith(s) for s in IGNORE_SUFFIXES)
            ]
            for filename in files:
                full_path = os.path.join(root, filename)
                rel_path = full_path.replace(directory, "").lstrip(os.sep)
                files_list.append(f"{directory}/{rel_path}")

        if not files_list:
            return "No files found."
        return "File paths:\n- " + "\n- ".join(files_list)


directory_read_tool = FilteredDirectoryReadTool()
file_read_tool = FileReadTool()
file_writer = FileWriterTool()