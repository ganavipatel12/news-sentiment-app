import streamlit as st
import requests
import gradio as gr
import requests

st.title("📊 News Sentiment Analysis & Hindi TTS 🎙️")

# Input field for the company name
company = st.text_input("Enter Company Name", "Tesla")

if st.button("Analyze News"):
    # Call the Flask API
    response = requests.get(f"http://127.0.0.1:5000/analyze?company={company}")
    
    if response.status_code == 200:
        result = response.json()

        # Display sentiment distribution
        st.subheader("📈 Sentiment Distribution")
        st.json(result["sentiment_report"]["sentiment_distribution"])

        # Display article analysis
        st.subheader("📰 News Articles Sentiment")
        for article in result["sentiment_report"]["articles"]:
            st.write(f"**{article['title']}**")
            st.write(f"📃 {article['summary']}")
            st.write(f"🔍 Sentiment: {article['sentiment']}")
            st.write("---")

    else:
        st.error("Error fetching data. Please check if the API is running.")


def analyze_news(company):
    response = requests.get(f"http://127.0.0.1:5000/analyze?company={company}")
    if response.status_code == 200:
        return response.json()
    return "Error fetching data"

iface = gr.Interface(
    fn=analyze_news,
    inputs="text",
    outputs="json",
    title="📊 News Sentiment Analysis & Hindi TTS 🎙️",
    description="Enter a company name to analyze recent news sentiment."
)

iface.launch()