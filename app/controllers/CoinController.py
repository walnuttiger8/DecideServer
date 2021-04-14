from app.main.models import Coin
from app.controllers.BinanceController import BinanceController
from app import db


class CoinController:

    def __init__(self, coin: Coin):
        self._coin = coin

    def __repr__(self):
        return f"<Coin {self._coin.symbol}; price={self._coin.price}>"

    @property
    def symbol(self) -> str:
        return self._coin.symbol

    @property
    def coin(self):
        return self._coin

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

    def get_history(self):
        history = BinanceController.get_candlestick_data(self.symbol, limit=20)
        data = [h[4] for h in history]
        return data
