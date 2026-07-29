import re
from textblob import TextBlob

def summarize(text):
    # Simple extractive summarization: get first 3 sentences
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) <= 3:
        return text
    
    # Take first 2 and last 1 sentence as summary
    summary_sentences = sentences[:2] + [sentences[-1]]
    summary = '. '.join(summary_sentences) + '.'
    
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
    
    sentiment_phrases = {
        "POSITIVE": "Overall, this text conveys a positive tone and suggests favorable outcomes.",
        "NEGATIVE": "The overall tone is negative, highlighting potential issues or concerns.",
        "NEUTRAL": "The text maintains a neutral perspective, presenting facts without strong bias."
    }
    
    # Generate a conclusion that synthesizes key takeaways
    key_points = summary[:200] + "..." if len(summary) > 200 else summary
    
    conclusion = f"{sentiment_phrases.get(sentiment, 'Overall')} Key takeaways: {key_points}"
    
    return conclusion