from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate(db)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.app_context().push()
    app.debug, app.testing = True, True  # don't forget to delete
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    @app.shell_context_processor
    def make_shell_context():
        from app.main.models import User, Coin, Wallet
        from app.controllers.WalletController import WalletController
        from app.controllers.CoinController import CoinController
        from app.controllers.user_controller import UserController
        return {'db': db, 'User': User, 'Coin': Coin, "Wallet": Wallet,
                "WC": WalletController, "CC": CoinController, "UC": UserController}

    return app
