"""
Part 2: Summarize Articles with GPT-4o-mini
This script reads fetched articles and generates AI summaries
"""

import json
import time
from openai import OpenAI

# Import configuration from config.py
try:
    from config import OPENAI_API_KEY, OPENAI_MODEL, MAX_SUMMARY_TOKENS
except ImportError:
    print("⚠️  ERROR: config.py not found!")
    print("\nPlease follow these steps:")
    print("1. Make sure config.py exists with your OpenAI API key")
    print("2. Run this script again")
    exit(1)


def summarize_article(client, article, model="gpt-4o-mini", max_tokens=150):
    """
    Summarize a single article using OpenAI's GPT-4o-mini
    
    Args:
        client: OpenAI client instance
        article (dict): Article dictionary with title, description, and content
        model (str): OpenAI model to use
        max_tokens (int): Maximum length of summary
        
    Returns:
        str: AI-generated summary or error message
    """
    
    # Combine article information for summarization
    article_text = f"""
Title: {article['title']}

Description: {article['description']}

Content: {article['content']}
    """.strip()
    
    # Create the prompt for the AI
    prompt = f"""Please provide a concise, informative summary of this news article in 2-3 sentences. 
Focus on the key facts and main points.

{article_text}

Summary:"""
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes news articles concisely and accurately."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.5  # Balanced between creative and factual
        )
        
        # Extract the summary from the response
        summary = response.choices[0].message.content.strip()
        return summary
        
    except Exception as e:
        error_msg = f"Error summarizing article: {str(e)}"
        print(f"  ❌ {error_msg}")
        return error_msg


def summarize_all_articles(articles, api_key, model="gpt-4o-mini", max_tokens=150):
    """
    Summarize multiple articles with rate limiting
    
    Args:
        articles (list): List of article dictionaries
        api_key (str): OpenAI API key
        model (str): OpenAI model to use
        max_tokens (int): Maximum tokens per summary
        
    Returns:
        list: Articles with added 'summary' field
    """
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    print(f"Using model: {model}")
    print(f"Max tokens per summary: {max_tokens}")
    print()
    
    summarized_articles = []
    
    for i, article in enumerate(articles, 1):
        print(f"[{i}/{len(articles)}] Summarizing: {article['title'][:60]}...")
        
        # Generate summary
        summary = summarize_article(client, article, model, max_tokens)
        
        # Add summary to article
        article_with_summary = article.copy()
        article_with_summary['summary'] = summary
        summarized_articles.append(article_with_summary)
        
        print(f"  ✓ Summary generated ({len(summary)} characters)")
        print()
        
        # Rate limiting: small delay between requests to avoid hitting limits
        if i < len(articles):
            time.sleep(0.5)  # 0.5 second delay between requests
    
    return summarized_articles


def main():
    """
    Main function to load articles and generate summaries
    """
    
    print("=" * 60)
    print("ARTICLE SUMMARIZER - Part 2 Test")
    print("=" * 60)
    print()
    
    # Check if API key is set
    if not OPENAI_API_KEY or OPENAI_API_KEY == "your_openai_api_key_here":
        print("⚠️  ERROR: Please add your OpenAI API key to config.py")
        print("Get your key at: https://platform.openai.com/api-keys")
        return
    
    # Load articles from Part 1
    input_file = "fetched_articles.json"
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except FileNotFoundError:
        print(f"⚠️  ERROR: '{input_file}' not found!")
        print("Please run 'fetch_news.py' first to fetch articles.")
        return
    except json.JSONDecodeError:
        print(f"⚠️  ERROR: '{input_file}' is not valid JSON")
        return
    
    if not articles:
        print("⚠️  No articles found in the file.")
        return
    
    print(f"Loaded {len(articles)} articles from '{input_file}'")
    print()
    
    # Summarize all articles
    summarized_articles = summarize_all_articles(
        articles,
        OPENAI_API_KEY,
        OPENAI_MODEL,
        MAX_SUMMARY_TOKENS
    )
    
    # Display results
    print("=" * 60)
    print("SUMMARIES GENERATED")
    print("=" * 60)
    print()
    
    for i, article in enumerate(summarized_articles, 1):
        print(f"\n{'='*60}")
        print(f"Article {i}: {article['topic'].upper()}")
        print(f"{'='*60}")
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"\nOriginal Description:")
        print(f"{article['description']}")
        print(f"\n✨ AI Summary:")
        print(f"{article['summary']}")
        print(f"\nRead more: {article['url']}")
    
    # Save summarized articles
    output_file = "summarized_articles.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summarized_articles, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 60)
    print(f"✓ Summarized articles saved to '{output_file}'")
    print("=" * 60)


if __name__ == "__main__":
    main()