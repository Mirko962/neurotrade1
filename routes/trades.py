from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
import csv, os

router = APIRouter()

# === SCHEMAS ===
class TradeInput(BaseModel):
    symbol: str
    direction: str
    entry: float
    stop_loss: float
    take_profit: float
    result: str = "open"  # open, win, loss

# === /api/ping ===
@router.get("/ping")
def ping():
    return {"status": "pong"}

# === /api/predict (mock logic) ===
@router.post("/predict")
def predict(trade: TradeInput):
    risk_reward = abs((trade.take_profit - trade.entry) / (trade.entry - trade.stop_loss))
    confidence = min(0.95, max(0.4, 0.5 + (risk_reward - 1) * 0.1))
    suggestion = "enter trade" if confidence > 0.6 else "wait"
    return {
        "symbol": trade.symbol,
        "direction": trade.direction,
        "confidence": round(confidence, 3),
        "suggestion": suggestion
    }

# === /api/journal ===
@router.post("/journal")
def save_trade(trade: TradeInput):
    file_path = "trades.csv"
    headers = ["timestamp", "symbol", "direction", "entry", "stop_loss", "take_profit", "result"]

    row = [
        datetime.utcnow().isoformat(),
        trade.symbol,
        trade.direction,
        trade.entry,
        trade.stop_loss,
        trade.take_profit,
        trade.result
    ]

    file_exists = os.path.exists(file_path)
    with open(file_path, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(headers)
        writer.writerow(row)

    return {
        "status": "logged",
        "trade": trade.dict()
    }





