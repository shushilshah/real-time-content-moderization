import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0)

QUEUE_NAME = "moderation_queue"


def send_to_queue(data: dict):
    r.lpush(QUEUE_NAME, json.dumps(data))
