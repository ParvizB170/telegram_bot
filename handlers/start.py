from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import upsert_user, get_user

def get_main_menu_keyboard(lang: str = 'en'):
    # Multilingual labels support
    labels = {
        'en': {
            'chat': '💬 Ask Sonic (Chat)',
            'profile': '👤 Profile',
            'settings': '⚙️ Settings',
            'language': '🌐 Language',
            'files': '📁 Generate File'
        },
        'ru': {
            'chat': '💬 Спросить Sonic (Чат)',
            'profile': '👤 Профиль',
            'settings': '⚙️ Настройки',
            'language': '🌐 Язык',
            'files': '📁 Создать файл'
        },
        'uz': {
            'chat': '💬 Sonic-dan so\'rash (Chat)',
            'profile': '👤 Profil',
            'settings': '⚙️ Sozlamalar',
            'language': '🌐 Til',
            'files': '📁 Fayl yaratish'
        }
    }
    l = labels.get(lang, labels['en'])
    
    keyboard = [
        [InlineKeyboardButton(l['chat'], callback_data='menu_chat')],
        [InlineKeyboardButton(l['profile'], callback_data='menu_profile'), InlineKeyboardButton(l['settings'], callback_data='menu_settings')],
        [InlineKeyboardButton(l['language'], callback_data='menu_language'), InlineKeyboardButton(l['files'], callback_data='menu_files')]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    upsert_user(user.id, user.username or "", user.first_name or "")
    db_user = get_user(user.id)
    lang = db_user['language'] if db_user else 'en'

    welcome_text = (
        f"⚡ *Hello {user.first_name}! I am Sonic* — your lightning-fast AI assistant powered by Google Gemini.\n\n"
        "Ask me questions, generate files, switch languages, or customize your settings using the menu below!"
    )
    
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=welcome_text, reply_markup=get_main_menu_keyboard(lang), parse_mode='Markdown')
    else:
        await update.message.reply_text(text=welcome_text, reply_markup=get_main_menu_keyboard(lang), parse_mode='Markdown')
