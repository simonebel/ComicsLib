from typing import List

from sqlalchemy import Column, Integer

from sql.database import Base


class Toy(Base):
    __tablename__ = "toy"

    id = Column(Integer, primary_key=True, index=True)
