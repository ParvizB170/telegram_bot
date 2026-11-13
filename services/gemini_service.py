import os
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_sonic(prompt: str, system_instruction: str = "You are Sonic, a friendly, witty, and exceptionally capable AI assistant on Telegram.") -> str:
    try:
        # Using gemini-2.5-flash or gemini-1.5-flash for fast and intelligent text generation
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={
                "system_instruction": system_instruction,
                "temperature": 0.7,
            }
        )
        return response.text
    except Exception as e:
        # Fallback to 1.5-flash if 2.5-flash encounters any issues
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.7,
                }
            )
            return response.text
        except Exception as fallback_error:
            return f"⚠️ Sorry, I encountered an error communicating with my AI core: {str(fallback_error)}"
