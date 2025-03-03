from decimal import Decimal
from typing import Optional

from config.settings import TRADING_STRATEGY
from indicators.indicators_summary import indicators_sum

from .trade_state import prices
from .trade_strategies import execute_profit_strategy, execute_step_strategy

_prev_price: Optional[Decimal] = None


def analyze_trade(current_price: float) -> None:
    """
    Аналізує нову ціну та викликає відповідну стратегію.
    """
    global _prev_price

    price = Decimal(str(current_price))

    if _prev_price is None:
        _prev_price = price
        prices.append(price)
        return

    prices.append(price)

    if TRADING_STRATEGY == "step":
        execute_step_strategy(price)
    elif TRADING_STRATEGY == "profit":
        execute_profit_strategy(price)
    else:
        pass

    _prev_price = price

    indicators_sum(prices, price)
