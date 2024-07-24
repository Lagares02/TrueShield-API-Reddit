from fastapi import APIRouter, HTTPException
from models.models.py import SearchRequest
from services.reddit import search_reddit_posts

router = APIRouter()

@router.post("/contrasting")
async def contrasting(request: SearchRequest):
    try:
        
        keywords = request.keywords + request.subjects
        
        results = search_reddit_posts(keywords)
        
        return {
            "Reddit": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))