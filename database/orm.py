import logging
from typing import Any, Union
from sqlalchemy.exc import IntegrityError
from .models import Todo
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

object_type_hint = Todo
objects_type_hints = list[Todo] | list


class ORMBase:

    def __init__(self, model):
        self.model = model

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, **object_data: dict):
        try:
            object_data = self.model(**object_data)
            db.add(object_data)
            db.commit()
            db.refresh(object_data)
            return object_data
        except IntegrityError:
            logging.info(f"Already added to the database.")

        except Exception as e:
            logging.error(f"An error occurred: {e}")

    def update(self, db: Session, id: int, **updated_data) -> object_type_hint:

        try:
            object = db.query(self.model).get(id)

            if not object:
                raise ValueError(f"{self.model.__name__} with ID {id} not found")

            # Update user fields selectively using object attributes
            for key, value in updated_data.items():
                if hasattr(object, key):  # Check if attribute exists
                    setattr(object, key, value)

            db.commit()
            return object
        except Exception as e:
            logging.error(f"An error occurred while updating user: {e}")
            raise  # Re-raise the exception for handling outside the function

    def delete(self, db: Session, id: int) -> Any:
        try:
            object = db.query(self.model).get(id)

            if object is not None:
                db.delete(object)
                db.commit()
                return True

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return False

    def all(self, db: Session) -> objects_type_hints:
        return db.query(self.model).all()

    def filter(self, db: Session, **filters) -> objects_type_hints:
        try:
            query = db.query(self.model)

            # Build dynamic query based on filter keywords
            conditions = []
            for key, value in filters.items():
                if hasattr(self.model, key):  # Check for valid filter field
                    conditions.append(getattr(self.model, key) == value)  # Basic comparison

            if "logic" in filters and filters["logic"].lower() == "or":
                query = query.filter(or_(*conditions))  # Combine filters with OR (default)
            else:
                query = query.filter(and_(*conditions))  # Combine filters with AND

            return query.all()  # Fetch all filtered objects
        except Exception as e:
            logging.error(f"An error occurred while filtering users: {e}")
            raise  # Re-raise the exception for handling outside the function

    def count(self, db: Session) -> int:
        return db.query(self.model).count()

    def get_or_create(self, db: Session, **data) -> object_type_hint:
        get = self.get(db, data["id"])
        if get is None:
            return self.create(db, **data)
        else:
            return get


TodoDB = ORMBase(model=Todo)
