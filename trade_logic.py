from decimal import Decimal, getcontext
from datetime import datetime
from order_requests import buy_request, sell_request
from vars import top, bottom, step

getcontext().prec = 10

stack = []
transactions = []
prev_price = None
totals_by_day = {}

def get_trade(price):
    global prev_price

    price = Decimal(str(price))

    if price < bottom or price > top:
        print(f"Price {price} is out of range ({bottom} - {top}), doing nothing.")
        return

    if prev_price is None:
        prev_price = price
        print("prev_price update")
        return

    if not stack or (price < stack[-1] - step):
        stack.append(price)
        buy_request(price)

    qty = 0
    while stack and price >= stack[-1] + step:
        stack.pop()
        qty += 1

    if qty > 0:
        sell_request(price, qty)

    prev_price = price
    print(f"transactions: {transactions}")
    print(f"stack: {stack}")

def update_totals_by_day(price, side, quantity, timestamp):
    global totals_by_day

    date_time_value = datetime.utcfromtimestamp(timestamp / 1000)

    date_str = date_time_value.strftime('%Y-%m-%d')

    if date_str not in totals_by_day:
        totals_by_day[date_str] = {'Buy': 0, 'Sell': 0}

    totals_by_day[date_str][side] += price * quantity

    print(f"Updated totals for {date_str}: {totals_by_day[date_str]}")