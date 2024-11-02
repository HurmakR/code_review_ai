from pydantic import BaseModel
from typing import List, Dict

class ReviewResult(BaseModel):
    found_files: List[str]
    comments: str
    rating: str
    conclusion: str