from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import BaseModel


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))
    wallets = db.relationship("Wallet", backref="user", lazy="dynamic")

    def __repr__(self):
        return f"<User: {self.id}; {self.name}>"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


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

    def __repr__(self):
        return f"<Wallet {self.coin.symbol}; {self.amount}; {self.percent}%>"