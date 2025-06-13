from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Optional

app = FastAPI(title="Stock Data API", description="Fetch historical stock prices and corporate actions for Indian stocks.")

class StockRequest(BaseModel):
    symbol: str  # e.g., SBIN.NS
    date: str    # e.g., 2024-07-16

class CorporateAction(BaseModel):
    date: str
    type: str  # Dividend, Split, or Bonus
    value: float  # Dividend amount or split ratio

class StockResponse(BaseModel):
    symbol: str
    requested_date: str
    actual_date: str
    actual_date_price: Optional[float]
    current_date: str
    current_date_price: Optional[float]
    corporate_actions: List[CorporateAction]
    message: Optional[str]

def parse_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD (e.g., 2024-07-16).")

@app.get("/stock-data", response_model=StockResponse)
async def get_stock_data(request: StockRequest):
    symbol = request.symbol.strip().upper()
    target_date = parse_date(request.date)
    current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) 
    current_date_str = current_date.strftime("%Y-%m-%d")

    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        if not info.get("longName"):
            raise HTTPException(status_code=404, detail=f"Invalid symbol {symbol} or no data found.")

        search_start = (target_date - timedelta(days=365)).strftime("%Y-%m-%d")
        search_end = min(target_date + timedelta(days=365), current_date).strftime("%Y-%m-%d")

        data = stock.history(start=search_start, end=(current_date + timedelta(days=1)).strftime("%Y-%m-%d"), actions=True)

        target_date_key = target_date.strftime("%Y-%m-%d")
        actual_date = None
        actual_price = None
        message = None

        if target_date_key in data.index:
            actual_date = target_date_key
            actual_price = data.loc[target_date_key]["Close"]
        else:
            trading_days = data.index
            if trading_days.empty:
                raise HTTPException(status_code=404, detail=f"No trading data found for {symbol} within ±1 year of {target_date_key}.")

            target_dt = datetime.strptime(target_date_key, "%Y-%m-%d")
            trading_days_dt = [datetime.strptime(day.strftime("%Y-%m-%d"), "%Y-%m-%d") for day in trading_days]
            time_diffs = [(abs((dt - target_dt).total_seconds()), day) for dt, day in zip(trading_days_dt, trading_days)]
            closest_day = min(time_diffs, key=lambda x: x[0])[1]
            actual_date = closest_day.strftime("%Y-%m-%d")
            actual_price = data.loc[actual_date]["Close"]
            message = f"No data for {target_date_key} (likely non-trading day). Using closest trading day: {actual_date}."

        current_price = None
        if current_date_str in data.index:
            current_price = data.loc[current_date_str]["Close"]
        else:
            prior_data = data[data.index < current_date_str]
            if not prior_data.empty:
                nearest_date = prior_data.index[-1].strftime("%Y-%m-%d")
                current_price = prior_data.loc[nearest_date]["Close"]
                message = (message or "") + f" No data for {current_date_str}. Using nearest trading day: {nearest_date}."

        actions = stock.actions
        corporate_actions = []
        if not actions.empty:
            actions = actions.loc[actual_date:current_date_str]
            dividends = actions[actions["Dividends"] > 0][["Dividends"]]
            for date, div in dividends.iterrows():
                corporate_actions.append(CorporateAction(
                    date=date.strftime("%Y-%m-%d"),
                    type="Dividend",
                    value=float(div["Dividends"])
                ))
            splits = actions[actions["Stock Splits"] > 0][["Stock Splits"]]
            for date, split in splits.iterrows():
                ratio = split["Stock Splits"]
                action_type = "Bonus" if ratio in [2.0, 3.0] else "Split"
                corporate_actions.append(CorporateAction(
                    date=date.strftime("%Y-%m-%d"),
                    type=action_type,
                    value=float(ratio)
                ))

        return StockResponse(
            symbol=symbol,
            requested_date=request.date,
            actual_date=actual_date,
            actual_date_price=float(actual_price) if actual_price else None,
            current_date=current_date_str,
            current_date_price=float(current_price) if current_price else None,
            corporate_actions=corporate_actions,
            message=message
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data for {symbol}: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)