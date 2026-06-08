from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
)

model_name = "anthropic/claude-sonnet-4.5"

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 204

    data = request.get_json(force=True, silent=True)
    prompt = data.get('prompt', '').strip() if data else ""

    if not prompt:
        return jsonify({"error": "No prompt"}), 400

    messages = [{"role": "user", "content": prompt}]

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            max_tokens=700,
            temperature=0.85,
        )
        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Server started!")
    app.run(host='0.0.0.0', port=5000)
