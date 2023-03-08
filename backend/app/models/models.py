from typing import List
from pydantic import BaseModel

class VideoAsset(BaseModel):
    id: str
    url: str

class SummarizeJob(BaseModel):
    id: str
    videoAssets: List[VideoAsset]
