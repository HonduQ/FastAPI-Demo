# Title & Description

This is a Mini FastAPI service that fetches live exchange rates (USD, AUD, CAD) and exposes endpoints for querying rates and converting amounts. It demonstrates API integration, data normalization, and business logic in Python.

# Requirements / Setup

- python3 -m venv .venv
- source .venv/bin/activate   # Windows: .venv\Scripts\activate
- pip3 install -r requirements.txt
    - `fastapi`
    - `uvicorn`
    - `pydantic`
    - `httpx`
- python3 -m uvicorn app:app --reload
#### Note: On Linux/Windows you can usually use pip/python instead of pip3/python3.

# API 

curl "http://127.0.0.1:8000/rates?base=USD&target=AUD,CAD"

curl -X POST "http://127.0.0.1:8000/convert" \
  -H "Content-Type: application/json" \
  -d '{"amount": 100, "from_currency": "USD", "to_currency": "AUD", "markup": 0.02}'

Interactive API docs available at http://127.0.0.1:8000/docs.

# Endpoints & Usage (with examples)

## GET /rates

Query params: base, target (comma-separated)

Example: GET `http://127.0.0.1:8000/rates?base=USD&target=AUD,CAD`

Response: ```{"base": "USD", "timestamp": "2025-08-26T14:30:00Z", "rates": { "AUD": 1.49, "CAD": 1.32 }}```

## POST /convert

Body: ```{ "amount": 100, "from_currency": "USD", "to_currency": "AUD", "markup": 0.02 }```

Response: ```{ "amount": 100, "from": "USD", "to": "AUD", "rate": 1.49, "converted": 152.0 }```

# Features / Concepts Demonstrated

Async API calls with httpx (timeouts + retries).

Input validation with Pydantic models.

Normalized internal contract (stable JSON format regardless of provider).

Optional business rules (markup, rounding).

Error handling (400 for bad input, 502 for upstream failure).

# Next Steps (Future Work)

Add database persistence (e.g., log all conversions).

Add auth (API keys or JWT).

Add unit/integration tests (pytest).

Extend to more currencies/providers.

# License / Disclaimer (optional)

This project is for demonstration purposes only and is not intended for production use.

# Tips
### Run and auto-continue until errors:
This tells PDB to run normally until an exception occurs. If the script finishes cleanly, the debugger never appears. If an error happens, it drops you straight into (Pdb) at the crash site. 

```python3 -m pdb -c continue myscript.py```

### Post-mortem debugging after a crash:
 
```python3 -m pdb myscript.py```

Then at the (Pdb) prompt, type: 

```post_mortem```

This jumps to the exact line where the exception happened, with a stack trace.

### Inline breakpoints (set_trace):

You can drop into PDB only where you need it by inserting this in your code:

```import pdb; pdb.set_trace()```

When the program hits that line, execution pauses and you get an interactive (Pdb) prompt with access to all variables in scope.