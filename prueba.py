from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import praw
import json
from datetime import datetime

class SearchRequest(BaseModel):
    keyword: str

app = FastAPI()

# Configuración de PRAW
UG = "TrueShield/0.1 by No_Motor5330"
reddit = praw.Reddit(
    client_id = 'h1XqaRXkyHmwMd7r7Yqe_Q',
    client_secret = 'XKc-XCP-eE5VNGGMLkntGZxK3R5MUg',
    user_agent = UG
)

@app.post("/search_posts")
async def search_posts(request: SearchRequest):
    try:
        results = []
        for submission in reddit.subreddit('all').search(request.keyword, limit=10):
            results.append({
                "Id": submission.id,
                "DatePub": datetime.utcfromtimestamp(submission.created_utc).isoformat(),
                "NameProfile": str(submission.author) if submission.author else "Unknown",
                "TitlePub": submission.title,
                "TextPub": submission.selftext,
                "CantUpVotes": submission.ups,
                "CantDownVotes": submission.downs,
                "CantComents": submission.num_comments,
                "CantShares": submission.num_crossposts,
                "TrueLevel": 0.60,  # Nivel de veracidad establecido (puedes ajustarlo según tus criterios)
                "Type_item": "reddit"
            })

        return {"Reddit": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)