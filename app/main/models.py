from app import db
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import BaseModel


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))

    def __repr__(self):
        return f"<User: {self.id}; {self.username}>"

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
