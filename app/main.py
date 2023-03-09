import os
from functools import lru_cache
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from rq import Queue, Retry
from rq.job import Job
from rq.exceptions import NoSuchJobError
from redis import Redis
from .config import Settings
from .models import models
from .jobs.summarize import process_summary

app = FastAPI()

@lru_cache()
def get_settings():
    """Get settings from config"""
    return Settings()

# Setup Redis Queue
settings = get_settings()
app.state.redis = Redis.from_url(settings.redis_url)
app.state.task_queue = Queue(connection=app.state.redis)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Check if API is running"""
    return { "status": "up" }

@app.post('/startSummaryJob')
async def start_summary_job(request: Request, data: models.SummarizeJob):
    """Start summary job"""
    job = request.app.state.task_queue.enqueue(
        process_summary,
        retry=Retry(max=3, interval=[10, 30, 60]),
        kwargs={
            'content_id': data.id,
            'video_assets': data.videoAssets
        }
    )

    return { 'jobId': job.get_id() }

@app.get("/getSummary/{content_id}")
async def get_summary(content_id: str):
    """Get summary from file"""
    dir_path = os.path.dirname(__file__)
    file_path = os.path.join(
        dir_path,
        f"assets/summaries/{content_id}.txt",
    )
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
            return { "file_content": file_content }
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail="File not found") from exc


@app.get("/checkStatus/{job_id}")
async def get_job(request: Request, job_id: str):
    """Check status of job"""
    try:
        job_data = Job.fetch(job_id, connection=request.app.state.redis)
    except NoSuchJobError as exc:
        raise HTTPException(status_code=404, detail="Job not found") from exc

    return {
        "id": job_id,
        "status": job_data.get_status(),
        "summary": job_data.result,
        "data": job_data.kwargs,
        "enqueued_at": job_data.enqueued_at,
        "started_at": job_data.started_at,
        "ended_at": job_data.ended_at,
    }
