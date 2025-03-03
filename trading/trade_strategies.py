from decimal import Decimal
from typing import List, Tuple

from config.settings import PROFIT, STEP, VALUE
from trading.order_manager import buy_order, sell_order
from trading.trade_state import stack
from utils.logger import logger


def execute_step_strategy(price: Decimal) -> None:
    """
    Step-стратегія:
    - Якщо ціна >= buy_price + STEP, продаємо всі такі позиції разом;
    - Якщо stack порожній чи ціна <= (last_buy_price - STEP), докуповуємо.
    """
    global stack

    if not stack:
        logger.info("empty stack, first buy")
        buy_order(price, VALUE)
        return

    positions_to_sell = []
    positions_to_keep = []

    for buy_price, qty in stack:
        if price >= buy_price + STEP:
            positions_to_sell.append((buy_price, qty))
        else:
            positions_to_keep.append((buy_price, qty))

    _grouped_sell(positions_to_sell, price)

    _update_stack_after_sell(positions_to_keep)

    if stack:
        last_buy_price, _ = stack[-1]
        buy_threshold = last_buy_price - STEP
        if price <= buy_threshold:
            buy_order(price, VALUE)
    else:
        buy_order(price, VALUE)


def execute_profit_strategy(price: Decimal) -> None:
    """
    Profit-стратегія:
    - Якщо ціна >= (buy_price * (VALUE+PROFIT)/VALUE), продаємо разом;
    - Якщо ціна <= (buy_price * (VALUE-PROFIT)/VALUE), докуповуємо.
    """
    global stack
    logger.debug(f"Stack at start of strategy: {list(stack)}")

    if not stack:
        logger.info(f"Stack is empty, making initial purchase at {price}")
        buy_order(price, VALUE)
        logger.debug(f"Stack after initial purchase: {list(stack)}")
        return

    positions_to_sell = []
    positions_to_keep = []

    for buy_price, qty in stack:
        target_sell_price = (VALUE + PROFIT) * buy_price / VALUE
        if price >= target_sell_price:
            positions_to_sell.append((buy_price, qty))
        else:
            positions_to_keep.append((buy_price, qty))

    _grouped_sell(positions_to_sell, price)

    _update_stack_after_sell(positions_to_keep)

    if stack:
        last_buy_price, _ = stack[-1]
        buy_threshold = (VALUE - PROFIT) * last_buy_price / VALUE
        if price <= buy_threshold:
            buy_order(price, VALUE)
    else:
        buy_order(price, VALUE)


def _grouped_sell(positions_to_sell: List[Tuple[Decimal, Decimal]], price) -> None:
    """
    Допоміжна функція: продає список позицій одним ордером.
    """
    if not positions_to_sell:
        return

    total_qty = sum(q for _, q in positions_to_sell)

    avg_buy_price = sum(bp * q for bp, q in positions_to_sell) / total_qty

    sell_order(avg_buy_price, price, total_qty)


def _update_stack_after_sell(positions_to_keep: List[Tuple[Decimal, Decimal]]) -> None:
    """
    Допоміжна функція: очищує stack та записує туди позиції, що залишилися.
    """
    stack.clear()
    stack.extend(positions_to_keep)
