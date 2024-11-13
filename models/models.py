from pydantic import BaseModel
from typing import List

class KeywordsModel(BaseModel):
    keywords_en: List[str]
    keywords_es: List[str]

class SearchRequest(BaseModel):
    prompt: str
    temporality: str
    location: List[str]
    keywords: KeywordsModel
    subjects: List[str]