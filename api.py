from flask import Flask, request, jsonify
from utils import fetch_news_articles, analyze_sentiment, comparative_analysis
import utils

app = Flask(__name__)

@app.route("/analyze", methods=["GET"])
def analyze():
    """
    API endpoint to analyze news sentiment for a given company.

    Query Parameter:
        company (str): Name of the company to fetch news articles for.

    Returns:
        JSON response containing news articles with sentiment analysis.
    """
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Please provide a company name"}), 400

    # 1️⃣ Fetch news articles
    articles = utils.fetch_news_articles(company)
    
    # 2️⃣ Perform sentiment analysis on each article
    for article in articles:
        article["sentiment"] = utils.analyze_sentiment(article["summary"])

    # 3️⃣ Generate a comparative sentiment report
    sentiment_report = utils.comparative_analysis(articles)

    # 4️⃣ Return the results as JSON
    return jsonify({
        "company": company,
        "sentiment_report": sentiment_report
    })

#if __name__ == "__main__":
    #app.run(debug=True, port=5000)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7860)


@app.route("/tts", methods=["POST"])
def generate_tts():
    """
    API endpoint to generate Hindi Text-to-Speech (TTS) for a given text.

    Request Body (JSON):
        {
            "text": "Some text to convert to speech"
        }

    Returns:
        JSON response with TTS file path.
    """
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    filename = "speech_output.mp3"
    text_to_speech(text, filename)

    return jsonify({"audio_file": filename})
