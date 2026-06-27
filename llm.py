from crewai import LLM

# base llm

llm = LLM(
    model="ollama/gemma4:e4b",
    base_url="http://localhost:11434",
    temperature=0.2,
    max_tokens=2048
)

# defining agent based llm

router_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.0,
    max_tokens=300
)

review_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.1,
    max_tokens=2500
)


dependency_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.1,
    max_tokens=1800
)

docker_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.05,
    max_tokens=1500
)
orchestrator_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.0,
    max_tokens=500
)
writer_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.2,
    max_tokens=3000
)