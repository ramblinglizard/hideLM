import json
import uuid
from collections.abc import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

from config import get_settings
from detector.detector import Detector
from proxy.forwarder import Forwarder
from tokenizer.restorer import Restorer, StreamingRestorer
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


def _mask(session_id: str, body: dict) -> tuple[dict, Tokenizer]:
    matches_by_content: dict[str, list] = {}
    for msg in body.get("messages", []):
        content = msg.get("content", "")
        if isinstance(content, str) and content:
            found = detector.find_all(content)
            if found:
                matches_by_content[content] = found
    tokenizer = Tokenizer(session_id, vault)
    return tokenizer.mask_messages(body, matches_by_content), tokenizer


async def _generate_stream(session_id: str, masked_body: dict) -> AsyncGenerator[str, None]:
    sr = StreamingRestorer(session_id, vault)
    try:
        async for line in forwarder.forward_stream("v1/chat/completions", masked_body):
            if not line:
                yield "\n"
                continue
            if not line.startswith("data: "):
                yield line + "\n"
                continue
            payload = line[6:]
            if payload.strip() == "[DONE]":
                leftover = sr.flush()
                if leftover:
                    # Emit a final synthetic chunk for any buffered content
                    final_chunk = {"choices": [{"delta": {"content": leftover}, "finish_reason": None, "index": 0}]}
                    yield f"data: {json.dumps(final_chunk)}\n\n"
                yield "data: [DONE]\n\n"
                return
            try:
                chunk = json.loads(payload)
                for choice in chunk.get("choices", []):
                    delta = choice.get("delta", {})
                    if isinstance(delta.get("content"), str):
                        delta["content"] = sr.feed(delta["content"])
                yield f"data: {json.dumps(chunk)}\n\n"
            except json.JSONDecodeError:
                yield line + "\n"
    except Exception as exc:
        yield f"data: {json.dumps({'error': str(exc)})}\n\n"


@app.post("/v1/chat/completions")
async def chat_completions(request: Request) -> JSONResponse | StreamingResponse:
    session_id = request.headers.get("X-HideLM-Session", str(uuid.uuid4()))
    body = await request.json()
    masked_body, _ = _mask(session_id, body)

    if body.get("stream"):
        return StreamingResponse(
            _generate_stream(session_id, masked_body),
            media_type="text/event-stream",
        )

    try:
        response_body = await forwarder.forward("v1/chat/completions", masked_body)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    restorer = Restorer(session_id, vault)
    return JSONResponse(content=restorer.restore_response(response_body))
