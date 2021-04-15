from flask import jsonify, request

from app import db
from app.main import bp
from app.main.models import User
from app.controllers.user_controller import UserController
from app.controllers.CoinController import CoinController


@bp.route("/", methods=["POST"])
def index():
    print(request.get_json())
    return jsonify({"data": "ok"})


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data["username"]
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(success=0, results={}, message="Пользователь с такой почтой уже зарегестрирован")
    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(success=1, results={"user_id": user.id}, message="Пользователь зарегестрирован")


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(success=0, results={}, message="Пользователь не найден")

    if user.check_password(password):
        return jsonify(success=1, results={"user_id": user.id}, message="Выполнен вход")

    return jsonify(success=0, results={}, message="Неверный пароль")


# Name: string; Email: string; Balance: float;
@bp.route("/get_user", methods=["POST"])
def get_user():
    data = request.get_json()
    user_id: int = data["user_id"]
    user = UserController.from_db(user_id)

    if not user:
        return jsonify(success=0, results={}, message="Пользователь не найден")

    user_data = {"Name": user.name, "Email": user.email, "Balance": user.balance}
    return jsonify(success=1, results=user_data, message="Пользователь получен успешно")


@bp.route("/get_wallet", methods=["POST"])
def get_wallet():
    data = request.get_json()

    if "symbol" in data and "user_id" in data:
        symbol = data["symbol"]
        user_id = data["user_id"]
    else:
        return jsonify(success=0, results={}, message="Некорректные данные")

    coin = CoinController.from_db(symbol=symbol)
    user = UserController.from_db(user_id)
    if not user:
        return jsonify(success=0, results={}, message="Пользователь не найден")
    if not coin:
        return jsonify(success=0, results={}, message="Монета не найдена")

    wallet = user.get_wallet(coin)

    if wallet:
        return jsonify(success=1, results=wallet.to_json(), message="Кошелек получен")
    jsonify(success=0, results={}, message="Кошелек не найден")


@bp.route("/add_coin", methods=["POST"])
def add_coin():
    data = request.get_json()
    percent = 100
    if "symbol" in data and "user_id" in data:
        symbol = data["symbol"]
        user_id = data["user_id"]
    else:
        return jsonify(success=0, results={}, message="Некорректные данные")

    if "percent" in data:
        percent = data["percent"]

    coin = CoinController.from_db(symbol=symbol)
    user = UserController.from_db(user_id)
    if not user:
        return jsonify(success=0, results={}, message="Пользователь не найден")
    if not coin:
        return jsonify(success=0, results={}, message="Монета не найдена")

    wallet = user.add_coin(coin, percent)

    if wallet:
        return jsonify(success=1, results=wallet.to_json(), message="Кошелек получен")
    jsonify(success=0, results={}, message="Кошелек не найден")


@bp.route("/get_wallets", methods=["POST"])
def get_wallets():
    data = request.get_json()

    if "user_id" in data:
        user_id = data["user_id"]
    else:
        return jsonify(success=0, results={}, message="Некорректные данные")

    user = UserController.from_db(user_id)
    if not user:
        return jsonify(success=0, results={}, message="Пользователь не найден")
    wallets = user.wallets
    results = list()

    for wallet in wallets:
        results.append(wallet.to_json())

    return jsonify(success=1, results=results, message="Успешно")


@bp.route("/get_trades", methods=["POST"])
def get_trades():
    data = request.get_json()

    if "user_id" in data:
        user_id = data["user_id"]
    else:
        return jsonify(success=0, results={}, message="Отсутствует user_id")

    user = UserController.from_db(user_id)
    if not user:
        return jsonify(success=0, results={}, message="Пользователь не найден")

    results = list()
    for trade in user.trades:
        results.append(trade.to_json())

    return jsonify(success=1, results=results, message="Успешно")
