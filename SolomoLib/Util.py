import os
from flask import request, current_app as app

def load_configuration(fileName):
    fieldMap = {}
    fieldList = []
    fileName = app.config['FIELD_MAP_DIR']+fileName
    with open(fileName, "r") as config_data:
        for line in config_data:
            line = line.strip()
            if not line:  # line is blank
                continue
            if line.startswith("#"):  # comment line
                continue
            (key, val) = line.strip().split('=')
            fieldMap[key] = val
    return fieldMap