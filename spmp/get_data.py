from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
import pandas as pd
import datetime

API_KEY = "your_api_key"
SECRET_KEY = "your_secret_key"

client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

request_params = StockBarsRequest(
    symbol_or_symbols=["AAPL"],
    timeframe=TimeFrame.Day,  # or Minute, Hour
    start=datetime.date(2024, 1, 1),
    end=datetime.date(2024, 3, 1)
)

barset = client.get_stock_bars(request_params)
df = barset.df.reset_index()

#store it in a csv file
df.to_csv("stock_price.csv", index=False)
