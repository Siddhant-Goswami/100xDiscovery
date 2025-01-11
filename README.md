---
title: 100xdiscovery
emoji: 🐨
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.29.0
app_file: app.py
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# 100xEngineers Discovery Platform Monorepo 🚀

This monorepo contains both the backend and frontend components of the 100xEngineers Discovery Platform.

## Project Structure

```
.
├── backend/                 # FastAPI Backend
│   ├── app/                # Application code
│   │   ├── main.py        # FastAPI application
│   │   ├── models/        # Pydantic models
│   │   └── services/      # Business logic
│   ├── tests/             # Backend tests
│   ├── requirements.txt   # Backend dependencies
│   └── .env.example       # Example environment variables
│
└── frontend/              # Streamlit Frontend
    ├── src/              # Source code
    │   └── app.py        # Streamlit application
    ├── tests/            # Frontend tests
    ├── requirements.txt  # Frontend dependencies
    └── .env.example      # Example environment variables
```

## Setup & Development

### Backend (FastAPI)

1. Create and activate a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the backend:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### Frontend (Streamlit)

1. Create and activate a virtual environment:
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the frontend:
```bash
streamlit run src/app.py
```

The UI will be available at http://localhost:8501

## Deployment

### Backend
- The backend can be deployed to any platform that supports Python/FastAPI (e.g., Heroku, DigitalOcean, AWS)
- Set the appropriate environment variables in your deployment platform

### Frontend
- The frontend can be deployed to Streamlit Cloud or any platform that supports Python/Streamlit
- Make sure to set the `BACKEND_API_URL` to point to your deployed backend

## Contributing

1. Clone the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
