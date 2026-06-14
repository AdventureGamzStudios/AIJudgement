from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)

# === ADD YOUR ALLOWED LINKS HERE ===
ALLOWED_ORIGINS = [
    "https://turbowarp.org",
    "https://*.turbowarp.org",           # Allows all turbowarp subdomains
    "http://localhost",                  # For local testing
    "http://127.0.0.1",
    # Add more links below, for example:
    # "https://your-project-name.onrender.com",
]

CORS(app, origins=ALLOWED_ORIGINS)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

model_name = "google/gemini-2.5-flash"

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 204

    # Show which website sent the request
    origin = request.headers.get('Origin')
    print("=== REQUEST RECEIVED FROM ===", origin)

    data = request.get_json(force=True, silent=True)
    prompt = data.get('prompt', '').strip() if data else ""

    if not prompt:
        return jsonify({"error": "No prompt"}), 400

    print("Prompt:", prompt)

    messages = [{"role": "user", "content": prompt}]

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=700,
            temperature=0.85,
        )
        reply = response.choices[0].message.content.strip()

        print("Reply sent:", reply)
        return jsonify({"reply": reply})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server started with origin logging...")
    app.run(host='0.0.0.0', port=5000)
