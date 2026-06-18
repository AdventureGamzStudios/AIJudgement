from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app, origins="*")  # Open for testing

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

model_name = "google/gemini-2.5-flash"

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    print("\n🚀 === NEW REQUEST RECEIVED ===")
    print("Origin:", request.headers.get('Origin'))
    print("Referer:", request.headers.get('Referer'))
    print("X-Forwarded-For:", request.headers.get('X-Forwarded-For'))
    print("IP:", request.remote_addr)

    data = request.get_json(force=True, silent=True)
    prompt = data.get('prompt', '').strip() if data else ""

    print("Prompt received:", prompt)

    if not prompt:
        print("❌ No prompt!")
        return jsonify({"error": "No prompt"}), 400

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=600,
            temperature=0.85,
        )
        reply = response.choices[0].message.content.strip()
        print("✅ Reply sent:", reply)
        return jsonify({"reply": reply})
    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server running with full logging...")
    app.run(host='0.0.0.0', port=5000)
