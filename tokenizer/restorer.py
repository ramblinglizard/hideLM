import copy
import re

from vault.vault import Vault

_TOKEN_PATTERN = re.compile(r"\[[A-Z_]+_\d+\]")


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
