import os
import datetime
from flask import Flask, request, redirect, url_for, session, g, flash, render_template
from flask_oauth import OAuth
import requests
#from urllib.parse import urlparse
from urllib.parse import urlencode
from werkzeug.exceptions import BadRequest
from SolomoLib.QBOLib import get_companyInfo
from utils import context, OAuth2Helper

from flask import Blueprint, request, jsonify
from kaupter_app.basic_auth import require_appkey
from flask import current_app as app

from json import dumps


# configuration
SECRET_KEY = 'dev key'
DEBUG = True

#app = Flask(__name__)
#app.debug = DEBUG
#app.secret_key = SECRET_KEY

qbo = Blueprint('qbo', __name__)


"""@transactions.route('/about', methods=['POST','GET'])
@require_appkey
def index():
    print(request.text)
    return "Solomo Platform v{}.  Created by Solomo 2018".format(app.config['VERSION'])"""

@qbo.route('/')
def index():
    print('updating excel {}'.format(session))
    global customer_list
    #customer_list = excel.load_excel()
    return render_template(
        'index.html',
        customer_dict=None,
        title='QB Customer Leads'
    )

@qbo.route('/', methods=['POST'])
def update_table():
    print('here here here')
    """Update Excel file after customer is added in QBO"""
    customer_id = request.form['id']
    
    #if config.AUTH_TYPE == 'OAuth1':
        #request_context = context.RequestContextOAuth1(session['realm_id'], session['access_token'], session['access_secret'])
    #else:
    request_context = context.RequestContext(session['realm_id'], session['access_token'], session['refresh_token'])
    print('@@@REQUEST CONTEXT: {}'.format(request_context))
    """for customer in customer_list:
        if customer['Id'] == customer_id:
            # Create customer object
            response = create_customer(customer, request_context)
            
            # If customer added successfully, remove them from html and excel file
            if (response.status_code == 200):
                font_color = 'green'
                new_customer_list = excel.remove_lead(customer_list, customer_id)
                flash('Customer successfully added!')
                return render_template(
                    'index.html',
                    customer_dict=new_customer_list,
                    title='QB Customer Leads',
                    text_color=font_color
                )
            else:
                font_color = 'red'
                flash('Something went wrong: ' + response.text)"""
    return redirect(url_for('index'))


@qbo.route('/company-info')
def company_info():
    """Gets CompanyInfo of the connected QBO account"""
    #if config.AUTH_TYPE == 'OAuth1':
        #request_context = context.RequestContextOAuth1(session['realm_id'], session['access_token'], session['access_secret'])
    #else:
    request_context = context.RequestContext(session['realm_id'], session['access_token'], session['refresh_token'])
    
    response = get_companyInfo(request_context)
    if (response.status_code == 200):
        return render_template(
            'index.html',
            customer_dict=None,
            company_info='Company Name: ' + response.json()['CompanyInfo']['CompanyName'],
            title='QB Customer Leads',
        )
    else:
        return render_template(
            'index.html',
            customer_dict=customer_list,
            company_info=response.text,
            title='QB Customer Leads',
        )
    

@qbo.route('/auth')
def auth():
    """Initiates the Authorization flow after getting the right config value"""

    """if config.AUTH_TYPE == "OAuth1":

        return qbo.authorize(callback=url_for('oauth_authorized')) 
    else:"""
        # OAuth2 initiate authorization flow
        #'scope': 'com.intuit.quickbooks.accounting', 

    params = {
        'scope': 'com.intuit.quickbooks.accounting', 
        'redirect_uri': app.config['REDIRECT_URI'],
        'response_type': 'code', 
        'client_id': app.config['CLIENT_ID'],
        'state': csrf_token()
    }
    print('@@@@CSRF TOKEN {}'.format(csrf_token))
        #url = OAuth2Helper.get_discovery_doc()['authorization_endpoint'] + '?' + urllib.parse.urlencode(params)
    url = OAuth2Helper.get_discovery_doc()['authorization_endpoint'] + '?' + urlencode(params)
    return redirect(url)
   
@qbo.route('/reset-session')
def reset_session():
    """Resets session"""
    session.pop('qbo_token', None)
    session['is_authorized'] = False
    #file_object  = open("refresh_token", "w")
    #file_object.write(None)
    os.remove("refresh_token")
    return redirect(request.referrer or url_for('index'))

@qbo.route('/callback')
def callback():
    """Handles callback only for OAuth2"""
    #session['realmid'] = str(request.args.get('realmId'))
    state = str(request.args.get('state'))
    error = str(request.args.get('error'))
    if error == 'access_denied':
        return redirect(index)
    if state is None:
        return BadRequest()
    elif state != csrf_token():  # validate against CSRF attacks
        return BadRequest('unauthorized')
    
    auth_code = str(request.args.get('code'))
    if auth_code is None:
        return BadRequest()
    
    bearer = OAuth2Helper.get_bearer_token(auth_code)
    realmId = str(request.args.get('realmId'))

    # update session here
    session['is_authorized'] = True 
    session['realm_id'] = realmId
    session['access_token'] = bearer['access_token']
    session['refresh_token'] = bearer['refresh_token']
    token_dict = {}
    token_dict['token_date'] = datetime.datetime.today().strftime('%Y-%m-%d')
    token_dict['refresh_token'] = bearer['refresh_token']
    file_object  = open("refresh_token", "w")
    file_object.write(dumps(token_dict))
    return redirect(url_for('qbo.index'))


def csrf_token():
    token = session.get('csrfToken', None)
    if token is None:
        token = OAuth2Helper.secret_key()
        print('@@@TOKEN: {} - {}'.format(OAuth2Helper.secret_key(), session))
        session['csrfToken'] = token
    return token
