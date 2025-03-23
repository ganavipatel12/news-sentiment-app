from utils import fetch_news_articles

company_name = "Tesla"  # Change as needed
articles = fetch_news_articles(company_name)

if "error" in articles:
    print("❌ ERROR:", articles["error"])
else:
    print("\n📢 🔹🔹🔹 News Summary for:", company_name.upper(), "🔹🔹🔹\n")
    
    for i, article in enumerate(articles, 1):
        title = article["title"]
        link = article["link"]
        summary = article["summary"]

        # Limit the summary to 3 sentences OR 50 words (whichever comes first)
        sentences = summary.split(". ")
        short_summary = " ".join(sentences[:5])  # First 3 sentences
        if len(short_summary.split()) > 150:  # If it's too long, trim by words
            short_summary = " ".join(short_summary.split()[:50]) + "..."

        print(f"📰 **Article {i}: {title}**")
        print(f"🔗 Link: {link}")
        print(f"📄 Summary: {short_summary}")
        print("-" * 80)  # Divider for readability

