from google.adk.agents import LlmAgent
from google.adk.tools import preload_memory, load_memory

from app import config

MEMORY_AGENT_INSTRUCTION = """
You are a memory test agent.

Your job:
- If the user asks you to remember, store, save, or memorize a fact, use the available memory tool.
- If the user asks what you remember, use the available memory retrieval tool.
- Never say you cannot remember if memory tools are available.
- Confirm when a fact has been stored.
- Answer with stored facts when memory is retrieved.
"""

memory_agent = LlmAgent(
    name="memory_agent",
    model=config.DEFAULT_LLM_MODEL,
    description="Agent for testing Vertex AI Memory Bank.",
    instruction=MEMORY_AGENT_INSTRUCTION,
    tools=[preload_memory, load_memory],
)