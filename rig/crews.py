from crewai import Crew, Process
from .agents import *
from .tasks import *


code_review_crew = Crew(
    agents=[senior_engineering_reviewer],
    tasks=[senior_engineering_reviewer_task],
    process=Process.sequential,
    memory=False,
    cache=False
)
dependency_crew = Crew(
    agents=[dependency_manifest_generator],
    tasks=[dependency_manifest_generator_task],
    process=Process.sequential,
    memory=False,
    cache=False
)
dock_crew = Crew(
    agents=[containerization_engineer],
    tasks=[containerization_engineer_task],
    process=Process.sequential,
    memory=False,
    cache=False
)

writer_crew = Crew(
    agents=[technical_writer],
    tasks=[technical_writer_task],
    process=Process.sequential,
    memory=False,
    cache=False
)
