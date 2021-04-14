from app.main import bp
from flask import jsonify, request
from app.main.models import User
from app import db


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
    #  email, password
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify(success=0, results={}, message="Пользователь не найден")

    if user.check_password(password):
        return jsonify(success=1, result={"user_id": user.id}, message="Выполнен вход")

    return jsonify(success=0, result={}, message="Неверный пароль")

