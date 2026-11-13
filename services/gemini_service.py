import os
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def load_bot_notes() -> str:
    try:
        notes_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'BOT_NOTES.md')
        if os.path.exists(notes_path):
            with open(notes_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception:
        pass
    return ""

def ask_sonic(prompt: str, system_instruction: str = "You are Sonic, a friendly, witty, and exceptionally capable AI assistant on Telegram.") -> str:
    bot_notes = load_bot_notes()
    full_system_instruction = f"{system_instruction}\n\nProject Notes & Owner Memory:\n{bot_notes}" if bot_notes else system_instruction
    
    try:
        # Using gemini-3.5-flash for fast and intelligent text generation
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config={
                "system_instruction": full_system_instruction,
                "temperature": 0.7,
            }
        )
        return response.text
    except Exception as e:
        # Fallback to gemini-3.5-flash-lite if primary encounters any issues
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
                config={
                    "system_instruction": full_system_instruction,
                    "temperature": 0.7,
                }
            )
            return response.text
        except Exception as fallback_error:
            return f"⚠️ Sorry, I encountered an error communicating with my AI core: {str(fallback_error)}"
