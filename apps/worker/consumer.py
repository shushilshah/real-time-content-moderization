from kafka import KafkaConsumer
import json
from streaming.topics import MODERATION_TOPIC
from models.inference.predictor import predictor
from database.db import SessionLocal
from database.crud.moderation_log import create_log
from core.logger import logger
import requests

#create kafka consumer
consumer= KafkaConsumer(
    MODERATION_TOPIC,
    # bootstrap_servers="localhost:9092",
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="moderation-group",
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)

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

    logger.info(f"Proceessing message: {text}")

    # ML prediction
    result = predictor.predict(text)
    score = result['score']

    label = "toxic" if score > 0.6 else "clean"
    action = decide_action(score)

    # save to database
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
    logger.info("Kafka Consumer Started.....")

    for msg in consumer:
        try:
            process_message(msg.value)
        except Exception as e:
            logger.error(f"Error Processing messsage: {e}")

if __name__ == "__main__":
    main()