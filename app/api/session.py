from typing import Generator

from sqlalchemy.orm import Session

from app.db.session import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """This Function will work as
        dependency for get db object

    Yields:
        db (Generator[Session, None, None]): Sqlalchemy Session Object
    """
    try:
        db: Session = SessionLocal()
        yield db
    except Exception:
        db.rollback()
    finally:
        db.close()
