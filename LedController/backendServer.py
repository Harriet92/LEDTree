from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def hello():
    return "Looks like it works!"

@app.route('/getmodes', methods=['GET'])
def getModes():
    data = """
    [{ "id": 1, "name": "Rainbow", "speed": 50},
    { "id": 2, "name": "Fade", "speed": 50},
    { "id": 3, "name": "Random", "speed": 50},
    { "id": 4, "name": "Red", "speed": 50},
    { "id": 5, "name": "Green", "speed": 50},
    { "id": 6, "name": "Blue", "speed": 50},
    { "id": 7, "name": "Strobe", "speed": 50}]
    """
    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    return response

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
