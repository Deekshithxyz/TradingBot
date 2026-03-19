from dataclasses import dataclass
from typing import Any

from bot.client import BinanceAPIError, BinanceFuturesTestnetClient
from bot.validators import (
    ValidationError,
    validate_order_type,
    validate_positive_decimal,
    validate_price,
    validate_side,
    validate_symbol,
)


@dataclass
class OrderRequest:
    symbol: str
    side: str
    order_type: str
    quantity: str
    price: str | None = None


class OrderService:
    def __init__(self, client: BinanceFuturesTestnetClient):
        self.client = client

    def validate(self, symbol: str, side: str, order_type: str, quantity: str, price: str | None) -> OrderRequest:
        normalized_order_type = validate_order_type(order_type)
        return OrderRequest(
            symbol=validate_symbol(symbol),
            side=validate_side(side),
            order_type=normalized_order_type,
            quantity=validate_positive_decimal(quantity, "quantity"),
            price=validate_price(normalized_order_type, price),
        )

    def place(self, request: OrderRequest) -> dict[str, Any]:
        try:
            return self.client.place_order(
                symbol=request.symbol,
                side=request.side,
                order_type=request.order_type,
                quantity=request.quantity,
                price=request.price,
            )
        except (ValidationError, BinanceAPIError, ConnectionError):
            raise
        except Exception as exc:
            raise RuntimeError(f"Unexpected failure while placing order: {exc}") from exc
