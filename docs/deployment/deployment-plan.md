# Deployment and Configuration Plan

## Selected deployment approach
The capstone prototype uses Docker as the preferred deployment method because it packages the application and dependencies into a repeatable runtime image. The same container can run locally, on a university lab server, on an on-premise Linux host, or on a cloud VM/container service.

## Prerequisites
- Docker Engine 24+ or Docker Desktop
- Optional local development: Python 3.11+
- Git for source retrieval
- 2 CPU cores and 2 GB RAM are sufficient for the current prototype workload

## Environment variables
- `CYBER_DB_PATH`: SQLite database path. Default local value: `data/cybersecurity.db`
- `APP_HOST`: documented local host value `0.0.0.0`
- `APP_PORT`: documented local port value `8000`

Never commit secrets to the repository. Future authentication keys or cloud credentials must be supplied through the deployment platform's secret manager.

## Local setup
```bash
git clone https://github.com/milhanahmed/ai-cybersecurity-threat-detection-risk-prioritization.git
cd ai-cybersecurity-threat-detection-risk-prioritization
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/` for the analyst dashboard.

## Docker deployment
```bash
docker build -t cyber-risk-capstone:1.0 .
docker run --rm -p 8000:8000 -e CYBER_DB_PATH=/app/data/cybersecurity.db cyber-risk-capstone:1.0
```

Or use Docker Compose:
```bash
docker compose up --build -d
docker compose logs -f
docker compose down
```

## Reliability considerations
Configuration is externalized from source code so the same image can run in different environments. The Compose configuration uses a named volume so SQLite data persists when the container restarts. Dependency versions should be pinned before production deployment, and production deployments should add HTTPS termination, authentication, backups, monitoring, and a managed database if concurrency increases.
