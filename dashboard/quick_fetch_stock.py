import requests
import pandas as pd
from os import getenv
from sys import argv
from dotenv import load_dotenv

load_dotenv('alpha_vantage.env')
API_KEY = getenv('AV_API_KEY',"")
STOCK_SYMBOL = argv[1]
URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK_SYMBOL}&interval=5min&apikey={API_KEY}"

response = requests.get(URL)
data = response.json()
print(data)

# Convert to DataFrame
df = pd.DataFrame.from_dict(data["Time Series (5min)"], orient="index")
df.columns = ["Open", "High", "Low", "Close", "Volume"]
df.to_csv(argv[2], index=True)
