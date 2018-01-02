from flask import Flask
from flask_cors import CORS
from flask import request
from maincontroller import MainController 
import json
import sys

app = Flask(__name__)
CORS(app)
controller = MainController()

def RGBtoBGR(stringRGB):
    result = "\"#"
    result += stringRGB[3:5]
    result += stringRGB[5:7]
    result += stringRGB[1:3]
    result += "\""
    return result

def changeColor(requestData):
    if requestData and "\"color\"" in requestData:
        i = requestData.index("\"color\"")
        newColor = RGBtoBGR(requestData[i+17:i+24])
        newData = requestData[:i+16]
        newData += newColor
        newData += requestData[i+25:]
        return newData
    else:
        return requestData

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
    params = json.loads(changeColor(request.data))
    controller.changeMode(params)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__=='__main__':
    try:
        app.run(host='0.0.0.0', debug=False, port=8080)
    except KeyboardInterrupt:
        print "Exiting"
        controller.terminate()
        sys.exit()
