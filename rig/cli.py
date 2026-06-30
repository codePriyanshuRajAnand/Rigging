import typer
from rig import worklfows
import os, json


def safe_json(data):
    try:
        return json.loads(data)
    except Exception:
        return {"raw": str(data)}

def docker_steps(path, result):
    docker_file = "Dockerfile"
    docker_ignore = ".dockerignore"
    
    # Bugfix: If the path is a file, get its directory
    
    if os.path.isfile(path):
        path = os.path.dirname(path)
    
    # Bugfix: Check if Dockerfile or .dockerignore already exists in the path
    
    if os.path.exists(os.path.join(path, 'Dockerfile')) or os.path.exists(os.path.join(path, '.dockerignore')):
        print("Dockerfile or .dockerignore already exists. Creating as Dockerfile.new and .dockerignore.new")
        docker_file = "Dockerfile.new"
        docker_ignore = ".dockerignore.new"
        
    docker_file = os.path.join(path, docker_file)
    docker_ignore = os.path.join(path, docker_ignore)
    with open(docker_file, 'w') as f:
        f.write(result["dockerfile"])
    with open(docker_ignore, 'w') as f:
        f.write(result["dockerignore"])
    print(f"Dockerfile created at: {docker_file}")
    print(f"Docker ignore created at: {docker_ignore}")
    print(f"Base image: {result['base_image']}")
    print(f"Entry point: {result['entrypoint']}")
    print(f"Exposed ports: {result.get('ports', [])}")

app = typer.Typer()

@app.command()
def scan(path: str):
    result = worklfows.workflows('scan', path)
    print(result)

@app.command()
def supply(path: str):
    review = worklfows.workflows('scan', path)
    review_context = safe_json(review.raw)
    result = worklfows.workflows('supply', path, review_context=review_context)
    print(result)

@app.command()
def dock(path: str):
    review = worklfows.workflows('scan', path)
    review_context = safe_json(review.raw)
    supply = worklfows.workflows('supply', path, review_context=review_context)
    dependency_context = safe_json(supply.raw)
    result = worklfows.workflows('dock', path, review_context=review_context, dependency_context=dependency_context)
    parsed = safe_json(result.raw)
    docker_steps(path, parsed)
    print(parsed.get("notes", []))

@app.command()
def full(path: str):
    review = worklfows.workflows('scan', path)
    review_context = safe_json(review.raw)
    supply = worklfows.workflows('supply', path, review_context=review_context)
    dependency_context = safe_json(supply.raw)
    dock = worklfows.workflows('dock', path, review_context=review_context, dependency_context=dependency_context)
    docker_steps(path, safe_json(dock.raw))
    docker_context = safe_json(dock.raw)
    result = worklfows.workflows('full', path, review_context=review_context, dependency_context=dependency_context, docker_context=docker_context)
    print(result)

if __name__ == "__main__":
    app()