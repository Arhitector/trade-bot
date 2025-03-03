from datetime import datetime

def get_current_time():
    return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

def convert_unix_to_human(unix_time_ms):
    timestamp = datetime.utcfromtimestamp(unix_time_ms / 1000)
    return timestamp.strftime('%Y-%m-%d %H:%M:%S')