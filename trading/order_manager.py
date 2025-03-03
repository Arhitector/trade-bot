from decimal import Decimal

import trading.trade_state
from config.vars import pair
from data.database import insert_order
from utils.logger import logger


def buy_order(price: Decimal, qty: Decimal):
    """Купівля певної кількості за поточною ціною."""
    trading.trade_state.stack.append((price, qty))
    trading.trade_state.transactions.append((price, "buy"))
    insert_order(pair, "Buy", float(price), float(qty), "Placed")
    logger.info(f"🟢 Купівля {qty} за ціною {price}")
    logger.info(f"📜 Стек (stack): {trading.trade_state.stack}")
    logger.info(f"📜 Transactions: {trading.trade_state.transactions}")


def sell_order(buy_price: Decimal, sell_price: Decimal, qty: Decimal):
    """
    Продаж конкретної (часткової) позиції.
    buy_price – ціна, за якою купували цю позицію;
    sell_price – поточна ціна продажу;
    qty – кількість, яку продаємо.
    """
    global profit_value
    position_profit = (sell_price - buy_price) * qty
    trading.trade_state.profit_value += position_profit
    trading.trade_state.transactions.append((sell_price, "sell", profit_value))
    insert_order(pair, "Sell", float(sell_price), float(qty), "Placed")

    logger.info(
        f"💰 Продано {qty} за {sell_price} (купували за {buy_price}), профіт: {trading.trade_state.position_profit}"
    )
    logger.info(f"📜 Transactions: {trading.trade_state.transactions}")
