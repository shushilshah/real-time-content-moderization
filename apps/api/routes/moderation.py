# Auto-generated file
from fastapi import APIRouter, Depends, HTTPException
from apps.api.schemas.request import ModerationRequest
from apps.api.schemas.response import ModerationResponse
from models.inference.predictor import predictor
from sqlalchemy.orm import Session
from database.db import SessionLocal
from database.crud.moderation_log import create_log
from cache.redis_client import redis_client
from cache.rate_limiter import is_rate_limited
from core.logger import logger
from streaming.kafka_config import get_producer
from streaming.topics import MODERATION_TOPIC
import uuid

producer = None

if producer is None:
    producer = get_producer()

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: db.close()






# simple keyword based toxic words
TOXIC_WORDS = ['stupid', 'idiot', 'hate', 'kill', 'dumb']

def simple_toxicity_check(text: str) -> float:
    text_lower = text.lower()
    score = 0.0

    for word in TOXIC_WORDS:
        if word in text_lower:
            score += 0.2

    return min(score, 1.0)

def decide_action(score: float) -> str:
    if score > 0.8:
        return "blocked"
    elif score > 0.4:
        return "review"
    else: return "allowed"


@router.post("/moderate", response_model=ModerationResponse)
def moderate(request: ModerationRequest, db: Session = Depends(get_db)):
    user_id = "default_user"
    request_id = str(uuid.uuid4())
    logger.info(f"Incoming request: {request.text}")

    # rate limiting
    if is_rate_limited(user_id):
        raise HTTPException(status_code=429, detail="Too many requests")

    # send to kafka
    message = {
        "request_id": request_id,
        "user_id": user_id,
        "text": request.text
    }

    # producer.send(MODERATION_TOPIC, message)
    if producer:
        try:
            producer.send(MODERATION_TOPIC, message)
            logger.info("Message sent to Kafka")
        except Exception as e:
            logger.error(f"Kafka send failed: {e}")
    
    else:
        logger.warning("Kafka not available, skipping send")
        logger.info("Message sent to kafka")

    # temp fallback
    # cache key
    cache_key = f"moderation:{request.text}"

    cached = redis_client.get(cache_key)
    if cached:
        logger.info("Cache hit")
        import json
        return json.loads(cached)
    
    logger.info("Cache miss -> running model")

    # model intference
    # result = predictor.predict(request.text)

    # score = result["score"]


    # if score > 0.6:
    #     label="toxic"
    # else:
    #     label="clean"

    # action = decide_action(score)
    # logger.info(f"Prediction -> score: {score}, action: {action}")


    # save to database
    # create_log(
    #     db=db,
    #     text=request.text,
    #     toxicity=score,
    #     label=label,
    #     action=action
    # )

    # return ModerationResponse(
    #     toxicity=score,
    #     label=label,
    #     action=action
    # )
    return {
        "toxicity": 0.0,
        "label": "processing",
        "action": "queued"
    }
    # return {
    #     "request_id": request_id,
    #     "status": "processing"
    # }


    # cache result
    import json
    redis_client.set(cache_key, json.dumps(response), ex=60)

    return response