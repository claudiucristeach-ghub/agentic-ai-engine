from google.adk.agents import LlmAgent

from app import config
from app.agent_repo.critique_agent.prompt import (
    CRITIQUE_AGENT_INSTRUCTION,
)

critique_agent = LlmAgent(
    name="critique_agent",
    model=config.DEFAULT_LLM_MODEL,
    description=(
        "Evaluates outputs from other agents.\n\n"
        "How to use:\n"
        "1 Paste output from another agent\n"
        "2 Ask for evaluation\n"
        "3 Review accuracy and hallucination risk\n\n"
        "Example:\n"
        "Evaluate this Tennis Team output."
    ),
    instruction=CRITIQUE_AGENT_INSTRUCTION,
)