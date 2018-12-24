from flask import Blueprint, request, jsonify
from kaupter_app.transactions import transaction_api 
from kaupter_app.basic_auth import require_appkey
from flask import current_app as app

transactions = Blueprint('transactions', __name__)

@transactions.route('/about', methods=['POST','GET'])
@require_appkey
def index():
    return "Solomo Platform v{}.  Created by Solomo 2018".format(app.config['VERSION'])

@transactions.route('/', methods=['POST','GET'])
@require_appkey
def home():
    return "Solomo API v{}".format(app.config['VERSION'])

@transactions.route('/fieldmapexample', methods=['POST','GET'])
@require_appkey
def fieldmap():
    return transaction_api.example_field_map('example_field_map.sdl')
    
def format_response(payload):
    if payload == "[]": 
        return respond({ValueError("No match found"), 204}, None)
    else:
        return respond(None, payload)

def respond(err, res=None):
    response = {
        'statusCode': err["status"] if err else '200',
        'data': err["message"] if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

    return jsonify(response)

