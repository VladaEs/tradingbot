import hashlib
import time
import hmac

from src.API.HTTPClient import HTTPClient

class BybitAPI: 

    http_client = HTTPClient(base_url="https://api.bybit.com")

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        

    async def get_server_time(self) -> dict:
        response = await self.http_client.get(
            "/v5/market/time"
        )
        return response.json()

    def get_ticker(self, symbol: str):
        url = f"/v2/public/tickers?symbol={symbol}"
        response = self.http_client.get(url)
        return response.json()

    def place_order(self, symbol: str, side: str, order_type: str, qty: float, price: float = None):
        url = f"/v2/private/order/create"
        payload = {
            "api_key": self.api_key,
            "symbol": symbol,
            "side": side,
            "order_type": order_type,
            "qty": qty,
            "price": price,
            "timestamp": int(time.time() * 1000)
        }
        payload["sign"] = self._generate_signature(payload)
        response = self.http_client.post(url, data=payload)
        return response.json()

    def _generate_signature(self, params: dict) -> str:
        sorted_params = sorted(params.items())
        query_string = "&".join(f"{key}={value}" for key, value in sorted_params)
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature


    async def close(self) -> None:
        await self.http_client.close()