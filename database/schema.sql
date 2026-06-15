CREATE TABLE stock_prices(
    id SERIAL PRIMARY KEY,  --uniquely identifies each row,
    ticker VARCHAR(255) NOT NULL, 
    market VARCHAR(50)  NOT NULL, 
    date DATE NOT NULL, 
    open_price FLOAT NOT NULL, 
    close_price FLOAT NOT NULL, 
    volume BIGINT NOT NULL, 
    created_at TIMESTAMPTZ NOT NULL, 
    UNIQUE(ticker, market, date) --this prevents dublicate entries, same stock, same market and same date can exist only once

);

CREATE TABLE insider_filings (
    id SERIAL PRIMARY KEY, 
    insider_name VARCHAR(255) NOT NULL, 
    ticker VARCHAR(255) NOT NULL, 
    market VARCHAR(50) NOT NULL, 
    trade_type VARCHAR(10) NOT NULL, 
    shares_traded BIGINT NOT NULL, 
    trade_price FLOAT NOT NULL, 
    trade_date DATE NOT NULL, 
    filing_date DATE NOT NULL, 
    days_to_file INTEGER,
    created_at TIMESTAMPTZ NOT NULL,
    UNIQUE(ticker, insider_name, trade_date)

);

CREATE TABLE flagged_trades (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(255) NOT NULL,
    market VARCHAR(50) NOT NULL,
    trade_date DATE NOT NULL,
    volume BIGINT NOT NULL,
    zscore FLOAT NOT NULL,
    suspicion_score FLOAT NOT NULL,
    flag_type VARCHAR(50) NOT NULL,
    announcement_date DATE,
    days_before_announcement INTEGER,
    created_at TIMESTAMPTZ NOT NULL,
    UNIQUE(ticker, market, trade_date, flag_type)
);

CREATE TABLE announcements (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(255) NOT NULL,
    market VARCHAR(50) NOT NULL,
    announcement_date DATE NOT NULL,
    announcement_type VARCHAR(50) NOT NULL,
    description TEXT,
    price_change_pct FLOAT,
    created_at TIMESTAMPTZ NOT NULL,
    UNIQUE(ticker, announcement_date, announcement_type)
);

CREATE TABLE reddit_sentiment (
    id SERIAL PRIMARY KEY,
    ticker VARCHAR(255) NOT NULL,
    date DATE NOT NULL,
    mention_count INTEGER NOT NULL,
    sentiment_score FLOAT NOT NULL,
    top_subreddit VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL,
    UNIQUE(ticker, date)
);