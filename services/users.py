import repository.users
from models.user import User
import bcrypt
import jwt
import datetime
from utils.configs import JWT_SECRET_KEY


def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
    }

    token = jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm="HS256"
    )

    return token


class UserService():
    def __init__(self, repo: repository.users.UserRepository):
        self.repo = repo

    def create_user(self, username: str, password: str):
        passbytes = password.encode("utf-8")
        HashedPass = bcrypt.hashpw(passbytes, bcrypt.gensalt()).decode("utf-8")
        return self.repo.CreateUser(username, HashedPass)

    def get_user(self, username: str, password: str):
        UserInfo = self.repo.GetUser(username)
        HashedPass = str(UserInfo.Password)
        if bcrypt.checkpw(
            password.encode("utf-8"),
            HashedPass.encode("utf-8")
        ):
            return create_token(UserInfo.user_id)
        else:
            return ("wrong Password!")
