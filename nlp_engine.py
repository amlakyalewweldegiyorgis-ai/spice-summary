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
    sentiment = analyze_sentiment(text)
    
    sentiment_phrases = {
        "POSITIVE": "This text expresses a positive outlook with promising developments.",
        "NEGATIVE": "This text highlights concerns and potential challenges.",
        "NEUTRAL": "This text presents a balanced, factual overview."
    }
    
    # Extract a brief key point (first sentence only)
    first_sentence = text.split('.')[0] if '.' in text else text
    key_point = first_sentence[:100] + "..." if len(first_sentence) > 100 else first_sentence
    
    conclusion = f"{sentiment_phrases.get(sentiment, 'Overall')} Key point: {key_point}"
    
    return conclusion