from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from .models.user import UserProfile
from .services.db import DatabaseService
from .services.groq_search import GroqSearchService

app = FastAPI(title="100xEngineers Discovery Platform")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db = DatabaseService()
groq_service = GroqSearchService()

class SearchRequest(BaseModel):
    query: str
    use_groq: bool = False
    groq_api_key: str | None = None

class SearchResponse(BaseModel):
    profile: UserProfile
    explanation: str

@app.post("/api/profiles", response_model=UserProfile)
async def create_profile(profile: UserProfile):
    return db.create_profile(profile)

@app.get("/api/profiles", response_model=List[UserProfile])
async def list_profiles():
    return db.list_profiles()

@app.get("/api/profiles/{profile_id}", response_model=UserProfile)
async def get_profile(profile_id: str):
    profile = db.get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.post("/api/search", response_model=List[SearchResponse])
async def search_profiles(search: SearchRequest):
    print(f"Debug: Received search request - Query: {search.query}, Use Groq: {search.use_groq}")
    profiles = db.list_profiles()
    print(f"Debug: Found {len(profiles)} total profiles")
    
    if search.use_groq:
        if not search.groq_api_key:
            print("Debug: No Groq API key provided")
            raise HTTPException(status_code=400, detail="Groq API key is required for semantic search")
        try:
            print("Debug: Attempting Groq search...")
            # Use Groq for semantic search
            matches = groq_service.search_profiles(search.query, profiles, search.groq_api_key)
            print(f"Debug: Groq search returned {len(matches)} matches")
            return [SearchResponse(profile=profile, explanation=explanation) for profile, explanation in matches]
        except Exception as e:
            print(f"Debug: Groq search failed with error: {str(e)}")
            print(f"Debug: Error type: {type(e)}")
            # Fallback to basic search
            print("Debug: Falling back to basic search")
            basic_matches = db.search_profiles(search.query)
            print(f"Debug: Basic search found {len(basic_matches)} matches")
            return [
                SearchResponse(profile=profile, explanation="Matched based on keyword search (Groq search failed)")
                for profile in basic_matches
            ]
    else:
        print("Debug: Using basic search")
        basic_matches = db.search_profiles(search.query)
        print(f"Debug: Basic search found {len(basic_matches)} matches")
        return [
            SearchResponse(profile=profile, explanation="Matched based on keyword search")
            for profile in basic_matches
        ] 