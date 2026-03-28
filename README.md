# Binance Futures Testnet Trading Bot

A small Python CLI application that places **MARKET** and **LIMIT** orders on **Binance Futures Testnet (USDT-M)**.

## Features

- Supports **BUY** and **SELL**
- Supports **MARKET** and **LIMIT** orders
- Validates CLI input
- Clean structure with separate client/API, order logic, validation, and CLI layers
- Logs API requests, responses, and errors to a log file
- Handles invalid input, API errors, and network failures

## Project Structure

```text
trading_bot_solution/
├── bot/
│   ├── __init__.py
│   ├── cli.py
│   ├── client.py
│   ├── logging_config.py
│   ├── orders.py
│   └── validators.py
├── logs/
│   ├── example_market_order.log
│   └── example_limit_order.log
├── requirements.txt
└── README.md
```

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Export your Binance Futures Testnet credentials:

```bash
export BINANCE_API_KEY="your_testnet_api_key"
export BINANCE_API_SECRET="your_testnet_api_secret"
```

## Run Examples

### 1) MARKET order

```bash
python -m bot.cli \
  --symbol BTCUSDT \
  --side BUY \
  --order-type MARKET \
  --quantity 0.001
```

### 2) LIMIT order

```bash
python -m bot.cli \
  --symbol BTCUSDT \
  --side SELL \
  --order-type LIMIT \
  --quantity 0.001 \
  --price 120000
```

### Custom log file

```bash
python -m bot.cli \
  --symbol ETHUSDT \
  --side BUY \
  --order-type MARKET \
  --quantity 0.01 \
  --log-file logs/my_run.log
```

## Output

The CLI prints:

- order request summary
- order response details
- success/failure message

## Assumptions

- The task targets Binance Futures Testnet **USDT-M** orders.
- `quantity` and `price` are passed as positive decimal strings.
- Binance exchange filters like step size / tick size are not pre-fetched in this version; the API returns a useful validation error if they do not match exchange rules.
- The included log files are **illustrative examples of expected logging format**. You should regenerate them with your own testnet credentials before submission.

