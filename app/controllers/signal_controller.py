from app.controllers.model_controller import ModelController
from app.main.models import Coin
from app.controllers.coin_controller import CoinController as CC
from flask import current_app
import time


class SignalController:

    def __init__(self):
        pass

    def mainloop(self, app):
        app.app_context().push()

        CC.update_all_price()
        coins = list()
        for coin in Coin.query.all():
            if coin.wallets.count() > 0:
                coins.append(coin)

        for coin in coins:
            coin = CC(coin)
            prediction = coin.get_prediction()
            print(f"Coin: {coin.symbol}; price={coin.price}; pred-price={prediction}")

            if prediction > coin.price:
                for wallet in coin.wallets:
                    wallet.buy()
            else:
                for wallet in coin.wallets:
                    wallet.sell()
