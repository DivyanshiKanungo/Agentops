# KAUSHAL PS-04 Backend

FastAPI backend foundation for the sustainability dashboard.

## Setup

```powershell
cd backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Run

```powershell
uvicorn app.main:app --reload
```

The API is available at:
- Health: http://127.0.0.1:8000/health
- Docs: http://127.0.0.1:8000/docs
