from app.main.models import Wallet, Trade
from app.controllers.coin_controller import CoinController
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

    @staticmethod
    def from_db(wallet_id):
        wallet = Wallet.query.get(wallet_id)
        if not wallet:
            return None
        return WalletController(wallet)

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
        amount = value / self.coin.price
        if amount > 0.0001:
            self.user.spend(value)
            self.wallet.buy(amount)
            self.add_trade(Trade.BUY, amount)

    def sell(self):
        value = self.coin.price * self.amount
        if value:
            self.user.top_up(value)
            self.add_trade(Trade.SELL)
            self.wallet.sell(self.amount)

    def get_profit(self):
        profit = 0
        for trade in self.trades:
            if trade.transaction == Trade.BUY:
                profit -= trade.price * trade.amount
            elif trade.transaction == Trade.SELL:
                profit += trade.price * trade.amount

        profit += self.amount * self.coin.price
        return profit

    def add_trade(self, transaction: str = Trade.BUY, amount=None):
        amount = amount or self.amount
        trade = Trade(wallet=self.wallet, price=self.coin.price, amount=amount, transaction=transaction)
        db.session.add(trade)
        db.session.commit()

    def sltp(self):
        """
        Stop loss & Take profit

        :return:
        """
        if self.amount < 0.0001:
            return
        profit = self.get_profit()
        profit_percent = (abs(profit) / (self.amount * self.coin.price)) * 100
        if self.wallet.take_profit and profit > 0 and profit_percent >= self.wallet.take_profit:
            self.sell()
            print(f"take profit {self.wallet}, for {self.user} profit: {profit}; {self.amount}")
        elif self.wallet.stop_loss and profit < 0 and profit_percent >= self.wallet.stop_loss:
            self.sell()
            print(f"stop loss {self.wallet}, for {self.user} loss: {profit}; {self.amount}")
