import os
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

async def generate_text(prompt: str, model: str = "gemini-2.0-flash-exp") -> str:
    """Generate text using the Gemini model."""
    generative_model = genai.GenerativeModel(model)
    
    # Run the blocking call in a thread pool
    def _generate_sync():
        response = generative_model.generate_content(prompt)
        return response.text
    
    return await asyncio.to_thread(_generate_sync)