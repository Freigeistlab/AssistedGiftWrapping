from flask import Flask, request
from flask_cors import CORS
import threading
import json
from statemachine import exceptions

class DeviceServer(threading.Thread):

    def __init__(self, orchestrator):
        super().__init__()
        self.app = Flask(__name__)
        CORS(self.app)
        self.orchestrator = orchestrator

        @self.app.route('/', methods=["GET"])
        def index():
            return "hola"

        @self.app.route('/LightSenseUnit', methods=["POST"])
        def lightpad_value_changed():
            id = int(request.form["ID"])
            mode = int(request.form["mode"])
            value = int(request.form["value"])
            print("[LIGHTPAD] " + str(id) + ":" + str(value))
            self.orchestrator.handle_lightpad_change(id, value)
            return ""

        @self.app.route('/DistanceUnit', methods=["POST"])
        def distance_sensor_value_changed():
            id = int(request.form["ID"])
            mode = request.form["mode"]
            value = float(request.form["value"])
            print("[DISTANCE UNIT] " + str(id) + ":" + str(value))
            if id == 0:
                self.orchestrator.sizeCalculator.set_width(value)
            if id == 1:
                self.orchestrator.sizeCalculator.set_height(value)
            if id == 2:
                self.orchestrator.sizeCalculator.set_depth(value)
            if id == 3:
                # TODO
                try:
                    if self.orchestrator.sizeCalculator.gift_depth != -1:
                        if self.orchestrator.sizeCalculator.gift_depth -2 <= value <= self.orchestrator.sizeCalculator.gift_depth +2:
                            print("gift is placed")
                            self.orchestrator.gift_placed()
                        else:
                            self.orchestrator.gift_removed()
                except exceptions.TransitionNotAllowed:
                    pass
            return ""

        @self.app.route('/EncoderUnit', methods=["POST"])
        def rotary_encoder_value_changed():
            id = int(request.form["ID"])
            mode = request.form["mode"]
            value = float(request.form["value"])
            print("[ENCODER UNIT] " + str(id) + ":" + str(value))
            # id of the wrapping paper encoder
            if id == 0:
                self.orchestrator.paperLengthWatcher.new_encoder_value(value)
            return ""

        @self.app.route('/ButtonUnit', methods=["POST"])
        def button_clicked():
            id = int(request.form["ID"])
            value = request.form["value"]
            print("[BUTTON UNIT] " + str(id) + ":" + str(value))
            # id of the wrapping paper button
            if id == 0:
                self.orchestrator.paperLengthWatcher.finish()
            return ""

        @self.app.route('/ScaleUnit', methods=["POST"])
        def scale_value_changed():
            id = request.form["ID"]
            mode = request.form["mode"]
            value = request.form["value"]
            print("[SCALE] " + str(id) + ":" + str(value))
            self.orchestrator.tape_teared()
            return ""

        @self.app.route('/order', methods=["POST"])
        def on_new_order():
            data = json.loads(request.data)
            print(data)
            """
            data: {
                "id":1,
                "orderProducts": {
                    "paperStyle": "style_id",  
                    "paper": "paper_id", 
                    "band": ["band1_id", "band2_id"],
                    "card": "card_id"
                }
            }"""
            self.orchestrator.orderHandler.add_order(data)
            return ""

    def run(self):
        # for debug mode the flask server must run on the main thread
        self.app.run(debug=False, host='0.0.0.0')
        return
