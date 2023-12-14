from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from sql import crud
from sql.database import get_db

router = APIRouter()


@router.get("/home/count", tags=["home"])
def get_comics_db_count(db: Session = Depends(get_db)):
    return len(crud.Comic.get_all(db))
