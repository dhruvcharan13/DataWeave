import os
from typing import Optional
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the client as None - it will be initialized on first use
_client = None

def get_client() -> genai.Client:
    """Get the singleton Gemini client instance."""
    global _client
    if _client is None:
        _client =  genai.Client()  # Uses GEMINI_API_KEY from environment
    return _client

async def generate_text(prompt: str, model: str = "gemini-2.5-flash-lite") -> str:
    """Generate text using the Gemini model."""
    client = get_client()
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    return response.text