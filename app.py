from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        url = data.get('url', '').strip()
        raw_text = data.get('text', '').strip()
        
        if not url and not raw_text:
            return jsonify({'error': 'Please provide a URL or text'}), 400
        
        if url:
            try:
                from utils import fetch_url_text
                text = fetch_url_text(url)
                if not text or len(text) < 20:
                    return jsonify({'error': 'Could not extract enough content from URL'}), 400
            except Exception as e:
                return jsonify({'error': f'Failed to fetch URL: {str(e)}'}), 400
        else:
            text = raw_text
            if len(text) < 20:
                return jsonify({'error': 'Text is too short (min 20 characters)'}), 400
        
        from nlp_engine import summarize, analyze_sentiment, generate_conclusion
        summary = summarize(text)
        sentiment = analyze_sentiment(text)
        conclusion = generate_conclusion(text)
        
        return jsonify({
            'summary': summary,
            'sentiment': sentiment,
            'conclusion': conclusion
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
