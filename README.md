# ⚡ Sonic Telegram AI ChatBot

Sonic is an advanced, lightning-fast Telegram AI ChatBot powered by Google Gemini and built with Python (`python-telegram-bot` and `google-genai`).

## Features
- 💬 **AI Q&A & Chat Mode**: Intelligent conversation powered by Google Gemini with customizable styles (Balanced, Creative, Concise).
- 👤 **User Profile**: Track user information, registration date, and preferences.
- ⚙️ **Settings**: Switch AI interaction styles on the fly.
- 🌐 **Language Selector**: Multilingual support (English, Russian, Uzbek).
- 📁 **File Generator**: Request code files, markdown documents, CSVs, or text files and receive them directly in Telegram as downloadable documents.

---

## Setup & Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd telegram_bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your credentials:
   - `TELEGRAM_BOT_TOKEN`: Get this from [@BotFather](https://t.me/BotFather) on Telegram.
   - `GEMINI_API_KEY`: Get this from [Google AI Studio](https://aistudio.google.com/).

4. **Run the Bot**:
   ```bash
   python main.py
   ```
