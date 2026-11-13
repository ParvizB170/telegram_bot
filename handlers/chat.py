from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.gemini_service import ask_sonic
from database import get_user

async def chat_menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    context.user_data['mode'] = 'chat'
    
    text = (
        "💬 *Sonic Chat Mode Activated!*\n\n"
        "Ask me any question, ask for programming help, or chat with me. "
        "Every message you send will now be answered by Gemini AI.\n\n"
        "*(Type /start or click below to return to the main menu)*"
    )
    keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.effective_user.id
    
    # Check if user requested file generation
    if context.user_data.get('mode') == 'file_prompt':
        from handlers.files import process_file_generation
        await process_file_generation(update, context)
        return

    # Otherwise, handle as AI chat
    db_user = get_user(user_id)
    style = db_user['settings'] if db_user else 'balanced'
    
    system_prompt = "You are Sonic, a friendly, witty, and exceptionally capable AI assistant on Telegram."
    if style == 'creative':
        system_prompt += " Be extremely expressive, creative, and detailed in your explanations."
    elif style == 'concise':
        system_prompt += " Be concise, direct, and straight to the point."

    # Show typing action and thinking message for animation/feedback while waiting
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    thinking_message = await update.message.reply_text("💭 *Sonic is thinking...*", parse_mode='Markdown')
    
    response = ask_sonic(user_message, system_instruction=system_prompt)
    
    try:
        await thinking_message.edit_text(response, parse_mode='Markdown')
    except Exception:
        try:
            await thinking_message.edit_text(response)
        except Exception:
            await update.message.reply_text(response)
