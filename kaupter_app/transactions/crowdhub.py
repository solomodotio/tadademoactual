from flask import Blueprint, request, jsonify
from kaupter_app.transactions import transaction_api, crowdhub_api
from kaupter_app.basic_auth import require_appkey
from flask import current_app as app

crowdhub = Blueprint('crowdhub', __name__)

@crowdhub.route('/about', methods=['POST','GET'])
@require_appkey
def index():
    return "Solomo Platform v{}.  Created by Solomo 2018. Crowdhub API".format(app.config['VERSION'])

@crowdhub.route('/account', methods=['POST'])
@require_appkey
def account():
    print('here')
    crowdhub_api.process_account(request.text)
    return "Solomo API v{}".format(app.config['VERSION'])

@crowdhub.route('/fieldmapexample', methods=['POST','GET'])
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

