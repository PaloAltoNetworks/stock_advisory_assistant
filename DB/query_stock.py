import requests
import time
import os
import json
from typing import List
from pprint import pprint
from datetime import datetime, timedelta


def fetch_historical_stock_data(symbol: str, fromdate: str, todate: str):
    '''
    fromdate: 2025-01-01 
    todate: 2025-03-15
    '''
    url = f"https://api.nasdaq.com/api/quote/{symbol}/historical"
    params = {
        "assetclass": "stocks",
        "fromdate": fromdate,
        "todate": todate,
        "limit": 100,
        "random": 1
    }
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "origin": "https://www.nasdaq.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.nasdaq.com/",
        "sec-ch-ua": '"Not:A-Brand";v="24", "Chromium";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}

def fetch_historical_stock_data_multi(symbol_list: List, fromdate: str, todate: str):
    data = dict()
    for symbol in symbol_list:
        hist = fetch_historical_stock_data(symbol, fromdate, todate)
        data[symbol] = hist.get('data', {}).get("tradesTable", {}).get("rows", [])
        time.sleep(4)   # Pleae be nice to the server
    return data

def fetch_historical_stock_past_days(symbol_list: List, days: int):
    todate = time.strftime("%Y-%m-%d")
    fromdate = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    return fetch_historical_stock_data_multi(symbol_list, fromdate, todate)



def fetch_top_stocks(fromdate: str, todate: str):   
    stock_symbols = [
        "AAPL", "MSFT", "GOOGL", "AMZN"
    ] 
    os.makedirs("./downloaded", exist_ok=True)
    
    for symbol in stock_symbols:
        print(f"Fetching data for {symbol}...")
        data = fetch_historical_stock_data(symbol, fromdate, todate)
        
        file_path = f"./downloaded/{symbol}.json"
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        
        print(f"Saved {symbol} data to {file_path}")
        time.sleep(15)  # 10-second delay between requests


