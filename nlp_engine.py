from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Summarization
summarizer_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
summarizer_model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

# Sentiment
sentiment_tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
sentiment_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")

def summarize(text):
    inputs = summarizer_tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = summarizer_model.generate(inputs["input_ids"], max_length=150, min_length=30, do_sample=False)
    return summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)

def analyze_sentiment(text):
    inputs = sentiment_tokenizer(text[:512], return_tensors="pt", truncation=True)
    outputs = sentiment_model(**inputs)
    pred = torch.argmax(outputs.logits, dim=1).item()
    return "POSITIVE" if pred == 1 else "NEGATIVE"


def generate_conclusion(text):
    summary = summarize(text)
    sentiment = analyze_sentiment(text)
    # Full summary, no truncation
    return f"Overall sentiment is {sentiment.lower()}. Key points: {summary}"
