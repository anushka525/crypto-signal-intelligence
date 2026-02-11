# AI Crypto Trading Signal Intelligence System

## Overview
This project is an AI-powered crypto trading signal intelligence system. It provides CRUD APIs for users, assets, and signals, and uses Gemini to generate intraday market analysis and recommendations.

## Tech Stack
- Python
- Flask (REST API)
- SQLite (SQLAlchemy)
- Gemini (GenAI)
- Thunder Client 

## Features
- CRUD APIs for users, assets, and signals
- Multi-table SQLite database
- AI-powered summary/recommendation endpoint
- Error handling and logging

## Project Structure
- app.py
- config.py
- database.py
- routes/
- services/
- logs/
- instance/

## Setup
1) Create virtual environment
```
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2) Install dependencies
```
pip install -r requirements.txt
```

3) Configure environment
Update `.env`:
```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3-flash-preview
DATABASE_PATH=./instance/crypto_intel.db
```

4) Run the server
```
python app.py
```

## API Endpoints
Base URL: `http://127.0.0.1:8000`

### Assets
- POST `/api/assets/`
- GET `/api/assets/`
- GET `/api/assets/{id}`
- PUT/PATCH `/api/assets/{id}`
- DELETE `/api/assets/{id}`

### Signals
- GET `/api/signals/`
- GET `/api/signals/{id}`
- PUT/PATCH `/api/signals/{id}`
- DELETE `/api/signals/{id}`
 - POST `/api/signals/auto`

### AI
- POST `/api/ai/summary`

Example AI request:
```json
{
  "signal_id": 1,
  "market": {
    "last_price": 43000,
    "rsi": 62.4,
    "macd": 1.2,
    "volatility": 0.018
  }
}
```

## Logging
Logs are stored in `logs/app.log`.

## Notes
- If you see model errors, ensure `GEMINI_MODEL` matches the model your API key supports.
- If you remove users from the schema, delete `instance/crypto_intel.db` once so tables are recreated.
