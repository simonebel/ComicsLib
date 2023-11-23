import logging
from typing import Any, List

from pydantic import BaseModel
from sqlalchemy import insert, orm, select, update

from sql import models, schemas
from sql.database import Base

logger = logging.getLogger()


class CrudModel:
    schema: BaseModel
    model: Base
    pk: str

    @classmethod
    def _model_pk(cls):
        return getattr(cls.model, cls.pk)

    @classmethod
    def _schema_pk(cls, schema: BaseModel):
        return getattr(schema, cls.pk)

    @classmethod
    def get_all(cls, db: orm.Session) -> List[BaseModel]:
        """
        Get a publication metadata by it id
        """
        return db.scalars(select(cls.model)).all()

    @classmethod
    def get_by_id(cls, db: orm.Session, id: Any) -> BaseModel:
        """
        Get a publication metadata by it id
        """
        return db.get(cls.model, id)

    @classmethod
    def get_by_ids(cls, db: orm.Session, ids: List[Any]) -> List[BaseModel]:
        """
        Get a publication metadata by it id
        """
        return db.scalars(select(cls.model).filter(cls._model_pk().in_(ids))).all()

    @classmethod
    def _safe_schema(cls, schema: BaseModel):
        if not isinstance(schema, cls.schema):
            if hasattr(schema, "__name__"):
                class_got = getattr(schema, "__name__")
            else:
                class_got = schema.__class__.__name__
            raise ValueError(
                f"Wrong schema class, got <{class_got}> should be <{cls.schema.__name__}>"
            )
        return True

    @classmethod
    def create(cls, db: orm.Session, schema: BaseModel) -> bool:
        """
        Add a publication metadata to the db.
        """
        if cls._safe_schema(schema):
            db_model = cls.model(
                **schema.dict(),
            )

            record_exist = cls.get_by_id(db, cls._schema_pk(schema)) is not None

            if not record_exist:
                db.add(db_model)
                db.commit()
                db.refresh(db_model)
                logger.info(
                    f"{cls.schema.__name__} id: {cls._schema_pk(schema)} successfully added"
                )
                return True

            logger.warning(
                f"{cls.schema.__name__} id: {cls._schema_pk(schema)} is already in the db"
            )
            return False

    @classmethod
    def bulk_create(cls, db: orm.Session, schemas: List[BaseModel]) -> bool:
        """
        Bulk upload datasets to the db.
        """
        filtered_schemas = [
            schema.dict()
            for schema in schemas
            if not cls.get_by_id(db, cls._schema_pk(schema))
            and cls._safe_schema(schema)
        ]

        logger.info(f"Inserting {len(filtered_schemas)} {cls.schema.__name__}s")
        if filtered_schemas:
            db.execute(insert(cls.model), filtered_schemas)
            db.commit()
            return True
        return False

    @classmethod
    def exists(cls, db: orm.Session, id: Any) -> bool:
        return cls.get_by_id(db, id) is not None

    @classmethod
    def delete(cls, db: orm.Session, id: Any) -> bool:
        """
        Delete a publication metadata from the db
        """
        schema = cls.get_by_id(db, id)
        if schema is not None:
            db.delete(schema)
            db.commit()
            logger.info(f"{cls.schema.__name__} id: {id} deleted")
            return True

        logger.error(f"{cls.schema.__name__} id: {id} does not exists in the database")
        return False

    @classmethod
    def bulk_delete(cls, db: orm.Session, ids: List[str]) -> bool:
        db.query(cls.model).filter(cls._model_pk().in_(ids)).delete(
            synchronize_session=False
        )
        db.commit()
        logger.info(f"{len(ids)} {cls.schema.__name__} deleted")
        return True

    @classmethod
    def update(cls, db: orm.Session, id: str, updated_schema: BaseModel) -> bool:
        """
        Update a record from the db
        """
        stmt = select(cls.model).where(cls._model_pk() == id)

        record = db.scalar(stmt)

        if record:
            db.execute(
                update(cls.model)
                .where(cls._model_pk() == id)
                .values(
                    {
                        field: value
                        for field, value in updated_schema.dict().items()
                        if value is not None
                    }
                )
            )
            db.commit()
            logger.info(f"{cls.schema.__name__}  successfully updated")
            return True

        logger.warning(f"{cls.schema.__name__} is not in the db")
        return False

    @classmethod
    def bulk_update(cls, db: orm.Session, updated_schemas: List[BaseModel]) -> bool:
        """
        Update a record from the db
        """
        db.execute(update(cls.model), [schema.dict() for schema in updated_schemas])
        db.commit()
        logger.info(
            f"{len(updated_schemas)} {cls.schema.__name__} successfully updated"
        )
        return True


class AssociationCrudModel(CrudModel):
    schema: BaseModel
    model: Base
    pk_1: Any
    pk_2: Any

    @classmethod
    def _model_pk(cls, pk: str):
        return getattr(cls.model, pk)

    @classmethod
    def _schema_pk(cls, schema: BaseModel, pk: str):
        return getattr(schema, pk)

    @classmethod
    def get(cls, db: orm.Session, schema: BaseModel):
        return db.get(
            cls.model,
            (
                cls._schema_pk(schema, cls.pk_1),
                cls._schema_pk(schema, cls.pk_2),
            ),
        )

    @classmethod
    def exists(cls, db: orm.Session, schema: BaseModel) -> bool:
        return cls.get(db, schema) is not None

    @classmethod
    def create(
        cls,
        db: orm.Session,
        schema: BaseModel,
    ) -> bool:
        """
        Add a new link between an user and a twitter account to the db.
        """

        link = cls.get(db, schema)

        if not link:
            db_link = cls.model(**schema.dict())
            db.add(db_link)
            db.commit()
            db.refresh(db_link)
            logger.info(f"{cls.schema.__name__} {schema} is added to the db")
            return True

        logger.warning(f"{cls.schema.__name__} {schema} is already on the db")
        return False

    @classmethod
    def delete(cls, db: orm.Session, schema: BaseModel) -> bool:
        """
        Delete a link between an user and a twitter account to the db.
        """
        link = cls.get(db, schema)

        if link:
            db.delete(link)
            db.commit()
            logger.info(f"{cls.schema.__name__} {schema} is removed from the db")
            return True

        logger.warning(f"{cls.schema.__name__} {schema} is not int the db")
        return False

    @classmethod
    def get_by_id(cls, db: orm.Session, id: Any) -> BaseModel:
        """
        Get a publication metadata by it id
        """
        raise NotImplementedError

    @classmethod
    def get_by_ids(cls, db: orm.Session, ids: List[Any]) -> List[BaseModel]:
        """
        Get a publication metadata by it id
        """
        raise NotImplementedError

    @classmethod
    def _safe_schema(cls, schema: BaseModel):
        raise NotImplementedError

    @classmethod
    def bulk_create(cls, db: orm.Session, schemas: List[BaseModel]) -> bool:
        """
        Bulk upload datasets to the db.
        """
        raise NotImplementedError

    @classmethod
    def bulk_delete(cls, db: orm.Session, ids: List[str]) -> bool:
        raise NotImplementedError

    @classmethod
    def update(
        cls, db: orm.Session, schema: BaseModel, updated_schema: BaseModel
    ) -> bool:
        """
        Update a record from the db
        """

        record = cls.get(db, schema)
        if record:
            db.execute(
                update(cls.model)
                .where(
                    cls._model_pk(cls.pk_1) == cls._schema_pk(schema, cls.pk_1),
                    cls._model_pk(cls.pk_2) == cls._schema_pk(schema, cls.pk_2),
                )
                .values(
                    {
                        field: value
                        for field, value in updated_schema.dict().items()
                        if value
                    }
                )
            )
            db.commit()
            logger.info(f"{cls.schema.__name__}  successfully updated")
            return True

        logger.warning(f"{cls.schema.__name__} is not in the db")
        return False


class ToyCrud(CrudModel):
    """
    Interface for crud operations on the publications metadata
    """

    schema = schemas.Toy
    model = models.Toy
    pk = "id"
