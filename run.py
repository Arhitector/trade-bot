import argparse
import asyncio

from config.settings import PAIR as DEFAULT_PAIR
from config.settings import TRADING_STRATEGY as DEFAULT_TRADING_STRATEGY
from core.websocket_client import start_trade_stream
from utils.logger import logger


async def main(strategy: str, pair: str):
    logger.info(f"Trading bot started for pair {pair} with {strategy} strategy.")

    from config.settings import PAIR, TRADING_STRATEGY

    PAIR = pair
    TRADING_STRATEGY = strategy

    await start_trade_stream()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bybit Trading Bot")
    parser.add_argument(
        "--strategy",
        type=str,
        default=DEFAULT_TRADING_STRATEGY,
        choices=["step", "profit"],
        help="Trading strategy to use (step or profit)",
    )
    parser.add_argument(
        "--pair",
        type=str,
        default=DEFAULT_PAIR,
        help="Trading pair to use (e.g., BTCUSDT, ETHUSDT)",
    )

    args = parser.parse_args()

    try:
        asyncio.run(main(args.strategy, args.pair))
    except KeyboardInterrupt:
        logger.info("Trading bot stopped by user.")
    except Exception as e:
        logger.exception(f"An unhandled error occurred: {e}")
