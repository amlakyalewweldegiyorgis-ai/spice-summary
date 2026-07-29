import re
from textblob import TextBlob

def summarize(text):
    # Simple extractive summarization: get first 3 sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) <= 3:
        return text[:300] + "..."
    
    # Take first 2 and last 1 sentence as summary
    summary_sentences = sentences[:2] + [sentences[-1]]
    summary = '. '.join(summary_sentences) + '.'
    
    # Limit length
    if len(summary) > 500:
        summary = summary[:500] + "..."
    
    return summary

def analyze_sentiment(text):
    try:
        blob = TextBlob(text[:1000])
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return "POSITIVE"
        elif polarity < -0.1:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
    except:
        return "NEUTRAL"

def generate_conclusion(text):
    summary = summarize(text)
    sentiment = analyze_sentiment(text)
    return f"Overall sentiment is {sentiment.lower()}. Key points: {summary}"
