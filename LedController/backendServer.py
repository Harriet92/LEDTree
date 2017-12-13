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
    data = ''
    with open('modes.json', 'r') as myfile:
        data=myfile.read().replace('\n', '')
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/change', methods=['POST'])
def changeLEDMode():
    print request.data
    controller.changeMode(json.loads(request.data))
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
