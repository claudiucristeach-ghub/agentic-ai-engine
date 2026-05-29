from google.adk.agents import LlmAgent

from app import config
from app.context.artifacts.artifact_tools import save_markdown_artifact, load_artifact

ARTIFACT_AGENT_INSTRUCTION = """
You are an artifact agent.

Use save_markdown_artifact when the user asks you to create or save a markdown document.
Use load_artifact when the user asks you to read a saved artifact.
Always use agent_id="artifact_agent".
"""

artifact_agent = LlmAgent(
    name="artifact_agent",
    model=config.DEFAULT_LLM_MODEL,
    description="Creates and loads markdown artifacts using Google Cloud Storage.",
    instruction=ARTIFACT_AGENT_INSTRUCTION,
    tools=[save_markdown_artifact, load_artifact],
)