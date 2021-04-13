from app.main.models import User
from app import db
from pydantic import BaseModel
from typing import Optional

data = {
    "name": "Oleg",
    "email": "oleg@mail.ru",
    "password": 123,
}


class UserController(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: str
    password: Optional[str] = None

    @staticmethod
    def get_controller(data: dict):
        return UserController(**data)

    def _get_user(self):
        if self.id:
            user = User.query.get(id=self.id)
            return user
        elif self.email:
            user = User.query.filter(email=self.email).first()
            return user
        else:
            print("Invalid data")
            return None

    def register(self):
        user: User = self._get_user()
        if user:
            print("user with such email already exists")
            return

        user = User(email=self.email, name=self.name)
        user.set_password(self.password)
        db.session.add(user)
        db.session.commit()
        return user

    def auth(self):
        user: User = self._get_user()
        if not user:
            print("user not found")
            return

        if user.check_password(self.password):
            return user
        else:
            print("auth failed!")




user = UserController.get_controller(data)
print(user)
