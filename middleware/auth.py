from fastapi import Request, HTTPException, Depends
import jwt
from utils.configs import JWT_SECRET_KEY


async def user_auth(request: Request):
    header = request.headers.get("Authorization")
    if not header:
        raise HTTPException(401, "missing token!")
    token = header.split(" ")[1]
    try:
        DecodedToken = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        user_id = DecodedToken["user_id"]
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(401, "invalid Token!")

    return user_id
