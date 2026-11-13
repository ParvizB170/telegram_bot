import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from config import TELEGRAM_BOT_TOKEN, GEMINI_API_KEY
from database import init_db
from handlers.start import start_command
from handlers.chat import chat_menu_callback, handle_message
from handlers.profile import profile_callback
from handlers.settings import settings_callback, update_settings_callback
from handlers.language import language_callback, update_language_callback
from handlers.files import files_menu_callback

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is missing from environment variables.")
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing from environment variables.")

    # Initialize SQLite Database
    init_db()
    logger.info("Database initialized successfully.")

    # Build Telegram Application
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Register Handlers
    app.add_handler(CommandHandler("start", start_command))
    
    # Callback Query Handlers for Menu & Buttons
    app.add_handler(CallbackQueryHandler(start_command, pattern="^back_to_menu$"))
    app.add_handler(CallbackQueryHandler(chat_menu_callback, pattern="^menu_chat$"))
    app.add_handler(CallbackQueryHandler(profile_callback, pattern="^menu_profile$"))
    app.add_handler(CallbackQueryHandler(settings_callback, pattern="^menu_settings$"))
    app.add_handler(CallbackQueryHandler(language_callback, pattern="^menu_language$"))
    app.add_handler(CallbackQueryHandler(files_menu_callback, pattern="^menu_files$"))
    
    # Settings & Language update callbacks
    app.add_handler(CallbackQueryHandler(update_settings_callback, pattern="^set_style_"))
    app.add_handler(CallbackQueryHandler(update_language_callback, pattern="^set_lang_"))

    # Text message handler for Chat & File generation prompts
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    logger.info("⚡ Sonic Telegram Bot is starting polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
