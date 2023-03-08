from fastapi import FastAPI, HTTPException
from os import os
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import redis

class VideoAsset(BaseModel):
    id: str
    url: str

class VideoRequest(BaseModel):
    id: str
    videoAssets: List[VideoAsset]

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


@app.post("/startSummaryJob")
async def summarize_video(request: VideoRequest):
    # summarizer = Summarizer(request.id, request.videoAssets)
    # summary = summarizer.summarize()
    return {"summary": ""}

@app.get("/checkStatus/{job_id}")
async def get_job(job_id: int):
    r = redis.Redis(host='localhost', port=6379)
    job_data = r.get(job_id)
    if job_data is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_data.decode('utf-8')
