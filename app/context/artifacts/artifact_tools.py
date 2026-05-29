from google.genai.types import Part

from app import config
from app.context.artifacts.artifact_service_handler import artifact_service_handler
from app.handlers.session_handler import session_handler


async def save_markdown_artifact(agent_id: str, filename: str, content: str) -> dict:
    if not filename.endswith(".md"):
        filename += ".md"

    session_id = session_handler._agent_session_mapping.get(agent_id)
    if not session_id:
        return {"status": "error", "message": "No active session found."}

    await artifact_service_handler.service.save_artifact(
        app_name="_app",
        user_id=config.USER_ID,
        session_id=session_id,
        filename=filename,
        artifact=Part(text=content),
    )

    return {"status": "ok", "filename": filename}


async def load_artifact(agent_id: str, filename: str) -> dict:
    session_id = session_handler._agent_session_mapping.get(agent_id)
    if not session_id:
        return {"status": "error", "message": "No active session found."}

    part = await artifact_service_handler.service.load_artifact(
        app_name="_app",
        user_id=config.USER_ID,
        session_id=session_id,
        filename=filename,
    )

    if not part:
        return {"status": "error", "message": "Artifact not found."}

    return {"status": "ok", "filename": filename, "content": part.text}