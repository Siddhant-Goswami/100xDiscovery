import os
from typing import List, Dict, Tuple
from groq import Groq
from app.models.user import UserProfile
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

class GroqSearchService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set")
            
        self.client = Groq(
            api_key=api_key,
        )
        
    def _create_profile_context(self, profile: UserProfile) -> str:
        """Create a searchable context string from a profile."""
        return f"""
Name: {profile.name}
Technical Skills: {', '.join(profile.technical_skills)}
Projects: {', '.join(profile.projects)}
AI Expertise: {', '.join(profile.ai_expertise)}
Mentoring Preferences: {profile.mentoring_preferences}
Collaboration Interests: {', '.join(profile.collaboration_interests)}
"""

    def search_profiles(self, query: str, profiles: List[UserProfile]) -> List[Tuple[UserProfile, str]]:
        """
        Search profiles using Groq LLM and return matches with explanations.
        Returns: List of tuples (profile, explanation)
        """
        if not profiles:
            return []

        # Create context from all profiles
        profile_contexts = {str(p.id): self._create_profile_context(p) for p in profiles}
        
        # Create the prompt for Groq
        prompt = f"""You are an expert at matching engineers based on their profiles. Your task is to find the most relevant profiles that match the given search query.

Search Query: "{query}"

Available Engineer Profiles:
{'-' * 80}
"""
        for pid, context in profile_contexts.items():
            prompt += f"\nProfile ID: {pid}\n{context}\n{'-' * 80}"

        prompt += """\nInstructions:
1. Analyze the search query and understand the key requirements.
2. Compare these requirements against each profile's skills, expertise, and preferences.
3. For each matching profile, calculate a match score (0-100) based on:
   - Direct skill matches
   - Related expertise
   - Project experience
   - Mentoring alignment
   - Collaboration potential

Return your analysis in the following JSON format:
[
  {
    "profile_id": "exact-profile-uuid-from-above",
    "match_score": number-between-0-and-100,
    "explanation": "Detailed explanation of why this profile matches the search query"
  }
]

Important:
- Include ANY profile that has relevant matches, even if the match score is moderate
- Be lenient with matching - if someone has related skills, they might be a good fit
- The explanation should be specific about why the profile matches
- Sort results by match_score in descending order
- Return an empty list [] if truly no profiles match

Remember: It's better to show more potential matches than to be too restrictive."""

        # Get response from Groq
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at matching engineers based on their profiles. You always return valid JSON in the exact format requested."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192",
                temperature=0.2,  # Slightly higher temperature for more inclusive matching
                max_tokens=2000,
            )
            
            response_text = chat_completion.choices[0].message.content.strip()
            
            # Try to extract JSON if it's wrapped in backticks or has extra text
            try:
                # First try direct JSON parsing
                matches = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON from the response
                import re
                json_match = re.search(r'\[[\s\S]*\]', response_text)
                if json_match:
                    try:
                        matches = json.loads(json_match.group(0))
                    except json.JSONDecodeError:
                        print(f"Failed to parse Groq response: {response_text}")
                        return self._fallback_search(query, profiles)
                else:
                    print(f"No JSON found in response: {response_text}")
                    return self._fallback_search(query, profiles)
            
            # Convert to list of tuples (profile, explanation)
            results = []
            for match in matches:
                profile_id = match.get("profile_id")
                explanation = match.get("explanation", "")
                score = match.get("match_score", 0)
                
                # Find the profile with this ID
                profile = next((p for p in profiles if str(p.id) == profile_id), None)
                if profile:
                    results.append((profile, f"Match Score: {score}%\n{explanation}"))
            
            # If no matches found through Groq, try fallback search
            if not results:
                return self._fallback_search(query, profiles)
                
            return results
                
        except Exception as e:
            print(f"Error during Groq search: {str(e)}")
            return self._fallback_search(query, profiles)

    def _fallback_search(self, query: str, profiles: List[UserProfile]) -> List[Tuple[UserProfile, str]]:
        """Fallback to basic keyword matching if Groq search fails."""
        results = []
        query_terms = query.lower().split()
        
        for profile in profiles:
            score = 0
            matches = []
            
            # Check each field for matches
            profile_text = self._create_profile_context(profile).lower()
            
            for term in query_terms:
                if term in profile_text:
                    score += 1
                    # Find which field matched
                    if term in profile.name.lower():
                        matches.append(f"Name matches '{term}'")
                    if any(term in skill.lower() for skill in profile.technical_skills):
                        matches.append(f"Has technical skill related to '{term}'")
                    if any(term in exp.lower() for exp in profile.ai_expertise):
                        matches.append(f"Has AI expertise related to '{term}'")
                    if term in profile.mentoring_preferences.lower():
                        matches.append(f"Mentoring preferences match '{term}'")
            
            if score > 0:
                explanation = "Basic Match:\n" + "\n".join(matches)
                results.append((profile, explanation))
        
        return sorted(results, key=lambda x: len(x[1].split('\n')), reverse=True) 