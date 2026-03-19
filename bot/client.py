import hashlib
import hmac
import time
from typing import Any
from urllib.parse import urlencode

import requests


class BinanceAPIError(Exception):
    def __init__(self, status_code: int, payload: Any):
        self.status_code = status_code
        self.payload = payload
        super().__init__(f"Binance API error ({status_code}): {payload}")


class BinanceFuturesTestnetClient:
    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://testnet.binancefuture.com",
        timeout: int = 15,
        logger=None,
    ):
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": api_key})

    def _sign(self, params: dict[str, Any]) -> str:
        query_string = urlencode(params, doseq=True)
        return hmac.new(self.api_secret, query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    def _request(self, method: str, path: str, signed: bool = False, **params: Any) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        payload = {k: v for k, v in params.items() if v is not None}

        if signed:
            payload["timestamp"] = int(time.time() * 1000)
            payload.setdefault("recvWindow", 5000)
            payload["signature"] = self._sign(payload)

        if self.logger:
            safe_payload = payload.copy()
            if "signature" in safe_payload:
                safe_payload["signature"] = "***redacted***"
            self.logger.info("API request | method=%s | url=%s | params=%s", method, url, safe_payload)

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=payload,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            if self.logger:
                self.logger.exception("Network error while calling Binance API")
            raise ConnectionError(f"Network error while calling Binance API: {exc}") from exc

        try:
            data = response.json()
        except ValueError:
            data = {"raw": response.text}

        if self.logger:
            self.logger.info(
                "API response | status_code=%s | body=%s",
                response.status_code,
                data,
            )

        if response.status_code >= 400:
            raise BinanceAPIError(response.status_code, data)

        return data

    def ping(self) -> dict[str, Any]:
        return self._request("GET", "/fapi/v1/ping")

    def place_order(
        self,
        *,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: str | None = None,
        time_in_force: str | None = None,
    ) -> dict[str, Any]:
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = time_in_force or "GTC"

        return self._request("POST", "/fapi/v1/order", signed=True, **params)
