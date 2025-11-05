"""
Configuration Template for News Newsletter Generator

INSTRUCTIONS:
1. Copy this file and rename it to 'config.py'
2. Fill in your actual API keys and credentials in config.py
3. NEVER commit config.py to GitHub (it's in .gitignore)
4. This template (config.example.py) is safe to commit
"""

# ========== API KEYS ==========
# Get your NewsAPI key from: https://newsapi.org/
NEWS_API_KEY = "your_newsapi_key_here"

# Get your OpenAI key from: https://platform.openai.com/api-keys
OPENAI_API_KEY = "your_openai_api_key_here"

# ========== EMAIL SETTINGS ==========
# Your Gmail address
SENDER_EMAIL = "your_email@gmail.com"

# Gmail App Password (NOT your regular password!)
# IMPORTANT: You MUST generate an App Password
# Steps:
#   1. Enable 2-Factor Authentication: https://myaccount.google.com/security
#   2. Generate App Password: https://myaccount.google.com/apppasswords
#   3. Copy the 16-character password here (no spaces)
SENDER_PASSWORD = "your_16_char_app_password"

# Who receives the newsletter (can be the same as SENDER_EMAIL)
RECIPIENT_EMAIL = "recipient@gmail.com"

# ========== NEWSLETTER SETTINGS ==========
# Topics to track (modify as needed)
TOPICS = [
    "artificial intelligence",
    "technology",
    "space exploration",
    "climate change",
    "cybersecurity"
]

# Number of articles to fetch per topic
# Note: Increase this if you're getting duplicate articles across topics
# The script will automatically filter out duplicates
ARTICLES_PER_TOPIC = 3  # Fetch 3 per topic, keep the best unique ones

# OpenAI model to use for summaries
OPENAI_MODEL = "gpt-4o-mini"

# Maximum tokens for each summary (150 = ~2-3 sentences)
# Increase for longer summaries, decrease for shorter
MAX_SUMMARY_TOKENS = 150

# ========== SMTP SETTINGS (for Gmail) ==========
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587