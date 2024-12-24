from datetime import datetime, timedelta

def convert_unix_to_human(unix_time_ms):
    timestamp = datetime.utcfromtimestamp(unix_time_ms / 1000)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')

def cleanup_old_data(trade_data):
    cutoff_time = datetime.utcnow() - timedelta(hours=1)
    while trade_data and trade_data[0]["timestamp"] < cutoff_time:
        trade_data.pop(0)
