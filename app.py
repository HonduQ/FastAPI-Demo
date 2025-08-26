from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx

app = FastAPI(title="Mini Integration API")

# ---- Pricing demo ----
class QuoteItem(BaseModel):
    sku: str
    qty: int = Field(gt=0)
    price: float = Field(ge=0)

class QuoteReq(BaseModel):
    external_id: str
    items: list[QuoteItem]
    markup: float = 0.10  # 10%

@app.post("/quote")
def quote(q: QuoteReq):
    subtotal = sum(i.qty * i.price for i in q.items)
    total = round(subtotal * (1 + q.markup), 2)
    return {"external_id": q.external_id, "subtotal": subtotal, "total": total}

# ---- External API demo ----
@app.get("/conditions")
async def conditions(lat: float = 42.36, lon: float = -71.06):
    url = ("https://api.open-meteo.com/v1/forecast"
           f"?latitude={lat}&longitude={lon}"
           "&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,wind_speed_10m"
           "&forecast_days=1&timezone=auto")
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.get(url)
            r.raise_for_status()
            data = r.json()
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))
    # normalize one hour for demo
    i = 0
    return {
        "temperatureC": data["hourly"]["temperature_2m"][i],
        "humidity": data["hourly"]["relative_humidity_2m"][i],
        "precipProb": data["hourly"]["precipitation_probability"][i],
        "windKph": data["hourly"]["wind_speed_10m"][i],
    }
