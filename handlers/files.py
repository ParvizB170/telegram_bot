import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.gemini_service import ask_sonic
from services.file_generator import create_temp_file

async def files_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    context.user_data['mode'] = 'file_prompt'
    
    text = (
        "📁 *Sonic File Generator*\n\n"
        "Send me a description or topic for the file you want to create!\n"
        "For example:\n"
        "• _'A python script for web scraping'_ \n"
        "• _'A markdown project roadmap'_ \n"
        "• _'A CSV file with employee records'_ \n\n"
        "Type your file request below:"
    )
    keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def process_file_generation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    chat_id = update.effective_chat.id
    
    await update.message.reply_text("⚡ Generating your file with Gemini AI...", parse_mode='Markdown')
    await context.bot.send_chat_action(chat_id=chat_id, action="upload_document")
    
    # Prompt Gemini to generate file content and suggested filename
    system_instruction = (
        "You are Sonic's File Generation engine. "
        "The user will request a file. You must respond ONLY with the exact raw file content requested, "
        "without markdown code blocks around the entire output if possible, OR if code, just the pure code/content. "
        "Wait, also provide the filename on the very first line in this exact format: FILENAME: <filename>.<ext>\n"
        "Followed by a newline, then the actual file content."
    )
    
    ai_response = ask_sonic(f"Generate file for: {user_prompt}", system_instruction=system_instruction)
    
    # Parse filename and content
    filename = "sonic_generated.txt"
    content = ai_response
    
    lines = ai_response.splitlines()
    if lines and lines[0].startswith("FILENAME:"):
        filename = lines[0].replace("FILENAME:", "").strip()
        content = "\n".join(lines[1:])
    
    # Create temp file
    file_path = create_temp_file(filename, content)
    
    try:
        with open(file_path, "rb") as f:
            await update.message.reply_document(
                document=f,
                filename=filename,
                caption=f"📁 Here is your generated file: `{filename}`",
                parse_mode='Markdown'
            )
    finally:
        # Reset mode to chat or default
        context.user_data['mode'] = 'chat'
        if os.path.exists(file_path):
            os.remove(file_path)
