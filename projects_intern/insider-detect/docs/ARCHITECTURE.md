# Architecture — Insider Trading Detection System

A data pipeline that continuously ingests stock market data and insider trading filings across multiple countires, detects statistically abnormal trading activity in the days before major announcments, scores each suspious event, and displays flagged trades on a live dashboard. 

## What this system does?
This system is a data pipeline that will be running 24/7 on my server, continously pulling stock market data and insider trading filings from multiple countires. The system will be analyzing/tracking trading activity in the days before major companies announce the increase/decrease such as earnings, mergers, aquisitions and flags trades that are statistically abnormal. Each flagged trade gets a suspicious score based on how abnormal the volume was, how close to the major company announcment it happened and whether the required filing was late or missing. Everything is displayed on a live dashboard.

## Why this problem matters? 
While insider trading is illegal in most countries, it is very hard to catch/trace into smaller markets such as Eastern Europe, the Balkans, Southeast Asia as they are almost completely unwatched and insiders know it. Regulators are quite understaffed and always focusing mostly on countries like US, UK. Existing tools are manual, slow, and limited to one country at a time. This system automates detection across multiple markets simultaneously, targeting exactly the places where oversight is weakest.

## System Components

**The Data SOurce**- External APIs thet data will be pulled from. Stock prices, yfinance, insider trading filings from the SEC EDGAR API, and news/announcements from NewsAPI
**Ingestion Layer**- The code that runs on a schedule and fetches data from each source. Built with Apache Airflow- think of it as an alarm clock that triggers our fetching code every few hours.
**Raw Storage**- Before processing anything, save the original data to AWS S3. If something breaks, we can always go back to the original.
**Transformation Layer**- Cleans the raw data, aligns dates, fills gaps, and prepares it for analysis. Built with pandas.
**Analytics Layer** — The brain of the system. Calculates z-scores, detects volume spikes, scores each suspicious trade, and writes flags to the database.
**Database**- PostgreSQL stores everything in structured tables — raw trades, filings, flags, scores.
**API**- FastAPI serves the processed data to the dashboard through clean endpoints.
**Dashboard**- A live webpage built with Django and Chart.js that displays flagged trades, suspicion scores, and volume charts.
**Infrastructure**- Docker keeps every component isolated and running consistently. GitHub Actions runs tests automatically on every code change.

## DATA FLOW 

Data Source-> Ingestion Layer -> Raw Storage (S3) -> Transformation Layer -> Analystic Layer -> Database -> API-> Dashboard 

## Market Coverage

