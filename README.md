# Telegram Gifts Analyzer

Telegram Gifts Analyzer - CLI application for collecting and analyzing statistics on gift sales in Telegram via the tonnelmp API. The script receives data on gift sales, calculates the main indicators and saves the report in Excel.

---

## [IMPORTANT] Where to get Auth Data

API tonnelmp requires your authentication data from tonnel, so don’t skip this section.

How to get your access key (Auth Data):

1. Go to market.tonnel.network and log in to your account
2. Open your browser console (Ctrl + Shift + C on Windows)
3. Navigate to the Application tab → Storage → Local Storage → select https://market.tonnel.network/
4. Find the entry with the key web-initData
5. Copy the entire value next to web-initData — this is your Auth Data

## What to do with AuthData?
In the main.py file, insert your authorization key:
```
myAuthData = "<your Auth Data here>"
```
---
## What does the project do?
- Retrieves gift sales history via the tonnelmp API
- Calculates price statistics: sales count, median, average, maximum, minimum, and range
- Saves raw data and summary statistics into an Excel file with multiple sheets



