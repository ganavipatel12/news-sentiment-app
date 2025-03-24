import re
import requests
from newspaper import Article

from textblob import TextBlob
import nltk
#nltk.download('punkt') 



UNWANTED_PATTERNS = [
    r"Live Events.*?$",  # Removes "Live Events (You can now subscribe...)"
    r"\(\(|\)\)",  # Removes extra (( and ))
    r"@[\w\d]+"  # Removes "@america", "@xyz"
     r"\(.*?GLOBE NEWSWIRE.*?\)",  # Removes "(GLOBE NEWSWIRE)" type text
    r"[A-Z\s]+, [A-Z\s]+, \d{1,2} [A-Za-z]+ \d{4}",  # Removes timestamps like "HINDHEAD, UK, March 21, 2025"
    r"\(\(|\)\)",
    r"You can now subscribe to our.*?$",  # Removes unwanted newsletter promotions
    r"Follow me on Twitter.*?$",  # Removes social media mentions
    r"Click here to read more.*?$",  # Removes "Read More" links
    r"Watch the .*? clip.*?$",  # Removes unnecessary video mentions
    r"Read full story at .*?$",  # Removes references to the full article
    r"What happens to.*?$",  # Removes "What happens to student loans now?"
    r"Why Trump wants.*?$",  # Removes unnecessary headers
    r"\b(You can now subscribe to our)\b.*?$",  # Removes WhatsApp/Newsletter messages
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, \d{4}\b",  # Removes "March 21, 2025"
    r"\b\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December) \d{4}\b",  # Removes "21 March 2025"
]
def clean_summary(text):
    """Remove unwanted phrases and extra spaces from the summary."""
    for pattern in UNWANTED_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.MULTILINE)

    text = re.sub(r"\s+", " ", text).strip()
    return text

API_KEY = "3d4b9cbbae2d4c879dadc669f08a4e6a"  # Replace with your actual NewsAPI key

def scrape_article(url):
    """Extract main text content from a news article using Newspaper3k."""
    
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        summary = article.text if article.text else "Content not found."
        cleaned_summary = clean_summary(summary)  # Clean unnecessary words
        
        return cleaned_summary
    
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



def analyze_sentiment(text):
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
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Initialize VADER
analyzer = SentimentIntensityAnalyzer()   
def analyze_sentiment(text):
    """
    Hybrid Sentiment Analysis using VADER & TextBlob with improved political/economic classification.

    Args:
        text (str): Input text to analyze.

    Returns:
        str: Sentiment label ("Positive", "Negative", "Neutral").

            """
    # 1️⃣ Compute sentiment scores
    vader_score = analyzer.polarity_scores(text)["compound"]  # Compound score (-1 to 1)
    blob_score = TextBlob(text).sentiment.polarity  # Also ranges from -1 to 1

    # 2️⃣ Weighted Combination
    final_score = (0.7 * vader_score) + (0.3 * blob_score)  # Give more weight to VADER

    # 3️⃣ Adjust sentiment based on custom words
    lower_text = text.lower()

    for word in custom_positive_words:
        if word in lower_text:
            return "Positive"

    for word in custom_negative_words:
        if word in lower_text:
            return "Negative"

    # 4️⃣ Adjusted Classification
    if final_score > 0.1:  # Previously 0.15 (Now improved)
        return "Positive"
    elif final_score < -0.1:  # Previously -0.15 (Now improved)
        return "Negative"
    else:
        return "Neutral"

custom_positive_words = [
    "record profits", "soared", "growth", "innovation", "breakthrough", "success",
    "approval rating increased", "new policy to support", "peace agreement", "economic stability"
]

custom_negative_words = [
    "regulatory scrutiny", "lawsuit", "decline", "fraud", "ban", "fine", "controversy",
    "market crash", "rising oil prices", "inflation surge", "economic downturn", "climate warning"
]

custom_neutral_words = [
    "peace talks", "negotiations have begun", "discussions underway", "scheduled meeting",
    "considering options", "under review", "no decision yet"
]


def comparative_analysis(articles):
    """
    Performs comparative sentiment analysis across multiple articles.

    Args:
        articles (list): List of article dictionaries.

    Returns:
        dict: Summary of sentiment distribution.
    """
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}

    for article in articles:
        sentiment = article.get("sentiment", "Neutral")  # Ensure sentiment exists
        sentiment_counts[sentiment] += 1

    return {
        "sentiment_distribution": sentiment_counts,
        "articles": articles
    }


    
    for text in sample_texts:
        sentiment = analyze_sentiment(text)
        print(f"Text: {text}\nSentiment: {sentiment}\n")

if __name__ == "__main__":
    test_articles = [
        {"title": "Tesla Stock Soars", "summary": "Tesla shares hit an all-time high.", "sentiment": "Positive"},
        {"title": "Tesla Faces Investigation", "summary": "Regulators are investigating Tesla's self-driving technology.", "sentiment": "Negative"},
        {"title": "Neutral Analysis on Tesla", "summary": "Experts remain uncertain about Tesla’s future.", "sentiment": "Neutral"},
        {"title": "Tesla's New Model Breaks Sales Records", "summary": "Tesla's latest EV sees record sales in Q3.", "sentiment": "Positive"},
        {"title": "Tesla Lawsuit Expands", "summary": "Legal issues for Tesla continue to grow.", "sentiment": "Negative"},
        {"title": "Tesla Expands to India", "summary": "Tesla announces plans to enter the Indian market.", "sentiment": "Positive"}
    ]

    result = comparative_analysis(test_articles)
    print(result)

from gtts import gTTS

def text_to_speech(text, filename="output.mp3"):
    """
    Converts text into Hindi speech.

    Args:
        text (str): Input text.
        filename (str): Output audio filename.

    Returns:
        str: Filename of generated speech.
    """
    tts = gTTS(text=text, lang='hi')
    tts.save(filename)
    return filename
