from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import httpx
from enum import Enum

app = FastAPI(title="Mini Integration API")

# ---- Pricing demo ----
class QuoteItem(BaseModel):
    sku: str
    qty: int = Field(gt=0)
    price: float = Field(ge=0)

class QuoteReq(BaseModel):
    external_id: str
    items: list[QuoteItem]
    markup: float = Field(defaut = 0.10, ge=0) # 10%, no negative values allowed

class Units(str, Enum):
    IMPERIAL = "imperial"
    METRIC = "metric"
    

@app.post("/quote")
def quote(q: QuoteReq):
    subtotal = sum(i.qty * i.price for i in q.items)
    total = round(subtotal * (1 + q.markup), 2)
    return {"external_id": q.external_id, "subtotal": subtotal, "total": total}

# ---- External API demo ----
@app.get("/conditions")
async def conditions(lat: float = 42.36, lon: float = -71.06, units: Units =  Units.IMPERIAL):
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
    temp = data["hourly"]["temperature_2m"][i]
    humidity = data["hourly"]["relative_humidity_2m"][i]
    precipProb = data["hourly"]["precipitation_probability"][i]
    windSpeed = data["hourly"]["wind_speed_10m"][i]
    if units == "imperial":
        temp_f = (temp * 9/5) + 32
        wind_mph = windSpeed * 0.621371
        return {
            "temperatureF": round(temp_f, 1),
            "humidity": humidity,
            "precipProb": precipProb,
            "windMph": round(wind_mph, 1)
        }
    else:
        return {
            "temperatureC": temp,
            "humidity": humidity,
            "precipProb": precipProb,
            "windKph": windSpeed,
        }
