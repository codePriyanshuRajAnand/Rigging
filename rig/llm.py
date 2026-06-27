from crewai import LLM

# use whatever llm you want to, if you want to use any other llm use crewai llm documentation and create a instance of llm in this file and update 'llm' parameter in agents.py

OLLAMA_URL = "http://localhost:11434"

# gemini 

gemini_llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key="<YOUR_API_KEY>",
    temperature=0.2,
    max_tokens=2048
)

# base llm

llm = LLM(
    model="ollama/gemma4:e4b",
    base_url=OLLAMA_URL,
    temperature=0.2,
    max_tokens=2048
)

# defining agent based llm

router_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.0,
    base_url=OLLAMA_URL,
    max_tokens=300
)

review_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.1,
    base_url=OLLAMA_URL,
    max_tokens=2500
)


dependency_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.1,
    base_url=OLLAMA_URL,
    max_tokens=1800
)

docker_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.05,
    base_url=OLLAMA_URL,
    max_tokens=1500
)
orchestrator_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.0,
    base_url=OLLAMA_URL,
    max_tokens=500
)
writer_llm = LLM(
    model="ollama/gemma4:e4b",
    temperature=0.2,
    base_url=OLLAMA_URL,
    max_tokens=3000
)