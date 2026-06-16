import utils.db
import repository.links
import services.links
from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel, HttpUrl
from mysql.connector.errors import DatabaseError
from middleware.auth import user_auth as middleware
from fastapi.responses import RedirectResponse

DBconn = utils.db.connectDB()
links_repo = repository.links.LinksRepository(DBconn)
links_services = services.links.LinksServices(links_repo)


class Link(BaseModel):
    original_url: HttpUrl


router = APIRouter(prefix="/links", tags=["links"])


@router.post("")
def create_link(link: Link, user_id: int = Depends(middleware)):
    try:
        slug = links_services.create_link(user_id, link.original_url)
    except DatabaseError:
        raise HTTPException(
            status_code=500, detail="failed!")

    return {"url": slug}


@router.get("")
def get_links(user_id: int = Depends(middleware)):
    return links_services.get_links(user_id)


@router.put("/{link_id}")
def update_link(newLink: Link, link_id, user_id: int = Depends(middleware)):
    try:
        links_services.updat_links(
            NewDest=str(newLink.original_url), link_id=link_id, user_id=user_id)
    except repository.links.InvalidLinkID:
        raise HTTPException(status_code=404)
    return {"message": "link updated successfully!"}


@router.delete("/{link_id}")
def delete_link(link_id, user_id: int = Depends(middleware)):
    try:
        links_services.delete_link(user_id=user_id, links_id=link_id)
    except repository.links.InvalidLinkID:
        raise HTTPException(status_code=404)

    return {"message": "link deleted successfully!"}


@router.get("/r/{slug}")
def redirect(slug: str):
    try:
        link = links_services.get_link_by_slug(slug)
    except DatabaseError:
        raise HTTPException(status_code=404)

    return RedirectResponse(
        url=link,
        status_code=307)
