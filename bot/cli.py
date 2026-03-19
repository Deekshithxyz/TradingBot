import argparse
import os
import sys
from typing import Any

from bot.client import BinanceAPIError, BinanceFuturesTestnetClient
from bot.logging_config import setup_logging
from bot.orders import OrderService
from bot.validators import ValidationError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Place MARKET or LIMIT orders on Binance Futures Testnet (USDT-M)",
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--order-type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity, e.g. 0.001")
    parser.add_argument("--price", help="Required for LIMIT orders")
    parser.add_argument(
        "--base-url",
        default="https://testnet.binancefuture.com",
        help="Binance Futures Testnet base URL",
    )
    parser.add_argument(
        "--log-file",
        default="logs/trading_bot.log",
        help="Path to the log file",
    )
    return parser


def print_request_summary(args: argparse.Namespace) -> None:
    print("\n=== Order Request Summary ===")
    print(f"Symbol     : {args.symbol.upper()}")
    print(f"Side       : {args.side.upper()}")
    print(f"Order Type : {args.order_type.upper()}")
    print(f"Quantity   : {args.quantity}")
    if args.price is not None:
        print(f"Price      : {args.price}")



def print_response_details(response: dict[str, Any]) -> None:
    print("\n=== Order Response Details ===")
    print(f"Order ID      : {response.get('orderId', 'N/A')}")
    print(f"Status        : {response.get('status', 'N/A')}")
    print(f"Executed Qty  : {response.get('executedQty', 'N/A')}")
    avg_price = response.get('avgPrice') or response.get('price') or 'N/A'
    print(f"Avg/Price     : {avg_price}")
    print(f"Client Order  : {response.get('clientOrderId', 'N/A')}")



def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    logger = setup_logging(args.log_file)

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print("Error: BINANCE_API_KEY and BINANCE_API_SECRET must be set as environment variables.")
        return 1

    print_request_summary(args)

    try:
        client = BinanceFuturesTestnetClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=args.base_url,
            logger=logger,
        )
        service = OrderService(client)
        request = service.validate(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
        response = service.place(request)
        print_response_details(response)
        print("\nSUCCESS: Order placed successfully.")
        return 0
    except ValidationError as exc:
        logger.error("Validation error: %s", exc)
        print(f"\nFAILED: Invalid input. {exc}")
        return 2
    except BinanceAPIError as exc:
        logger.error("Binance API error: %s", exc)
        print(f"\nFAILED: Binance API error. {exc.payload}")
        return 3
    except ConnectionError as exc:
        logger.error("Network failure: %s", exc)
        print(f"\nFAILED: Network failure. {exc}")
        return 4
    except Exception as exc:
        logger.exception("Unexpected application error")
        print(f"\nFAILED: Unexpected error. {exc}")
        return 5


if __name__ == "__main__":
    sys.exit(main())
