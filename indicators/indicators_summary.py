from data.database import insert_technical_indicators
from indicators.rsi import calculate_rsi
from indicators.bollinger_bands import calculate_bollinger_bands
from utils.logger import logger


def indicators_sum(prices, price):
    rsi = calculate_rsi(prices)
    bb_upper, bb_sma, bb_lower = calculate_bollinger_bands(prices)

    logger.info(f"📈 RSI: {rsi:.2f}" if rsi else "📈 RSI: Недостатньо даних")
    if bb_upper:
        logger.info(f"📉 Bollinger Bands: Верхня={bb_upper:.6f}, SMA={bb_sma:.6f}, Нижня={bb_lower:.6f}")

    insert_technical_indicators(float(price), float(rsi if rsi else 0),
                                float(bb_upper if bb_upper else 0),
                                float(bb_sma if bb_sma else 0),
                                float(bb_lower if bb_lower else 0))