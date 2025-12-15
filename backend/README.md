# ShowUp Backend - Initial Setup

This directory contains the FastAPI backend for the ShowUp appointment no-show predictor.

## Quick Start

```bash
# From the backend directory:

# 1. Create virtual environment
python -m venv venv

# 2. Activate it (Windows)
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure environment
copy .env.example .env
# Edit .env with your API keys

# 5. Initialize database
python -c "from app.database import init_db; init_db()"

# 6. Run the server
python -m uvicorn app.main:app --reload
```

## API Endpoints

Once running, visit:
- **API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## Development

See the main README.md for full development roadmap and AI prompting guide.
