from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import get_user, update_user_settings

async def settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    db_user = get_user(user_id)
    current_setting = db_user['settings'] if db_user else 'balanced'
    
    text = (
        f"⚙️ *Sonic Settings*\n\n"
        f"Current AI Tone/Style: *{current_setting.capitalize()}*\n\n"
        "Select your preferred AI interaction style:"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("⚖️ Balanced", callback_data='set_style_balanced'),
            InlineKeyboardButton("🎨 Creative", callback_data='set_style_creative')
        ],
        [
            InlineKeyboardButton("⚡ Concise", callback_data='set_style_concise'),
        ],
        [InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')

async def update_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = query.data # e.g., 'set_style_creative'
    style = data.split('_')[-1]
    
    update_user_settings(user_id, style)
    
    text = f"✅ Success! AI Style updated to *{style.capitalize()}*."
    keyboard = [[InlineKeyboardButton("« Back to Menu", callback_data='back_to_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode='Markdown')
