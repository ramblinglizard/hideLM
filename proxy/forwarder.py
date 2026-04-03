import httpx


class Forwarder:
    def __init__(self, settings: object) -> None:
        self._target_url = getattr(settings, "target_api_url", "").rstrip("/")
        self._api_key = getattr(settings, "target_api_key", "")

    async def forward(self, path: str, body: dict) -> dict:
        url = f"{self._target_url}/{path.lstrip('/')}"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=body, headers=headers)
            response.raise_for_status()
            return response.json()
