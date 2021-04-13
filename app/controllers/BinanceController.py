import os
import requests


class BinanceController:
    _base_url = "https://api.binance.com"
    _api_key = "nPRAFgF0HRnzErDW8dmRDrrkM9UtPizzE24ECtR0Ombh2TnPzY4sscRBPEKQyaKCs"

    @staticmethod
    def get_candlestick_data(symbol: str, interval, start_time=None, end_time=None, limit: int = 100):
        url = "/api/v3/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "startTime": start_time,
            "end_time": end_time,
            "limit": limit
        }
        response = requests.get(BinanceController._base_url + url, params=params)
        return response.json()


if __name__ == "__main__":
    symbol = "ETHUSDT"
    interval = "15m"
    for data in BinanceController.get_candlestick_data(symbol, interval):
        print(data)
