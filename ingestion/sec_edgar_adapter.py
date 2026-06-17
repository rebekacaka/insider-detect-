"""
SEC EDGAR Adapter- fetches Form 4 insider trading filings using edgartools
edgartools is a well-maintained open source library (2.3M downloads, MIT licensed)
that parses SEC EDGAR filings into typed Python objects automatically.

Chosen over raw requests + XML parsing because:
- Handles XML parsing automatically
- Returns typed objects with trade_type, shares, price already extracted
- Manages SEC rate limits (10 requests/second) automatically
- API is stable and backwards compatible

Research: edgartools accepted into Anthropic Claude for Open Source Program (2026)
"""

from datetime import date
from typing import List
from dataclasses import dataclass
from edgar import set_identity, Company
import os
import math
from dotenv import load_dotenv

load_dotenv()


@dataclass
class InsiderFiling:
    insider_name: str
    ticker: str
    market: str
    trade_type: str
    shares_traded: int
    trade_price: float
    trade_date: date
    filing_date: date
    days_to_file: int
    sector: str


class SecEdgarAdapter:

    source = "sec_edgar"
    market = "US"

    def __init__(self):
        identity = os.getenv(
            "SEC_IDENTITY",
            "Rebeka Caka rebeka@constructor.university"
        )
        set_identity(identity)

    def fetch_filings(self, ticker: str, num_filings: int = 10) -> List[InsiderFiling]:
        try:
            company = Company(ticker)
            filings = company.get_filings(form="4").latest(num_filings)

            results = []

            for i in range(len(filings)):
                try:
                    filing = filings[i]
                    form4 = filing.obj()
                    filing_date = filing.filing_date
                    df = form4.to_dataframe()

                    if df is None or df.empty:
                        continue

                    for _, row in df.iterrows():
                        trade_date = row.get("Date", filing_date)
                        if trade_date is None:
                            trade_date = filing_date

                        if hasattr(trade_date, 'date'):
                            trade_date_clean = trade_date.date()
                        else:
                            trade_date_clean = filing_date

                        days_to_file = (filing_date - trade_date_clean).days

                        code = str(row.get("Code", ""))
                        if code == "P":
                            trade_type = "BUY"
                        elif code == "S":
                            trade_type = "SELL"
                        else:
                            trade_type = code

                        shares = int(row.get("Shares", 0) or 0)
                        
                        price_raw = row.get("Price", 0.0)
                        price = float(price_raw) if price_raw is not None else 0.0
                        if math.isnan(price):
                            price = 0.0

                        insider = str(row.get("Insider", "Unknown") or "Unknown")

                        record = InsiderFiling(
                            insider_name=insider,
                            ticker=ticker,
                            market=self.market,
                            trade_type=trade_type,
                            shares_traded=shares,
                            trade_price=price,
                            trade_date=trade_date_clean,
                            filing_date=filing_date,
                            days_to_file=days_to_file,
                            sector="US_EQUITY"
                        )
                        results.append(record)

                except Exception as e:
                    print(f"Warning: skipping filing {i} for {ticker}: {e}")
                    continue

            print(f"Fetched {len(results)} insider transactions for {ticker}")
            return results

        except Exception as e:
            raise RuntimeError(f"Failed to fetch SEC EDGAR filings for {ticker}: {e}")