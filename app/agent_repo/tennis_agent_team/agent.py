"""Tennis agent team – analyzes tennis information."""

import structlog

from google.adk.agents import LlmAgent
from google.adk.tools.google_search_tool import GoogleSearchTool

from app import config
from app.agent_repo.summarizer_agent.tools import fetch_url
from app.agent_repo.tennis_agent_team.prompt import (
    TENNIS_AGENT_TEAM_INSTRUCTION,
)

logger = structlog.get_logger(__name__)

_google_search = GoogleSearchTool(
    bypass_multi_tools_limit=True
)

_tools = [_google_search, fetch_url]

tennis_agent_team = LlmAgent(
    name="tennis_agent_team",
    model=config.DEFAULT_LLM_MODEL,
    description=(
        "Tennis analysis agent with search and URL support.\n\n"
        "How to use:\n"
        "1 Paste player data or URL\n"
        "2 Ask for analysis\n"
        "3 Review match, mental and tactical insights\n\n"
        "Examples:\n"
        "- Analyze this match report\n"
        "- Review this ITF player profile\n"
        "- Create training priorities"
    ),
    instruction=TENNIS_AGENT_TEAM_INSTRUCTION,
    tools=_tools,
)