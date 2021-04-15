from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))
    wallets = db.relationship("Wallet", backref="user", lazy="dynamic")
    balance = db.Column(db.Float(), default=0)

    def __repr__(self):
        return f"<User: {self.id}; {self.name}>"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def spend(self, amount):
        if amount > self.balance:
            raise Exception("cant spend more money than you have")
        self.balance -= amount
        db.session.commit()

    def top_up(self, amount):
        assert amount >= 0, "cant top up balance on negative value"
        self.balance += amount
        db.session.commit()


class Coin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), unique=True, index=True)
    price = db.Column(db.Float())
    wallets = db.relationship("Wallet", backref="coin", lazy="dynamic")

    def __repr__(self):
        return f"<Coin {self.symbol}; price={self.price}>"


class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    percent = db.Column(db.Float())
    amount = db.Column(db.Float())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    coin_id = db.Column(db.Integer, db.ForeignKey("coin.id"))
    trades = db.relationship("Trade", backref="wallet", lazy="dynamic")

    def __repr__(self):
        return f"<Wallet {self.coin.symbol}; {self.amount}; {self.percent}%>"

    def buy(self, value):
        assert value >= 0, "cant buy negative amount of coins"
        self.amount += value
        db.session.commit()

    def sell(self, value):
        assert value <= self.amount, "cant sell more than you have"
        self.amount -= value
        db.session.commit()


class Trade(db.Model):
    BUY = "buy"
    SELL = "sell"

    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallet.id"))
    price = db.Column(db.Float)
    amount = db.Column(db.Float)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    transaction = db.Column(db.String(10))

    def __repr__(self):
        return f"<Trade: {self.transaction} {self.amount} {self.wallet.coin.symbol} for {self.price*self.amount}$>"
