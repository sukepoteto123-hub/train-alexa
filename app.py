from flask import Flask, request
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_model import Response
import json
from datetime import datetime

app = Flask(__name__)
sb = SkillBuilder()

with open("train_nagoya.json", encoding="utf-8") as f:
    nagoya = json.load(f)

with open("train_toyohashi.json", encoding="utf-8") as f:
    toyohashi = json.load(f)

def get_next_train(timetable):
    now = datetime.now().strftime("%H:%M")
    future = [t for t in timetable if t["time"] > now]
    return future[0] if future else timetable[0]

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.object_type == "LaunchRequest"

    def handle(self, handler_input):
        speak = "次の電車は？と聞いてください。"
        return handler_input.response_builder.speak(speak).response

class NextTrainIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return handler_input.request_envelope.request.intent.name == "NextTrainIntent"

    def handle(self, handler_input):
        n = get_next_train(nagoya)
        t = get_next_train(toyohashi)

        speech = f"名古屋方面は {n['time']} {n['dest']}行き {n['type']}。豊橋方面は {t['time']} {t['dest']}行き {t['type']}です。"
        return handler_input.response_builder.speak(speech).response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(NextTrainIntentHandler())
skill = sb.create()

@app.route("/", methods=["POST"])
def invoke_skill():
    return skill.invoke(request.json)
