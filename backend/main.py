from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from typing import List

from .db import init_db, get_session
from .models import Record
from .crud import create_record, get_records, get_record, delete_record, update_record

app = FastAPI(title="Markdown Record System API")


# Initialize DB on startup
@app.on_event("startup")
def on_startup() -> None:
    init_db()


# Routes
@app.get("/records", response_model=List[Record])
def list_records(session: Session = Depends(get_session)):
    return get_records(session)


@app.get("/records/{record_id}", response_model=Record)
def read_record(record_id: int, session: Session = Depends(get_session)):
    db_obj = get_record(session, record_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_obj


@app.post("/records", response_model=Record, status_code=201)
def create_record_endpoint(record: Record, session: Session = Depends(get_session)):
    return create_record(session, record)


@app.put("/records/{record_id}", response_model=Record)
def update_record_endpoint(record_id: int, record: Record, session: Session = Depends(get_session)):
    db_obj = get_record(session, record_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Record not found")
    updated = update_record(session, db_obj, **record.dict(exclude_unset=True))
    return updated


@app.delete("/records/{record_id}", status_code=204)
def delete_record_endpoint(record_id: int, session: Session = Depends(get_session)):
    db_obj = get_record(session, record_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Record not found")
    delete_record(session, db_obj) 