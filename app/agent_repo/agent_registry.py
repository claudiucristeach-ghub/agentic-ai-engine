"""Agent registry – maps agent_id to LlmAgent instances and display metadata.

To add a new agent:
  1. Create a new sub-package under agent_repo/
  2. Import the agent here
  3. Add an entry to AGENT_REGISTRY
"""

from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

from app.agent_repo.greeting_agent import greeting_agent
from app.agent_repo.summarizer_agent import summarizer_agent
from app.agent_repo.memory_agent import memory_agent
from app.agent_repo.tennis_agent_team import tennis_agent_team
from app.agent_repo.critique_agent import critique_agent

try:
    from google.adk.tools import preload_memory, load_memory
    _MEMORY_TOOLS = {preload_memory, load_memory}
except ImportError:
    _MEMORY_TOOLS = set()


AGENT_REGISTRY: dict[str, dict] = {
    "greeting_agent": {
        "agent": greeting_agent,
        "label": "Welcome",
        "description": "Welcomes students and helps them get started.",
        "icon": "👋",
    },
    "summarizer_agent": {
        "agent": summarizer_agent,
        "label": "Summarizer",
        "description": "Summarizes pasted text and uploaded documents.",
        "icon": "📝",
    },
    "memory_agent": {
        "agent": memory_agent,
        "label": "Memory",
        "description": "Tests Vertex AI Memory Bank.",
        "icon": "🧠",
    },
    "tennis_agent_team": {
        "agent": tennis_agent_team,
        "label": "Tennis Team",
        "description": (
            "Tennis analysis agent team with summary, "
            "mental, tactical and action plan."
        ),
        "icon": "🎾",
    },
    "critique_agent": {
        "agent": critique_agent,
        "label": "Critique",
        "description": "Evaluates outputs and detects issues.",
        "icon": "🧐",
    },
}


def get_agent(agent_id: str) -> LlmAgent:
    """Look up an agent by ID. Raises KeyError if not found."""
    entry = AGENT_REGISTRY[agent_id]
    return entry["agent"]


def list_agents() -> list[dict]:
    """Return metadata for all registered agents (for the UI)."""
    return [
        {
            "id": agent_id,
            "label": meta["label"],
            "description": meta["description"],
            "icon": meta["icon"],
            "has_tools": bool(getattr(meta["agent"], "tools", None)),
            "has_memory": has_memory_tools(meta["agent"]),
        }
        for agent_id, meta in AGENT_REGISTRY.items()
    ]


def has_memory_tools(agent: LlmAgent) -> bool:
    """Check whether *agent* has any memory tools."""
    for tool in getattr(agent, "tools", []) or []:
        if tool in _MEMORY_TOOLS:
            return True
    return False