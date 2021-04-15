from app.main.models import Wallet, Trade
from app.controllers.CoinController import CoinController
from app import db


class WalletController:

    def __init__(self, wallet: Wallet):
        self._wallet = wallet

    def __repr__(self):
        return f"<Wallet Controller {self.wallet.coin}; {self.wallet.amount}; {self.wallet.percent}%>"

    @property
    def wallet(self):
        return self._wallet
    
    @property
    def id(self):
        return self.wallet.id

    @property
    def coin(self):
        return CoinController(self.wallet.coin)

    @property
    def percent(self):
        return self.wallet.percent

    @property
    def amount(self):
        return self.wallet.amount

    @property
    def trades(self):
        return self.wallet.trades

    @property
    def user(self):
        return self.wallet.user

    def convert_amount(self):
        coin = CoinController(self.wallet.coin)
        coin.get_price()

        return coin.price * self.wallet.amount

    def to_json(self):
        json = {
            "coin": self.coin.to_json(),
            "amount": self.amount,
            "percent": self.percent,
        }
        return json

    def buy(self):
        value = self.user.balance * (self.percent / 100)
        self.user.spend(value)
        amount = value / self.coin.price
        self.wallet.buy(amount)
        self.add_trade(Trade.BUY)

    def sell(self):
        value = self.coin.price * self.amount
        self.user.top_up(value)
        self.add_trade(Trade.SELL)
        self.wallet.sell(self.amount)

    def add_trade(self, transaction: str = Trade.BUY):
        trade = Trade(wallet=self.wallet, price=self.coin.price, amount=self.amount, transaction=transaction)
        db.session.add(trade)
        db.session.commit()
