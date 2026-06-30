from crewai import LLM
import os

# Set OPENROUTER_API_KEY in your environment before running:
# $env:OPENROUTER_API_KEY = "sk-or-v1-..."
# OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# if not OPENROUTER_API_KEY:
#     raise EnvironmentError(
#         "OPENROUTER_API_KEY is not set. "
#         "Run: $env:OPENROUTER_API_KEY = 'sk-or-v1-...' in your terminal before using rig."
#     )

# # =============================================================================
# # ACTIVE: OpenRouter LLMs
# # =============================================================================

# # Heavy reasoning model — used for codebase review
# review_llm = LLM(
#     model="openrouter/meta-llama/llama-3.2-3b-instruct:free",
#     api_key=OPENROUTER_API_KEY,
#     temperature=0.1,
#     max_tokens=8192,
# )

# # Faster/cheaper model — used for dependency, docker, writer tasks
# deepseek_chat_llm = LLM(
#     model="openrouter/deepseek/deepseek-chat",
#     api_key=OPENROUTER_API_KEY,
#     temperature=0.1,
#     max_tokens=4096,
# )

# dependency_llm   = deepseek_chat_llm
# docker_llm       = deepseek_chat_llm
# writer_llm       = deepseek_chat_llm
# router_llm       = deepseek_chat_llm
# orchestrator_llm = deepseek_chat_llm


# =============================================================================
# INACTIVE: Local Ollama LLMs (qwen2.5-coder:7b-instruct-q4_K_M)
# To switch back: comment out the OpenRouter section above and uncomment below.
# Requires Ollama running at localhost:11434 with the model pulled.
# Note: use provider="litellm" to force LiteLLM's ollama/ path — CrewAI's
# native OpenAI-compatible provider uses /v1 which breaks tool_calls for Ollama.
# =============================================================================

OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "ollama/llama3.2"

review_llm = LLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.1,
    max_tokens=8192,
    provider="litellm"
)

dependency_llm = LLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.1,
    max_tokens=4096,
    provider="litellm"
)

docker_llm = LLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.05,
    max_tokens=4096,
    provider="litellm"
)

writer_llm = LLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.2,
    max_tokens=3000,
    provider="litellm"
)

router_llm = LLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.0,
    max_tokens=300,
    provider="litellm"
)

orchestrator_llm = LLM(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_URL,
    temperature=0.0,
    max_tokens=500,
    provider="litellm"
)


# =============================================================================
# INACTIVE: Gemini (requires GEMINI_API_KEY)
# =============================================================================

# gemini_llm = LLM(
#     model="gemini/gemini-2.0-flash",
#     api_key=os.environ.get("GEMINI_API_KEY", ""),
#     temperature=0.2,
#     max_tokens=2048
# )
