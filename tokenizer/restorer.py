import copy
import re

from vault.vault import Vault

_TOKEN_PATTERN = re.compile(r"\[[A-Z_]+_\d+\]")
# Matches a potential partial token at the end of a string (open bracket, not yet closed)
_PARTIAL_TOKEN = re.compile(r"\[[A-Z_]*\d*$")


class Restorer:
    def __init__(self, session_id: str, vault: Vault) -> None:
        self._session_id = session_id
        self._vault = vault

    def restore_text(self, text: str) -> str:
        def replace(match: re.Match) -> str:
            original = self._vault.get_value(self._session_id, match.group())
            return original if original is not None else match.group()

        return _TOKEN_PATTERN.sub(replace, text)

    def restore_response(self, body: dict) -> dict:
        body = copy.deepcopy(body)
        for choice in body.get("choices", []):
            msg = choice.get("message", {})
            if isinstance(msg.get("content"), str):
                msg["content"] = self.restore_text(msg["content"])
        return body


class StreamingRestorer:
    """
    Restores PII tokens in a streaming (SSE) response.

    Because a token like [EMAIL_1] may be split across multiple chunks, this
    class buffers any potential partial token at the tail and only flushes it
    once the token is confirmed complete or replaced by new content.
    """

    def __init__(self, session_id: str, vault: Vault) -> None:
        self._session_id = session_id
        self._vault = vault
        self._buffer = ""

    def feed(self, delta: str) -> str:
        """Feed a new delta string; returns the portion safe to send downstream."""
        self._buffer += delta
        partial = _PARTIAL_TOKEN.search(self._buffer)
        if partial:
            safe, self._buffer = self._buffer[: partial.start()], self._buffer[partial.start():]
        else:
            safe, self._buffer = self._buffer, ""
        return _TOKEN_PATTERN.sub(self._replace, safe)

    def flush(self) -> str:
        """Call at end-of-stream to drain any buffered content."""
        remaining = _TOKEN_PATTERN.sub(self._replace, self._buffer)
        self._buffer = ""
        return remaining

    def _replace(self, m: re.Match) -> str:
        original = self._vault.get_value(self._session_id, m.group())
        return original if original is not None else m.group()
