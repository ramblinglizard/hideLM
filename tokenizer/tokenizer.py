import copy

from detector.base import PIIMatch
from vault.vault import Vault


class Tokenizer:
    def __init__(self, session_id: str, vault: Vault) -> None:
        self._session_id = session_id
        self._vault = vault
        self._counters: dict[str, int] = {}

    def mask_text(self, text: str, matches: list[PIIMatch]) -> str:
        # Replace matches right-to-left to preserve earlier positions
        for match in sorted(matches, key=lambda m: m.start, reverse=True):
            token = self._get_or_create_token(match)
            text = text[: match.start] + token + text[match.end :]
        return text

    def mask_messages(self, body: dict, matches_by_content: dict[str, list]) -> dict:
        body = copy.deepcopy(body)
        for msg in body.get("messages", []):
            content = msg.get("content", "")
            if isinstance(content, str) and content in matches_by_content:
                msg["content"] = self.mask_text(content, matches_by_content[content])
        return body

    def _get_or_create_token(self, match: PIIMatch) -> str:
        existing = self._vault.get_token(self._session_id, match.value, match.pii_type)
        if existing:
            return existing
        count = self._counters.get(match.pii_type, 0) + 1
        self._counters[match.pii_type] = count
        token = f"[{match.pii_type}_{count}]"
        self._vault.store(self._session_id, token, match.value, match.pii_type)
        return token
