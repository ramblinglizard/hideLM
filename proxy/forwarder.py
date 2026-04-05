from collections.abc import AsyncGenerator

import httpx


class Forwarder:
    def __init__(self, settings: object) -> None:
        self._target_url = getattr(settings, "target_api_url", "").rstrip("/")
        self._api_key = getattr(settings, "target_api_key", "")

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    async def forward(self, path: str, body: dict) -> dict:
        url = f"{self._target_url}/{path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=body, headers=self._headers())
            response.raise_for_status()
            return response.json()

    async def forward_stream(self, path: str, body: dict) -> AsyncGenerator[str, None]:
        url = f"{self._target_url}/{path.lstrip('/')}"
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, json=body, headers=self._headers()) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    yield line
