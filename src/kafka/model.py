from pydantic import BaseModel, Field
from typing import Literal
import time


class StockRecord(BaseModel):
    symbol: Literal["AAPL", "GOOGL", "AMZN", "MSFT", "TSLA", "META", "NFLX"]
    price: float = Field(..., gt=0, description="Current stock price in USD")
    volume: int = Field(..., ge=0, description="Trade volume")
    timestamp: float = Field(default_factory=time.time, description="Unix timestamp in seconds")