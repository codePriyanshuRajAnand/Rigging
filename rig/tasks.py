from crewai import Task
from .tools import *
from .agents import *


senior_engineering_reviewer_task = Task(
    description=(
        "Repository path: {repo_path}\n\n"
        "The full contents of every source file in the repository are provided below. "
        "You do NOT need to call any tools — all the code is already here.\n\n"
        "{file_contents}\n\n"
        "Analyze the code above and return a JSON report. "
        "Base your findings ONLY on what you can see in the file contents above. "
        "Do not invent function names, issues, or dependencies that are not visible."
    ),
    expected_output=(
        "Valid JSON with exactly these keys: "
        "project_type (string), "
        "entry_points (list of strings), "
        "architecture_summary (string), "
        "detected_stack (list of strings), "
        "business_logic_issues (list of {file, issue, severity}), "
        "configuration_issues (list of {file, issue, risk_level}), "
        "dependency_issues (list of {dependency, issue}), "
        "code_quality_issues (list of {file, issue}), "
        "missing_files (list of strings), "
        "risk_assessment ({overall_risk, reason}). "
        "No markdown, no extra text, just the JSON object."
    ),
    agent=senior_engineering_reviewer,
)


dependency_manifest_generator_task = Task(
    description=(
        "Repository path: {repo_path}\n"
        "Review context: {review_context}\n\n"
        "The full contents of every source file are provided below. "
        "You do NOT need to call any tools.\n\n"
        "{file_contents}\n\n"
        "From the file contents above, identify all import statements and existing manifest files. "
        "Build a complete dependency list and generate the correct manifest. Return as JSON."
    ),
    expected_output=(
        "Valid JSON with exactly these keys: "
        "languages (list), "
        "frameworks (list), "
        "dependencies (list of {name, version, source}), "
        "generated_manifests ({requirements.txt, package.json, go.mod, Cargo.toml} — null if not applicable), "
        "conflicts (list), "
        "unknowns (list). "
        "No markdown, no extra text, just the JSON object."
    ),
    agent=dependency_manifest_generator,
)


containerization_engineer_task = Task(
    description=(
        "Repository path: {repo_path}\n"
        "Review context: {review_context}\n"
        "Dependency context: {dependency_context}\n"
        "Use review_context to identify the runtime and entry point. "
        "Use dependency_context to determine installed packages and versions. "
        "Only call file_read_tool if the entry point is unclear from the context. "
        "Generate a production-ready Dockerfile and .dockerignore and return them as JSON."
    ),
    expected_output=(
        "Valid JSON with exactly these keys: "
        "dockerfile (string), "
        "dockerignore (string), "
        "base_image (string), "
        "entrypoint (string), "
        "ports (list of strings), "
        "build_strategy (single-stage or multi-stage), "
        "notes (list of strings). "
        "No markdown, no extra text, just the JSON object."
    ),
    agent=containerization_engineer,
    tools=[directory_read_tool, file_read_tool],
)


technical_writer_task = Task(
    description=(
        "You have three JSON reports to combine into documentation:\n"
        "Review: {review_context}\n"
        "Dependencies: {dependency_context}\n"
        "Docker: {docker_context}\n"
        "Do not call any tools. Just format the provided data into clean markdown documentation."
    ),
    expected_output=(
        "Markdown document with these sections: "
        "Project Summary, Architecture Overview, Security Findings, "
        "Dependency Report, Generated Files, Deployment (Docker), Final Recommendations."
    ),
    agent=technical_writer,
)
