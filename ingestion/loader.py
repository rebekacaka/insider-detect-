"""
Database Loader - saves MarketRecord objects into PostgreSQL
Takes the output of any adapter and persists it to the stock_prices table.

Used execute_values() from psycopg2.extras instead of looping execute().
Research from psycopg2 bulk insert best practices showed execute_values()
inserts all records in a single SQL statement, significantly faster than
one INSERT per record, especially for large datasets.

Uses ON CONFLICT DO NOTHING to make the loader indempotent/unchangedso its safe to run
multiple times without creating duplicate rows.
"""

from datetime import datetime
from typing import List
from psycopg2.extras import execute_values
from ingestion.base_adapter import MarketRecord
from database.database_connection import get_connection


def load_market_records(records: List[MarketRecord]) -> int:
    #the function to return the number of records successfully inserted
    if not records:
        print("Warning: no records to load")
        return 0

    conn = None

    try:
        conn = get_connection()
        cursor = conn.cursor()

        #build list of tuples so one per record
        #execute_values inserts all of them in one SQL statement
        values = [
            (
                record.ticker,
                record.market,
                record.record_date,
                record.open_price,
                record.close_price,
                record.volume,
                datetime.utcnow()
            )
            for record in records
        ]

        execute_values(cursor, """
            INSERT INTO stock_prices
                (ticker, market, date, open_price, close_price, volume, created_at)
            VALUES %s
            ON CONFLICT (ticker, market, date) DO NOTHING
        """, values)

        inserted = cursor.rowcount
        conn.commit()
        print(f"Successfully inserted {inserted} records into stock_prices")
        return inserted

    except Exception as e:
        if conn:
            conn.rollback()
        raise RuntimeError(f"Failed to load records into database: {e}")

    finally:
        if conn:
            conn.close()