import streamlit as st
import requests
from typing import Dict, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="100xEngineers Discovery Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API client setup
class APIClient:
    def __init__(self):
        # Get the backend API URL from environment or use localhost
        self.base_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")
        st.sidebar.text(f"API URL: {self.base_url}")
        
    def _handle_response(self, response):
        if response.ok:
            return response.json()
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

    def get(self, endpoint: str):
        try:
            response = requests.get(f"{self.base_url}{endpoint}")
            return self._handle_response(response)
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            return None

api = APIClient()

def create_profile(profile_data: dict):
    try:
        response = requests.post(f"{api.base_url}/profiles", json=profile_data)
        if response.status_code == 422:
            error_detail = response.json().get('detail', [])
            if isinstance(error_detail, list):
                for error in error_detail:
                    st.error(f"Validation Error: {error.get('msg')}")
            else:
                st.error(f"Validation Error: {error_detail}")
            return None
        elif not response.ok:
            st.error(f"Server Error: {response.status_code}")
            return None
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server. Please make sure the backend is running.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None

def search_profiles(query: str):
    try:
        response = requests.post(
            f"{api.base_url}/search",
            json={"query": query}
        )
        if not response.ok:
            if response.status_code == 422:
                st.error("Invalid search query format")
            else:
                st.error(f"Search failed with status code: {response.status_code}")
            return []
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server. Please make sure the backend is running.")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred during search: {str(e)}")
        return []

def list_profiles():
    try:
        response = requests.get(f"{api.base_url}/profiles")
        if not response.ok:
            st.error(f"Failed to fetch profiles: {response.status_code}")
            return []
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the server. Please make sure the backend is running.")
        return []
    except Exception as e:
        st.error(f"An unexpected error occurred while fetching profiles: {str(e)}")
        return []

# UI Components
st.title("100xEngineers Discovery Platform 🚀")

# Sidebar navigation
page = st.sidebar.radio("Navigation", ["Search Profiles", "Create Profile", "View All Profiles"])

if page == "Create Profile":
    st.header("Create Your Profile")
    
    with st.form("profile_form"):
        name = st.text_input("Name", help="Enter your full name (minimum 2 characters)")
        technical_skills = st.text_input("Technical Skills (comma-separated)", 
                                       help="Enter your technical skills, separated by commas")
        projects = st.text_input("Projects (comma-separated)",
                               help="List your notable projects, separated by commas")
        ai_expertise = st.text_input("AI Expertise (comma-separated)",
                                   help="List your AI-related skills and expertise")
        mentoring_preferences = st.text_area("Mentoring Preferences",
                                           help="Describe your mentoring preferences (minimum 10 characters)")
        collaboration_interests = st.text_input("Collaboration Interests (comma-separated)",
                                              help="List your interests for collaboration")
        portfolio_url = st.text_input("Portfolio URL",
                                    help="Enter your portfolio URL (optional)")
        
        submitted = st.form_submit_button("Create Profile")
        
        if submitted:
            if len(name.strip()) < 2:
                st.error("Name must be at least 2 characters long")
            elif len(mentoring_preferences.strip()) < 10:
                st.error("Mentoring preferences must be at least 10 characters long")
            else:
                profile_data = {
                    "name": name.strip(),
                    "technical_skills": [s.strip() for s in technical_skills.split(",") if s.strip()],
                    "projects": [p.strip() for p in projects.split(",") if p.strip()],
                    "ai_expertise": [a.strip() for a in ai_expertise.split(",") if a.strip()],
                    "mentoring_preferences": mentoring_preferences.strip(),
                    "collaboration_interests": [c.strip() for c in collaboration_interests.split(",") if c.strip()],
                    "portfolio_url": portfolio_url.strip() if portfolio_url.strip() else None
                }
                
                if profile := create_profile(profile_data):
                    st.success("Profile created successfully!")
                    st.json(profile)

elif page == "Search Profiles":
    st.header("Search Profiles")
    
    st.markdown("""
    Search for engineers using natural language. Examples:
    - "Find someone experienced in machine learning and NLP"
    - "Looking for a mentor in backend development"
    - "Need a collaborator for an open source AI project"
    """)
    
    query = st.text_input("Enter your search query in natural language")
    
    if query:
        results = search_profiles(query)
        
        if results:
            st.subheader(f"Found {len(results)} matches")
            for result in results:
                profile = result['profile']
                explanation = result['explanation']
                
                with st.expander(f"{profile['name']}"):
                    # Display match explanation
                    st.markdown(f"**Match Analysis:**\n{explanation}")
                    st.markdown("---")
                    
                    # Display profile details
                    st.write("**Technical Skills:**", ", ".join(profile["technical_skills"]))
                    st.write("**AI Expertise:**", ", ".join(profile["ai_expertise"]))
                    st.write("**Projects:**", ", ".join(profile["projects"]))
                    st.write("**Mentoring Preferences:**", profile["mentoring_preferences"])
                    st.write("**Collaboration Interests:**", ", ".join(profile["collaboration_interests"]))
                    if profile.get("portfolio_url"):
                        st.write("**Portfolio:**", profile["portfolio_url"])
        else:
            st.info("No matching profiles found. Try adjusting your search query.")

else:  # View All Profiles
    st.header("All Profiles")
    
    profiles = list_profiles()
    
    if profiles:
        for profile in profiles:
            with st.expander(f"{profile['name']}"):
                st.write("**Technical Skills:**", ", ".join(profile["technical_skills"]))
                st.write("**AI Expertise:**", ", ".join(profile["ai_expertise"]))
                st.write("**Projects:**", ", ".join(profile["projects"]))
                st.write("**Mentoring Preferences:**", profile["mentoring_preferences"])
                st.write("**Collaboration Interests:**", ", ".join(profile["collaboration_interests"]))
                if profile.get("portfolio_url"):
                    st.write("**Portfolio:**", profile["portfolio_url"])
    else:
        st.info("No profiles found. Create one to get started!") 