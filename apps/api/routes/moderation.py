from fastapi import APIRouter, Depends, HTTPException
from apps.api.schemas.request import ModerationRequest
from apps.api.schemas.response import ModerationResponse
from sqlalchemy.orm import Session
from database.db import SessionLocal
from cache.redis_client import redis_client
from cache.rate_limiter import is_rate_limited
from core.logger import logger
import uuid
import json

from streaming.redis_client import send_to_queue

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/moderate", response_model=ModerationResponse)
def moderate(request: ModerationRequest, db: Session = Depends(get_db)):
    user_id = "default_user"
    request_id = str(uuid.uuid4())

    logger.info(f"Incoming request: {request.text}")

    # Rate limiting
    if is_rate_limited(user_id):
        raise HTTPException(status_code=429, detail="Too many requests")

    # Cache check
    cache_key = f"moderation:{request.text}"
    cached = redis_client.get(cache_key)

    if cached:
        logger.info("Cache hit")
        return json.loads(cached)

    logger.info("Cache miss -> sending to queue")

    # Send to Redis queue
    send_to_queue({
        "request_id": request_id,
        "text": request.text
    })

    # Immediate response (async processing)
    response = {
        "toxicity": 0.0,
        "label": "processing",
        "request_id": request_id,
        "action": "queued"
    }

    return response
