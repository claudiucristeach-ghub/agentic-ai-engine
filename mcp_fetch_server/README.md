# Fetch MCP Server

A small [MCP](https://modelcontextprotocol.io/) server that exposes a single tool,
**`fetch_url`**, which retrieves a remote web page and returns its readable text
content. Used by the summarizer agent (Task 3).

## Run locally

```bash
cd mcp_fetch_server
pip install -r requirements.txt
python server.py
```

The SSE endpoint is then available at **http://127.0.0.1:8080/sse**.

## Run in Docker

```bash
cd mcp_fetch_server
docker build -t fetch-mcp .
docker run -p 8080:8080 fetch-mcp
```

## Connect the app to it

Set this in the main app's `.env`, then restart the app:

```env
MCP_FETCH_URL=http://localhost:8080/sse
```

When `MCP_FETCH_URL` is set, the summarizer uses this MCP server's `fetch_url`
tool. When it's empty, the summarizer falls back to its in-process `fetch_url`
function (`app/agent_repo/summarizer_agent/tools.py`).

## The tool

`fetch_url(url: str) -> dict` — returns `{ url, status, content_type, title, text, truncated }`,
or `{ url, error }` on failure. HTML is reduced to readable text (scripts/styles
stripped); long pages are truncated to keep the agent's context manageable.