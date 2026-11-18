import os
from google import genai
from config import GEMINI_API_KEY
import config

client = genai.Client(api_key=GEMINI_API_KEY)

def load_bot_notes(user_id: int = None, username: str = None) -> str:
    try:
        notes_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'BOT_NOTES.md')
        if os.path.exists(notes_path):
            with open(notes_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            is_admin = False
            admin_env = getattr(config, 'ADMIN_USER_ID', None)
            if admin_env and (user_id or username):
                admin_entries = [e.strip() for e in str(admin_env).split(',') if e.strip()]
                for entry in admin_entries:
                    if user_id:
                        try:
                            if int(user_id) == int(entry):
                                is_admin = True
                                break
                        except ValueError:
                            pass
                        if str(user_id) == entry:
                            is_admin = True
                            break
                    if username and entry.lstrip('@').lower() == username.lstrip('@').lower():
                        is_admin = True
                        break
            
            print(f"[DEBUG] Admin check: user_id={user_id}, username={username}, ADMIN_USER_ID={admin_env}, is_admin={is_admin}")

            if is_admin:
                owner_info = (
                    "## Important Owner Information\n"
                    "- **Owner / Creator:** The user interacting with this bot is the **owner and creator** of Sonic Bot.\n"
                    "- **Privileges:** As the owner, they have full administrative control, highest priority, and custom development access. Always address the owner with respect, loyalty, and recognition of their authority as creator (\"Boss\", \"Owner\", \"Creator\")."
                )
            else:
                owner_info = (
                    "## User Information\n"
                    "- **User Status:** The user interacting with this bot is a regular user of Sonic Bot (not the owner/creator). Be helpful, polite, and friendly as their AI assistant."
                )
            
            if "{USER_STATUS_SECTION}" in content:
                content = content.replace("{USER_STATUS_SECTION}", owner_info)
            else:
                content += f"\n\n{owner_info}"
                
            return content
    except Exception as e:
        print(f"[DEBUG] Error in load_bot_notes: {e}")
        pass
    return ""

def ask_sonic(prompt: str, system_instruction: str = "You are Sonic, a friendly, witty, and exceptionally capable AI assistant on Telegram.", user_id: int = None, username: str = None) -> str:
    bot_notes = load_bot_notes(user_id, username)
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
