import utils.db
import repository.users
import services.users
from fastapi import FastAPI, HTTPException, APIRouter, Depends
from pydantic import BaseModel
from mysql.connector.errors import DatabaseError
from middleware.auth import user_auth as middleware

DBconn = utils.db.connectDB()
user_repo = repository.users.UserRepository(DBconn)
user_service = services.users.UserService(user_repo)


class User(BaseModel):
    username: str
    password: str


router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def get_user(user_id: int = Depends(middleware)):
    return {"user_id": user_id}


@router.post("/auth")
def user_authentication(user: User):
    try:
        return user_service.get_user(user.username, user.password)
    except repository.users.UserNotfound:
        raise HTTPException(404, "user not found!")


@router.post("")
def user_signup(user: User):

    try:
        user_service.create_user(user.username, user.password)
    except DatabaseError:
        raise HTTPException(status_code=409, detail="this user already exist")

    return {"username": user.username}
