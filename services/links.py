import repository.links
import secrets
from logger_config import logger
from mysql.connector.errors import DatabaseError
from redis import Redis
from services.ratelimit import SlidingWindow


class RateLimitPassed(Exception):
    pass


class LinksServices():
    def __init__(
        self,
        repo: repository.links.LinksRepository,
        redis: Redis,
        rate_limiter=SlidingWindow,
    ):
        self.repo = repo
        self.redis = redis
        self.rate_limiter = rate_limiter

    def create_link(self, user_id, destination):
        logger.info(f"create link for {destination}")
        slug = secrets.token_urlsafe(8)
        try:
            self.repo.CreateLink(user_id, destination, slug)
        except DatabaseError as err:
            logger.error(f"error:{err}")
            raise err
        logger.info(f"created link: {slug}")
        return slug

    def get_links(self, user_id: int):
        return self.repo.GetLinks(user_id)

    def updat_links(self, user_id: int, NewDest: str, link_id: str):
        self.repo.UpdateLinks(
            user_id=user_id, link_id=link_id, NewDest=NewDest)

    def delete_link(self, user_id: int, links_id: str):
        self.repo.DeleteLinks(user_id=user_id, link_id=links_id)

    def get_link_by_slug(self, slug):
        ok = self.rate_limiter.allow_request(slug)
        if not ok:
            logger.info("limit passed!")
            raise RateLimitPassed
        print(slug)
        cache_value = self.redis.get(slug)
        print(cache_value)
        if cache_value is None:
            logger.info("not found in redis. reading from db.")
            dest = self.repo.GetLinkBySlug(slug)[0]
            self.redis.set(slug, dest, ex=1800)
            return dest
        else:
            logger.info("returning from redis.")
            return self.redis.get(slug)
