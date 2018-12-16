from flask import Blueprint, request, jsonify
#from kaupter_app.transactions import transaction_api 
from kaupter_app.basic_auth import require_appkey

transactions = Blueprint('transactions', __name__)

@transactions.route('/about')
@require_appkey
def index():
    return "Solomo API v1.0.  Created by Solomo 2018"

@transactions.route('/')
@require_appkey
def home():
    #print(request.args.get())
    return "Solomo API v1.0"


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

