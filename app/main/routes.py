from app.main import bp
from flask import jsonify, request


@bp.route("/", methods=["POST"])
def index():
    print(request.get_json())
    return jsonify({"data": "ok"})
