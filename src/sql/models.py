from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sql.database import Base


class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True, index=True)
    drawer_id = mapped_column(ForeignKey("authors.id"))
    scenarist_id = mapped_column(ForeignKey("authors.id"))
    serie = Column(String, index=True)
    title = Column(String, index=True)
    editor = Column(String, index=True)
    published_date = Column(String, index=True)
    edition = Column(String, index=True)
    format = Column(String)
    ean = Column(String)
    image = Column(String)

    # drawers = Mapped["Author"] = relationship(back_populates="children")
    # scenarists = Mapped["Author"] = relationship(back_populates="children")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    nick_name = Column(String, index=True)
    biography = Column(String)
    activity = Column(String)
