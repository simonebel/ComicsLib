from enum import Enum
from typing import Optional

from pydantic import BaseModel

from api.comics.schemas import RequestComic
from utils.hash import hash_xxh

# AUTHORS_ROLE_MAP = {
#     "dessinateur": 0,
#     "dessinatrice": 0,
#     "coloriste": 0,
#     "scénariste": 1,
# }

DRAWER = 0
SCENARIST = 1

AUTHORS_ROLE_MAP = {
    "scénario": 0,
    "dessin": 1,
    "couleurs": 2,
    "lettrage": 3,
    "textes": 4,
    "traduction": 5,
    "effets spéciaux": 6,
    "couverture": 7,
    "story-board": 8,
}


class AUTHORS_ROLE_MAP(Enum):
    pass


class Comic(BaseModel):
    id: int = None
    serie: str
    title: str
    drawer_id: int
    scenarist_id: int
    editor: str
    published_date: str
    edition: str
    format: str
    ean: str
    image: str

    def generate_id(self) -> None:
        """
        Generate a unique 32 bits based integer
        """
        self.id = hash_xxh(
            self.serie
            + self.title
            + str(self.drawer_id)
            + str(self.scenarist_id)
            + self.editor
            + self.published_date
        )

    @classmethod
    def from_request_comics(
        cls, request_comic: RequestComic, drawer_id: int, scenarist_id: int
    ):
        comic = {}
        forbidden_keys = set(["drawer", "scenarist", "image"])
        for key, value in request_comic.dict().items():
            if key not in forbidden_keys:
                comic[key] = value["text"]
            elif key == "image":
                comic[key] = value

        comic["drawer_id"] = drawer_id
        comic["scenarist_id"] = scenarist_id

        cls_comic = cls(**comic)
        cls_comic.generate_id()
        return cls_comic


class Author(BaseModel):
    id: Optional[int] = None
    first_name: str
    last_name: str
    nick_name: str
    biography: str
    activity: str

    def generate_id(self) -> None:
        """
        Generate a unique 32 bits based integer
        """
        self.id = hash_xxh(self.first_name + self.last_name + self.nick_name)


class Serie(BaseModel):
    id: int
    name: str
    editor: str
    published_date: str
    edition: str
    format: str
    ean: str
    image: str
    synopsis: str


class AuthorSerieAssociation(BaseModel):
    serie_id: int
    author_id: int
    role: int
