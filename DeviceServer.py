from flask import Flask, request, Response
from flask_cors import CORS
import threading

class DeviceServer(threading.Thread):

    def __init__(self, orchestrator):
        super().__init__()
        self.app = Flask(__name__)
        CORS(self.app)
        self.orchestrator = orchestrator

        @self.app.route('/', methods=["GET"])
        def index():
            return "hola"


        @self.app.route('/lightpad', methods=["POST"])
        def lightpad_value_changed():
            id = int(request.form["id"])
            value = int(request.form["value"])
            self.orchestrator.handle_lightpad_change(id, value)
            return Response({"status": 200}, mimetype='application/json')

        @self.app.route('/distance_sensor', methods=["POST"])
        def distance_sensor_value_changed():
            id = request.form["id"]
            value = request.form["value"]
            if id == 0:
                self.orchestrator.sizeCalculator.set_width(value)
            if id == 1:
                self.orchestrator.sizeCalculator.set_height(value)
            if id == 2:
                self.orchestrator.sizeCalculator.set_depth(value)
            return ""

        @self.app.route('/rotary_encoder', methods=["POST"])
        def rotary_encoder_value_changed():
            id = int(request.form["id"])
            value = int(request.form["value"])
            # id of the wrapping paper encoder
            if id == 0:
                self.orchestrator.paperLengthWatcher.new_encoder_value(value)
            return ""

        @self.app.route('/button', methods=["POST"])
        def button_clicked():
            id = int(request.form["id"])
            # id of the wrapping paper button
            if id == 0:
                self.orchestrator.paperLengthWatcher.finish()
            return ""

        @self.app.route('/order', methods=["POST"])
        def on_new_order():
            id = request.form["id"]
            order_products = request.form["orderProducts"]
            return Response({"status": 200}, mimetype='application/json')


    def run(self):
        #for debug mode the flask server must run on the main thread
        self.app.run(debug=False, host='0.0.0.0')