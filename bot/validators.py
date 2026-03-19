from decimal import Decimal, InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


class ValidationError(ValueError):
    pass


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not symbol or not symbol.isalnum():
        raise ValidationError("Symbol must be a non-empty alphanumeric string, e.g. BTCUSDT")
    return symbol



def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Side must be one of: {', '.join(sorted(VALID_SIDES))}")
    return side



def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Order type must be one of: {', '.join(sorted(VALID_ORDER_TYPES))}")
    return order_type



def validate_positive_decimal(value: str, field_name: str) -> str:
    try:
        decimal_value = Decimal(str(value))
    except InvalidOperation as exc:
        raise ValidationError(f"{field_name} must be a valid number") from exc

    if decimal_value <= 0:
        raise ValidationError(f"{field_name} must be greater than 0")
    return format(decimal_value, "f")



def validate_price(order_type: str, price: str | None) -> str | None:
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("price is required for LIMIT orders")
        return validate_positive_decimal(price, "price")
    return None
