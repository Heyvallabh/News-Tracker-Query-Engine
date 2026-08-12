# News Tracker & Query Engine

A Python pipeline that automatically fetches live news headlines across 
multiple categories, stores them over time in a SQLite database, and lets 
users search historical news by keyword, category, or date range.

## What it does

- Fetches top headlines from NewsAPI across 4 categories (business, health, 
  entertainment, technology) on a repeating schedule
- Stores each article with a timestamp, avoiding duplicate entries
- Provides a query interface to search stored news by keyword, category, 
  or date range
- Tracks user search activity in a separate table

## Tech stack

- Python 3
- SQLite3 (via Python's built-in `sqlite3` module)
- NewsAPI (external data source)
- `requests` for API calls
- `python-dotenv` for secure API key management

## Project structure

├── fetcher.py       # Fetches and stores news data (run this to build history)
├── query.py         # Search and query interface (run this to explore data)
├── .env             # Your API key (not included — see setup below)
├── .gitignore
└── README.md

## Setup

1. Clone this repo:
git clone <your-repo-url>
cd news-tracker

2. Install dependencies:
pip install requests python-dotenv

3. Get a free API key from [newsapi.org](https://newsapi.org)

4. Create a `.env` file in the project root:
MY_API_KEY=your_actual_key_here

## How to run

**To fetch and store news (run this first, let it run for a bit to build history):**
python fetcher.py

**To search stored news:**
python query.py

## What I learned building this

- Handling API authentication securely with environment variables
- Designing a SQLite schema for time-series data (tracking data over time, 
  not just single snapshots)
- Preventing duplicate database entries with pre-insert existence checks
- Building dynamic SQL queries that adapt based on which filters a user provides
- Defensive parsing of API responses to handle missing/null fields gracefully

## Possible improvements

- Automate the fetch cycle with a proper scheduler (cron/Task Scheduler) 
  instead of an in-script sleep loop
- Add a `UNIQUE` database constraint instead of manual duplicate-checking
- Support additional filters like source or country
