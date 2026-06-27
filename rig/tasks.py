from crewai import Task
from tools import *
from agents import *

# define code base reviewer task

senior_engineering_reviewer_task = Task(
    description="""
Perform a full codebase analysis.

Repository Path:
{repo_path}

Steps:
1. Scan directory structure.
2. Identify entry points.
3. Analyze business logic correctness.
4. Detect syntax/structural issues.
5. Review architecture quality.
6. Identify security vulnerabilities.
7. Check for hardcoded secrets.
8. Validate dependencies and missing files:
   - package.json
   - requirements.txt
   - go.mod
   - Cargo.toml
   - Dockerfile (if exists)

Focus on correctness, security, and maintainability.
""",
    expected_output="""
Return ONLY valid JSON.

Schema:
{
  "executive_summary": "string",
  "architecture_review": {
    "design_quality": "string",
    "modularity": "string",
    "scalability": "string",
    "issues": ["string"]
  },
  "business_logic_issues": [
    {
      "file": "string",
      "issue": "string",
      "severity": "low | medium | high | critical"
    }
  ],
  "syntax_and_structural_issues": [
    {
      "file": "string",
      "error": "string"
    }
  ],
  "security_issues": [
    {
      "type": "string",
      "description": "string",
      "risk_level": "low | medium | high | critical"
    }
  ],
  "dependency_issues": [
    {
      "dependency": "string",
      "issue": "string"
    }
  ],
  "missing_files": ["string"],
  "risk_assessment": {
    "overall_risk": "low | medium | high | critical",
    "reason": "string"
  }
}
""",
    agent=senior_engineering_reviewer,
    tools=[directory_read_tool, file_read_tool]

)

# define dependency manifest generator task

dependency_manifest_generator_task = Task(
    description="""
    Analyze the codebase and generate missing dependency files.

    Repository Path:
    {repo_path}
    If previous analysis is provided, use it:
    {review_context}

    Otherwise perform fresh scan.

    Focus ONLY on dependency detection.

    Steps:
    1. Detect programming language(s).
    2. Scan imports and package usage.
    3. Identify missing dependencies.
    4. Generate or update:
    - requirements.txt OR pyproject.toml
    - package.json
    - go.mod
    - Cargo.toml
    - pom.xml / build.gradle (if applicable)
    5. Resolve version compatibility where possible.
    6. Avoid duplicates or conflicting dependencies.
    """,
    expected_output="""
Return ONLY valid JSON.

Schema:
{
  "detected_languages": ["string"],
  "frameworks": ["string"],
  "dependencies": [
    {
      "name": "string",
      "version": "string or null",
      "reason": "string"
    }
  ],
  "missing_manifest_files": ["string"],
  "generated_files": [
    {
      "file_name": "string",
      "content_summary": "string"
    }
  ],
  "conflicts": [
    {
      "dependency": "string",
      "issue": "string",
      "suggestion": "string"
    }
  ],
  "notes": ["string"]
}
""",
    agent=dependency_manifest_generator,
    tools=[directory_read_tool, file_read_tool]
)

containerization_engineer_task = Task(
    description="""
    Generate Docker configuration for the project.

    Repository Path:
    {repo_path}
    If previous analysis is provided, use it:
    {review_context}

    Otherwise perform fresh scan.

    Steps:
    1. Detect language and runtime.
    2. Identify entry point.
    3. Analyze project structure.
    4. Generate:
    - Dockerfile
    - .dockerignore
    5. Ensure:
    - minimal base image
    - multi-stage builds if needed
    - non-root execution
    - proper port exposure
    6. Optimize for production deployment.
    """,
       expected_output="""
Return ONLY valid JSON:

{
  "dockerfile": "string (full content)",
  "dockerignore": "string (full content)",
  "base_image": "string",
  "entrypoint": "string",
  "exposed_ports": ["string"],
  "notes": ["string"]
}
""",
    agent=containerization_engineer,
    tools=[directory_read_tool, file_read_tool]
)

technical_writer_task = Task(
    description="""
You will receive outputs from one or more agents.

User Input:{repo_path}
If previous analysis is provided, use it:
  {review_context}

Your job:
1. Combine all agent outputs.
2. Remove duplication.
3. Format into clean markdown.
4. Highlight:
   - critical issues
   - warnings
   - generated files
   - final summary
5. Ensure response is readable for developers.

DO NOT modify technical results.
DO NOT re-analyze code.
ONLY format and present.
""",
expected_output="""
Return a clean Markdown document.

Structure:
# Summary
# Findings (merged & deduplicated)
# Security Issues
# Architecture Notes
# Generated Files
# Warnings / Risks
# Final Recommendations

Rules:
- Do NOT modify technical outputs
- Do NOT re-analyze code
- Only format and organize provided data
- Must be readable for developers
""",
    agent=technical_writer
)