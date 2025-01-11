from pydantic import BaseModel, Field, HttpUrl, AnyHttpUrl
from typing import List, Optional
from uuid import UUID, uuid4

class UserProfile(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=2, max_length=100)
    technical_skills: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    ai_expertise: List[str] = Field(default_factory=list)
    mentoring_preferences: str = Field(..., min_length=10, max_length=500)
    collaboration_interests: List[str] = Field(default_factory=list)
    portfolio_url: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "technical_skills": ["Python", "FastAPI", "Machine Learning"],
                "projects": ["AI Chatbot", "Web Scraping Tool"],
                "ai_expertise": ["NLP", "Computer Vision"],
                "mentoring_preferences": "Available for weekly 1-hour sessions, focusing on AI and backend development",
                "collaboration_interests": ["Open Source", "AI Projects"],
                "portfolio_url": "https://github.com/johndoe"
            }
        }
        
    def model_dump(self, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
        # Convert UUID to string
        data['id'] = str(data['id'])
        return data 