from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import praw
from datetime import datetime
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class SearchRequest(BaseModel):
    prompt: str
    temporality: str
    location: str
    keywords: List[str]
    main_topic: str
    subjects: List[str]

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
        # Crear la lista de palabras clave en minúsculas
        keywords = [keyword.lower() for keyword in request.keywords + request.subjects]

        results = []
        for submission in reddit.subreddit('all').search(" OR ".join(keywords), limit=100):
            # Contar el número de coincidencias de palabras clave en el título y el texto del post
            title_text = (submission.title + " " + submission.selftext).lower()
            matches = sum(1 for keyword in keywords if keyword in title_text)

            if matches >= 2:
                results.append({
                    "Id": submission.id,
                    "DatePub": datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d'),
                    "NameProfile": str(submission.author) if submission.author else "Unknown",
                    "TitlePub": submission.title,
                    "TextPub": submission.selftext,
                    "CantUpVotes": submission.ups,
                    "CantDownVotes": submission.downs,
                    "CantComents": submission.num_comments,
                    "CantShares": submission.num_crossposts,  # Número de veces compartido
                    "TrueLevel": 0.60,  # Nivel de veracidad establecido (puedes ajustarlo según tus criterios)
                    "Type_item": "reddit"
                })

        # Ordenar los resultados por el número de coincidencias de palabras clave (descendente)
        #results.sort(key=lambda x: sum(1 for keyword in keywords if keyword in (x['TitlePub'] + " " + x['TextPub']).lower()), reverse=True)
        # Sort mresult by matches (descending)
        results = sorted(results, key=lambda x: x.get("matches", 0), reverse=True)


        return {"Reddit": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)