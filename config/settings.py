from decimal import Decimal, getcontext

getcontext().prec = 10

URL = "wss://stream.bybit.com/v5/public/spot"
PAIR = "SALDUSDT"
# DEFAULT_PAIR = "HMSTRUSDT"

TOP = Decimal("0.000700")
BOTTOM = Decimal("0.000500")
STEP = Decimal("0.00001")

VALUE = Decimal("25")
PROFIT = Decimal("0.11")

COMMISSION = Decimal("0.0018")
QTY_EXP = Decimal("610")
TIMEOUT = 300

DB_NAME = "trades.db"

TRADING_STRATEGY = "step"  # "step" або "profit"

# RSI та Bollinger Bands
RSI_PERIOD = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70
BB_PERIOD = 20
BB_STD_DEV_MULTIPLIER = 2
