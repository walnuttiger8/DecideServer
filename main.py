from app import create_app
from app import db
from app.main.models import User, Coin, Wallet

app = create_app()
app.app_context().push()
