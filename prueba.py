from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import praw
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class SearchRequest(BaseModel):
    keyword: str

app = FastAPI()

# Configuración de PRAW
reddit = praw.Reddit(
    client_id = os.getenv('CLIENT_ID'),
    client_secret = os.getenv('CLIENT_SECRET'),
    user_agent = os.getenv('UG')
)

@app.post("/contrasting")
async def contrasting(request: SearchRequest):
    try:
        results = []
        for submission in reddit.subreddit('all').search(request.keyword, limit=10):
            results.append({
                "Id": submission.id,
                "DatePub": datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d'),
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