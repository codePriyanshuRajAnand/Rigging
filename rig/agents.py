from crewai import Agent
from .tools import file_writer, directory_read_tool, file_read_tool
from .llm import review_llm, dependency_llm, docker_llm, writer_llm


senior_engineering_reviewer = Agent(
    name="Senior Engineering Reviewer",
    role="Senior software engineer who reviews codebases for bugs, quality problems, and architectural issues.",
    goal="Analyze the provided source code and return a JSON report covering architecture, business logic, code quality, dependencies, and configuration issues.",
    backstory="You are an experienced software engineer who audits codebases. You analyze code provided to you and give precise, evidence-based findings.",
    verbose=True,
    memory=False,
    max_iter=3,
    respect_context_window=True,
    llm=review_llm,
    allow_delegation=False
)

dependency_manifest_generator = Agent(
    name="Dependency & Manifest Generator",
    role="Dependency analyst who identifies project dependencies and generates manifest files.",
    goal="Use the provided source code to identify all imports and produce accurate dependency manifests.",
    backstory="You are a build engineer who specializes in dependency resolution across Python, Node, Go, Rust, and Java ecosystems.",
    verbose=True,
    memory=False,
    max_iter=3,
    respect_context_window=True,
    llm=dependency_llm,
    allow_delegation=False
)

containerization_engineer = Agent(
    name="Containerization Engineer",
    role="DevOps engineer who generates production-ready Docker configuration for applications.",
    goal="Use the review and dependency context to produce an optimized Dockerfile and .dockerignore.",
    backstory="You are a DevOps engineer with deep Docker expertise. You build minimal, secure container images tailored to the detected stack.",
    verbose=True,
    memory=False,
    max_iter=5,
    respect_context_window=True,
    llm=docker_llm,
    tools=[directory_read_tool, file_read_tool, file_writer],
    allow_delegation=False
)

technical_writer = Agent(
    name="Technical Writer",
    role="Technical writer who produces developer documentation from structured analysis data.",
    goal="Combine the review, dependency, and Docker context into clean markdown documentation.",
    backstory="You are a technical writer who turns structured JSON reports into clear, well-organized developer docs.",
    verbose=True,
    memory=False,
    max_iter=3,
    respect_context_window=True,
    llm=writer_llm,
    allow_delegation=False
)
