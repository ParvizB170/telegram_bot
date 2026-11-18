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

---

## 🚀 Deploying to Railway (railway.com)

Sonic Bot comes fully prepared for deployment on [Railway](https://railway.com) with Nixpacks, `Procfile`, and `railway.json`.

### Steps to Deploy:
1. **Push your repository** to GitHub.
2. Log in to [Railway](https://railway.com) and click **New Project** -> **Deploy from GitHub repo**.
3. Select your repository.
4. Go to your project service **Variables** tab and add your environment variables:
   - `TELEGRAM_BOT_TOKEN`: Your Telegram Bot token from @BotFather.
   - `GEMINI_API_KEY`: Your Gemini API key from Google AI Studio.
5. Railway will automatically build using Nixpacks and start your bot using the `Procfile` (`worker: python main.py`).

