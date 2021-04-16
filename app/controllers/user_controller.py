from app.main.models import User, Wallet, Trade
from app.controllers.CoinController import CoinController
from app.controllers.WalletController import WalletController
from app import db

data = {
    "name": "Oleg",
    "email": "oleg@mail.ru",
    "password": 123,
}


class UserController():

    def __init__(self, user: User):
        self._user = user

    @property
    def user(self):
        return self._user

    @property
    def balance(self):
        return self.user.balance

    @property
    def wallets(self):
        wallets = self.user.wallets
        return [WalletController(w) for w in wallets]
    
    @property
    def name(self):
        return self.user.name

    @property
    def trades(self):
        trades = list()
        for wallet in self.wallets:
            for trade in wallet.trades:
                trades.append(trade)
        return sorted(trades, key=lambda x: x.time)

    @property
    def email(self):
        return self.user.email

    def __repr__(self):
        return f"<User Controller {self.user.id}; {self.user.name}>"

    @staticmethod
    def from_db(user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        return UserController(user)

    def add_coin(self, coin: CoinController, percent=0):
        wallets = self._user.wallets
        coin_wallet = wallets.filter_by(coin=coin.coin).first()
        if not coin_wallet:
            coin_wallet = Wallet(coin_id=coin.coin.id, user_id=self.user.id, percent=percent, amount=0)
            db.session.add(coin_wallet)
        else:
            coin_wallet.percent = percent
        db.session.commit()
        return WalletController(coin_wallet)

    def get_overall_balance(self):
        balance = self.user.balance
        for wallet in self.wallets:
            balance += wallet.convert_amount()

        return balance

    def get_wallet(self, coin: CoinController):
        for wallet in self.wallets:
            if wallet.coin.coin.id == coin.coin.id:
                return wallet

    def buy(self, coin: CoinController):
        wallet = self.get_wallet(coin)
        if not wallet:
            return
        wallet.buy()

    def sell(self, coin: CoinController):
        wallet = self.get_wallet(coin)
        if not wallet:
            return
        wallet.sell()

