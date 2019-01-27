from flask import current_app as app

class RequestContext(object):
    """The context class sets the realm id with the app's Client tokens every time user authorizes an app for their QB company"""
    def __init__(self, realm_id, access_token, refresh_token):
        self.client_id = app.config['CLIENT_ID']
        self.client_secret = app.config['CLIENT_SECRET']
        self.realm_id = realm_id
        self.access_token = access_token
        self.refresh_token = refresh_token
    
    def __str__(self):
        return self.realm_id