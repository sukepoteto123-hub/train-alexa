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

def alexa_response(text):
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

@app.route("/", methods=["POST","GET"])
def alexa():
    n = get_next_train(nagoya)
    t = get_next_train(toyohashi)

    speech = (
        f"名古屋方面は {n['time']} {n['dest']}行き {n['type']}。"
        f"豊橋方面は {t['time']} {t['dest']}行き {t['type']}です。"
    )

    return jsonify(alexa_response(speech))