from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)

# Open for now (we'll restrict later)
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

    # === BETTER SOURCE LOGGING ===
    origin = request.headers.get('Origin')
    referer = request.headers.get('Referer')
    user_agent = request.headers.get('User-Agent')

    print("=== NEW REQUEST RECEIVED ===")
    print(f"Origin  : {origin}")
    print(f"Referer : {referer}")
    print(f"User-Agent: {user_agent}")
    print("------------------------")

    data = request.get_json(force=True, silent=True)
    prompt = data.get('prompt', '').strip() if data else ""

    if not prompt:
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
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server started with detailed logging...")
    app.run(host='0.0.0.0', port=5000)
