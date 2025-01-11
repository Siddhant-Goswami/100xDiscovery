from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Tuple
from pydantic import BaseModel
import json
import os
from pathlib import Path
from app.models.user import UserProfile
from app.services.groq_search import GroqSearchService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="100xEngineers Discovery Platform")

# Initialize Groq service with error handling
try:
    groq_search = GroqSearchService()
except Exception as e:
    print(f"Warning: Failed to initialize Groq service: {str(e)}")
    groq_search = None

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data storage
DATA_FILE = Path("data/profiles.json")
DATA_FILE.parent.mkdir(exist_ok=True)

# Initialize the JSON file if it doesn't exist
if not DATA_FILE.exists():
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_profiles() -> Dict[str, UserProfile]:
    try:
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
                return {k: UserProfile(**v) for k, v in data.items()}
            except json.JSONDecodeError:
                # If file is corrupted, start fresh
                return {}
    except FileNotFoundError:
        # Create file if it doesn't exist
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
        return {}

def save_profiles(profiles: Dict[str, UserProfile]):
    # Create directory if it doesn't exist
    DATA_FILE.parent.mkdir(exist_ok=True)
    
    # Write to a temporary file first
    temp_file = DATA_FILE.with_suffix('.tmp')
    try:
        with open(temp_file, "w") as f:
            # Use model_dump() which now handles UUID conversion
            json.dump({k: v.model_dump() for k, v in profiles.items()}, f, indent=2)
        
        # Rename temp file to actual file (atomic operation)
        temp_file.replace(DATA_FILE)
    except Exception as e:
        if temp_file.exists():
            temp_file.unlink()  # Delete temp file if it exists
        raise HTTPException(status_code=500, detail=str(e))

# API endpoints
@app.post("/api/profiles", response_model=UserProfile)
async def create_profile(profile: UserProfile):
    profiles = load_profiles()
    profile_id = str(profile.id)
    profiles[profile_id] = profile
    save_profiles(profiles)
    return profile

@app.get("/api/profiles", response_model=List[UserProfile])
async def list_profiles():
    profiles = load_profiles()
    return list(profiles.values())

@app.get("/api/profiles/{profile_id}", response_model=UserProfile)
async def get_profile(profile_id: str):
    profiles = load_profiles()
    if profile_id not in profiles:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profiles[profile_id]

# Update SearchResponse model
class SearchResponse(BaseModel):
    profile: UserProfile
    explanation: str

class SearchQuery(BaseModel):
    query: str

@app.post("/api/search", response_model=List[SearchResponse])
async def search_profiles(search: SearchQuery):
    profiles = load_profiles()
    
    if not groq_search:
        # Fallback to basic search if Groq is not available
        results = []
        query = search.query.lower()
        for profile in profiles.values():
            if (query in profile.name.lower() or
                any(query in skill.lower() for skill in profile.technical_skills) or
                any(query in expertise.lower() for expertise in profile.ai_expertise) or
                query in profile.mentoring_preferences.lower()):
                results.append((profile, "Basic match based on keyword search"))
        return [SearchResponse(profile=profile, explanation=explanation) 
                for profile, explanation in results]
    
    # Use Groq for semantic search
    matches = groq_search.search_profiles(search.query, list(profiles.values()))
    
    # Convert to response format
    return [SearchResponse(profile=profile, explanation=explanation) 
            for profile, explanation in matches] 