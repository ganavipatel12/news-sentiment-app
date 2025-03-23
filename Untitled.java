from utils import analyze_sentiment

# Sample test sentences
test_sentences = [
    "Tesla's stock has reached an all-time high after a record-breaking quarter.",
    "There are serious concerns over Tesla's self-driving technology after recent accidents.",
    "The company has announced a new product launch event next month."
]

for sentence in test_sentences:
    sentiment = analyze_sentiment(sentence)
    print(f"Text: {sentence}\nSentiment: {sentiment}\n")
