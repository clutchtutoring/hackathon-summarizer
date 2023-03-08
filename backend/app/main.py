from fastapi import FastAPI, Request
from functools import lru_cache
from rq import Queue, Retry
from redis import Redis

from .config import Settings
from .models import models
from .jobs.summarize import process_summary

app = FastAPI()

@lru_cache()
def get_settings():
    return Settings()

# Setup Redis Queue
settings = get_settings()
app.state.redis = Redis.from_url(settings.redis_url)
app.state.task_queue = Queue(connection=app.state.redis)

@app.get("/")
async def root():
    return { "status": "up" }

@app.post('/startSummaryJob')
async def start_summary_job(request: Request, data: models.Job):
    job = request.app.state.task_queue.enqueue(
        process_summary,
        retry=Retry(max=3, interval=[10, 30, 60]),
        kwargs={
            'id': data.id,
            'videoAssets': data.videoAssets
        }
    )

    return { 'jobId': job.get_id() }
