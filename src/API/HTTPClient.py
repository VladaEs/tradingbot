from typing import Any
from urllib import response
import httpx

class HTTPClient:

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
        )


    async def request(self, method: str, endpoint: str, *, params: dict[str, Any] | None = None, json: dict[str, Any] | None = None, headers: dict[str, str] | None = None) -> dict[str, Any]:
        response = await self._client.request(
            method=method,
            url=endpoint,
            params=params,
            json=json,
            headers=headers,
        )
        print(response)
        response.raise_for_status()
        return response

    async def get(self, endpoint: str, params: dict = None):
        return await self.request("GET", endpoint, params=params)

    async def post(self, endpoint: str, data: dict = None):
        return await self.request("POST", endpoint, json=data)

    async def put(self, endpoint: str, data: dict = None):
        return await self.request("PUT", endpoint, json=data)

    async def delete(self, endpoint: str):
        return await self.request("DELETE", endpoint)


    async def close(self) -> None:
        await self._client.aclose()