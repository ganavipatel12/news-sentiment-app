import requests
from bs4 import BeautifulSoup

def fetch_news_articles(company):
    """Fetch top 10 news articles related to a company using Google News RSS."""
    
    url = f"https://news.google.com/rss/search?q={company}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch news."}

    soup = BeautifulSoup(response.content, "lxml-xml")
    items = soup.find_all("item")[:10]  # Get the top 10 articles

    articles = []
    for item in items:
        title = item.title.text
        link = item.link.text
        summary = scrape_article(link)  # Fetch full content
       # summary = item.description.text if item.description else "No summary available"
        
        articles.append({
            "title": title,
            "link": link,
            "summary": summary
        })

    return articles
def scrape_article(url):
    """Extract main text content from a news article."""
    
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        """Extract paragraphs from the article"""
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.text for p in paragraphs[:5]])  # First 5 paragraphs
        
        return article_text if article_text else "Content not found."
    
    except requests.exceptions.RequestException:
        return "Failed to fetch article content."
    


from utils import fetch_news_articles

company_name = "Tesla"
articles = fetch_news_articles(company_name)

for i, article in enumerate(articles, 1):
    print(f"{i}. {article['title']}")
    print(f"Link: {article['link']}")
    print(f"Summary: {article['summary']}\n")

#from utils import scrape_article

#url = "https://www.bbc.com/news/world-us-canada-64177649"  # Replace with an article URL
#content = scrape_article(url)
#print("Extracted Content:\n", content)

#from utils import scrape_article

# Test with a real news article URL
#url = "https://www.bbc.com/news/world-us-canada-64177649"  # Replace with an actual news article link
#content = scrape_article(url)
#print("Extracted Content:\n", content)

from utils import scrape_article

# Replace with a real news article link
url = "https://www.bbc.com/news/world-us-canada-64177649"  
print(f"🔗 Testing Scraper with URL: {url}")
content = scrape_article(url)
print(f"📄 Extracted Content:\n{content}")



import requests
from bs4 import BeautifulSoup
from newspaper import Article
from time import sleep

def scrape_article(url):
    """Extract main text content from a news article using Newspaper3k."""
    
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        return article.text if article.text else "Content not found."
    
    except Exception as e:
        return f"Failed to fetch content: {str(e)}"

def fetch_news_articles(company):
    """Fetch top 10 news articles related to a company and extract full content."""
    
    search_url = f"https://news.search.yahoo.com/search?p={company}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(search_url, headers=headers, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for item in soup.find_all("h3")[:10]:  # Fetch top 10 articles
        title = item.text.strip()
        link = item.a["href"]

        print(f"🔗 Fetching content from: {link}")  # Debugging step

        summary = scrape_article(link)  # Extract full content
        
        articles.append({
            "title": title,
            "link": link,
            "summary": summary
        })

        sleep(2)  # Prevent getting blocked by the website (respectful scraping)

    return articles
from utils import fetch_news_articles

company_name = "Tesla"
articles = fetch_news_articles(company_name)

if "error" in articles:
    print("❌ ERROR:", articles["error"])
else:
    for i, article in enumerate(articles, 1):
        print(f"\n🔹 ARTICLE {i}")
        print(f"📰 Title: {article['title']}")
        print(f"🔗 Link: {article['link']}")
        print("⏳ Fetching full content...")
        print(f"📄 Summary:\n{article['summary']}\n")
import requests
from bs4 import BeautifulSoup

def fetch_news_articles(company):
    """Fetch top 10 news articles related to a company using Google News RSS."""
    
    url = f"https://news.google.com/rss/search?q={company}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch news."}

    soup = BeautifulSoup(response.content, "lxml-xml")
    items = soup.find_all("item")[:10]  # Get the top 10 articles

    articles = []
    for item in items:
        title = item.title.text
        link = item.link.text
        summary = scrape_article(link)  # Fetch full content
       # summary = item.description.text if item.description else "No summary available"
        
        articles.append({
            "title": title,
            "link": link,
            "summary": summary
        })

    return articles
def scrape_article(url):
    """Extract main text content from a news article."""
    
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        """Extract paragraphs from the article"""
        paragraphs = soup.find_all('p')
        article_text = ' '.join([p.text for p in paragraphs[:5]])  # First 5 paragraphs
        
        return article_text if article_text else "Content not found."
    
    except requests.exceptions.RequestException:
        return "Failed to fetch article content."
    

    from utils import fetch_news_articles

company_name = "Tesla"
articles = fetch_news_articles(company_name)

if "error" in articles:
    print("❌ ERROR:", articles["error"])
else:
    print("\n📢 🔹🔹🔹 News Summary for:", company_name.upper(), "🔹🔹🔹\n")
"""stmt 9 is added instead of for loop for else condition"""
for i, article in enumerate(articles, 1):
        print(f"\n🔹 ARTICLE {i}")
        print(f"📰 Title: {article['title']}")
        print(f"🔗 Link: {article['link']}")  # Print the link before scraping
        
        # Test if this link actually contains an article
        print("⏳ Fetching full content...")
        content = article["summary"]
        print(f"📄 Extracted Summary:\n{content}\n")
the above code is for long summary
from utils import fetch_news_articles

company_name = "Tesla"  # Change the company name as needed
articles = fetch_news_articles(company_name)

if "error" in articles:
    print("❌ ERROR:", articles["error"])
else:
    print("\n📢 🔹🔹🔹 News Summary for:", company_name.upper(), "🔹🔹🔹\n")
    
    for i, article in enumerate(articles, 1):
        title = article["title"]
        link = article["link"]
        summary = article["summary"]

        # Limit the summary to the first 3 sentences
        short_summary = " ".join(summary.split(". ")[:3]) + "."

        print(f"📰 **Article {i}: {title}**")
        print(f"🔗 Link: {link}")
        print(f"📄 Summary: {short_summary}")
        print("-" * 80)  # Divider for readability

the above is still long


to remove advertisements
import re
import requests
from newspaper import Article

# List of common unwanted phrases to remove
UNWANTED_PATTERNS = [
    r"Live Events.*?$",  # Removes "Live Events (You can now subscribe...)"
    r"You can now subscribe to our.*?$",  # Removes unwanted newsletter promotions
    r"Follow me on Twitter.*?$",  # Removes social media mentions
    r"Click here to read more.*?$",  # Removes "Read More" links
    r"Watch the .*? clip.*?$",  # Removes unnecessary video mentions
    r"Read full story at .*?$",  # Removes references to the full article
]

def clean_summary(text):
    """Remove unwanted phrases and extra spaces from the summary."""
    for pattern in UNWANTED_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.MULTILINE)
    return text.strip()

def scrape_article(url):
    """Extracts main text content from a news article and cleans unnecessary parts."""
    
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        summary = article.text if article.text else "Content not found."
        cleaned_summary = clean_summary(summary)  # Clean unnecessary words
        
        return cleaned_summary
    
    except Exception as e:
        return f"Failed to fetch content: {str(e)}"
    
    existing code 
import requests
from newspaper import Article

API_KEY = "3d4b9cbbae2d4c879dadc669f08a4e6a"  # Replace with your actual NewsAPI key

def scrape_article(url):
    """Extract main text content from a news article using Newspaper3k."""
    
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        return article.text if article.text else "Content not found."
    
    except Exception as e:
        return f"Failed to fetch content: {str(e)}"

def fetch_news_articles(company):
    """Fetch top 10 news articles using NewsAPI."""
    
    url = f"https://newsapi.org/v2/everything?q={company}&sortBy=publishedAt&language=en&apiKey={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch news: {str(e)}"}

    articles = []

    for item in data.get("articles", [])[:10]:
        title = item["title"]
        link = item["url"]

        print(f"🔗 Fetching content from: {link}")

        summary = scrape_article(link)  # Extract full content
        
        articles.append({
            "title": title,
            "link": link,
            "summary": summary
        })

    return articles


ef analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text.

    Args:
        text (str): The input text.

    Returns:
        str: Sentiment label ("Positive", "Negative", "Neutral").
    """
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # Value between -1 to 1

    if polarity > 0:
        return "Positive"
    elif polarity < 0:
        return "Negative"
    else:
        return "Neutral"

if __name__ == "__main__":
    sample_texts = [
        "Tesla's profits have soared, breaking previous records.",  # Positive
        "Tesla is facing regulatory scrutiny over its self-driving technology.",  # Negative
        "Tesla has announced a new model with advanced features.",  # Neutral
    ]
    
    for text in sample_texts:
        sentiment = analyze_sentiment(text)
        print(f"Text: {text}\nSentiment: {sentiment}\n")
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using VADER.

    Args:
        text (str): The input text.

    Returns:
        str: Sentiment label ("Positive", "Negative", "Neutral").
    """
    score = analyzer.polarity_scores(text)

    if score["compound"] >= 0.05:
        return "Positive"
    elif score["compound"] <= -0.05:
        return "Negative"
    else:
        return "Neutral"
    
if __name__ == "__main__":
    sample_texts = [
    "Tesla's profits have soared, breaking previous records.",  # Should be Positive
    "Tesla is facing regulatory scrutiny over its self-driving technology.",  # Should be Negative
    "Tesla has announced a new model with advanced features.",  # Should be Neutral
    ]
    
    for text in sample_texts:
        sentiment = analyze_sentiment(text)
        print(f"Text: {text}\nSentiment: {sentiment}\n")


def analyze_sentiment(text):
    """
    Analyzes sentiment using a hybrid approach: TextBlob + VADER.
    
    Args:
        text (str): The input text.
    
    Returns:
        str: Sentiment label ("Positive", "Negative", "Neutral").
    """
    # 1️⃣ VADER Sentiment Score
    vader_score = analyzer.polarity_scores(text)
    vader_compound = vader_score["compound"]  # Compound score (-1 to 1)

    # 2️⃣ TextBlob Polarity Score
    blob = TextBlob(text)
    blob_polarity = blob.sentiment.polarity  # Range: -1 to 1

    # 3️⃣ Combine Scores (Weighted Average)
    final_score = (vader_compound + blob_polarity) / 2  

    # 4️⃣ Classify Sentiment
    if final_score > 0.05:
        return "Positive"
    elif final_score < -0.05:
        return "Negative"
    else:
        return "Neutral"
    if __name__ == "__main__":
    sample_texts = [
        "Tesla's profits have soared, breaking previous records.",  # Should be Positive
        "Tesla is facing regulatory scrutiny over its self-driving technology.",  # Should be Negative
        "Tesla has announced a new model with advanced features.",  # Should be Neutral or Positive
    ]
    
    for text in sample_texts:
        sentiment = analyze_sentiment(text)
        print(f"Text: {text}\nSentiment: {sentiment}\n")


def analyze_sentiment(text):
    """
    Analyzes sentiment using a hybrid approach: VADER + TextBlob + Custom Word Dictionary.

    Args:
        text (str): The input text.

    Returns:
        str: Sentiment label ("Positive", "Negative", "Neutral").
    """
    # 1️⃣ Compute sentiment scores
    vader_score = analyzer.polarity_scores(text)["compound"]
    blob_score = TextBlob(text).sentiment.polarity
    final_score = (vader_score + blob_score) / 2  

    # 2️⃣ Adjust sentiment based on custom words
    lower_text = text.lower()
    
    for word in custom_negative_words:
        if word in lower_text:
            return "Negative"

    for word in custom_positive_words:
        if word in lower_text:
            return "Positive"

    # 3️⃣ Final classification based on score
    if final_score > 0.05:
        return "Positive"
    elif final_score < -0.05:
        return "Negative"
    else:
        return "Neutral"



