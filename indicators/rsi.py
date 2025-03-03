from config.vars import RSI_PERIOD


def calculate_rsi(prices, period=RSI_PERIOD):
    if len(prices) < period + 1:
        return None
    
    gains, losses = 0, 0
    for i in range(1, period + 1):
        delta = float(prices[-i]) - float(prices[-i - 1])
        if delta > 0:
            gains += delta
        else:
            losses += abs(delta)
    
    avg_gain = gains / period if period != 0 else 0
    avg_loss = losses / period if period != 0 else 0
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))
