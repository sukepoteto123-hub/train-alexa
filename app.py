from flask import Flask, jsonify
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

@app.route("/")
def home():
    return "Train API running"

@app.route("/next")
def next_train():
    n = get_next_train(nagoya)
    t = get_next_train(toyohashi)

    speech = (
        f"名古屋方面は {n['time']} {n['dest']}行き {n['type']}。"
        f"豊橋方面は {t['time']} {t['dest']}行き {t['type']}です。"
    )

    return jsonify({"speech": speech})