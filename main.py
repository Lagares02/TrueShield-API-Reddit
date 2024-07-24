from fastapi import FastAPI
from routes.reddit import router as reddit_router

app = FastAPI()

app.include_router(reddit_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)