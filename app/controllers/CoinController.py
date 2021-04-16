from app.main.models import Coin
from app.controllers.BinanceController import BinanceController
from app import db, model


class CoinController:

    def __init__(self, coin: Coin):
        self._coin = coin

    def __repr__(self):
        return f"<Coin {self._coin.symbol}; price={self.price}>"

    @property
    def symbol(self) -> str:
        return self._coin.symbol

    @property
    def coin(self):
        return self._coin

    @property
    def price(self):
        return self.coin.price

    def get_price(self):
        price: float = BinanceController.get_price(self.symbol)
        if not price:
            return
        self._coin.price = price
        db.session.commit()

    @staticmethod
    def from_db(coin_id: int = None, symbol: str = None):
        coin = None
        if coin_id:
            coin = Coin.query.get(coin_id)
        elif symbol:
            coin = Coin.query.filter_by(symbol=symbol).first()

        if not coin:
            return None
        return CoinController(coin)

    def get_history(self, limit=10, interval="1h"):
        history = BinanceController.get_candlestick_data(self.symbol, limit=limit, interval=interval)
        data = [h[4] for h in history]
        return data

    def get_prediction(self):
        data = self.get_history()
        return model.predict(data)

    def to_json(self):
        json = {
            "symbol": self.symbol,
            "price": self.price,
        }
        return json

    @staticmethod
    def update_all_price():
        symbols = BinanceController.get_symbols_price()
        symbols = list(filter(lambda symbol: symbol["symbol"].endswith("USDT"), symbols))
        for symbol in symbols:
            coin = CoinController.from_db(symbol=symbol["symbol"])
            if not coin:
                continue
            coin.coin.price = symbol["price"]
        db.session.commit()
