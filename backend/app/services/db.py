from supabase import create_client
from dotenv import load_dotenv
import os
from typing import List, Optional
from app.models.user import UserProfile

# Load environment variables
load_dotenv()

class DatabaseService:
    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
            
        self.client = create_client(supabase_url, supabase_key)
        
    def create_profile(self, profile: UserProfile) -> UserProfile:
        data = profile.model_dump()
        result = self.client.table("profiles").insert(data).execute()
        return UserProfile(**result.data[0])
        
    def get_profile(self, profile_id: str) -> Optional[UserProfile]:
        result = self.client.table("profiles").select("*").eq("id", profile_id).execute()
        return UserProfile(**result.data[0]) if result.data else None
        
    def list_profiles(self) -> List[UserProfile]:
        result = self.client.table("profiles").select("*").execute()
        return [UserProfile(**profile) for profile in result.data]
        
    def search_profiles(self, query: str) -> List[UserProfile]:
        # Use Supabase's text search capabilities
        search_query = f"%{query}%"
        
        result = (
            self.client.table("profiles")
            .select("*")
            .ilike("name", search_query)
            .execute()
        )
        
        # Also search in arrays and text fields
        result2 = (
            self.client.table("profiles")
            .select("*")
            .ilike("mentoring_preferences", search_query)
            .execute()
        )
        
        # Combine results and remove duplicates
        profiles = []
        seen_ids = set()
        
        for data in [result.data, result2.data]:
            for profile_data in data:
                if profile_data["id"] not in seen_ids:
                    # Also check array fields manually
                    if (
                        any(query.lower() in skill.lower() for skill in profile_data["technical_skills"])
                        or any(query.lower() in exp.lower() for exp in profile_data["ai_expertise"])
                        or any(query.lower() in interest.lower() for interest in profile_data["collaboration_interests"])
                    ):
                        profiles.append(UserProfile(**profile_data))
                        seen_ids.add(profile_data["id"])
        
        return profiles 