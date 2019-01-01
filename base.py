from flask import Flask, render_template, request, abort, jsonify, current_app as app
from kaupter_app.basic_auth import require_appkey
from kaupter_app.transactions import transaction_views
import views

# create the application object
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('kaupter.cfg')


app.register_blueprint(transaction_views.transactions, url_prefix='/api/v1.0/transactions')


def respond(err, res):
    response = {
        'statusCode': err["status"] if err else '200',
        'data': err["message"] if err else res,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

    return jsonify(response)

@app.errorhandler(401)
def not_authorized(error):
    message = "not authorized"
    err = dict({"message": message, "status": 401})
    #app.logger.error(message)
    return respond(err, None)

"""@app.errorhandler(Exception)
def unhandled_exception(error):
    if error == 'abort':
        print(error)
    message = "Unhandled Exception on page %s: %s" % (request.path, error)
    err = dict({"message": message, "status": 400})
    #app.logger.error(message)
    return respond(err, None)"""

@app.errorhandler(500)
def internal_server_error(error):
    message = "Internal Server Error on page %s: %s" % (request.path, error)
    err = dict({"message": message, "status": 500})
    #app.logger.error(message)
    return respond(err, None)
