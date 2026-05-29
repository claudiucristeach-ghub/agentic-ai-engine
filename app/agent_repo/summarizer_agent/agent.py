"""Summarizer agent – summarizes pasted text and uploaded documents."""

import structlog

from google.adk.agents import LlmAgent
from google.adk.tools import preload_memory, load_memory
from google.adk.tools.google_search_tool import GoogleSearchTool

from app import config
from app.agent_repo.summarizer_agent.prompt import SUMMARIZER_AGENT_INSTRUCTION
from app.agent_repo.summarizer_agent.tools import fetch_url

logger = structlog.get_logger(__name__)

_google_search = GoogleSearchTool(bypass_multi_tools_limit=True)

_tools = [_google_search, preload_memory, load_memory]

if config.MCP_FETCH_URL:
    from google.adk.tools.mcp_tool import McpToolset, SseConnectionParams

    _tools.append(
        McpToolset(connection_params=SseConnectionParams(url=config.MCP_FETCH_URL))
    )
    logger.info("Summarizer using MCP fetch server", url=config.MCP_FETCH_URL)
else:
    _tools.append(fetch_url)
    logger.info("Summarizer using in-process fetch_url tool")


summarizer_agent = LlmAgent(
    name="summarizer_agent",
    model=config.DEFAULT_LLM_MODEL,
    description=(
        "Agent that summarizes pasted text and uploaded documents (txt, md, json, "
        "pdf, docx), can fetch and summarize web pages, can use Google Search "
        "for current or external information, and can use memory across sessions."
    ),
    instruction=SUMMARIZER_AGENT_INSTRUCTION,
    tools=_tools,
)