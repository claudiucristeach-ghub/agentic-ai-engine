# MCP fetch server – exposes a fetch_url tool over an SSE endpoint (/sse).
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .

# Bind to all interfaces inside the container; SSE endpoint served on this port.
ENV MCP_FETCH_HOST=0.0.0.0 \
    MCP_FETCH_PORT=8080
EXPOSE 8080

CMD ["python", "server.py"]