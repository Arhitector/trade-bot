import asyncio

from core.websocket_client import start_trade_stream
from data.create_tables import create_tables
from utils.logger import logger


async def main():
    create_tables()

    await start_trade_stream()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Зупинка бота через KeyboardInterrupt.")
    except Exception as e:
        logger.exception(f"Непередбачувана помилка в main: {e}")
