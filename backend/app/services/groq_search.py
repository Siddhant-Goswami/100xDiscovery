import os
from typing import List, Tuple
from groq import Groq
from app.models.user import UserProfile
import json

class GroqSearchService:
    def _create_profile_context(self, profile: UserProfile) -> str:
        """Create a searchable context string from a profile."""
        return f"""
Profile ID: {profile.id}
Name: {profile.name}
Technical Skills: {', '.join(profile.technical_skills)}
Projects: {', '.join(profile.projects)}
AI Expertise: {', '.join(profile.ai_expertise)}
Mentoring Preferences: {profile.mentoring_preferences}
Collaboration Interests: {', '.join(profile.collaboration_interests)}
Portfolio: {profile.portfolio_url if profile.portfolio_url else 'Not provided'}
"""

    def search_profiles(self, query: str, profiles: List[UserProfile], api_key: str) -> List[Tuple[UserProfile, str]]:
        """
        Search profiles using Groq LLM and return matches with explanations.
        Returns: List of tuples (profile, explanation)
        """
        if not profiles:
            return []
            
        if not api_key:
            raise ValueError("Groq API key is required for semantic search")
            
        # Debug: Check API key format
        print(f"Debug: API key length: {len(api_key)}")
        print(f"Debug: API key prefix: {api_key[:10]}...")
        
        try:
            # Initialize Groq client with provided API key
            client = Groq(api_key=api_key.strip())  # Ensure no whitespace
            print("Debug: Groq client initialized successfully")

            # Create context from all profiles
            profile_contexts = {str(p.id): self._create_profile_context(p) for p in profiles}
            print(f"Debug: Created context for {len(profiles)} profiles")
            
            # Create the prompt for Groq
            prompt = f"""You are an expert at matching engineers based on their profiles. Your task is to find the most relevant profiles that match the given search query.

Search Query: "{query}"

Available Engineer Profiles:
{'-' * 80}
"""
            for pid, context in profile_contexts.items():
                prompt += f"\nProfile ID: {pid}\n{context}\n{'-' * 80}"

            prompt += """\nInstructions:
1. Analyze the search query to understand the key requirements and preferences.
2. For each profile, evaluate:
   - Direct skill matches
   - Related expertise and experience
   - Project relevance
   - Mentoring compatibility
   - Collaboration potential
   - Overall fit for the query
3. Score each profile (0-100) based on:
   - Exact matches: +40 points
   - Related/Similar matches: +30 points
   - Soft skill alignment: +20 points
   - Additional relevant factors: +10 points

Return your analysis in the following JSON format:
{
  "matches": [
    {
      "profile_id": "exact-profile-uuid-from-above",
      "match_score": number-between-0-and-100,
      "explanation": "Detailed explanation of why this profile matches"
    }
  ]
}

Important:
- Include ANY profile with a score > 30
- Be thorough but concise in explanations
- Focus on the most relevant aspects for the query
- Sort by match_score in descending order
- Return valid JSON only"""

            print("Debug: Sending request to Groq API...")
            # Get response from Groq
            chat_completion = client.chat.completions.create(
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
                temperature=0.3,
                max_tokens=4000,
            )
            print("Debug: Received response from Groq API")
            
            response_text = chat_completion.choices[0].message.content.strip()
            print(f"Debug: Response length: {len(response_text)}")
            
            # Parse JSON response
            try:
                # Find the first occurrence of '{'
                json_start = response_text.find('{')
                if json_start == -1:
                    print("Debug: No JSON found in response")
                    return []
                
                # Find the last occurrence of '}'
                json_end = response_text.rfind('}') + 1
                if json_end == 0:
                    print("Debug: No closing brace found in response")
                    return []
                    
                # Extract only the complete JSON object
                json_text = response_text[json_start:json_end]
                print(f"Debug: Extracted JSON text: {json_text[:200]}...")
                
                # Clean the JSON text
                json_text = json_text.strip()
                
                matches = json.loads(json_text)["matches"]
                print(f"Debug: Successfully parsed {len(matches)} matches")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Debug: Failed to parse response - {str(e)}")
                print(f"Debug: Response text: {response_text[:200]}...")
                return []
            
            # Convert to list of tuples (profile, explanation)
            results = []
            for match in matches:
                profile_id = match.get("profile_id")
                explanation = match.get("explanation", "")
                score = match.get("match_score", 0)
                
                # Find the profile with this ID
                profile = next((p for p in profiles if str(p.id) == profile_id), None)
                if profile:
                    results.append((
                        profile, 
                        f"Match Score: {score}%\n{explanation}"
                    ))
            
            print(f"Debug: Returning {len(results)} results")
            return sorted(results, key=lambda x: float(x[1].split('%')[0].split(': ')[1]), reverse=True)
                
        except Exception as e:
            print(f"Debug: Error during Groq search: {str(e)}")
            print(f"Debug: Error type: {type(e)}")
            if hasattr(e, 'response'):
                print(f"Debug: Response status: {e.response.status_code}")
                print(f"Debug: Response body: {e.response.text}")
            return [] 