import repository.links
import secrets


class LinksServices():
    def __init__(self, repo: repository.links.LinksRepository):
        self.repo = repo

    def create_link(self, user_id, destination):
        slug = secrets.token_urlsafe(8)
        self.repo.CreateLink(user_id, destination, slug)
        return slug

    def get_links(self, user_id: int):
        return self.repo.GetLinks(user_id)

    def updat_links(self, user_id: int, NewDest: str, link_id: str):
        self.repo.UpdateLinks(
            user_id=user_id, link_id=link_id, NewDest=NewDest)

    def delete_link(self, user_id: int, links_id: str):
        self.repo.DeleteLinks(user_id=user_id, link_id=links_id)

    def get_link_by_slug(self, slug):
        return self.repo.GetLinkBySlug(slug)
