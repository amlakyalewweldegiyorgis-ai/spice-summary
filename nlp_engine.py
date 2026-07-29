import requests
import os

# Use the correct Hugging Face inference endpoint
HF_TOKEN = os.environ.get("HF_TOKEN", "")
API_URL_SUMMARY = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_URL_SENTIMENT = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def summarize(text):
    if not HF_TOKEN:
        return "Please set HF_TOKEN environment variable"
    
    try:
        # Truncate text to avoid token limits
        inputs = text[:1024]
        response = requests.post(
            API_URL_SUMMARY,
            headers=headers,
            json={"inputs": inputs},
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('summary_text', 'No summary generated')
        elif response.status_code == 503:
            return "Model is loading, please wait 30 seconds and try again"
        else:
            return f"API Error: {response.status_code} - {response.text[:100]}"
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_sentiment(text):
    if not HF_TOKEN:
        return "NEUTRAL"
    
    try:
        inputs = text[:512]
        response = requests.post(
            API_URL_SENTIMENT,
            headers=headers,
            json={"inputs": inputs},
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('label', 'NEUTRAL')
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def generate_conclusion(text):
    summary = summarize(text)
    sentiment = analyze_sentiment(text)
    if summary.startswith("Error"):
        return f"Could not generate conclusion. Sentiment: {sentiment}. Please try again."
    return f"Overall sentiment is {sentiment.lower()}. Key points: {summary}"