from app.main.models import Wallet
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
    def coin(self):
        return CoinController(self.wallet.coin)

    @property
    def percent(self):
        return self.wallet.percent
    
    @property
    def amount(self):
        return self.wallet.amount

    def convert_amount(self):
        coin = CoinController(self.wallet.coin)
        coin.get_price()

        return coin.price * self.wallet.amount


