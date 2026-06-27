from crewai import Task
from tools import *
from agents import *

# Define the router task that will analyze user input and determine the appropriate agents to execute based on the request and repository context.

router_task = Task(
    description="""
    You are given a user request and repository context.

    User Input:
    {user_input}

    Repository Path:
    {repo_path}

    Your job:
    1. Understand user intent.
    2. Decide which agent(s) should be executed:
    - Agent 1: Code validation / review
    - Agent 2: Dependency / manifest generation
    - Agent 3: Docker / containerization
    - Agent 4: Full pipeline execution
    3. Validate if input is sufficient.
    4. If unclear, request clarification.
    5. Output a structured execution plan ONLY.

    DO NOT perform any code analysis or generate outputs.
    DO NOT format final user response.
    """,
        expected_output="""
    A structured plan:
    - intent
    - selected agent(s)
    - execution order
    - required inputs
    - missing information (if any)
""",
    agent=None
)


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
Structured report:
- Executive Summary
- Architecture Review
- Business Logic Issues
- Syntax/Structural Issues
- Security Issues
- Dependency Issues
- Missing Files
- Risk Assessment
""",
    agent=None
)

# define dependency manifest generator task

dependency_manifest_generator_task = Task(
    description="""
    Analyze the codebase and generate missing dependency files.

    Repository Path:
    {repo_path}

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
    - Detected languages
    - Frameworks
    - Dependency list
    - Generated/updated manifest files
    - Version notes
    - Warnings or conflicts
""",
    agent=None
)

containerization_engineer_task = Task(
    description="""
    Generate Docker configuration for the project.

    Repository Path:
    {repo_path}

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
    - Dockerfile
    - .dockerignore
    - Build instructions
    - Runtime notes
""",
    agent=None
)

end_to_end_orchestrator_task = Task(
    description="""
Execute full end-to-end project preparation.

Repository Path:
{repo_path}

You must:
1. Run full code validation (senior_engineering_reviewer agent)
2. Generate missing dependencies (dependency_manifest_generator agent)
3. Generate Docker setup (containerization_engineer agent)
4. Ensure outputs are consistent across steps
5. Consolidate results

This is a sequential pipeline.
""",
    expected_output="""
- Validation Report
- Dependency Report
- Docker Files
- Final Readiness Summary
""",
    agent=None
)


technical_writer_task = Task(
    description="""
You will receive outputs from one or more agents.

User Input:
{user_input}

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
A clean structured markdown report:
- Summary
- Findings
- Generated Files
- Issues
- Recommendations
""",
    agent=None
)