from functools import lru_cache
from redis import Redis
from rq import Queue, Connection
from rq.worker import Worker

from app.config import Settings

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
listen = ['default']

conn = Redis.from_url(settings.redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()