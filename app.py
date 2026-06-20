from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DEEPSEEK_API_KEY = "换成你的API_KEY"

# =========================
# DeepSeek对话
# =========================
def ask_deepseek(text):
    url = "https://api.deepseek.com/chat/completions"

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个语音助手，回答简短"},
            {"role": "user", "content": text}
        ],
        "temperature": 0.7
    }

    res = requests.post(url, json=data, headers=headers)
    return res.json()["choices"][0]["message"]["content"]


# =========================
# ESP32接口（先用文字模拟）
# =========================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_text = data.get("text")

    reply = ask_deepseek(user_text)

    return jsonify({
        "reply": reply
    })


@app.route("/")
def home():
    return "ESP32 AI Server Running"


if __name__ == "__main__":
    app.run()