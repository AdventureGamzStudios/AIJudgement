from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from datetime import datetime

app = Flask(__name__)

# Allow all for now (you can restrict later)
CORS(app, origins="*")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

model_name = "google/gemini-2.5-flash"

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 204

    # === CLEAR AND DETAILED LOGGING ===
    print("\n" + "="*60)
    print(f"NEW REQUEST - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print(f"Source Origin     : {request.headers.get('Origin')}")
    print(f"Referer URL       : {request.headers.get('Referer')}")
    print(f"IP Address        : {request.remote_addr}")
    print(f"User-Agent        : {request.headers.get('User-Agent')}")
    print(f"Content-Type      : {request.headers.get('Content-Type')}")
    print("-" * 40)

    data = request.get_json(force=True, silent=True)
    prompt = data.get('prompt', '').strip() if data else ""

    print(f"Prompt Received   : {prompt}")

    if not prompt:
        print("ERROR: No prompt received!")
        return jsonify({"error": "No prompt"}), 400

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=700,
            temperature=0.85,
        )
        reply = response.choices[0].message.content.strip()

        print(f"Reply Sent        : {reply}")
        print("="*60 + "\n")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"ERROR: {str(e)}")
        print("="*60 + "\n")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server started with detailed logging...")
    app.run(host='0.0.0.0', port=5000)
