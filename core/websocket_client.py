import asyncio
import json
import socket
from decimal import Decimal
from typing import Any, Callable, Dict

import websockets

from config.settings import PAIR, PROFIT, STEP, TIMEOUT, TRADING_STRATEGY, URL, VALUE
from data.database import get_price_history, insert_price_history
from trading.trade_analyzer import analyze_trade
from trading.trade_state import store
from utils.logger import logger


async def check_internet() -> bool:
    try:
        socket.gethostbyname("1.1.1.1")
        return True
    except Exception:
        return False


def process_trade_data(data_json: Dict[str, Any]) -> None:
    if "data" not in data_json:
        logger.warning("Некоректна структура даних (відсутнє поле 'data').")
        return

    for trade in data_json["data"]:
        price = trade.get("p")
        quantity = trade.get("v")
        side = trade.get("S", "Unknown")
        time_ms = trade.get("T")

        if not (price and quantity):
            logger.warning(f"⚠️ Некоректні дані у трейді: {trade}")
            continue

        side_lower = side.lower()
        if side_lower == "sell":
            logger.debug(f"Skipping SELL trade at price={price}, side={side_lower}")
            continue

        price_f = float(price)
        quantity_f = float(quantity)

        insert_price_history(PAIR, price_f)
        store.add_price(Decimal(str(price_f)))

        from utils.time_utils import convert_unix_to_human

        formatted_time = convert_unix_to_human(time_ms)
        logger.info("----------------------------------------------")
        logger.info(
            f"{formatted_time} - Trade received: {price_f} USDT, "
            f"Quantity: {quantity_f}, Side: {side}"
        )

        analyze_trade(price_f)

        logger.info(f"🔹 Загальний профіт: {store.get_current_profit()}")


async def start_trade_stream() -> None:
    global TRADING_STRATEGY

    while True:
        try:
            if await check_internet():
                if not store.prices:
                    db_prices = [p for _, p in get_price_history(PAIR, 200)]
                    store.prices.extend(db_prices)

                await _create_connection(URL, f"publicTrade.{PAIR}", process_trade_data)
            else:
                logger.warning("⚠️ Немає інтернету. Повтор через 10 секунд...")
                await asyncio.sleep(10)

        except websockets.exceptions.ConnectionClosedError as e:
            logger.error(f"❌ З'єднання розірвано, повторюємо... {e}")
            await asyncio.sleep(5)
        except asyncio.TimeoutError:
            logger.warning(f"⚠️ Немає нових даних для {PAIR} за останні 5 хвилин.")
        except Exception as e:
            logger.exception(f"❌ Виникла помилка: {e}")
            await asyncio.sleep(5)


async def _create_connection(
    ws_url: str, topic: str, process_function: Callable[[Dict[str, Any]], None]
) -> None:
    global TRADING_STRATEGY

    async with websockets.connect(ws_url, ping_interval=None) as websocket:
        params = {"op": "subscribe", "args": [topic]}
        await websocket.send(json.dumps(params))
        logger.info(f"✅ Підключено до {topic}.")
        logger.info(f"Стратегія {TRADING_STRATEGY}.")

        if TRADING_STRATEGY == "profit":
            logger.info(f"Купівля на {VALUE}, профіт = {PROFIT}.")
        elif TRADING_STRATEGY == "step":
            logger.info(f"Купівля з кроком {STEP}.")

        asyncio.create_task(_send_ping(websocket))

        while True:
            try:
                data = await asyncio.wait_for(websocket.recv(), timeout=TIMEOUT)
                data_json = json.loads(data)
                process_function(data_json)
            except websockets.exceptions.ConnectionClosedError:
                logger.error("❌ З'єднання закрите. Повторне підключення...")
                break
            except asyncio.TimeoutError:
                logger.warning(f"⚠️ Немає даних для {topic} за останні 5 хвилин.")
                break


async def _send_ping(websocket: websockets.WebSocketClientProtocol) -> None:
    while True:
        try:
            await websocket.ping()
            await asyncio.sleep(20)
        except Exception as e:
            logger.error(f"Ping failed: {e}")
            break
