from typing import List
from pydantic import BaseModel

class Asset(BaseModel):
    id: str
    url: str

class Job(BaseModel):
    id: str
    videoAssets: List[Asset]