from typing import List
from pydantic import BaseModel

class VideoAsset(BaseModel):
    """Video asset model"""
    id: str
    url: str

class SummarizeJob(BaseModel):
    """Summarize job model"""
    id: str
    videoAssets: List[VideoAsset]
