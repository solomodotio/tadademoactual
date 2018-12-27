import os
from json import loads, dumps
from flask import request, current_app as app
from SolomoLib import Util as util


def example_field_map(fieldmap):
    return dumps(util.load_configuration(fieldmap))

def process_account(data):
	print(data)