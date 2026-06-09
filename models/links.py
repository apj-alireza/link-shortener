from dataclasses import dataclass


@dataclass
class Link:
    link_id: str
    destination_url: str
    slug: str
