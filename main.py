"""
Main Script: AI-Powered News Newsletter Generator
This script combines all parts to create and send a daily newsletter
"""

import json
import time
import logging
import sys
from datetime import datetime

# Fix Windows console encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Import all the functions from previous parts
from fetch_news import fetch_news_articles
from summarize_articles import summarize_all_articles
from send_email import create_email_html, send_email

# Import configuration
try:
    from config import (
        NEWS_API_KEY,
        OPENAI_API_KEY,
        SENDER_EMAIL,
        SENDER_PASSWORD,
        RECIPIENT_EMAIL,
        TOPICS,
        ARTICLES_PER_TOPIC,
        OPENAI_MODEL,
        MAX_SUMMARY_TOKENS
    )
except ImportError:
    print("ERROR: config.py not found!")
    print("Please make sure config.py exists with all required settings.")
    exit(1)


# Set up logging with UTF-8 encoding
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('newsletter.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def validate_config():
    """
    Validate that all configuration values are set
    
    Returns:
        bool: True if valid, False otherwise
    """
    
    errors = []
    
    if not NEWS_API_KEY or NEWS_API_KEY == "your_newsapi_key_here":
        errors.append("NewsAPI key not set")
    
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        errors.append("OpenAI API key not set")
    
    if not SENDER_EMAIL or SENDER_EMAIL == "your_email@gmail.com":
        errors.append("Sender email not set")
    
    if not SENDER_PASSWORD or SENDER_PASSWORD == "your_16_char_app_password":
        errors.append("Gmail App Password not set")
    
    if not RECIPIENT_EMAIL or RECIPIENT_EMAIL == "recipient@gmail.com":
        errors.append("Recipient email not set")
    
    if errors:
        logger.error("Configuration errors found:")
        for error in errors:
            logger.error(f"  - {error}")
        return False
    
    return True


def run_newsletter():
    """
    Main function that orchestrates the entire newsletter process
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    start_time = time.time()
    today = datetime.now().strftime("%B %d, %Y")
    
    logger.info("=" * 60)
    logger.info("AI-POWERED NEWS NEWSLETTER GENERATOR")
    logger.info(f"Date: {today}")
    logger.info("=" * 60)
    
    try:
        # ========== STEP 1: FETCH ARTICLES ==========
        logger.info("\n📰 STEP 1: Fetching news articles...")
        logger.info(f"Topics: {', '.join(TOPICS)}")
        
        all_articles = []
        seen_urls = set()
        
        for topic in TOPICS:
            logger.info(f"  Fetching: {topic}")
            articles = fetch_news_articles(topic, NEWS_API_KEY, ARTICLES_PER_TOPIC)
            
            # Filter duplicates
            for article in articles:
                if article['url'] not in seen_urls:
                    all_articles.append(article)
                    seen_urls.add(article['url'])
                    break  # Got one unique article for this topic
        
        logger.info(f"✓ Fetched {len(all_articles)} unique articles")
        
        if not all_articles:
            logger.error("❌ No articles found. Aborting.")
            return False
        
        # Save fetched articles
        with open("fetched_articles.json", "w", encoding="utf-8") as f:
            json.dump(all_articles, f, indent=2, ensure_ascii=False)
        
        # ========== STEP 2: SUMMARIZE ARTICLES ==========
        logger.info("\n🤖 STEP 2: Generating AI summaries...")
        logger.info(f"Model: {OPENAI_MODEL}")
        
        summarized_articles = summarize_all_articles(
            all_articles,
            OPENAI_API_KEY,
            OPENAI_MODEL,
            MAX_SUMMARY_TOKENS
        )
        
        logger.info(f"✓ Generated {len(summarized_articles)} summaries")
        
        # Save summarized articles
        with open("summarized_articles.json", "w", encoding="utf-8") as f:
            json.dump(summarized_articles, f, indent=2, ensure_ascii=False)
        
        # ========== STEP 3: SEND EMAIL ==========
        logger.info("\n📧 STEP 3: Sending email newsletter...")
        
        subject = f"📰 Your Daily News Digest - {today}"
        html_content = create_email_html(summarized_articles)
        
        success = send_email(
            subject,
            html_content,
            SENDER_EMAIL,
            SENDER_PASSWORD,
            RECIPIENT_EMAIL
        )
        
        if not success:
            logger.error("❌ Failed to send email")
            return False
        
        logger.info(f"✓ Newsletter sent to {RECIPIENT_EMAIL}")
        
        # ========== SUMMARY ==========
        elapsed_time = time.time() - start_time
        logger.info("\n" + "=" * 60)
        logger.info("✅ NEWSLETTER GENERATION COMPLETE!")
        logger.info(f"Articles: {len(summarized_articles)}")
        logger.info(f"Time taken: {elapsed_time:.2f} seconds")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ ERROR: {str(e)}", exc_info=True)
        return False


def main():
    """
    Entry point for the newsletter generator
    """
    
    # Validate configuration
    if not validate_config():
        logger.error("\n⚠️  Please fix configuration errors in config.py")
        return
    
    # Run the newsletter generation
    success = run_newsletter()
    
    if success:
        logger.info("\n✅ Newsletter successfully generated and sent!")
    else:
        logger.error("\n❌ Newsletter generation failed. Check the logs above.")


if __name__ == "__main__":
    main()