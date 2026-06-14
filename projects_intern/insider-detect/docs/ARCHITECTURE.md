# Architecture — Insider Trading Detection System

A data pipeline that continuously ingests stock market data and insider trading filings across multiple countires, detects statistically abnormal trading activity in the days before major announcments, scores each suspious event, and displays flagged trades on a live dashboard. 

## What this system does?
This system is a data pipeline that will be running 24/7 on my server, continously pulling stock market data and insider trading filings from multiple countires. The system will be analyzing/tracking trading activity in the days before major companies announce the increase/decrease such as earnings, mergers, aquisitions and flags trades that are statistically abnormal. Each flagged trade gets a suspicious score based on how abnormal the volume was, how close to the major company announcment it happened and whether the required filing was late or missing. Everything is displayed on a live dashboard.

## Why this problem matters? 
While insider trading is illegal in most countries, it is very hard to catch/trace into smaller markets such as Eastern Europe, the Balkans, Southeast Asia as they are almost completely unwatched and insiders know it. Regulators are quite understaffed and always focusing mostly on countries like US, UK. Existing tools are manual, slow, and limited to one country at a time. This system automates detection across multiple markets simultaneously, targeting exactly the places where oversight is weakest.
