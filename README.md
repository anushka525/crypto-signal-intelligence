<div align="center">

# 🚀 AI Crypto Trading Signal Intelligence System

### AI-Powered Crypto Market Analysis & Trading Recommendation Engine

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/Flask-REST--API-black?logo=flask" />
  <img src="https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite" />
  <img src="https://img.shields.io/badge/Gemini-GenAI-orange" />
  <img src="https://img.shields.io/badge/Status-Active-success" />
</p>

</div>

---

## 📖 Overview

The **AI Crypto Trading Signal Intelligence System** is a backend application built using **Flask + SQLite + Gemini AI** that:

- 📊 Manages crypto assets and trading signals  
- 🗄️ Stores structured market data  
- 🧠 Generates AI-powered intraday summaries  
- 📈 Provides Buy / Sell / Hold recommendations  

It combines traditional backend engineering with Generative AI to simulate a real-world crypto intelligence system.

---

## ✨ Features

### 🔹 Core Backend
- Full CRUD APIs (Users, Assets, Signals)
- Multi-table relational database
- Clean route-service architecture
- Centralized error handling

### 🔹 AI Intelligence
- Intraday market summary generation
- Trade recommendation engine
- Risk analysis insights
- Auto signal generation endpoint

### 🔹 System
- Environment-based configuration
- Structured logging
- Modular project structure

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| Framework | Flask |
| Database | SQLite |
| ORM | SQLAlchemy |
| AI | Gemini (Google GenAI) |
| Testing | Thunder Client / Postman |

---

## 🏗️ Project Structure
```
AI-Crypto-Trading-Signal-Intelligence/
│
├── app.py                # Entry point
├── config.py             # Configuration
├── database.py           # Database initialization
│
├── routes/               # API routes
│   ├── assets.py
│   ├── signals.py
│   └── ai.py
│
├── services/             # Business logic & Gemini integration
├── logs/                 # Application logs
└── instance/             # SQLite database
```

---

## 🚀 Getting Started

Follow these steps to run the project locally.

### 1️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows**
```bash
.venv\Scripts\Activate.ps1
```

**Mac/Linux**
```bash
source .venv/bin/activate
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=gemini-3-flash-preview
DATABASE_PATH=./instance/crypto_intel.db
```

⚠️ Do not commit the `.env` file to GitHub.

---

### 4️⃣ Run the Application

```bash
python app.py
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 🔌 API Endpoints

### Base URL
```
http://127.0.0.1:8000
```

---

### 📦 Assets

| Method | Endpoint | Description |
|--------|----------|------------|
| POST | `/api/assets/` | Create new asset |
| GET | `/api/assets/` | Get all assets |
| GET | `/api/assets/{id}` | Get asset by ID |
| PUT/PATCH | `/api/assets/{id}` | Update asset |
| DELETE | `/api/assets/{id}` | Delete asset |

---

### 📊 Signals

| Method | Endpoint | Description |
|--------|----------|------------|
| GET | `/api/signals/` | Get all signals |
| GET | `/api/signals/{id}` | Get signal by ID |
| PUT/PATCH | `/api/signals/{id}` | Update signal |
| DELETE | `/api/signals/{id}` | Delete signal |
| POST | `/api/signals/auto` | Generate signal automatically |

---

### 🤖 AI

**Endpoint**

```
POST /api/ai/summary
```

**Example Request**

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

---

## 🧠 AI Workflow

1. Fetch signal data from database  
2. Accept real-time market indicators  
3. Build structured AI prompt  
4. Send request to Gemini API  
5. Return AI-generated recommendation  

---

## 📝 Logging

Logs are stored in:

```
logs/app.log
```

Includes:

- API errors  
- Database exceptions  
- AI processing failures  

---

## ⚠️ Important Notes

- Ensure `GEMINI_MODEL` matches your API key capability.
- If database schema changes, delete:
  ```
  instance/crypto_intel.db
  ```
  and restart the server.
- Never commit `.env` file to GitHub.

---

