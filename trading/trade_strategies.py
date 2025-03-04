from decimal import Decimal
from typing import List, Tuple

from config.settings import PROFIT, STEP, VALUE
from trading.order_manager import buy_order, sell_order
from trading.trade_state import store
from utils.logger import logger


def execute_step_strategy(price: Decimal) -> None:
    stack_copy = store.get_stack_copy()

    if not stack_copy:
        logger.info("empty stack, first buy")
        buy_order(price, VALUE)
        return

    positions_to_sell = []
    positions_to_keep = []

    for buy_price, qty in stack_copy:
        threshold = buy_price + STEP
        logger.debug(
            f"[STEP DEBUG] Checking buy_price={buy_price}, threshold={threshold}, current price={price}"
        )
        if price >= threshold:
            positions_to_sell.append((buy_price, qty))
        else:
            positions_to_keep.append((buy_price, qty))

    logger.debug(f"[STEP DEBUG] positions_to_sell: {positions_to_sell}")
    logger.debug(f"[STEP DEBUG] positions_to_keep: {positions_to_keep}")

    _grouped_sell(positions_to_sell, price)
    _update_stack_after_sell(positions_to_keep)

    new_stack = store.get_stack_copy()
    if new_stack:
        last_buy_price, _ = new_stack[-1]
        buy_threshold = last_buy_price - STEP
        logger.debug(
            f"[STEP DEBUG] last_buy_price={last_buy_price}, buy_threshold={buy_threshold}, current={price}"
        )
        if price <= buy_threshold:
            buy_order(price, VALUE)
    else:
        buy_order(price, VALUE)


def execute_profit_strategy(price: Decimal) -> None:
    stack = store.get_stack_copy()
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

    if store.get_stack_copy():
        last_buy_price, _ = store.get_stack_copy()[-1]
        buy_threshold = (VALUE - PROFIT) * last_buy_price / VALUE
        if price <= buy_threshold:
            buy_order(price, VALUE)
    else:
        buy_order(price, VALUE)


def _grouped_sell(positions_to_sell: List[Tuple[Decimal, Decimal]], price) -> None:
    if not positions_to_sell:
        return

    for buy_price, qty in positions_to_sell:
        sell_order(buy_price, price, qty)


def _update_stack_after_sell(positions_to_keep: List[Tuple[Decimal, Decimal]]) -> None:
    store.clear_stack()
    for item in positions_to_keep:
        if item not in store.get_stack_copy():
            store.record_buy(item[0], item[1])
