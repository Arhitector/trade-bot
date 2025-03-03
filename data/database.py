import sqlite3
from datetime import datetime

from config.settings import DB_NAME, PAIR, TRADING_STRATEGY
from data.create_tables import create_tables


def insert_trade(symbol, price, quantity, side):
    """Insert a trade into the trade_history table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO trade_history (timestamp, symbol, price, quantity, side)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, symbol, price, quantity, side))
    conn.commit()
    conn.close()

def insert_order(symbol, side, price, quantity, status):
    """Insert a new order into the orders table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO orders (timestamp, symbol, side, price, quantity, status, strategy)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, symbol, side, price, quantity, status, TRADING_STRATEGY))
    conn.commit()
    conn.close()

def insert_technical_indicators(price, rsi, bb_upper, bb_sma, bb_lower):
    """Insert RSI and Bollinger Bands data into the technical_indicators table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute("""
        INSERT INTO technical_indicators (timestamp, symbol, price, rsi, bb_upper, bb_sma, bb_lower, strategy)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, PAIR, price, rsi, bb_upper, bb_sma, bb_lower, TRADING_STRATEGY))

    conn.commit()
    conn.close()

def insert_price_history(symbol, price):
    """Insert a trade into the price_history table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("""
        INSERT INTO price_history (timestamp, symbol, price, strategy)
        VALUES (?, ?, ?, ?)
    """, (timestamp, symbol, price, TRADING_STRATEGY))
    conn.commit()
    conn.close()

import sqlite3

DB_NAME = "trades.db"

def get_price_history(symbol, limit=100):
    """
    Retrieves up to `limit` records from the price_history table
    for the specified `symbol` and `strategy`.
    Results are returned in ascending chronological order (oldest first).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT timestamp, price
        FROM price_history
        WHERE symbol = ? AND strategy = ?
        ORDER BY timestamp DESC
        LIMIT ?
        """,
        (symbol, TRADING_STRATEGY, limit)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows[::-1]


create_tables()
