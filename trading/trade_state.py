from decimal import Decimal
from typing import List, Tuple

totals_by_day = {}

price_history = {}

profit_value: Decimal = Decimal("0")

stack: List[Tuple[Decimal, Decimal]] = []

transactions: List[Tuple[Decimal, str]] = []

prices: List[Decimal] = []
