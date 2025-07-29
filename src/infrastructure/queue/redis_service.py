import redis
import os
import json
from domain.documents.services import IQueueService

class RedisQueueService(IQueueService):
    def __init__(self):
        self.redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379)

    def publish_analysis_task(self, task_payload: dict):
        self.redis_client.lpush('tasks_queue', json.dumps(task_payload))