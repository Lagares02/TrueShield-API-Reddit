from pydantic import BaseModel
from typing import List

class SearchRequest(BaseModel):
    prompt: str
    temporality: str
    location: str
    keywords: List[str]
    main_topic: str
    subjects: List[str]