import uuid

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from config import get_settings
from detector.detector import Detector
from proxy.forwarder import Forwarder
from tokenizer.restorer import Restorer
from tokenizer.tokenizer import Tokenizer
from vault.vault import Vault

app = FastAPI(title="hideLM", version="0.1.0")

settings = get_settings()
vault = Vault(db_path=settings.vault_db_path, ttl_seconds=settings.vault_ttl_seconds)
detector = Detector(settings)
forwarder = Forwarder(settings)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "version": "0.1.0"}


@app.post("/v1/chat/completions")
async def chat_completions(request: Request) -> JSONResponse:
    session_id = request.headers.get("X-HideLM-Session", str(uuid.uuid4()))
    body = await request.json()

    # Detect PII in every message and build a per-content match map
    matches_by_content: dict[str, list] = {}
    for msg in body.get("messages", []):
        content = msg.get("content", "")
        if isinstance(content, str) and content:
            found = detector.find_all(content)
            if found:
                matches_by_content[content] = found

    # Mask PII
    tokenizer = Tokenizer(session_id, vault)
    masked_body = tokenizer.mask_messages(body, matches_by_content)

    # Forward to target API
    try:
        response_body = await forwarder.forward("v1/chat/completions", masked_body)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    # Restore tokens in response
    restorer = Restorer(session_id, vault)
    restored_body = restorer.restore_response(response_body)

    return JSONResponse(content=restored_body)
