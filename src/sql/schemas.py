from typing import Optional

from pydantic import BaseModel

from api.comics.schemas import RequestComic
from utils.hash import hash_xxh


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
