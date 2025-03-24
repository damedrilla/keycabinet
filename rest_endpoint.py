from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from lock_controller import changeLockState
app = Flask(__name__)
cors = CORS(app) 
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/lock')
@cross_origin()
def lock():
    message = {'message': 'Locked'}
    changeLockState('lock')
    return jsonify(message)

@app.route('/unlock')
@cross_origin()
def unlock():
    message = {'message': 'Unlocked'}
    changeLockState('unlock')
    return jsonify(message)

def runApi():
   app.run(host='0.0.0.0')  