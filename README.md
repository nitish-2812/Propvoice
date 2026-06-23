# 🎙️ PropVoice — Multi-Tenant Agentic Voice Orchestrator

PropVoice is a modern SaaS platform designed for real estate agencies to automate their outbound lead qualification process using Conversational AI. It leverages an autonomous multi-agent architecture to call leads, evaluate transcripts via LLMs, and update lead statuses in real-time.

**Live Deployment:**
- **Frontend:** [https://propvoice.vercel.app](https://propvoice.vercel.app)
- **Backend API:** [https://propvoice-backend.onrender.com](https://propvoice-backend.onrender.com)

---

## ✨ Key Features

- **Multi-Tenant Architecture:** Supports multiple real estate agencies, dynamically injecting each company's specific persona and system prompt into the AI caller.
- **Agentic Workflow (LangGraph):** Orchestrates the call dispatch and transcript evaluation via a defined state graph.
- **Automated AI Calling (Vapi.ai):** Triggers live phone calls with sub-second latency conversational AI.
- **Intelligent Evaluation (OpenAI):** Parses the call transcript using GPT-4o-mini to classify leads as `QUALIFIED` or `NOT_INTERESTED` based on conversation context.
- **Real-Time Webhooks:** Processes end-of-call webhooks to asynchronously evaluate and update the database.

---

## 🏗️ Technical Architecture

### Tech Stack
- **Backend:** FastAPI (Python), LangGraph, Motor (Async MongoDB)
- **Frontend:** React (Vite), TailwindCSS, Lucide Icons
- **Database:** MongoDB Atlas
- **AI/LLM:** Vapi.ai (Voice AI), OpenAI (Evaluation)
- **Deployment:** Render / GCP Cloud Run (Backend/Docker), Vercel (Frontend)

---

## ⚙️ 1. Environment Variables Setup (.env)

You must create a `.env` file in the `backend/` directory with the following keys. A `.env.example` is provided for reference.

```ini
# MongoDB connection string
MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/voiceagent

# Vapi.ai credentials for triggering AI voice calls
VAPI_API_KEY=your_vapi_key
VAPI_ASSISTANT_ID=your_assistant_id
VAPI_PHONE_NUMBER_ID=your_phone_number_id

# OpenAI API key for LangGraph transcript classification
OPENAI_API_KEY=your_openai_api_key

# App URLs (used for CORS and webhook configuration)
BACKEND_URL=http://localhost:8000
FRONTEND_URL=http://localhost:5173
```

---

## 🚀 2. Local Setup: Build, Run, and Test

### Backend Setup
1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. **Seed the database** (Generates companies and test leads):
   ```bash
   python seed.py
   ```
5. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Open a new terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

### How to Test Locally
1. Ensure both servers are running.
2. Open `http://localhost:5173` in your browser.
3. Click on a company (e.g., Sunrise Realty) to load its `PENDING` leads.
4. Click **Launch Campaign** to trigger the Vapi outbound call.
5. Answer the call on your mobile device.
6. Once the call ends, watch the backend logs as the LangGraph node evaluates the transcript.
7. The Frontend will automatically poll and update the lead to `QUALIFIED` or `NOT_INTERESTED`.

---

## 🐳 3. Dockerfile & GCP Cloud Run Deployment

The backend contains a production-ready, multi-stage `Dockerfile`. 

```dockerfile
# Stage 1: Install dependencies
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Production image
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /install /usr/local
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Deploying to GCP Cloud Run
To deploy this Docker container to your own GCP project:
1. **Authenticate with Google Cloud:**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```
2. **Submit the Docker build to Google Container Registry (GCR):**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/propvoice-backend
   ```
3. **Deploy to Cloud Run:**
   ```bash
   gcloud run deploy propvoice-backend \
     --image gcr.io/YOUR_PROJECT_ID/propvoice-backend \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars MONGODB_URI="...",VAPI_API_KEY="...",OPENAI_API_KEY="..."
   ```

*(Note: For this submission, the backend is currently hosted live on Render to ensure a seamless evaluation experience without GCP billing constraints).*

---

## 🧩 4. LangGraph Architecture (Nodes, Edges, & State)

The core intelligence of this platform is orchestrated using **LangGraph**, decoupling the real-time voice interaction from the heavy-lifting post-call analysis.

### State Representation
The `VoiceAgentState` is a `TypedDict` that acts as the single source of truth across the graph. It holds keys like `company_id`, `customer_id`, `transcript`, and the final `outcome`.

### Nodes (The Workers)
1. **`dispatch_node`**: Triggered when the campaign launches. It fetches pending leads, injects the dynamic company prompt, and calls the Vapi API.
2. **`evaluation_node`**: Triggered when the Vapi webhook hits the server. It extracts the raw transcript and uses `OpenAI (GPT-4o-mini)` to reason about the conversation, outputting exactly `QUALIFIED`, `NOT_INTERESTED`, or `FAILED`.
3. **`state_update_node`**: Takes the outcome from the evaluation node and persists it to MongoDB, updating the customer status and writing a permanent `call_log`.

### Edges (The Flow)
- The execution is linear but asynchronous. 
- The Vapi webhook serves as the entry point to the evaluation pipeline: `START -> evaluation_node -> state_update_node -> END`. 
- This graph-based state management ensures deterministic outcomes and makes it incredibly easy to add future nodes (e.g., an `email_node` that triggers only if the state is `QUALIFIED`).

---

*Built for the Krid.AI Agentic Voice Orchestrator Assignment.*
