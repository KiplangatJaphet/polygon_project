import requests
import json
import pandas as pd

api_key = "zEXBgXeV8ByiYSUeGz76YVDybISza9nV"
symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
date = "2026-01-09"

def fetch_stock_data():
    all_symbol_data = []
    for symbol in symbols:
        api_url = f"https://api.massive.com/v1/open-close/{symbol}/{date}?adjusted=true&apiKey={api_key}"
        response = requests.get(api_url)
        if response.status_code != 200:
            print(f"Failed for {symbol}: {response.text}")
            continue
        
        data = response.json()
        
        data['symbol'] = symbol
        
        
        all_symbol_data.append(data)
    
    if all_symbol_data:
        df = pd.DataFrame(all_symbol_data)
        df = df.rename(columns={'from': 'date'})
        return df
    
    return pd.DataFrame()  # Return empty DataFrame if no data was fetched
        
if __name__ == "__main__":
    df = fetch_stock_data()
    if not df.empty:
        print(df[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']])

