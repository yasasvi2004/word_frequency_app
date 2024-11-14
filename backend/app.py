from flask import Flask, request, jsonify, send_from_directory
from bs4 import BeautifulSoup
import requests
from collections import Counter
import re
import os

app = Flask(__name__)

# Serve the HTML frontend
@app.route('/')
def serve_index():
    return send_from_directory(os.getcwd(), 'index.html')


# Endpoint to fetch and analyze word frequencies
@app.route('/fetch', methods=['POST'])
def fetch():
    data = request.get_json()
    url = data.get("url")
    top_n = int(data.get("topN", 10))  # Default to 10 if topN is not provided

    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text

        # Extract text content and clean it
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        words = re.findall(r'\w+', text.lower())

        # Count words and get the top N
        word_counts = Counter(words)
        most_common = word_counts.most_common(top_n)

        return jsonify(most_common)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
