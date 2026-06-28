from .crews import ( 
    code_review_crew,
    dependency_crew, 
    dock_crew,
    writer_crew)
from .router import COMMAND_MAP
from .tools import IGNORE_DIRS
import os

IGNORE_SUFFIXES = (".egg-info",)
SOURCE_EXTENSIONS = (".py", ".toml", ".cfg", ".ini", ".txt", ".md", ".json", ".yaml", ".yml")
MAX_FILE_SIZE = 20_000  # chars — skip files larger than this to avoid context overflow


def load_repo_files(repo_path: str) -> str:
    """Walk the repo and return all source file contents as a single string."""
    parts = []
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS
            and not any(d.endswith(s) for s in IGNORE_SUFFIXES)
        ]
        for filename in files:
            if not any(filename.endswith(ext) for ext in SOURCE_EXTENSIONS):
                continue
            full_path = os.path.join(root, filename)
            try:
                content = open(full_path, encoding="utf-8", errors="ignore").read()
                if len(content) > MAX_FILE_SIZE:
                    content = content[:MAX_FILE_SIZE] + "\n... [truncated]"
                parts.append(f"=== FILE: {full_path} ===\n{content}\n")
            except Exception:
                pass
    return "\n".join(parts) if parts else "No source files found."


def workflows(command, repo_path, review_context=None, dependency_context=None, docker_context=None):
    decision = COMMAND_MAP.get(command)

    if decision == "review":
        file_contents = load_repo_files(repo_path)
        return code_review_crew.kickoff({
            "repo_path": repo_path,
            "file_contents": file_contents
        })
    elif decision == "dependency":
        file_contents = load_repo_files(repo_path)
        return dependency_crew.kickoff({
            "repo_path": repo_path,
            "review_context": review_context or {},
            "file_contents": file_contents
        })
    elif decision == "docker":
        return dock_crew.kickoff({
            "repo_path": repo_path,
            "review_context": review_context or {},
            "dependency_context": dependency_context or {}
        })
    elif decision == "pipeline":
        return writer_crew.kickoff({
            "review_context": review_context or {},
            "dependency_context": dependency_context or {},
            "docker_context": docker_context or {}
        })
    return "Invalid command"
