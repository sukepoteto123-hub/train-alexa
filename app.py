from flask import Flask, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

with open("train_nagoya.json", encoding="utf-8") as f:
    nagoya = json.load(f)

with open("train_toyohashi.json", encoding="utf-8") as f:
    toyohashi = json.load(f)

def get_next_train(timetable):
    now = datetime.now().strftime("%H:%M")
    future = [t for t in timetable if t["time"] > now]
    return future[0] if future else timetable[0]

def alexa_speech(text):
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": text
            },
            "shouldEndSession": True
        }
    }

@app.route("/", methods=["POST"])
def alexa_webhook():
    data = request.json

    # リクエスト種類取得
    req_type = data["request"]["type"]

    # スキル起動時
    if req_type == "LaunchRequest":
        return jsonify(alexa_speech("電車スキルです。次の電車は？と聞いてください。"))

    # Intent呼び出し
    if req_type == "IntentRequest":
        intent = data["request"]["intent"]["name"]

        if intent == "NextTrainIntent":
            n = get_next_train(nagoya)
            t = get_next_train(toyohashi)

            speech = (
                f"名古屋方面は {n['time']} {n['dest']}行き {n['type']}。"
                f"豊橋方面は {t['time']} {t['dest']}行き {t['type']}です。"
            )

            return jsonify(alexa_speech(speech))

    # それ以外
    return jsonify(alexa_speech("うまく理解できませんでした"))
