from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
from rq import Queue, Retry
from rq.job import Job
from redis import Redis
from os import os

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

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return { "status": "up" }

@app.post('/startSummaryJob')
async def start_summary_job(request: Request, data: models.SummarizeJob):
    job = request.app.state.task_queue.enqueue(
        process_summary,
        retry=Retry(max=3, interval=[10, 30, 60]),
        kwargs={
            'id': data.id,
            'videoAssets': data.videoAssets
        }
    )

    return { 'jobId': job.get_id() }

@app.get("/getSummary/{content_id}")
async def get_summary(content_id: int):
    dir = os.path.dirname(__file__)
    file_path = os.path.join(dir, f"/assets/summaries/{content_id}.txt") # assuming file name is same as id
    try:
        with open(file_path, "r") as f:
            file_content = f.read()
            return {"file_content": file_content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")


@app.get("/checkStatus/{job_id}")
async def get_job(request: Request, job_id: int):
    job_data = Job.fetch('my_job_id', connection=request.app.state.redis)
    if job_data is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_data.decode('utf-8')
