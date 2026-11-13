from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_user

async def profile_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    db_user = get_user(user_id)
    
    if not db_user:
        text = "⚠️ Profile not found. Please type /start to register."
    else:
        text = (
            f"👤 *Your Sonic Profile*\n\n"
            f"• *Name:* {db_user['first_name']}\n"
            f"• *Username:* @{db_user['username'] if db_user['username'] else 'None'}\n"
            f"• *User ID:* `{db_user['user_id']}`\n"
            f"• *Language:* `{db_user['language'].upper()}`\n"
            f"• *AI Style:* `{db_user['settings'].capitalize()}`\n"
            f"• *Joined:* {db_user['created_at']}\n"
        )
    
    keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')
