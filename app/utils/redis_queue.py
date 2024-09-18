import redis
from rq import Queue
from app.core.config import settings

redis_conn = redis.from_url(settings.REDIS_URL)
queue = Queue(connection=redis_conn)

def enqueue_task(task, *args, **kwargs):
    job = queue.enqueue(task, *args, **kwargs)
    return job.id

def pop_queue():
    job = queue.dequeue()
    return job