from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, select

from .models import Record


def create_record(session: Session, record: Record) -> Record:
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def get_records(session: Session, limit: int = 100) -> List[Record]:
    statement = select(Record).order_by(Record.created_at.desc()).limit(limit)
    return session.exec(statement).all()


def get_record(session: Session, record_id: int) -> Optional[Record]:
    return session.get(Record, record_id)


def update_record(session: Session, record: Record, **kwargs) -> Record:
    for key, value in kwargs.items():
        setattr(record, key, value)
    record.updated_at = datetime.utcnow()
    session.add(record)
    session.commit()
    session.refresh(record)
    return record


def delete_record(session: Session, record: Record) -> None:
    session.delete(record)
    session.commit() 