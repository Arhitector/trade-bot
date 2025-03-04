from decimal import Decimal
from typing import Optional

from config.settings import TRADING_STRATEGY
from indicators.indicators_summary import indicators_sum
from trading.trade_state import store

from .trade_strategies import execute_profit_strategy, execute_step_strategy


def analyze_trade(current_price: float) -> None:
    price = Decimal(str(current_price))

    prev_price = store.get_prev_price()

    if prev_price is None:
        store.add_price(price)
        return

    store.add_price(price)

    if TRADING_STRATEGY == "step":
        execute_step_strategy(price)
    elif TRADING_STRATEGY == "profit":
        execute_profit_strategy(price)
    else:
        pass

    indicators_sum(store.get_prices_copy(), price)
