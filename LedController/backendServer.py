from flask import Flask
from flask_cors import CORS
from flask import request
from maincontroller import MainController 
import json
app = Flask(__name__)
CORS(app)
controller = MainController()

@app.route('/')
def hello():
    return "Looks like it works!"

@app.route('/getmodes', methods=['GET'])
def getModes():
    data = """
    [{ "id": 1, "name": "clear", "speed": 50},
    { "id": 2, "name": "colorWipe", "speed": 50},
    { "id": 3, "name": "theaterChase", "speed": 50},
    { "id": 4, "name": "rainbow", "speed": 50},
    { "id": 5, "name": "rainbowCycle", "speed": 50},
    { "id": 6, "name": "theaterChaseRainbow", "speed": 50}
    ]
    """
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/change', methods=['POST'])
def changeLEDMode():
    controller.changeMode(json.loads(request.data))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
