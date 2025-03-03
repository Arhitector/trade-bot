import sqlite3

from config.settings import DB_NAME

def create_tables():
    """Creates tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Trade History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trade_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            price REAL,
            quantity REAL,
            side TEXT
        )
    """)

    # Orders Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            side TEXT,
            price REAL,
            quantity REAL,
            status TEXT,
            strategy TEXT
        )
    """)

    # Technical Indicators Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS technical_indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            price REAL,
            rsi REAL,
            bb_upper REAL,
            bb_sma REAL,
            bb_lower REAL,
            strategy TEXT
        )
    """)

    # Technical Indicators Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            symbol TEXT,
            price REAL,
            strategy TEXT
        )
    """)

    conn.commit()
    conn.close()
