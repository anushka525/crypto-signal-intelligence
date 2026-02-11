🚀 AI Crypto Trading Signal Intelligence System

AI-powered crypto trading signal intelligence platform that generates intraday market analysis and smart trade recommendations using Gemini GenAI.

📌 Overview

The AI Crypto Trading Signal Intelligence System is a Flask-based RESTful backend application that:

Manages crypto assets and trading signals

Stores structured market data

Generates AI-powered intraday summaries & trade recommendations

It combines traditional backend engineering with Generative AI to simulate a real-world trading intelligence system.

🛠️ Tech Stack

Python

Flask (REST API)

SQLite + SQLAlchemy (ORM)

Gemini (Google GenAI)

Thunder Client / Postman

✨ Features

🔹 CRUD APIs for Users, Assets & Signals

🔹 Multi-table relational database (SQLite)

🔹 AI-powered market summary & recommendation engine

🔹 Auto signal generation endpoint

🔹 Structured logging & centralized error handling

🔹 Environment-based configuration (.env support)

📂 Project Structure
AI-Crypto-Trading-Signal-Intelligence/
│
├── app.py               # Application entry point
├── config.py            # Environment configuration
├── database.py          # DB initialization
│
├── routes/              # API routes
│   ├── assets.py
│   ├── signals.py
│   └── ai.py
│
├── services/            # Business logic & Gemini integration
│
├── logs/                # Application logs
└── instance/            # SQLite database file

⚙️ Setup & Installation
1️⃣ Create Virtual Environment
python -m venv .venv


Activate environment:

Windows (PowerShell)

.venv\Scripts\Activate.ps1


Mac/Linux

source .venv/bin/activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Configure Environment Variables

Create a .env file in root directory:

GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3-flash-preview
DATABASE_PATH=./instance/crypto_intel.db

4️⃣ Run the Server
python app.py


Server runs at:

http://127.0.0.1:8000

🔌 API Endpoints
📦 Assets
Method	Endpoint	Description
POST	/api/assets/	Create new asset
GET	/api/assets/	Get all assets
GET	/api/assets/{id}	Get asset by ID
PUT/PATCH	/api/assets/{id}	Update asset
DELETE	/api/assets/{id}	Delete asset
📊 Signals
Method	Endpoint	Description
GET	/api/signals/	Get all signals
GET	/api/signals/{id}	Get signal by ID
PUT/PATCH	/api/signals/{id}	Update signal
DELETE	/api/signals/{id}	Delete signal
POST	/api/signals/auto	Auto-generate trading signal
🤖 AI Intelligence
Method	Endpoint	Description
POST	/api/ai/summary	Generate AI-based market summary
📝 Example AI Request
{
  "signal_id": 1,
  "market": {
    "last_price": 43000,
    "rsi": 62.4,
    "macd": 1.2,
    "volatility": 0.018
  }
}

🧠 How AI Works

User provides signal ID and current market indicators

Backend fetches stored signal data

Market data + signal data are sent to Gemini

Gemini generates:

Market summary

Buy/Sell/Hold recommendation

Risk insight

Structured response returned via API

📜 Logging

Logs are stored in:

logs/app.log


Includes:

API errors

Database errors

AI response issues

System events

⚠️ Important Notes

Ensure GEMINI_MODEL matches the model supported by your API key.

If database schema changes:

Delete instance/crypto_intel.db

Restart server to recreate tables.

Do NOT commit .env to GitHub.

🚀 Future Enhancements

JWT Authentication

Role-based Access Control

PostgreSQL support

Docker containerization

Real-time crypto price integration

Backtesting engine

👩‍💻 Author

Anushka
Backend & AI Developer
