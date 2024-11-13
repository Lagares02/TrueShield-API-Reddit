from fastapi import APIRouter, HTTPException, WebSocket
from models.models import SearchRequest
from services.reddit import search_reddit_posts
import json

router = APIRouter()

@router.get("/")
async def home():
    return {"message": "Bienvenido!"}

@router.post("/contrasting_reddit")
async def contrasting(request: SearchRequest):
    try:
        print("Recibido!!!")
        keywords = request.keywords.keywords_es + request.subjects
        
        prompt = request.prompt
        
        results = search_reddit_posts(keywords, prompt)
        
        return {
            "Reddit": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.websocket("/contrasting")
async def websocket_endpoint(websocket: WebSocket, request: SearchRequest):
    await websocket.accept()
    print("WebSocket connection established")
    
    try:
        data = await websocket.receive_text()
        print(f"Texto recibido: {data}")
        message = json.loads(data)
        print(f"Message transformado a JSON: {message}")
        
        Keywords = request.keywords + request.subjects
        
        while True:
            
            items = search_reddit_posts(Keywords)
            
            return {
                "Reddit": items
            }
        
    except Exception as e:
        print(f"Connection error: {e}")