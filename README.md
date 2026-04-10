SupaChat – Conversational Analytics Platform

SupaChat is a full-stack conversational analytics application that allows users to query a PostgreSQL database using natural language and receive results as tables and visualizations.
It is designed with production-grade DevOps practices including containerization, CI/CD, and monitoring.

🏗️ Architecture
User (Browser)
   ↓
Next.js Frontend (Chat UI + Charts)
   ↓
FastAPI Backend (NL → MCP → SQL)
   ↓
Supabase PostgreSQL Database
   ↓
Monitoring (Prometheus + Grafana)
🔧 Tech Stack
Frontend
Next.js (App Router)
React
Axios
Recharts
Backend
FastAPI
Python
MCP Query Translator (NL → JSON → SQL)
Database
Supabase (PostgreSQL)
DevOps
Docker
Docker Compose
Nginx (Reverse Proxy)
GitHub Actions (CI/CD)
Prometheus & Grafana (Monitoring)
AI Tools
Groq API (LLM inference)
Prompt Engineering for SQL generation
⚙️ Setup Instructions
1. Clone Repo
git clone https://github.com/copyfromabove/supachat.git
cd supachat
2. Backend Setup
cd backend
pip install -r requirements.txt

Create .env:

GROQ_API_KEY=your_api_key
DB_HOST=localhost
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password

Run backend:

uvicorn main:app --reload
3. Frontend Setup
cd frontend
npm install

Create .env.local:

NEXT_PUBLIC_API_URL=http://localhost:5000

Run frontend:

npm run dev
🐳 Docker Setup
Build & Run
docker-compose up --build
Services
Frontend → http://localhost:3000
Backend → http://localhost:5000
Grafana → http://localhost:3001
Prometheus → http://localhost:9090
🚀 Deployment
Steps
Build Docker images
Push to container registry (Docker Hub / ECR)
Deploy on VM / Cloud (AWS / GCP)
Configure Nginx reverse proxy
Enable HTTPS (optional)
🔄 CI/CD Pipeline

Implemented using GitHub Actions

Workflow:
Code Push → Build → Test → Docker Build → Deploy
Features:
Automated builds
Linting & checks
Docker image creation
Deployment trigger
📊 Monitoring & Dashboards

![Screenshot 2026-04-10 171335](https://github.com/user-attachments/assets/2a0482f3-1efb-4cee-b996-3666a0f33ffe)

Prometheus
Collects backend metrics
Tracks API latency & requests
Grafana
Visual dashboards
System health monitoring
Example Metrics:
Request count
Response time
CPU & memory usage
🤖 MCP Query Translator (Core Feature)
Flow:
User Query → MCP JSON → SQL → Database
Example:

Input:

Show top articles in last 30 days

MCP Output:

{
  "action": "select",
  "table": "articles",
  "filters": [...],
  "order_by": "views DESC"
}

SQL Generated:

SELECT * FROM articles ORDER BY views DESC;
📈 Features
Natural language querying
Chat-based UI
Data visualization (charts + tables)
Query history tracking
Error handling & loading states
Production-ready DevOps pipeline
🎥 Demo

[👉 [Add your demo video link here]](https://screenrec.com/share/1PVqBW5CpR)

📂 Project Structure
supachat/
 ├── frontend/       # Next.js app
 ├── backend/        # FastAPI server
 ├── docker-compose.yml
 ├── nginx/
 ├── monitoring/
 └── .github/workflows/
🔥 Future Improvements
Authentication (JWT / OAuth)
Role-based access control
Query caching (Redis)
Advanced analytics
Multi-database support
👨‍💻 Author

Likhith Nagavelli

www.linkedin.com/in/likhith-nagavelli-1ab58b235
https://github.com/likhith777666?tab=repositories
