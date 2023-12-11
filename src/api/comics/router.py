from urllib.request import urlretrieve

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.comics.schemas import RequestComic, RequestURL
from api.comics.utils import donwload_img
from conf.base import IMAGE_FOLDER
from search.requests import getAuthorData, getComicData, search
from sql import crud
from sql.database import get_db
from sql.schemas import Author, Comic

router = APIRouter()


@router.get("/comics/data", tags=["comics"])
def get_comics_list(query: str):
    return search(query)


@router.post("/comics/data", tags=["comics"])
def get_comic_data(url: RequestURL):
    return getComicData(url.url)


@router.post("/comics/create", tags=["comics"])
def create_comic(comic: RequestComic, db: Session = Depends(get_db)):
    drawer_meta = getAuthorData(comic.drawer["url"])
    scenarist_meta = getAuthorData(comic.scenarist["url"])

    drawer = Author(**drawer_meta)
    scenarist = Author(**scenarist_meta)

    drawer.generate_id()
    scenarist.generate_id()

    crud.Author.create(db, drawer)
    crud.Author.create(db, scenarist)

    print(comic.image)

    comic = Comic.from_request_comics(comic, drawer.id, scenarist.id)

    img_path = donwload_img(comic.image, comic.id)

    print(img_path)

    if img_path:
        comic.image = img_path

    is_created = crud.Comic.create(db, comic)

    if is_created:
        return "success"
    else:
        return HTTPException(
            status_code=401,
            detail="Can't add these comic to the db",
        )


@router.post("/authors/create", tags=["comics"])
def create_author(author: Author, db: Session = Depends(get_db)):
    return crud.Author.create(db, author)


@router.get("/comics/all", tags=["comics"])
def get_comics_in_db(db: Session = Depends(get_db)):
    return [comic.dict() for comic in crud.Comic.get_all(db)]
