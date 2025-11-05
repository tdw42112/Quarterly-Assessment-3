"""
Part 1: Fetch News Articles
This script fetches the latest news articles from NewsAPI.org
"""

import requests
import json
from datetime import datetime

# Import configuration from config.py
try:
    from config import NEWS_API_KEY, TOPICS, ARTICLES_PER_TOPIC
except ImportError:
    print("ERROR: config.py not found!")
    print("\nPlease follow these steps:")
    print("1. Copy 'config.example.py' and rename it to 'config.py'")
    print("2. Edit config.py and add your API keys")
    print("3. Run this script again")
    exit(1)


def calculate_relevance_score(article, topic):
    """
    Calculate how relevant an article is to a topic
    
    Args:
        article (dict): Article dictionary
        topic (str): Topic to check against
        
    Returns:
        int: Relevance score (higher = more relevant)
    """
    topic_lower = topic.lower()
    topic_words = set(topic_lower.split())
    
    # Count topic mentions in title (weighted more heavily)
    title = article.get("title", "").lower()
    title_score = sum(3 for word in topic_words if word in title)
    
    # Count topic mentions in description
    description = article.get("description", "").lower()
    desc_score = sum(2 for word in topic_words if word in description)
    
    # Count topic mentions in content
    content = article.get("content", "").lower()
    content_score = sum(1 for word in topic_words if word in content)
    
    return title_score + desc_score + content_score


def fetch_news_articles(topic, api_key, max_articles=1):
    """
    Fetch news articles for a specific topic from NewsAPI
    
    Args:
        topic (str): The topic/keyword to search for
        api_key (str): Your NewsAPI key
        max_articles (int): Maximum number of articles to fetch
        
    Returns:
        list: List of article dictionaries with title, description, url, and content
    """
    
    # NewsAPI endpoint for searching everything
    url = "https://newsapi.org/v2/everything"
    
    # Parameters for the API request
    params = {
        "q": topic,                    # Search query
        "apiKey": api_key,             # Your API key
        "language": "en",              # English articles only
        "sortBy": "publishedAt",       # Get the most recent articles
        "pageSize": max_articles        # Limit results
    }
    
    try:
        # Make the request to NewsAPI
        response = requests.get(url, params=params, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract articles from response
            articles = data.get("articles", [])
            
            # Format the articles and calculate relevance
            formatted_articles = []
            for article in articles:
                formatted_article = {
                    "topic": topic,
                    "title": article.get("title", "No title"),
                    "description": article.get("description", "No description"),
                    "url": article.get("url", ""),
                    "content": article.get("content", ""),
                    "published_at": article.get("publishedAt", ""),
                    "source": article.get("source", {}).get("name", "Unknown")
                }
                # Calculate and add relevance score
                formatted_article["relevance_score"] = calculate_relevance_score(formatted_article, topic)
                formatted_articles.append(formatted_article)
            
            # Sort by relevance score (highest first)
            formatted_articles.sort(key=lambda x: x["relevance_score"], reverse=True)
            
            return formatted_articles
        else:
            print(f"Error fetching news for '{topic}': Status code {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching news for '{topic}': {e}")
        return []


def main():
    """
    Main function to fetch and display news articles
    """
    
    print("=" * 60)
    print("NEWS ARTICLE FETCHER - Part 1 Test")
    print("=" * 60)
    print()
    
    # Check if API key is set
    if not NEWS_API_KEY or NEWS_API_KEY == "your_newsapi_key_here":
        print("ERROR: Please add your NewsAPI key to config.py")
        print("Get your free key at: https://newsapi.org/")
        return
    
    # Collect all articles
    all_articles = []
    seen_urls = set()  # Track URLs we've already added
    
    # Fetch articles for each topic
    for topic in TOPICS:
        print(f"Fetching news for: {topic}...")
        articles = fetch_news_articles(topic, NEWS_API_KEY, ARTICLES_PER_TOPIC)
        
        # Filter out duplicates and try to get at least one unique article per topic
        added_for_topic = False
        for article in articles:
            if article['url'] not in seen_urls:
                all_articles.append(article)
                seen_urls.add(article['url'])
                added_for_topic = True
                break  # Got one unique article for this topic, move to next topic
        
        if added_for_topic:
            print(f"  ✓ Found unique article")
        else:
            print(f"  ⚠ All articles were duplicates")
        print()
    
    # Display results
    print("=" * 60)
    print(f"TOTAL ARTICLES FETCHED: {len(all_articles)}")
    print("=" * 60)
    print()
    
    if all_articles:
        for i, article in enumerate(all_articles, 1):
            print(f"Article {i}:")
            print(f"  Topic: {article['topic']}")
            print(f"  Title: {article['title']}")
            print(f"  Source: {article['source']}")
            print(f"  Published: {article['published_at']}")
            print(f"  URL: {article['url']}")
            print(f"  Description: {article['description'][:150]}...")  # First 150 chars
            print("-" * 60)
            print()
        
        # Save to a JSON file for later use
        output_file = "fetched_articles.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(all_articles, f, indent=2, ensure_ascii=False)
        print(f">> Articles saved to '{output_file}'")
        
    else:
        print("WARNING: No articles found. Check your API key and internet connection.")


if __name__ == "__main__":
    main()