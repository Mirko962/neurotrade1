from fastapi import FastAPI
from routes.trades import router as trade_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "NeuroTrade API is online"}

app.include_router(trade_router, prefix="/api")
