from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)

# Completely open for testing
CORS(app, origins="*", allow_headers="*", methods=["GET", "POST", "OPTIONS"])

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

model_name = "google/gemini-2.5-flash"

@app.route('/chat', methods=['POST', 'OPTIONS', 'GET'])
def chat():
    print("=== REQUEST RECEIVED ===")
    print("Method:", request.method)
    print("Origin:", request.headers.get('Origin'))
    print("Referer:", request.headers.get('Referer'))
    print("Content-Type:", request.headers.get('Content-Type'))
    print("Raw data:", request.get_data(as_text=True))

    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json(force=True, silent=True)
    prompt = data.get('prompt', '').strip() if data else ""

    print("Extracted prompt:", prompt)

    if not prompt:
        return jsonify({"error": "No prompt"}), 400

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.85,
        )
        reply = response.choices[0].message.content.strip()

        print("Reply:", reply)
        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("=== MAX DEBUG SERVER STARTED ===")
    app.run(host='0.0.0.0', port=5000)
