from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 👉 这里填你的 DeepSeek API Key
DEEPSEEK_API_KEY = "sk-0608aa39f84043008ffb3c1a40c3ed04"

DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"


@app.route("/")
def home():
    return "ESP32 AI Server Running"


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_text = data.get("text", "")

    if not user_text:
        return jsonify({"error": "no input"}), 400

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": user_text}
        ]
    }

    response = requests.post(DEEPSEEK_URL, headers=headers, json=payload)
    result = response.json()

    try:
        reply = result["choices"][0]["message"]["content"]
    except:
        reply = "AI error"

    return jsonify({"reply": reply})

@app.route("/test")
def test():
    return "OK"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
