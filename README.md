---
title: 100xdiscovery
emoji: 🐨
colorFrom: red
colorTo: gray
sdk: streamlit
sdk_version: 1.41.1
app_file: app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# 100xEngineers Discovery Platform 🚀

A platform for discovering and connecting with engineers based on their technical skills, AI expertise, and collaboration interests. Built with FastAPI, Streamlit, and powered by Groq LLM for intelligent profile matching.

## Features

- 👤 Create and manage detailed engineer profiles
- 🔍 Natural language search powered by Groq LLM
- 🤝 Find collaborators based on skills and interests
- 📊 View all registered profiles
- 🎯 Get detailed match explanations

## Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **LLM Integration**: Groq
- **Data Storage**: JSON with atomic operations
- **Deployment**: Hugging Face Spaces

## Environment Variables

The following environment variables need to be set in your Hugging Face Space:

- `GROQ_API_KEY`: Your Groq API key
- `HF_SPACE_URL`: Your Hugging Face Space URL (set automatically)
- `ENVIRONMENT`: Set to "production" for deployment
- `CORS_ORIGINS`: List of allowed origins (automatically configured)

## Local Development

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with required variables
5. Run the application:
```bash
# Terminal 1: Backend
python run.py

# Terminal 2: Frontend
streamlit run frontend/app.py
```

## Deployment

This application is deployed on Hugging Face Spaces. The deployment is configured using the `Spacefile` which sets up both the FastAPI backend and Streamlit frontend services.

## Usage

1. **Create Profile**: Add your engineering profile with skills, expertise, and interests
2. **Search Profiles**: Use natural language to find matching engineers
3. **View Matches**: See detailed explanations of why profiles match your search
4. **Browse All**: View all registered engineer profiles

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - feel free to use this project as a template for your own applications!
