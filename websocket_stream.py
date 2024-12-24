import asyncio
import websockets
import json
import socket

from collections import deque
from datetime import datetime
from decimal import getcontext
from helpers import cleanup_old_data, convert_unix_to_human
from trade_logic import update_totals_by_day
from vars import pair, timeout, url

trade_data = deque()

getcontext().prec = 10

trade_data = []

async def check_internet():
    """Check if there is an active internet connection."""
    try:
        socket.gethostbyname("1.1.1.1")
        return True
    except Exception:
        return False

def process_trade_data(data_json):
    if "data" in data_json:
        for trade in data_json["data"]:
            price = trade.get("p")
            quantity = trade.get("v")
            side = trade.get("S", "Unknown")
            time = trade.get("T")
            formatted_time = convert_unix_to_human(time)

            if price and quantity:
                price = float(price)
                quantity = float(quantity)
                print(f"{formatted_time} - Trade received: {price} USDT, Quantity: {quantity}, Side: {side}")
                update_totals_by_day(price, side, quantity, time)
            else:
                print("Missing data in trade:", trade)

async def stream_trades():
    while True:
        try:
            if await check_internet():
                async with websockets.connect(url, ping_interval=None) as websocket:
                    params = {
                        "op": "subscribe",
                        "args": [f"publicTrade.{pair}"]
                    }
                    await websocket.send(json.dumps(params))
                    print(f"Subscribed to {pair} trade data.")

                    async def send_ping():
                        while True:
                            try:
                                await websocket.ping()
                                print(f"Ping sent at {datetime.utcnow()}")
                                await asyncio.sleep(20)
                            except Exception as e:
                                print(f"Ping failed: {e}")
                                break

                    asyncio.create_task(send_ping())

                    while True:
                        data = await asyncio.wait_for(websocket.recv(), timeout=timeout)
                        data_json = json.loads(data)
                        process_trade_data(data_json)

            else:
                print("No internet connection. Retrying in 10 seconds...")
                await asyncio.sleep(10)

        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed, retrying... {e}")
            await asyncio.sleep(5)
        except asyncio.TimeoutError:
            print(f"No new data received for {pair} in the last 5 minutes.")
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(5)

        cleanup_old_data(trade_data)
