# 🎙️ VoiceAgent SaaS — Multi-Tenant Agentic Voice Orchestrator

A production-quality SaaS platform where real estate companies can launch **AI-powered voice campaigns** to automatically call and qualify leads. Built with **FastAPI + LangGraph + Vapi.ai + MongoDB + React**.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Vapi](https://img.shields.io/badge/Vapi.ai-5046E5?style=for-the-badge)
![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

---

## 🏗️ Architecture

```
Manager clicks "Start Campaign"
        ↓
System fetches PENDING leads from MongoDB
        ↓
LangGraph Dispatch Node → triggers Vapi AI calls
        ↓
Vapi AI calls each lead → has natural conversation
        ↓
Call ends → Vapi webhook → our backend
        ↓
LangGraph Evaluation Node → Groq LLaMA classifies transcript
        ↓
State Update Node → updates MongoDB
        ↓
Dashboard auto-refreshes → live status updates
```

### Two LLMs Working Together

| | LLM 1 (Vapi) | LLM 2 (Groq) |
|---|---|---|
| **When** | During call (real-time) | After call ends |
| **Job** | Natural conversation | Classify transcript |
| **Model** | GPT-4o Mini | LLaMA 3.3-70B |
| **Cost** | Vapi credits | Free tier |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB Atlas account (free M0 tier)
- Vapi.ai account ($10 free credits)
- Groq API key (free tier)

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/voice-agent-saas.git
cd voice-agent-saas
cp .env.example .env
# Fill in your API keys in .env
```

### 2. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Seed the database
python seed.py

# Start the server
uvicorn main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Open Dashboard
Visit **http://localhost:5173** — you should see the dashboard!

---

## 📁 Project Structure

```
voice-agent-saas/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Environment variables
│   ├── database.py          # MongoDB (Motor async)
│   ├── models/              # Pydantic schemas
│   ├── routers/             # API endpoints
│   ├── services/            # Vapi + Groq integrations
│   ├── agent/               # LangGraph (3 nodes, 2 graphs)
│   └── seed.py              # Database seeder
├── frontend/
│   ├── src/components/      # React components
│   ├── src/pages/           # Dashboard page
│   └── src/api/             # Axios API client
└── docker-compose.yml
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/companies` | List all companies |
| GET | `/customers?company_id=...` | List leads for a company |
| POST | `/campaign/start` | Launch AI voice campaign |
| POST | `/api/webhooks/vapi` | Vapi call completion webhook |
| GET | `/health` | Health check |

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Motor (async MongoDB)
- **AI Orchestration:** LangGraph (dispatch + evaluation graphs)
- **Voice AI:** Vapi.ai (STT + LLM + TTS + phone dialing)
- **LLM Classification:** Groq — LLaMA 3.3-70B
- **Database:** MongoDB Atlas (free M0)
- **Frontend:** React + Vite + Tailwind CSS + Framer Motion
- **Deployment:** Docker + GCP Cloud Run
- **Total Cost:** $0 (all free tiers)

---

## 📝 License

MIT License
