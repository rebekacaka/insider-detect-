"""
The yfinance adapter is the first concrete implementation of the BaseAdapter contract. 
It connects to Yahoo Finance API, fetch OHLCV data for a specific ticker betwenn two dates and converts each row of the raw pandas 
DataFrame into a typed MarketRecord object that the rest of the pipeline can process consistently. 
One important thing that i discovered during research is that yfinance is not an official API it scrapes Yahoo FInance backend meaning yahoo can change their structure overnight 
and break it without warning. Because of this I wrapped the entire fetch in a try/except block so that if yfinance fails, the pipeline logs a clear error message and returns 
an empty list instead of crashing the entire DAG. 

I also added an empty data chech because sometimes Yahoo returns nothing on a ticker without rainsing an error. 
Without this check the loop wpuld silently produce zero records with no indication of what went wrong. 
I used progress=False to stop yfinance printing a progress bar to the terminal,  by default it does this, which would pollute our Airflow logs with noise.

I explicitly cast data types, float(row["Open"]), int(row["Volume"]), because pandas returns numpy types like numpy.float64 instead of Python's native float. Passing numpy types directly into psycopg2 raises a type error when inserting into PostgreSQL.
I calculate Daily_Return during ingestion using pct_change(), computed once here rather than recalculating it in every downstream module.
I expanded available_tickers() beyond just large caps to include Biotech and Gold sectors,  based on research showing these sectors have the highest information asymmetry. 
Biotech insiders know drug trial results before publication,
 Gold mining insiders know discovery assay results before announcement. 
 The same volume spike in a Biotech stock is far more suspicious than in Apple.

"""

from __future__ import annotations
import pandas as pd
from datetime import date
from typing import List
import yfinance as yf
from src.common.base_adapter import BaseAdapter, MarketRecord


class YFinanceAdapter(BaseAdapter):

    source: str = "yfinance"
    market: str = "US"

    def fetch(self, ticker: str, start: date, end: date) -> List[MarketRecord]:
        try:
            raw_data = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
            raw_data.columns = raw_data.columns.get_level_values(0)

            if raw_data is None or raw_data.empty:
                print(f"Warning: no data returned for {ticker}")
                return []

            raw_data["Daily_Return"] = raw_data["Close"].pct_change()

            records = []

            for record_date, row in raw_data.iterrows():
                ts = pd.Timestamp(record_date)
                record = MarketRecord(
                    source=self.source,
                    ticker=ticker,
                    market=self.market,
                    record_date=ts.date(),
                    open_price=float(row["Open"]),
                    close_price=float(row["Close"]),
                    volume=int(row["Volume"])
                )
                records.append(record)

            return records

        except Exception as e:
            raise RuntimeError(f"Error fetching {ticker} from yfinance: {e}")

    def available_tickers(self) -> List[str]:
        large_caps = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA"]
        biotech = ["MRNA", "BNTX", "NVAX", "SAVA", "ACAD"]
        gold = ["NEM", "GOLD", "KGC", "AU", "AGI"]
        return large_caps + biotech + gold