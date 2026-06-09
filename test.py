import requests
from utils.db import connectDB
import repository.links as repolinks

repolinks.LinksRepository.CreateLink(self=connectDB(),
                                     user_id=1, destination="google.com", slug="sdafkhfew;fh")


requests.Request
