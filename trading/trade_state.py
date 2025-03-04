from decimal import Decimal
from typing import List, Tuple


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Store(metaclass=SingletonMeta):
    __slots__ = [
        "prices",
        "transactions",
        "stack",
        "profit_value",
        "price_history",
        "totals_by_day",
        "_prev_price",
    ]

    def __init__(self):
        self.prices: List[Decimal] = []
        self.transactions: List[Tuple[Decimal, str, Decimal]] = []
        self.stack: List[Tuple[Decimal, Decimal]] = []
        self.profit_value: Decimal = Decimal("0")
        self.price_history = {}
        self.totals_by_day = {}
        self._prev_price: Decimal | None = None

    def add_price(self, price: Decimal):
        self.prices.append(price)
        self._prev_price = price

    def get_prices_copy(self):
        return self.prices.copy()

    def record_buy(self, price: Decimal, qty: Decimal):
        self.stack.append((price, qty))
        self.transactions.append((price, "buy", self.profit_value))

    def record_sell(self, buy_price: Decimal, sell_price: Decimal, qty: Decimal):
        position_profit = (sell_price - buy_price) * qty
        self.profit_value += position_profit
        self.transactions.append((sell_price, "sell", self.profit_value))
        self.remove_from_stack(buy_price, qty)

    def remove_from_stack(self, buy_price: Decimal, qty: Decimal):
        for i, (price, quantity) in enumerate(self.stack):
            if price == buy_price and quantity == qty:
                del self.stack[i]
                return

        raise ValueError(
            f"Position with buy_price {buy_price} and qty {qty} not found in stack"
        )

    def get_current_profit(self) -> Decimal:
        return self.profit_value

    def get_stack_copy(self) -> List[Tuple[Decimal, Decimal]]:
        return self.stack.copy()

    def clear_stack(self):
        """clear stack"""
        self.stack.clear()

    def clear_prices(self):
        """clear prices"""
        self.prices.clear()

    def get_prev_price(self) -> Decimal | None:
        return self._prev_price


store = Store()
