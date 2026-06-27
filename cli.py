import typer
from rig import worklfows
import os

def docker_steps(path, result):
    docker_file = os.path.join(path, 'Dockerfile')
    docker_ignore = os.path.join(path, '.dockerignore')
    with open(docker_file, 'w') as f:
        f.write(result["dockerfile"])
    with open(docker_ignore, 'w') as f:
        f.write(result["dockerignore"])
    print(f"Dockerfile created at: {docker_file}")
    print(f"Docker ignore created at: {docker_ignore}")
    print(f"Base image: {result['base_image']}")
    print(f"Entry point: {result['entrypoint']}")
    print(f"Exposed Port: {result['exposed_ports']}")

app = typer.Typer()

@app.command()
def scan(path: str):
    result = worklfows.workflows('scan', path)
    print(result)

@app.command()
def supply(path: str):
    result = worklfows.workflows('supply', path)
    print(result)

@app.command()
def dock(path: str):
    result = worklfows.workflows('dock', path)
    docker_steps(path, result)
    print(f"result['notes]")

@app.command()
def full(path: str):
    review = worklfows.workflows('scan', path)
    supply = worklfows.workflows('supply', path, review_context=review)
    dock = worklfows.workflows('dock', path, review_context=[review, supply])
    docker_steps(path, dock)
    result = worklfows.workflows('write', path, review_context=[review, supply, dock])
    print(result)

if __name__ == "__main__":
    app()