from app.main.models import User, Wallet
from app.controllers.CoinController import CoinController
from app import db
from pydantic import BaseModel
from typing import Optional

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
        return coin_wallet
