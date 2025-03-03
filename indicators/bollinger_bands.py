import statistics

from config.vars import BB_PERIOD, BB_STD_DEV_MULTIPLIER

def calculate_bollinger_bands(prices, period=BB_PERIOD, mult=BB_STD_DEV_MULTIPLIER):
    if len(prices) < period:
        return None, None, None
    
    recent_prices = [float(p) for p in prices[-period:]]
    sma = statistics.mean(recent_prices)
    std_dev = statistics.pstdev(recent_prices)
    
    upper_band = sma + (mult * std_dev)
    lower_band = sma - (mult * std_dev)
    
    return upper_band, sma, lower_band
