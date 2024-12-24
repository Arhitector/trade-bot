from decimal import Decimal, getcontext

getcontext().prec = 10

url = "wss://stream.bybit.com/v5/public/spot"
pair = "SALDUSDT"
top = Decimal('0.0018')
bottom = Decimal('0.0015')
step = Decimal('0.00001')
qtyExp = 610
timeout = 300