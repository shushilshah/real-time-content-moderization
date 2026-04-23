import redis
import json
from models.inference.predictor import predictor
from database.db import SessionLocal
from database.crud.moderation_log import create_log
from core.logger import logger
import requests

# 🔁 Create Redis client
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

QUEUE_NAME = "moderation_queue"


def decide_action(score: float) -> str:
    if score > 0.85:
        return "blocked"
    elif score > 0.6:
        return "review"
    else:
        return "allowed"


def process_message(message):
    request_id = message['request_id']
    text = message['text']

    logger.info(f"Processing message: {text}")

    # 🤖 ML prediction
    result = predictor.predict(text)
    score = result['score']

    label = "toxic" if score > 0.6 else "clean"
    action = decide_action(score)

    # 💾 Save to database
    db = SessionLocal()
    try:
        create_log(
            db=db,
            request_id=request_id,
            text=text,
            toxicity=score,
            label=label,
            action=action
        )
    finally:
        db.close()

    # 🔔 Notify API
    try:
        requests.post(
            "http://127.0.0.1:8000/internal/result",
            json={
                "request_id": request_id,
                "toxicity": score,
                "label": label,
                "action": action
            },
            timeout=5
        )
    except Exception as e:
        logger.error(f"Failed to notify API: {e}")

    logger.info(f"Processed -> score: {score}, action: {action}")
    logger.info(f"Consumer ID -> {request_id}")


def main():
    logger.info("Redis Consumer Started.....")

    while True:
        try:
            # ⏳ Blocking wait for message
            _, message = r.brpop(QUEUE_NAME)

            # Convert JSON string → dict
            data = json.loads(message)

            process_message(data)

        except Exception as e:
            logger.error(f"Error processing message: {e}")


if __name__ == "__main__":
    main()
