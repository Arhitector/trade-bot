from pybit.unified_trading import HTTP
import os
import asyncio
from websocket_stream import stream_trades

async def main():
    await stream_trades()

if __name__ == "__main__":
    asyncio.run(main())
