from flask import jsonify, request

from app import db
from app.main import bp
from app.main.models import User
from app.controllers.user_controller import UserController


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
