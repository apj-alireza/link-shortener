import utils.db
import repository.users
import repository.links
import services.users
import services.links
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from mysql.connector.errors import DatabaseError
from middleware.auth import user_auth as middleware
from fastapi.responses import RedirectResponse


DBconn = utils.db.connectDB()
user_repo = repository.users.UserRepository(DBconn)
user_service = services.users.UserService(user_repo)
links_repo = repository.links.LinksRepository(DBconn)
links_services = services.links.LinksServices(links_repo)


class User(BaseModel):
    username: str
    password: str


class Link(BaseModel):
    user_id: int
    destination: str


app = FastAPI()


@app.get("/users")
def get_user(user_id: int = Depends(middleware)):
    return {"user_id": user_id}


@app.post("/users/auth")
def user_authentication(user: User):
    try:
        return user_service.get_user(user.username, user.password)
    except repository.users.UserNotfound:
        raise HTTPException(404, "user not found!")


@app.post("/users")
def user_signup(user: User):

    try:
        user_service.create_user(user.username, user.password)
    except DatabaseError:
        raise HTTPException(status_code=409, detail="this user already exist")

    return {"username": user.username}


@app.post("/links")
def create_link(link: Link):
    slug = links_services.create_link(link.user_id, link.destination)
    return {"url": slug}


@app.get("/links")
def get_links(user_id: int = Depends(middleware)):
    return links_services.get_links(user_id)


@app.post("/links/update")
def update_link(newdest, link_id, user_id: int = Depends(middleware)):
    try:
        links_services.updat_links(
            NewDest=newdest, link_id=link_id, user_id=user_id)
    except DatabaseError:
        raise HTTPException(status_code=404)
    return {"message": "link updated successfully!"}


@app.post("/links/delete")
def delete_link(link_id, user_id: int = Depends(middleware)):
    try:
        links_services.delete_link(user_id=user_id, links_id=link_id)
    except DatabaseError:
        raise HTTPException(status_code=404)

    return {"message": "link deleted successfully!"}


@app.get("/r/{slug}")
def redirect(slug: str):
    try:
        link = links_services.get_link_by_slug(slug)
    except DatabaseError:
        raise HTTPException(status_code=404)

    return RedirectResponse(
        url=link,
        status_code=307)
