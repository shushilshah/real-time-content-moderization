from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.crud.moderation_log import get_log_by_request_id

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/result/{request_id}")
def get_result(request_id: str, db: Session = Depends(get_db)):
    log = get_log_by_request_id(db, request_id)

    if not log:
        return {
            "request_id": request_id,
            "status": "processing"
        }

    return {
        "request_id": request_id,
        "status": "completed",
        "toxicity": log.toxicity,
        "label": log.label,
        "action": log.action
    }