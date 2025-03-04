from decimal import Decimal

from config.settings import PAIR
from data.database import insert_order
from trading.trade_state import store
from utils.logger import logger


def buy_order(price: Decimal, qty: Decimal):
    store.record_buy(price, qty)
    insert_order(PAIR, "Buy", float(price), float(qty), "Placed")
    logger.info(f"🟢 Купівля {qty} за ціною {price}")
    logger.info(f"📜 Стек (stack): {store.get_stack_copy()}")
    logger.info(f"📜 Transactions: {store.transactions}")


def sell_order(buy_price: Decimal, sell_price: Decimal, qty: Decimal):
    store.record_sell(buy_price, sell_price, qty)
    insert_order(PAIR, "Sell", float(sell_price), float(qty), "Placed")

    logger.info(
        f"💰 Продано {qty} за {sell_price} (купували за {buy_price}), профіт: {(sell_price - buy_price) * qty}"
    )
    logger.info(f"📜 Transactions: {store.transactions}")
