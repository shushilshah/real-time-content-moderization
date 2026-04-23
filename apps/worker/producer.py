import redis
import json

r = redis.Redis(host="localhost", port=6379, db=0)

def send_to_queue(data):
    r.lpush("moderation_queue", json.dumps(data))