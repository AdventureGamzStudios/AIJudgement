from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)

# Allowed origins (add your links here)
ALLOWED_ORIGINS = [
    "https://turbowarp.org",
    "https://*.turbowarp.org",
    "http://localhost",
    "http://127.0.0.1",
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

    # === CLEAR SOURCE LOGGING ===
    origin = request.headers.get('Origin')
    referer = request.headers.get('Referer')
    
    print("=== NEW REQUEST RECEIVED ===")
    print("Source / Origin :", origin)
    print("Referer URL     :", referer)
    print("------------------------")

    data = request.get_json(force=True, silent=True)
    prompt = data.get('prompt', '').strip() if data else ""

    if not prompt:
        print("ERROR: No prompt received")
        return jsonify({"error": "No prompt"}), 400

    print("Prompt received:", prompt)

    messages = [{"role": "user", "content": prompt}]

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=700,
            temperature=0.85,
        )
        reply = response.choices[0].message.content.strip()

        print("Reply sent to TurboWarp:", reply)
        print("=== REQUEST COMPLETE ===\n")
        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server started with clear source logging...")
    app.run(host='0.0.0.0', port=5000)
