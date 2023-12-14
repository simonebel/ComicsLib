from typing import Any, List, Set

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from sql.database import Base

PRIVATE_KEYS = {"_sa_instance_state"}


class Base(DeclarativeBase):
    def dict(self):
        obj = {}
        for key, value in self.__dict__.items():
            if key not in PRIVATE_KEYS:
                obj[key] = value

        return obj

    def __repr__(self) -> str:
        repr = f"({self.__class__.__name__} "
        for key, value in self.__dict__.items():
            if key not in PRIVATE_KEYS:
                repr += f"\n\t{key}: '{value}'"
        return repr + ")"


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    nick_name = Column(String, index=True)
    biography = Column(String)
    activity = Column(String)

    series: Mapped[Set["Serie"]] = relationship(
        secondary="author_serie_association",
        overlaps="scenarist, drawer, author_serie_association",
    )


class AuthorSerieAssociation(Base):
    __tablename__ = "author_serie_association"

    serie_id: Mapped[int] = mapped_column(ForeignKey("series.id"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)
    role = Column(Integer, index=True)


class Serie(Base):
    __tablename__ = "series"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    language = Column(String)
    # authors =
    # editors = Column(String, index=True)
    published_date = Column(String)
    status = Column(String)
    notes = Column(String)

    drawer: Mapped[Set[Author]] = relationship(
        "Author",
        secondary="author_serie_association",
        secondaryjoin="and_(Author.id == AuthorSerieAssociation.author_id, "
        "Serie.id == AuthorSerieAssociation.serie_id, "
        "AuthorSerieAssociation.role == 0)",
        overlaps="scenarist, author_serie_association",
    )

    scenarist: Mapped[Set[Author]] = relationship(
        "Author",
        secondary="author_serie_association",
        secondaryjoin="and_(Author.id == AuthorSerieAssociation.author_id, "
        "Serie.id == AuthorSerieAssociation.serie_id, "
        "AuthorSerieAssociation.role == 1)",
        overlaps="drawer, author_serie_association",
    )


class AuthorComicAssociation(Base):
    __tablename__ = "author_comic_association"

    comic_id: Mapped[int] = mapped_column(ForeignKey("comics.id"), primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), primary_key=True)
    role = Column(Integer, index=True)


class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True, index=True)
    serie_id: Mapped[int] = mapped_column(ForeignKey("series.id"), primary_key=True)
    title = Column(String, index=True)
    editor = Column(String, index=True)
    published_date = Column(String, index=True)
    edition = Column(String, index=True)
    format = Column(String)
    ean = Column(String)
    image = Column(String)
    synopsis = Column(String)

    serie: Mapped[Serie] = relationship("Serie")
