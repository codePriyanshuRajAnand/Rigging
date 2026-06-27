from crewai import Crew, Process
from agents import *
from tasks import *

crew = Crew(
    agents=[
        input_manager,
        senior_engineering_reviewer,
        dependency_manifest_generator,
        containerization_engineer,
        end_to_end_orchestrator,
        technical_writer
    ],
    tasks=[
        router_task,
        senior_engineering_reviewer_task,
        dependency_manifest_generator_task,
        containerization_engineer_task,
        end_to_end_orchestrator_task,
        technical_writer_task
    ],
    process=Process.hierarchical,
    manager_agent=input_manager,
    verbose=True,
    cache=True,
    max_rpm=100,
    memory=True,
    share_crew=True
)