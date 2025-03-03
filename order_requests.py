from data.database import insert_order
from pybit.unified_trading import HTTP
import os
from dotenv import load_dotenv
from config.vars import qtyExp, pair

load_dotenv()

api_key = os.getenv("BYBIT_API_KEY")
api_secret = os.getenv("BYBIT_API_SECRET")

session = HTTP(
    testnet=False,
    api_key=api_key,
    api_secret=api_secret
)

def buy_request(price):
    try:
        # response = session.place_order(
        #     category="spot",
        #     symbol=pair,
        #     side="Buy",
        #     orderType="Limit",
        #     qty=qtyExp,
        #     price=price,
        #     timeInForce="GTC"
        # )
        insert_order(pair, "Buy", price, qtyExp, "Placed")
        print('--------------------------------')
        # print(f"Buy order placed at price: {price}. Response: {response}")
        print('--------------------------------')
    except Exception as e:
        print(f"Error placing buy order: {e}")

def sell_request(price, qty):
    try:
        # response = session.place_order(
        #     category="spot",
        #     symbol=pair,
        #     side="Sell",
        #     orderType="Limit",
        #     qty=qty*qtyExp,
        #     price=price,
        #     timeInForce="GTC"
        # )

        insert_order(pair, "Sell", price, qty, "Placed")
        print('--------------------------------')
        # print(f"Sell order placed: {qty} by price {price} . Response: {response}")
        print('--------------------------------')
    except Exception as e:
        print(f"Error placing sell order: {e}")
