from .crews import ( 
    code_review_crew,
    dependency_crew, 
    dock_crew,
    writer_crew)
from .router import COMMAND_MAP

def workflows(command, repo_path, review_context=None):
    decision = COMMAND_MAP.get(command) 
    
    if decision == "dependency":
        return dependency_crew.kickoff({"repo_path": repo_path, "review_context": review_context})
    elif decision == "dock":
        return dock_crew.kickoff({"repo_path": repo_path, "review_context": review_context})
    elif decision == "review":
        return code_review_crew.kickoff({"repo_path": repo_path})
    elif decision == "write":
        return writer_crew.kickoff({"repo_path": repo_path, "review_context": review_context})
    return "Invalid command"
