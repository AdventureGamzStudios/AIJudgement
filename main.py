from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from datetime import datetime

app = Flask(__name__)
CORS(app, origins="*")  # Open for now

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

model_name = "google/gemini-2.5-flash"

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "="*70)
    print(f"🚀 NEW REQUEST - {timestamp}")
    print("="*70)

    # Source Information
    print(f"Origin          : {request.headers.get('Origin')}")
    print(f"Referer         : {request.headers.get('Referer')}")
    print(f"IP Address      : {request.remote_addr}")
    print(f"User-Agent      : {request.headers.get('User-Agent')}")
    print(f"Content-Type    : {request.headers.get('Content-Type')}")

    if request.method == 'OPTIONS':
        print("→ OPTIONS Preflight Request")
        print("="*70 + "\n")
        return '', 204

    # Get the prompt
    data = request.get_json(force=True, silent=True)
    prompt = data.get('prompt', '').strip() if data else ""

    print(f"Prompt Received : {prompt}")

    if not prompt:
        print("❌ ERROR: No prompt received!")
        print("="*70 + "\n")
        return jsonify({"error": "No prompt"}), 400

    # Call AI
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.85,
        )
        reply = response.choices[0].message.content.strip()

        print(f"AI Reply        : {reply}")
        print("="*70 + "\n")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("="*70 + "\n")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server started with detailed logging...")
    app.run(host='0.0.0.0', port=5000)
