from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_user, update_user_language

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    db_user = get_user(user_id)
    current_lang = db_user['language'] if db_user else 'en'
    
    text = (
        f"🌐 *Language Settings*\n\n"
        f"Current Language: *{current_lang.upper()}*\n\n"
        "Please select your preferred language:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data='set_lang_en'),
            InlineKeyboardButton("🇷🇺 Русский", callback_data='set_lang_ru'),
            InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='set_lang_uz')
        ],
        [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def update_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data # e.g., 'set_lang_ru'
    lang = data.split('_')[-1]
    
    update_user_language(user_id, lang)
    
    text = f"✅ Language updated to *{lang.upper()}* successfully!"
    keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')
