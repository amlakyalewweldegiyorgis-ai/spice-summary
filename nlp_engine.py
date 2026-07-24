import requests
import os

HF_TOKEN = os.environ.get("HF_TOKEN", "")
API_URL_SUMMARY = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
API_URL_SENTIMENT = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

def summarize(text):
    if not HF_TOKEN:
        return "Please set HF_TOKEN environment variable in Render dashboard"
    
    try:
        response = requests.post(API_URL_SUMMARY, headers=headers, json={"inputs": text[:1024]}, timeout=30)
        if response.status_code == 200:
            return response.json()[0]['summary_text']
        return f"API Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def analyze_sentiment(text):
    if not HF_TOKEN:
        return "NEUTRAL"
    
    try:
        response = requests.post(API_URL_SENTIMENT, headers=headers, json={"inputs": text[:512]}, timeout=30)
        if response.status_code == 200:
            return response.json()[0]['label']
        return "NEUTRAL"
    except:
        return "NEUTRAL"

def generate_conclusion(text):
    summary = summarize(text)
    sentiment = analyze_sentiment(text)
    return f"Overall sentiment is {sentiment.lower()}. Key points: {summary}"