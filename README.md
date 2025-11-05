# 📰 AI-Powered News Newsletter Generator

An automated Python system that fetches the latest news articles, generates AI-powered summaries using GPT-4o-mini, and delivers a beautifully formatted newsletter to your email inbox daily.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

---

## 📋 Table of Contents

- [Features](#features)
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Automation](#automation)
- [Project Structure](#project-structure)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)
- [Cost Estimate](#cost-estimate)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## ✨ Features

- 🗞️ **Automated News Fetching** - Retrieves latest articles from NewsAPI on topics of your choice
- 🤖 **AI-Powered Summaries** - Uses OpenAI's GPT-4o-mini to generate concise, readable summaries
- 📧 **Email Delivery** - Sends beautifully formatted HTML newsletters via Gmail
- 🔄 **Duplicate Detection** - Filters out duplicate articles across different topics
- 📊 **Comprehensive Logging** - Tracks all runs, errors, and performance metrics
- ⏰ **Task Scheduler Integration** - Fully automated daily execution on Windows
- 🔒 **Secure Configuration** - API keys safely stored in local config file (not committed to Git)

---

## 📖 Project Overview

This project was built as a Quarterly Assessment to demonstrate:
- REST API integration (NewsAPI)
- Large Language Model usage (OpenAI GPT-4o-mini)
- Email automation (SMTP with Gmail)
- Task scheduling and automation
- Best practices for configuration management and security
- Modular Python project structure

**Problem Solved:** Staying up-to-date with news on multiple topics is time-consuming. This system automatically delivers a personalized, AI-summarized news digest to your inbox every morning.

---

## 🔧 Prerequisites

### Required Accounts & API Keys

1. **NewsAPI** - For fetching news articles
   - Sign up: [https://newsapi.org/register](https://newsapi.org/register)
   - Free tier: 100 requests/day
   - Cost: Free

2. **OpenAI API** - For AI-powered article summaries
   - Sign up: [https://platform.openai.com/signup](https://platform.openai.com/signup)
   - Get API key: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Cost: ~$0.0005 per newsletter (less than 1 cent per day)

3. **Gmail Account** - For sending emails
   - Must enable 2-Factor Authentication
   - Must generate App Password: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
   - Cost: Free

### System Requirements

- **Python:** 3.11 or higher
- **Operating System:** Windows 10/11 (for Task Scheduler automation)
- **Internet Connection:** Required for API calls

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/news-newsletter-generator.git
cd news-newsletter-generator
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - For HTTP requests to NewsAPI
- `openai` - For GPT-4o-mini summarization

**Note:** Email functionality uses Python's built-in `smtplib` (no additional installation needed)

---

## ⚙️ Configuration

### 1. Create Configuration File

```bash
# Copy the example config
cp config.example.py config.py
```

### 2. Edit `config.py` with Your Credentials

Open `config.py` in your editor and fill in:

```python
# ========== API KEYS ==========
NEWS_API_KEY = "your_newsapi_key_here"
OPENAI_API_KEY = "your_openai_key_here"

# ========== EMAIL SETTINGS ==========
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_16_char_app_password"  # Gmail App Password
RECIPIENT_EMAIL = "recipient@gmail.com"  # Can be same as SENDER_EMAIL

# ========== NEWSLETTER SETTINGS ==========
TOPICS = [
    "artificial intelligence",
    "technology",
    "space exploration",
    "climate change",
    "cybersecurity"
]

ARTICLES_PER_TOPIC = 3  # Fetches 3, keeps best unique one per topic
OPENAI_MODEL = "gpt-4o-mini"
MAX_SUMMARY_TOKENS = 150  # ~2-3 sentences
```

### 3. Get Gmail App Password

**Important:** You CANNOT use your regular Gmail password!

1. Enable 2-Factor Authentication: [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. Generate App Password: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Type a name (e.g., "News Newsletter")
4. Click "Create"
5. Copy the 16-character password (remove spaces!)
6. Paste into `config.py` as `SENDER_PASSWORD`

**Security Note:** `config.py` is in `.gitignore` and will NEVER be committed to GitHub.

---

## 🚀 Usage

### Test Individual Components

**Part 1: Fetch News Articles**
```bash
python fetch_news.py
```
- Fetches articles from NewsAPI
- Saves to `fetched_articles.json`
- Displays article titles and sources

**Part 2: Generate AI Summaries**
```bash
python summarize_articles.py
```
- Reads `fetched_articles.json`
- Generates summaries using GPT-4o-mini
- Saves to `summarized_articles.json`
- Displays summaries

**Part 3: Send Email**
```bash
python send_email.py
```
- Reads `summarized_articles.json`
- Formats as HTML email
- Sends to your inbox

### Run Complete Newsletter

```bash
python main.py
```

This runs all three parts in sequence:
1. Fetches articles
2. Generates summaries
3. Sends email
4. Logs everything to `newsletter.log`

---

## ⏰ Automation (Windows Task Scheduler)

### Setup Instructions

#### 1. Update Batch File Path

Edit `run_newsletter.bat` and update the paths:

```batch
@echo off
cd /d "C:\path\to\your\project"
"C:\Users\YourName\AppData\Local\Programs\Python\Python313\python.exe" main.py
REM pause
```

**To find your Python path:**
```bash
where python
```
Use the second path (the real Python installation, not WindowsApps)

#### 2. Test Batch File

Double-click `run_newsletter.bat` to verify it works.

#### 3. Open Task Scheduler

1. Press `Windows Key + R`
2. Type: `taskschd.msc`
3. Press Enter

#### 4. Create Basic Task

1. Click **"Create Basic Task..."** in the right panel
2. **Name:** Daily News Newsletter
3. **Description:** Sends automated AI-powered news digest
4. Click **Next**

#### 5. Set Trigger

1. Select **"Daily"**
2. Set **Start time** (e.g., 8:00 AM)
3. **Recur every:** 1 days
4. Click **Next**

#### 6. Set Action

1. Select **"Start a program"**
2. Click **Browse** and select `run_newsletter.bat`
3. Click **Next**

#### 7. Finish and Configure

1. Check **"Open the Properties dialog when I click Finish"**
2. Click **Finish**

#### 8. Important Settings (Properties Window)

**Conditions Tab:**
- ☐ Uncheck: "Start the task only if the computer is on AC power"
- ☐ Uncheck: "Stop if the computer switches to battery power"

**Settings Tab:**
- ☑ Check: "Run task as soon as possible after a scheduled start is missed"

Click **OK** to save.

#### 9. Test the Task

1. Right-click your task → **Run**
2. Check your email inbox
3. Verify "Last Run Result" shows `(0x0)`

### Managing Automation

**Disable temporarily:**
- Right-click task → Disable

**Re-enable:**
- Right-click task → Enable

**Delete permanently:**
- Right-click task → Delete

**View history:**
- Right-click task → View History

---

## 📁 Project Structure

```
news-newsletter-generator/
│
├── fetch_news.py              # Part 1: Fetches articles from NewsAPI
├── summarize_articles.py      # Part 2: Generates AI summaries
├── send_email.py              # Part 3: Sends formatted email
├── main.py                    # Main script combining all parts
├── run_newsletter.bat         # Windows batch file for Task Scheduler
│
├── config.py                  # Your API keys & settings (NOT in Git)
├── config.example.py          # Configuration template (safe to commit)
├── requirements.txt           # Python dependencies
├── .gitignore                 # Protects sensitive files
├── README.md                  # This file
│
├── fetched_articles.json      # Generated: Fetched articles
├── summarized_articles.json   # Generated: Articles with summaries
└── newsletter.log             # Generated: Execution logs
```

### Files Explained

| File | Purpose | In Git? |
|------|---------|---------|
| `fetch_news.py` | Fetches articles from NewsAPI | ✅ Yes |
| `summarize_articles.py` | Generates AI summaries | ✅ Yes |
| `send_email.py` | Sends email newsletter | ✅ Yes |
| `main.py` | Orchestrates all parts | ✅ Yes |
| `run_newsletter.bat` | Automation batch file | ✅ Yes |
| `config.py` | **YOUR API KEYS** | ❌ **NO** |
| `config.example.py` | Template with fake keys | ✅ Yes |
| `*.json` | Generated data files | ❌ No |
| `newsletter.log` | Execution logs | ❌ No |

---

## 🎨 Customization

### Change News Topics

Edit `config.py`:

```python
TOPICS = [
    "NFL",                    # Sports
    "stock market",           # Finance
    "machine learning",       # Tech
    "climate change",         # Environment
    "SpaceX"                  # Space
]
```

**Tips for good topics:**
- ✅ Specific: "NBA playoffs", "Tesla stock"
- ✅ Broad categories: "technology", "sports"
- ✅ Names: "Elon Musk", "Taylor Swift"
- ❌ Avoid too vague: "news", "updates"

### Adjust Summary Length

Edit `config.py`:

```python
# Short summaries (1-2 sentences)
MAX_SUMMARY_TOKENS = 100

# Medium summaries (2-3 sentences) - Default
MAX_SUMMARY_TOKENS = 150

# Longer summaries (4-5 sentences)
MAX_SUMMARY_TOKENS = 250
```

### Change Number of Articles

Edit `config.py`:

```python
ARTICLES_PER_TOPIC = 3  # Fetches 3 per topic, keeps best unique one
```

Higher numbers give you more options to find relevant, unique articles.

### Modify Email Design

Edit `send_email.py` → `create_email_html()` function

Customize:
- Colors (CSS in the `<style>` section)
- Layout (HTML structure)
- Header text
- Footer content

---

## 🐛 Troubleshooting

### Issue: "config.py not found"

**Solution:** 
```bash
cp config.example.py config.py
# Then edit config.py with your API keys
```

### Issue: "Authentication failed" (Email)

**Causes:**
- Using regular Gmail password instead of App Password
- 2-Factor Authentication not enabled
- App Password has spaces in it

**Solution:**
1. Enable 2FA: [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. Generate new App Password: [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Remove all spaces from the 16-character password in `config.py`

### Issue: "No articles found"

**Causes:**
- Invalid NewsAPI key
- No internet connection
- Topics too specific

**Solution:**
1. Verify API key at [https://newsapi.org/](https://newsapi.org/)
2. Check internet connection
3. Try broader topics (e.g., "technology" instead of "quantum computing news")

### Issue: "Python was not found" (Batch File)

**Solution:**
Edit `run_newsletter.bat` with full Python path:

```bash
# Find your Python path
where python

# Use the second path (real Python, not WindowsApps)
# Example:
"C:\Users\YourName\AppData\Local\Programs\Python\Python313\python.exe" main.py
```

### Issue: OpenAI API Error

**Common Errors:**
- `RateLimitError` - Too many requests, wait a moment
- `AuthenticationError` - Invalid API key
- `InsufficientQuotaError` - No credits on OpenAI account

**Solution:**
1. Check API key is correct
2. Verify account has credits: [https://platform.openai.com/usage](https://platform.openai.com/usage)
3. Add rate limiting between requests (already implemented)

### Issue: Task Scheduler Says "Running" Forever

**Solution:**
1. Check `run_newsletter.bat` has `REM pause` (not just `pause`)
2. End the task: Right-click → End
3. Test batch file manually first

### Check Logs for Details

Always check `newsletter.log` for detailed error messages:

```bash
# View recent logs
tail -n 50 newsletter.log

# Or open in any text editor
```

---

## 💰 Cost Estimate

| Service | Tier | Daily Cost | Monthly Cost |
|---------|------|------------|--------------|
| **NewsAPI** | Free (100 req/day) | $0.00 | $0.00 |
| **OpenAI GPT-4o-mini** | Pay-per-use | ~$0.0005 | ~$0.015 |
| **Gmail SMTP** | Free | $0.00 | $0.00 |
| **Total** | | **~$0.0005/day** | **~$0.015/month** |

**Less than 2 cents per month!** 💸

### OpenAI Pricing Breakdown

- Input: ~500 tokens per article × 5 articles = 2,500 tokens
- Output: 150 tokens per summary × 5 = 750 tokens
- Cost: GPT-4o-mini is $0.150 per 1M input tokens, $0.600 per 1M output tokens
- **Daily cost:** ~$0.0005 (half a cent)






---

## 🙏 Acknowledgments

- **NewsAPI** - [https://newsapi.org/](https://newsapi.org/) - News data provider
- **OpenAI** - [https://openai.com/](https://openai.com/) - GPT-4o-mini language model
- **Gmail SMTP** - Email delivery service



---

## 🎓 Educational Use

This project was developed as a learning exercise to demonstrate:
- API integration and REST principles
- AI/LLM integration with OpenAI
- Email automation and SMTP protocols
- Task scheduling and cron-like automation
- Security best practices (API key management)
- Python project structure and modularity
- Error handling and logging
- Documentation and README creation



