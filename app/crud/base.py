from typing import Any, Generic, Type, TypeVar, Optional

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Generic Method to Implement Basic Create Read Update and Delete Operations"""

    def __init__(self, model: Type[ModelType]) -> None:
        """Intialization Method, Specify The SQLALCHEMY Model

        Args:
            model (Type[ModelType]): Sqlalchemy Model
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType] | None:
        product_db = db.query(self.model).filter(self.model.id == id).first()
        if product_db:
            return product_db
        else:
            return None

    def get_many(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 25,
    ) -> list[ModelType]:
        """Get List of ModelType

        Args:
            db (Session): sqlalchemy DataBase Session Object
            skip (int, optional): DataBase Offset. Defaults to 0.
            limit (int, optional): Limit of the data. Defaults to 25.

        Returns:
            list[ModelType]: Returns a list of ModelType
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Create new ModelType and Commit on DB

        Args:
            db (Session): sqlalchemy DataBase Session Object
            obj_in (CreateSchemaType): Create Schema Type,
                pydantic Base model or a dict

        Returns:
            ModelType: Returns the Created Model
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """Update Existing Row on DB

        Args:
            db (Session): sqlalchemy DataBase Session Object
            db_obj (ModelType): Data From the DataBase
            obj_in (UpdateSchemaType | dict[str, Any]): Updated Data
                pydantic BaseModel or an Dictionary

        Returns:
            ModelType: Returns the Updated Model Type object
        """
        db_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in db_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> ModelType | None:
        """Delete an existing ModelType from DB

        Args:
            db (Session): sqlalchemy DataBase Session Object
            id (int): id of the ModelType Object

        Returns:
            ModelType | None: if the id present in DB
                then delete and returns object
                else return None
        """
        obj = self.get(db, id)

        db.delete(obj)
        db.commit()
        return obj
