from fastapi import FastAPI
import requests
from dotenv import load_dotenv
from os import getenv

app = FastAPI()

load_dotenv('alpha_vantage.env')
API_KEY = getenv('AV_API_KEY',"")

@app.get("/stock/{symbol}")
def get_stock_data(symbol: str, interval: str = "5min"):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch data"}
    
    data = response.json()
    
    if "Time Series" not in data:
        return {"error": "Invalid response from Alpha Vantage"}
    
    time_series_key = f"Time Series ({interval})"
    stock_data = [
        {
            "timestamp": timestamp,
            "open": values["1. open"],
            "high": values["2. high"],
            "low": values["3. low"],
            "close": values["4. close"],
            "volume": values["5. volume"]
        }
        for timestamp, values in data[time_series_key].items()
    ]
    
    return stock_data
