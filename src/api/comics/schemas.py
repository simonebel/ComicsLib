from typing import Dict

from pydantic import BaseModel


class RequestURL(BaseModel):
    url: str


class RequestComic(BaseModel):
    serie: Dict[str, str]
    title: Dict[str, str]
    drawer: Dict[str, str]
    scenarist: Dict[str, str]
    editor: Dict[str, str]
    published_date: Dict[str, str]
    edition: Dict[str, str]
    format: Dict[str, str]
    ean: Dict[str, str]
    image: str
