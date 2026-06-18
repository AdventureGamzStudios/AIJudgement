from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)

# ====================== ADD YOUR ALLOWED URLS HERE ======================
ALLOWED_ORIGINS = [
    "https://turbowarp.org",
    "https://*.turbowarp.org",           # Allows all TurboWarp domains
    "http://localhost",
    "http://127.0.0.1",
    "https://automatic-doodle-wrqwv566gpjp294p7-5000.app.github.dev",  # your old one
    # Add your Render URL here when you get it:
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

    # Log every request with source
    origin = request.headers.get('Origin') or request.headers.get('Referer') or "Unknown"
    print("=== NEW REQUEST RECEIVED ===")
    print(f"Source: {origin}")
    print("Time:", os.popen('date').read().strip())
    print("------------------------")

    data = request.get_json(force=True, silent=True)
    prompt = data.get('prompt', '').strip() if data else ""

    if not prompt:
        print("ERROR: No prompt received")
        return jsonify({"error": "No prompt"}), 400

    print("Prompt:", prompt)

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.85,
        )
        reply = response.choices[0].message.content.strip()

        print("Reply sent:", reply)
        print("=== REQUEST COMPLETE ===\n")
        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server started with URL whitelist and logging...")
    app.run(host='0.0.0.0', port=5000)
